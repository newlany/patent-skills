#!/usr/bin/env python3
"""
Package selected patent references into Markdown and PDF artifacts.

This helper uses:
- google_patents_fetch.py for markdown/json/html extraction
- a headless browser render as the default PDF path
- the patent-support-google-patents-pdfs skill only as an optional secondary backend
- a browser-automation fallback hint when automated PDF generation still fails
"""

from __future__ import annotations

import argparse
import io
import json
import os
import re
import subprocess
import sys
from pathlib import Path
from typing import Any
from urllib.request import Request, urlopen

from google_patents_fetch import extract_google_patent_record, save_google_patent_record
from PIL import Image


def _normalized_publication_number(value: str) -> str:
    return "".join(ch for ch in value.upper() if ch.isalnum())


def _codex_home() -> Path:
    return Path(os.environ.get("CODEX_HOME", Path.home() / ".codex")).expanduser().resolve()


def _pdf_backend_script() -> Path:
    return (
        _codex_home()
        / "skills"
        / "patent-support-google-patents-pdfs"
        / "scripts"
        / "download_google_patent_pdf.py"
    )


def _playwright_wrapper() -> Path:
    return _codex_home() / "skills" / "playwright" / "scripts" / "playwright_cli.sh"


def _browser_pdf_executable() -> Path | None:
    candidates = [
        Path("/Applications/Microsoft Edge.app/Contents/MacOS/Microsoft Edge"),
        Path("/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"),
        Path("/Applications/Chromium.app/Contents/MacOS/Chromium"),
        Path("/Applications/Brave Browser.app/Contents/MacOS/Brave Browser"),
    ]
    for candidate in candidates:
        if candidate.exists():
            return candidate
    return None


def _browser_fallback_commands(publication_number: str) -> list[str]:
    pwcli = _playwright_wrapper()
    normalized = _normalized_publication_number(publication_number)
    return [
        'export CODEX_HOME="${CODEX_HOME:-$HOME/.codex}"',
        'export PWCLI="$CODEX_HOME/skills/playwright/scripts/playwright_cli.sh"',
        f'"$PWCLI" --session patent-pdf open "https://patents.google.com/patent/{normalized}/en" --headed',
        '"$PWCLI" --session patent-pdf snapshot',
        '"$PWCLI" --session patent-pdf pdf',
    ]


def _render_pdf_with_headless_browser(
    publication_number: str,
    pdf_path: Path,
) -> dict[str, Any]:
    browser = _browser_pdf_executable()
    if browser is None:
        return {
            "status": "error",
            "error": "No supported headless browser executable was found.",
        }

    normalized = _normalized_publication_number(publication_number)
    url = f"https://patents.google.com/patent/{normalized}/en"
    pdf_path.parent.mkdir(parents=True, exist_ok=True)
    command = [
        str(browser),
        "--headless",
        "--disable-gpu",
        "--no-first-run",
        f"--print-to-pdf={pdf_path}",
        url,
    ]
    result = subprocess.run(
        command,
        capture_output=True,
        text=True,
        check=False,
    )
    if result.returncode == 0 and pdf_path.exists():
        return {
            "status": "rendered-by-headless-browser",
            "saved_to": str(pdf_path),
            "source": "google_patents_page_pdf",
            "browser": str(browser),
            "publication_number": normalized,
        }

    return {
        "status": "error",
        "error": result.stderr.strip() or result.stdout.strip() or "Headless browser PDF render failed.",
    }


def _download_pdf(publication_number: str, pdf_path: Path) -> dict[str, Any]:
    backend = _pdf_backend_script()
    if not backend.exists():
        return {
            "status": "backend-missing",
            "error": f"PDF backend script not found: {backend}",
        }

    command = [
        sys.executable,
        str(backend),
        "--publication",
        publication_number,
        "--output",
        str(pdf_path),
    ]
    result = subprocess.run(
        command,
        capture_output=True,
        text=True,
        check=False,
    )

    payload: dict[str, Any]
    stdout = result.stdout.strip()
    try:
        payload = json.loads(stdout) if stdout else {}
    except json.JSONDecodeError:
        payload = {"raw_stdout": stdout}

    if result.returncode == 0:
        payload.setdefault("status", "downloaded")
        return payload

    payload.setdefault("status", "error")
    payload.setdefault("error", result.stderr.strip() or "PDF download failed")
    payload["browser_fallback"] = {
        "reason": "direct-pdf-download-failed",
        "suggested_commands": _browser_fallback_commands(publication_number),
    }
    return payload


def _extract_pdf_url_from_html(html_text: str) -> str | None:
    patterns = [
        r'<meta name="citation_pdf_url" content="([^"]+)"',
        r'<a href="([^"]+)" itemprop="pdfLink">Download PDF</a>',
    ]
    for pattern in patterns:
        match = re.search(pattern, html_text, flags=re.I)
        if match:
            return match.group(1)
    return None


