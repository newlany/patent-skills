#!/usr/bin/env python3
"""
Fetch full patent text from Google Patents as a low-cost fallback.

This helper avoids expensive BigQuery full-text queries by reading the
Google Patents HTML page for a publication and extracting:

- title
- abstract
- description
- claims

Optionally it can save the raw HTML plus extracted JSON/Markdown files.
"""

from __future__ import annotations

import argparse
import html
import json
import re
import sys
from pathlib import Path
from typing import Any
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen


USER_AGENT = (
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
    "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/135.0.0.0 Safari/537.36"
)


def _normalized_publication_number(value: str) -> str:
    return "".join(ch for ch in value.upper() if ch.isalnum())


def google_patents_url(patent_number: str, language: str = "en") -> str:
    normalized = _normalized_publication_number(patent_number)
    return f"https://patents.google.com/patent/{normalized}/{language}"


def fetch_google_patents_html(patent_number: str, language: str = "en") -> tuple[str, str]:
    url = google_patents_url(patent_number, language=language)
    request = Request(
        url,
        headers={
            "User-Agent": USER_AGENT,
            "Accept-Language": "en-US,en;q=0.9",
        },
    )
    try:
        with urlopen(request, timeout=30) as response:
            html_text = response.read().decode("utf-8", "ignore")
    except HTTPError as exc:
        raise RuntimeError(f"Google Patents HTTP {exc.code}: {exc.reason}") from exc
    except URLError as exc:
        raise RuntimeError(f"Google Patents network error: {exc.reason}") from exc

    if "<title>Error" in html_text or "patent not found" in html_text.lower():
        raise RuntimeError(f"Patent not found on Google Patents: {patent_number}")

    return url, html_text


def _collapse_whitespace(text: str) -> str:
    text = html.unescape(text)
    text = re.sub(r"<br\\s*/?>", "\n", text, flags=re.I)
    text = re.sub(r"</?(?:div|p|section|heading|claim-statement|h\\d)[^>]*>", "\n", text, flags=re.I)
    text = re.sub(r"<[^>]+>", " ", text)
    text = text.replace("\xa0", " ")
    text = re.sub(r"[ \t]+", " ", text)
    text = re.sub(r" *\n *", "\n", text)
    text = re.sub(r"\n{3,}", "\n\n", text)
    return text.strip()


def _extract_first(pattern: str, html_text: str) -> str | None:
    match = re.search(pattern, html_text, flags=re.I | re.S)
    if not match:
        return None
    return _collapse_whitespace(match.group(1))


def _extract_raw(pattern: str, html_text: str) -> str | None:
    match = re.search(pattern, html_text, flags=re.I | re.S)
    if not match:
        return None
    return match.group(1)


def _extract_all(pattern: str, html_text: str) -> list[str]:
    return [_collapse_whitespace(match) for match in re.findall(pattern, html_text, flags=re.I | re.S)]


def _extract_claims(claims_section_html: str) -> list[str]:
    marked = re.sub(
        r"<div id=\"CLM-[^\"]+\" num=\"(\d+)\" class=\"claim\">",
        r"\n[[CLAIM \1]]\n",
        claims_section_html,
        flags=re.I,
    )
    parts = re.split(r"\[\[CLAIM (\d+)\]\]", marked)

    claims: list[str] = []
    for index in range(1, len(parts), 2):
        claim_no = parts[index].lstrip("0") or "0"
        body = _collapse_whitespace(parts[index + 1])
        if body:
            body = re.sub(rf"^{re.escape(claim_no)}\.\s*", "", body)
            claims.append(f"{claim_no}. {body}")
    return claims


def _extract_description(description_section_html: str) -> str:
    transformed = re.sub(
        r"<heading[^>]*>(.*?)</heading>",
        lambda m: f"\n\n## {_collapse_whitespace(m.group(1))}\n\n",
        description_section_html,
        flags=re.I | re.S,
    )
    transformed = re.sub(
        r"<div[^>]*class=\"description-paragraph\"[^>]*>(.*?)</div>",
        lambda m: f"\n{_collapse_whitespace(m.group(1))}\n",
        transformed,
        flags=re.I | re.S,
    )
    return _collapse_whitespace(transformed)


