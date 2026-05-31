#!/usr/bin/env python3
"""Review low-risk formal defects in a Chinese patent correction DOCX."""

from __future__ import annotations

import argparse
import json
import re
import sys
from dataclasses import asdict, dataclass
from pathlib import Path

from split_patent_application_docx import block_text, detect_sections, read_document


@dataclass
class Issue:
    code: str
    severity: str
    part: str
    body_index: int
    message: str
    text: str
    suggestion: str


def text_preview(text: str, length: int = 120) -> str:
    return text[:length]


def iter_section_blocks(blocks, section):
    if not section.present:
        return
    assert section.start is not None and section.end is not None
    for index in range(section.start, section.end):
        text = block_text(blocks[index])
        yield index, text


def add_duplicate_marker_issues(issues: list[Issue], part: str, index: int, text: str) -> None:
    for match in re.finditer(r"（(\d{1,3})）（(\d{1,3})）", text):
        issues.append(
            Issue(
                code="duplicate-parenthetical-marker",
                severity="error",
                part=part,
                body_index=index,
                message="A technical feature is followed by two parenthetical figure marks.",
                text=text_preview(text),
                suggestion=f"Keep the correct single figure mark instead of {match.group(0)}.",
            )
        )


def add_glued_marker_issues(issues: list[Issue], part: str, index: int, text: str) -> None:
    terms = [
        "内侧支撑部",
        "外侧支撑部",
        "足弓支撑块",
        "主体部",
        "让位部",
        "支撑部",
        "沉槽",
        "支撑缺口",
        "支撑凸缘",
        "上层中底",
        "下层大底",
    ]
    term_pattern = r"(?P<term>" + "|".join(map(re.escape, terms)) + r")(?P<digits>\d{4})(?!\d)"
    for match in re.finditer(term_pattern, text):
        digits = match.group("digits")
        suggested = f"{match.group('term')}{digits[:2]}"
        issues.append(
            Issue(
                code="glued-or-duplicate-marker",
                severity="error",
                part=part,
                body_index=index,
                message="A feature name appears to carry two glued figure marks.",
                text=text_preview(text),
                suggestion=f"Check whether {match.group(0)} should be {suggested}.",
            )
        )


def add_punctuation_issues(issues: list[Issue], part: str, index: int, text: str) -> None:
    if text in {"。", ".", "．"}:
        issues.append(
            Issue(
                code="standalone-period-paragraph",
                severity="error",
                part=part,
                body_index=index,
                message="A standalone period paragraph is present.",
                text=text_preview(text),
                suggestion="Remove the standalone punctuation paragraph unless it is part of a required layout.",
            )
        )
    if "，," in text or "，，" in text or "。。" in text:
        issues.append(
            Issue(
                code="duplicate-punctuation",
                severity="warning",
                part=part,
                body_index=index,
                message="Repeated punctuation was detected.",
                text=text_preview(text),
                suggestion="Reduce repeated punctuation to the intended single punctuation mark.",
            )
        )


def claim_paragraphs(blocks, claims_section):
    items: list[tuple[int, int, str]] = []
    claim_no = 0
    if not claims_section.present:
        return items
    for index, text in iter_section_blocks(blocks, claims_section):
        if not text or text in {"。", ".", "．"}:
            continue
        if "其特征是" in text or text.startswith("如权利要求") or text.startswith("一种"):
            claim_no += 1
            items.append((claim_no, index, text))
    return items


def add_dependency_issues(issues: list[Issue], blocks, claims_section) -> None:
    items = claim_paragraphs(blocks, claims_section)
    existing = {claim_no for claim_no, _, _ in items}
    for claim_no, index, text in items:
        for raw_ref in re.findall(r"如权利要求([0-9]+)", text):
            ref = int(raw_ref)
            if ref not in existing:
                message = "A claim dependency points to a non-existent claim."
            elif ref >= claim_no:
                message = "A claim dependency does not point to an earlier claim."
            else:
                continue
            issues.append(
                Issue(
                    code="claim-dependency",
                    severity="error",
                    part="claims",
                    body_index=index,
                    message=message,
                    text=text_preview(text),
                    suggestion="Confirm and repair the claim dependency before filing.",
                )
            )


def add_claim_period_issues(issues: list[Issue], blocks, claims_section) -> None:
    items = claim_paragraphs(blocks, claims_section)
    for claim_no, index, text in items:
        period_count = text.count("。") + text.count("．")
        if period_count > 1:
            issues.append(
                Issue(
                    code="multiple-periods-in-claim",
                    severity="error",
                    part="claims",
                    body_index=index,
                    message=f"Claim {claim_no} contains more than one sentence-ending period.",
                    text=text_preview(text),
                    suggestion="Keep a period only at the end of the claim unless a special layout requires otherwise.",
                )
            )


def review(input_docx: Path) -> list[Issue]:
    _, blocks, _ = read_document(input_docx)
    sections = detect_sections(blocks)
    issues: list[Issue] = []

    for part in ("claims", "specification", "abstract"):
        section = sections.get(part)
        if section is None or not section.present:
            issues.append(
                Issue(
                    code="missing-section",
                    severity="error",
                    part=part,
                    body_index=-1,
                    message="Expected section was not detected.",
                    text="",
                    suggestion="Inspect section boundaries before editing or splitting.",
                )
            )
            continue
        for index, text in iter_section_blocks(blocks, section):
            add_duplicate_marker_issues(issues, part, index, text)
            add_glued_marker_issues(issues, part, index, text)
            add_punctuation_issues(issues, part, index, text)

    add_dependency_issues(issues, blocks, sections["claims"])
    add_claim_period_issues(issues, blocks, sections["claims"])
    return issues


def print_text(issues: list[Issue]) -> None:
    if not issues:
        print("No low-risk formal issues detected.")
        return
    for issue in issues:
        print(f"[{issue.severity}] {issue.code} {issue.part}@{issue.body_index}")
        print(f"  {issue.message}")
        if issue.text:
            print(f"  text: {issue.text}")
        print(f"  suggestion: {issue.suggestion}")


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Review low-risk formal defects in a Chinese patent correction DOCX."
    )
    parser.add_argument("input_docx", type=Path)
    parser.add_argument("--format", choices=("json", "text"), default="json")
    args = parser.parse_args()

    if not args.input_docx.exists():
        print(f"Input DOCX not found: {args.input_docx}", file=sys.stderr)
        return 2

    issues = review(args.input_docx)
    if args.format == "json":
        print(json.dumps([asdict(issue) for issue in issues], ensure_ascii=False, indent=2))
    else:
        print_text(issues)
    return 1 if any(issue.severity == "error" for issue in issues) else 0


if __name__ == "__main__":
    raise SystemExit(main())