def _download_pdf_from_page_link(html_text: str, pdf_path: Path) -> dict[str, Any]:
    pdf_url = _extract_pdf_url_from_html(html_text)
    if not pdf_url:
        return {
            "status": "not-found",
            "error": "No direct PDF link was found in the Google Patents HTML.",
        }

    request = Request(
        pdf_url,
        headers={
            "User-Agent": (
                "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
                "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/135.0.0.0 Safari/537.36"
            )
        },
    )
    with urlopen(request, timeout=30) as response:
        data = response.read()
        content_type = response.headers.get("content-type", "")

    pdf_path.parent.mkdir(parents=True, exist_ok=True)
    pdf_path.write_bytes(data)
    return {
        "status": "downloaded-from-page-link",
        "saved_to": str(pdf_path),
        "source": "google_patents_pdf_link",
        "pdf_url": pdf_url,
        "content_type": content_type,
        "bytes": len(data),
    }


def _extract_page_image_urls(html_text: str) -> list[str]:
    urls = re.findall(
        r'<meta itemprop="full" content="(https://patentimages\.storage\.googleapis\.com/[^"]+\.png)">',
        html_text,
        flags=re.I,
    )
    unique_urls: list[str] = []
    seen: set[str] = set()
    for url in urls:
        if url not in seen:
            seen.add(url)
            unique_urls.append(url)
    return unique_urls


def _download_image(url: str) -> bytes:
    request = Request(
        url,
        headers={
            "User-Agent": (
                "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
                "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/135.0.0.0 Safari/537.36"
            )
        },
    )
    with urlopen(request, timeout=30) as response:
        return response.read()


def _render_pdf_from_page_images(
    publication_number: str,
    html_text: str,
    pdf_path: Path,
) -> dict[str, Any]:
    image_urls = _extract_page_image_urls(html_text)
    if not image_urls:
        return {
            "status": "error",
            "error": "No page-image URLs found on the Google Patents page.",
        }

    pages: list[Image.Image] = []
    for url in image_urls:
        image_bytes = _download_image(url)
        image = Image.open(io.BytesIO(image_bytes))
        if image.mode != "RGB":
            image = image.convert("RGB")
        pages.append(image)

    first_page, *rest = pages
    first_page.save(pdf_path, save_all=True, append_images=rest)
    return {
        "status": "rendered-from-page-images",
        "saved_to": str(pdf_path),
        "page_count": len(pages),
        "source": "google_patents_page_images",
        "publication_number": _normalized_publication_number(publication_number),
    }


def package_reference(publication_number: str, save_dir: Path) -> dict[str, Any]:
    normalized = _normalized_publication_number(publication_number)
    payload = extract_google_patent_record(publication_number)
    record = payload["record"]
    html_text = payload["html"]

    saved_files = save_google_patent_record(
        publication_number,
        record,
        html_text,
        save_dir,
    )

    pdf_path = save_dir / f"{normalized}.pdf"
    direct_pdf = _download_pdf_from_page_link(html_text, pdf_path)
    if direct_pdf.get("status") in {"downloaded-from-page-link", "exists"}:
        pdf_result = direct_pdf
    else:
        browser_pdf = _render_pdf_with_headless_browser(publication_number, pdf_path)
        if browser_pdf.get("status") in {"rendered-by-headless-browser", "exists"}:
            browser_pdf["fallback_from"] = direct_pdf
            pdf_result = browser_pdf
        else:
            pdf_result = _download_pdf(publication_number, pdf_path)
            if pdf_result.get("status") not in {"downloaded", "exists"}:
                rendered_pdf = _render_pdf_from_page_images(publication_number, html_text, pdf_path)
                if rendered_pdf.get("status") in {"rendered-from-page-images", "exists"}:
                    rendered_pdf["fallback_from"] = pdf_result
                    rendered_pdf["browser_pdf_attempt"] = browser_pdf
                    rendered_pdf["page_link_attempt"] = direct_pdf
                    pdf_result = rendered_pdf
                else:
                    pdf_result["browser_pdf_attempt"] = browser_pdf
                    pdf_result["page_link_attempt"] = direct_pdf

    result: dict[str, Any] = {
        "publication_number": normalized,
        "google_patents_url": record.get("google_patents_url"),
        "saved_files": saved_files,
        "pdf_result": pdf_result,
    }
    return result


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Package patent references into PDF and Markdown.")
    parser.add_argument(
        "publication_numbers",
        nargs="+",
        help="Publication numbers, hyphenated or plain.",
    )
    parser.add_argument(
        "--save-dir",
        required=True,
        help="Directory for packaged outputs.",
    )
    return parser


def main() -> int:
    args = build_parser().parse_args()
    save_dir = Path(args.save_dir).expanduser().resolve()
    save_dir.mkdir(parents=True, exist_ok=True)

    results = [package_reference(item, save_dir) for item in args.publication_numbers]
    payload = {
        "save_dir": str(save_dir),
        "results": results,
    }
    json.dump(payload, sys.stdout, ensure_ascii=False, indent=2)
    sys.stdout.write("\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