def extract_google_patent_record(patent_number: str, language: str = "en") -> dict[str, Any]:
    url, html_text = fetch_google_patents_html(patent_number, language=language)
    claims_section = _extract_raw(r"<section itemprop=\"claims\" itemscope>(.*?)</section>", html_text)
    description_section = _extract_raw(
        r"<section itemprop=\"description\" itemscope>(.*?)</section>", html_text
    )
    citation_patent_number = _extract_first(
        r"<meta name=\"citation_patent_number\" content=\"([^\"]+)\"",
        html_text,
    )

    record: dict[str, Any] = {
        "source": "google_patents",
        "patent_number": _normalized_publication_number(patent_number),
        "citation_patent_number_raw": citation_patent_number,
        "title": _extract_first(r"<meta name=\"DC.title\" content=\"([^\"]+)\"", html_text) or "",
        "abstract": _extract_first(r"<meta name=\"DC.description\" content=\"([^\"]+)\"", html_text)
        or "",
        "google_patents_url": url,
        "dates": _extract_all(r"<meta name=\"DC.date\" content=\"([^\"]+)\"", html_text),
        "contributors": _extract_all(r"<meta name=\"DC.contributor\" content=\"([^\"]+)\"", html_text),
        "claims": _extract_claims(claims_section) if claims_section else [],
        "description": _extract_description(description_section) if description_section else "",
        "raw_html_length": len(html_text),
    }

    return {"record": record, "html": html_text}


def _to_markdown(record: dict[str, Any]) -> str:
    lines = [
        f"# {record.get('patent_number', '')}",
        "",
        f"## Title",
        "",
        record.get("title", ""),
        "",
        "## Source",
        "",
        record.get("google_patents_url", ""),
        "",
    ]

    dates = record.get("dates") or []
    if dates:
        lines.extend(["## Dates", "", *[f"- {item}" for item in dates], ""])

    contributors = record.get("contributors") or []
    if contributors:
        lines.extend(["## Contributors", "", *[f"- {item}" for item in contributors], ""])

    abstract = record.get("abstract", "")
    if abstract:
        lines.extend(["## Abstract", "", abstract, ""])

    claims = record.get("claims") or []
    if claims:
        lines.extend(["## Claims", ""])
        for claim in claims:
            lines.extend([claim, ""])

    description = record.get("description", "")
    if description:
        lines.extend(["## Description", "", description, ""])

    return "\n".join(lines).strip() + "\n"


def save_google_patent_record(
    patent_number: str,
    record: dict[str, Any],
    html_text: str,
    save_dir: str | Path,
) -> dict[str, str]:
    normalized = _normalized_publication_number(patent_number)
    root = Path(save_dir).expanduser().resolve()
    root.mkdir(parents=True, exist_ok=True)

    html_path = root / f"{normalized}.html"
    json_path = root / f"{normalized}.json"
    md_path = root / f"{normalized}.md"

    html_path.write_text(html_text, encoding="utf-8")
    json_path.write_text(json.dumps(record, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    md_path.write_text(_to_markdown(record), encoding="utf-8")

    return {
        "html": str(html_path),
        "json": str(json_path),
        "markdown": str(md_path),
    }


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Fetch full patent text from Google Patents.")
    subparsers = parser.add_subparsers(dest="command", required=True)

    fetch_parser = subparsers.add_parser("fetch", help="Fetch one Google Patents publication page.")
    fetch_parser.add_argument("patent_number", help="Publication number, hyphenated or plain.")
    fetch_parser.add_argument("--language", default="en")
    fetch_parser.add_argument("--save-dir", help="Optional directory for HTML/JSON/Markdown output.")

    return parser


def main() -> int:
    args = build_parser().parse_args()

    try:
        payload = extract_google_patent_record(args.patent_number, language=args.language)
        record = payload["record"]
        html_text = payload["html"]
        if args.save_dir:
            record["saved_files"] = save_google_patent_record(
                args.patent_number,
                record,
                html_text,
                args.save_dir,
            )
        json.dump(record, sys.stdout, indent=2, ensure_ascii=False)
        sys.stdout.write("\n")
        return 0
    except Exception as exc:
        json.dump({"error": str(exc)}, sys.stdout, indent=2, ensure_ascii=False)
        sys.stdout.write("\n")
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
