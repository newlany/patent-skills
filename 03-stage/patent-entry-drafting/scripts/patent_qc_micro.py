#!/usr/bin/env python3
"""Small deterministic QC checks for Chinese patent application drafts.

The checks here are intentionally shallow and conservative. They catch frequent
mechanical issues before the richer patent QC skills perform legal or technical
judgment.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path
from typing import Any
from xml.etree import ElementTree as ET
from zipfile import ZipFile


HEADING_ALIASES = {
    "摘要": "abstract",
    "说明书摘要": "abstract",
    "权利要求书": "claims",
    "权利要求": "claims",
    "说明书": "specification",
    "技术领域": "field",
    "背景技术": "background",
    "发明内容": "summary",
    "实用新型内容": "summary",
    "附图说明": "drawings",
    "具体实施方式": "embodiments",
    "具体实施例": "embodiments",
    "实施例": "embodiments",
    "主要附图标记说明": "reference_signs",
    "附图标记说明": "reference_signs",
}

SPEC_REQUIRED = ["field", "background", "summary", "embodiments"]
PLACEHOLDER_RE = re.compile(
    r"(XXX+|XX+|TODO|TBD|待补充|请补充|待确认|这里填写|发明点待确认|附图待补|图\d+位|权利要求待补)",
    re.IGNORECASE,
)
CLAIM_RE = re.compile(r"(?ms)^\s*(\d+)[.．、]\s*(.*?)(?=^\s*\d+[.．、]\s*|\Z)")
FIGURE_RE = re.compile(r"图\s*([0-9０-９]+[A-Za-z]?|[一二三四五六七八九十]+[A-Za-z]?)")
PROMO_RE = re.compile(r"(革命性|颠覆性|世界领先|国际领先|最佳|完美|卓越|显著优于所有|极其优异)")
BARE_ABSTRACT_REF_RE = re.compile(r"[\u4e00-\u9fffA-Za-z]{2,}[0-9０-９]{1,4}")
NS = {"w": "http://schemas.openxmlformats.org/wordprocessingml/2006/main"}


def read_text(path: Path) -> tuple[str, dict[str, Any]]:
    if path.suffix.lower() == ".docx":
        return read_docx_text(path)
    text = path.read_text(encoding="utf-8")
    return text, {"kind": "text", "paragraphs": len([line for line in text.splitlines() if line.strip()])}


def read_docx_text(path: Path) -> tuple[str, dict[str, Any]]:
    paragraphs: list[str] = []
    with ZipFile(path) as zf:
        root = ET.fromstring(zf.read("word/document.xml"))
    for paragraph in root.findall(".//w:p", NS):
        text = "".join(node.text or "" for node in paragraph.findall(".//w:t", NS))
        if text.strip():
            paragraphs.append(text.strip())
    return "\n".join(paragraphs), {"kind": "docx", "paragraphs": len(paragraphs)}


def normalize_heading(line: str) -> str:
    line = re.sub(r"^[\s#一二三四五六七八九十0-9、.．（）()第章节]+", "", line.strip())
    line = re.sub(r"[:：\s]+$", "", line)
    return line


def split_sections(text: str) -> tuple[dict[str, str], dict[str, str]]:
    sections: dict[str, list[str]] = {}
    headings_seen: dict[str, str] = {}
    current = "body"
    sections[current] = []

    for raw_line in text.splitlines():
        line = raw_line.strip()
        normalized = normalize_heading(line)
        label = HEADING_ALIASES.get(normalized)
        if label:
            current = label
            sections.setdefault(current, [])
            headings_seen[label] = normalized
            continue
        sections.setdefault(current, []).append(raw_line)

    return {key: "\n".join(value).strip() for key, value in sections.items()}, headings_seen


def issue(
    code: str,
    severity: str,
    message: str,
    location: str | None = None,
    evidence: str | None = None,
    suggestion: str | None = None,
) -> dict[str, str]:
    payload = {"code": code, "severity": severity, "message": message}
    if location:
        payload["location"] = location
    if evidence:
        payload["evidence"] = shorten(evidence)
    if suggestion:
        payload["suggestion"] = suggestion
    return payload


def shorten(text: str, limit: int = 180) -> str:
    text = re.sub(r"\s+", " ", text).strip()
    return text if len(text) <= limit else text[: limit - 1] + "…"


def count_nonspace(text: str) -> int:
    return len(re.sub(r"\s+", "", text))


def check_required_headings(sections: dict[str, str], headings_seen: dict[str, str]) -> list[dict[str, str]]:
    findings: list[dict[str, str]] = []
    for label, display in [
        ("abstract", "摘要"),
        ("claims", "权利要求书"),
        ("specification", "说明书"),
    ]:
        if label not in headings_seen:
            findings.append(
                issue(
                    "missing-heading",
                    "suspected",
                    f"未检测到 `{display}` 标题；若这是完整申请稿，应补齐或核对标题格式。",
                    display,
                )
            )

    if "specification" in headings_seen or any(label in headings_seen for label in SPEC_REQUIRED):
        for label, display in [
            ("field", "技术领域"),
            ("background", "背景技术"),
            ("summary", "发明内容"),
            ("embodiments", "具体实施方式"),
        ]:
            if label not in headings_seen:
                findings.append(
                    issue(
                        "missing-spec-section",
                        "suspected",
                        f"未检测到说明书章节 `{display}`。",
                        display,
                    )
                )

    if "图" in sections.get("body", "") + sections.get("embodiments", "") and "drawings" not in headings_seen:
        findings.append(
            issue(
                "missing-drawings-section",
                "suspected",
                "正文出现附图引用，但未检测到 `附图说明` 章节。",
                "附图说明",
            )
        )
    return findings


def check_abstract(sections: dict[str, str]) -> list[dict[str, str]]:
    findings: list[dict[str, str]] = []
    abstract = sections.get("abstract", "")
    if not abstract:
        return findings

    abstract_len = count_nonspace(abstract)
    if abstract_len > 300:
        findings.append(
            issue(
                "abstract-too-long",
                "confirmed",
                f"摘要文字部分约 {abstract_len} 个非空白字符，超过 300 字机械阈值。",
                "摘要",
                suggestion="删减为 300 字以内，并保留技术问题、技术方案要点和主要用途。",
            )
        )
    for match in PROMO_RE.finditer(abstract):
        findings.append(
            issue(
                "abstract-promotional-wording",
                "suspected",
                "摘要中出现可能偏商业宣传的表述。",
                "摘要",
                match.group(0),
                "改为客观技术效果表述。",
            )
        )
    for match in BARE_ABSTRACT_REF_RE.finditer(abstract):
        token = match.group(0)
        if not re.search(r"[A-Za-z][0-9]|[0-9]+[年月日%％℃°]", token):
            findings.append(
                issue(
                    "abstract-ref-sign-parentheses",
                    "suspected",
                    "摘要中的附图标记通常应加括号；请核对该数字是否为附图标记。",
                    "摘要",
                    token,
                )
            )
    return findings


def check_claims(sections: dict[str, str]) -> list[dict[str, str]]:
    findings: list[dict[str, str]] = []
    claims_text = sections.get("claims", "")
    if not claims_text:
        return findings

    claims = [(int(num), body.strip()) for num, body in CLAIM_RE.findall(claims_text)]
    if not claims:
        findings.append(
            issue(
                "claims-not-numbered",
                "suspected",
                "未检测到以阿拉伯数字连续编号的权利要求。",
                "权利要求书",
            )
        )
        return findings

    seen_numbers = {num for num, _ in claims}
    expected = set(range(1, max(seen_numbers) + 1))
    missing = sorted(expected - seen_numbers)
    if missing:
        findings.append(
            issue(
                "claim-number-gap",
                "confirmed",
                f"权利要求编号不连续，缺少：{', '.join(map(str, missing))}。",
                "权利要求书",
            )
        )

    for num, body in claims:
        citations = [int(item) for item in re.findall(r"权利要求\s*(\d+)", body)]
        if any(citation >= num for citation in citations):
            findings.append(
                issue(
                    "claim-forward-or-self-citation",
                    "confirmed",
                    f"权利要求 {num} 引用了自身或后续权利要求。",
                    f"权利要求{num}",
                    shorten(body),
                )
            )
        if citations and any(citation not in seen_numbers for citation in citations):
            findings.append(
                issue(
                    "claim-citation-missing-target",
                    "confirmed",
                    f"权利要求 {num} 引用了不存在的权利要求编号。",
                    f"权利要求{num}",
                    shorten(body),
                )
            )
        if num > 1 and not citations and re.match(r"^(根据|如|按照).*所述", body):
            findings.append(
                issue(
                    "dependent-claim-without-citation",
                    "suspected",
                    f"权利要求 {num} 看起来像从属权利要求，但未检测到引用编号。",
                    f"权利要求{num}",
                    shorten(body),
                )
            )
    return findings


def check_figures(text: str, sections: dict[str, str]) -> list[dict[str, str]]:
    findings: list[dict[str, str]] = []
    refs = {match.group(1) for match in FIGURE_RE.finditer(text)}
    if not refs:
        return findings

    drawings = sections.get("drawings", "")
    if not drawings:
        return findings

    described = {match.group(1) for match in FIGURE_RE.finditer(drawings)}
    missing = sorted(refs - described)
    for fig in missing:
        findings.append(
            issue(
                "figure-reference-not-described",
                "suspected",
                f"正文引用 `图{fig}`，但附图说明中未检测到对应说明。",
                "附图说明",
            )
        )
    return findings


def parse_reference_signs(section: str) -> list[tuple[str, str]]:
    pairs: list[tuple[str, str]] = []
    for line in section.splitlines():
        line = line.strip()
        if not line:
            continue
        match = re.search(r"([0-9０-９]{1,4})\s*[-—:：、]\s*([\u4e00-\u9fffA-Za-z][\u4e00-\u9fffA-Za-z0-9（）()]+)", line)
        if match:
            pairs.append((match.group(2), match.group(1)))
            continue
        match = re.search(r"([\u4e00-\u9fffA-Za-z][\u4e00-\u9fffA-Za-z0-9（）()]{1,20})\s*[（(]?([0-9０-９]{1,4})[）)]?", line)
        if match:
            pairs.append((match.group(1), match.group(2)))
    return pairs


def check_reference_signs(text: str, sections: dict[str, str]) -> list[dict[str, str]]:
    findings: list[dict[str, str]] = []
    sign_section = sections.get("reference_signs", "")
    if not sign_section:
        return findings

    body_text = text.replace(sign_section, "")
    for term, number in parse_reference_signs(sign_section):
        if term and term not in body_text:
            findings.append(
                issue(
                    "reference-term-unused",
                    "suspected",
                    "附图标记表中的术语未在正文中检测到。",
                    "主要附图标记说明",
                    f"{term}={number}",
                )
            )
        if number and number not in body_text:
            findings.append(
                issue(
                    "reference-number-unused",
                    "suspected",
                    "附图标记表中的编号未在正文中检测到。",
                    "主要附图标记说明",
                    f"{term}={number}",
                )
            )
    return findings


def check_placeholders(text: str) -> list[dict[str, str]]:
    findings: list[dict[str, str]] = []
    for match in PLACEHOLDER_RE.finditer(text):
        findings.append(
            issue(
                "placeholder-text",
                "confirmed",
                "文稿中存在占位或待确认文本。",
                evidence=match.group(0),
                suggestion="提交前删除占位文本并补齐对应内容。",
            )
        )
    return findings


def run_checks(path: Path) -> dict[str, Any]:
    text, input_meta = read_text(path)
    sections, headings_seen = split_sections(text)
    checks: list[dict[str, str]] = []
    checks.extend(check_required_headings(sections, headings_seen))
    checks.extend(check_abstract(sections))
    checks.extend(check_claims(sections))
    checks.extend(check_figures(text, sections))
    checks.extend(check_reference_signs(text, sections))
    checks.extend(check_placeholders(text))

    summary = {"confirmed": 0, "suspected": 0, "info": 0}
    for item in checks:
        summary[item["severity"]] = summary.get(item["severity"], 0) + 1

    return {
        "input": str(path),
        "input_meta": input_meta,
        "detected_headings": headings_seen,
        "summary": summary,
        "checks": checks,
    }


def emit_report(report: dict[str, Any], as_json: bool, output: str | None) -> None:
    if output:
        Path(output).expanduser().resolve().write_text(
            json.dumps(report, ensure_ascii=False, indent=2) + "\n",
            encoding="utf-8",
        )
    if as_json:
        print(json.dumps(report, ensure_ascii=False, indent=2))
        return

    summary = report["summary"]
    print(
        "confirmed={confirmed} suspected={suspected} info={info}".format(
            confirmed=summary.get("confirmed", 0),
            suspected=summary.get("suspected", 0),
            info=summary.get("info", 0),
        )
    )
    for item in report["checks"]:
        location = f" [{item['location']}]" if item.get("location") else ""
        print(f"- {item['severity']} {item['code']}{location}: {item['message']}")


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Run deterministic micro-QC checks.")
    sub = parser.add_subparsers(dest="command", required=True)
    check = sub.add_parser("check", help="Check a TXT/MD/DOCX patent draft.")
    check.add_argument("input", help="Draft file to check")
    check.add_argument("--json", action="store_true")
    check.add_argument("--output", help="Optional JSON output path")
    return parser


def cmd_check(args: argparse.Namespace) -> int:
    path = Path(args.input).expanduser().resolve()
    if not path.exists():
        raise SystemExit(f"file not found: {path}")
    report = run_checks(path)
    emit_report(report, args.json, args.output)
    return 0


def main() -> int:
    args = build_parser().parse_args()
    if args.command == "check":
        return cmd_check(args)
    raise SystemExit(f"unknown command: {args.command}")


if __name__ == "__main__":
    raise SystemExit(main())
