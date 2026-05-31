#!/usr/bin/env python3
"""Compare DOCX style/theme invariance between a source and a revised copy."""

from __future__ import annotations

import argparse
import hashlib
import json
import zipfile
from collections import Counter
from pathlib import Path
from xml.etree import ElementTree as ET


NS = {
    "w": "http://schemas.openxmlformats.org/wordprocessingml/2006/main",
    "wp": "http://schemas.openxmlformats.org/drawingml/2006/wordprocessingDrawing",
}
W_VAL = f"{{{NS['w']}}}val"

DEFAULT_PARTS = [
    "word/styles.xml",
    "word/settings.xml",
    "word/fontTable.xml",
    "word/numbering.xml",
    "word/theme/theme1.xml",
]


def sha256_part(package: zipfile.ZipFile, part: str) -> dict[str, object]:
    try:
        data = package.read(part)
    except KeyError:
        return {"part": part, "present": False, "sha256": None, "size": None}
    return {
        "part": part,
        "present": True,
        "sha256": hashlib.sha256(data).hexdigest(),
        "size": len(data),
    }


def text_of(paragraph: ET.Element) -> str:
    return "".join(node.text or "" for node in paragraph.findall(".//w:t", NS))


def page_break_count(root: ET.Element) -> int:
    return sum(
        1
        for node in root.findall(".//w:br", NS)
        if node.attrib.get(W_VAL) == "page" or node.attrib.get(f"{{{NS['w']}}}type") == "page"
    )


def document_profile(path: Path) -> dict[str, object]:
    with zipfile.ZipFile(path) as package:
        root = ET.fromstring(package.read("word/document.xml"))

    paragraphs = root.findall(".//w:p", NS)
    runs = root.findall(".//w:r", NS)
    paragraph_texts = [text_of(paragraph) for paragraph in paragraphs]
    p_styles = Counter(
        node.attrib.get(W_VAL, "")
        for node in root.findall(".//w:pStyle", NS)
        if node.attrib.get(W_VAL)
    )
    r_styles = Counter(
        node.attrib.get(W_VAL, "")
        for node in root.findall(".//w:rStyle", NS)
        if node.attrib.get(W_VAL)
    )

    return {
        "paragraph_count": len(paragraphs),
        "run_count": len(runs),
        "runs_with_rPr": sum(1 for run in runs if run.find("w:rPr", NS) is not None),
        "table_count": len(root.findall(".//w:tbl", NS)),
        "drawing_count": len(root.findall(".//w:drawing", NS)),
        "section_count": len(root.findall(".//w:sectPr", NS)),
        "page_break_count": page_break_count(root),
        "paragraph_style_counts": dict(sorted(p_styles.items())),
        "run_style_counts": dict(sorted(r_styles.items())),
        "paragraph_texts": paragraph_texts,
    }


def changed_paragraph_count(before_texts: list[str], after_texts: list[str]) -> int:
    total = max(len(before_texts), len(after_texts))
    changed = 0
    for index in range(total):
        before = before_texts[index] if index < len(before_texts) else None
        after = after_texts[index] if index < len(after_texts) else None
        if before != after:
            changed += 1
    return changed


def compare_parts(before_path: Path, after_path: Path, parts: list[str]) -> list[dict[str, object]]:
    results: list[dict[str, object]] = []
    with zipfile.ZipFile(before_path) as before_pkg, zipfile.ZipFile(after_path) as after_pkg:
        for part in parts:
            before = sha256_part(before_pkg, part)
            after = sha256_part(after_pkg, part)
            results.append(
                {
                    "part": part,
                    "same": before["present"] == after["present"] and before["sha256"] == after["sha256"],
                    "before": before,
                    "after": after,
                }
            )
    return results


def build_report(before_path: Path, after_path: Path, parts: list[str]) -> dict[str, object]:
    before_profile = document_profile(before_path)
    after_profile = document_profile(after_path)
    part_results = compare_parts(before_path, after_path, parts)
    before_runs = int(before_profile["run_count"])
    after_runs = int(after_profile["run_count"])
    run_count_ratio = (after_runs / before_runs) if before_runs else 1.0
    core_structure_keys = ["table_count", "drawing_count", "section_count", "page_break_count"]
    core_structure_same = all(before_profile[key] == after_profile[key] for key in core_structure_keys)
    key_parts_same = all(item["same"] for item in part_results)
    style_usage_same = (
        before_profile["paragraph_style_counts"] == after_profile["paragraph_style_counts"]
        and before_profile["run_style_counts"] == after_profile["run_style_counts"]
    )

    issues: list[dict[str, object]] = []
    if not key_parts_same:
        issues.append({"code": "key-style-part-different", "severity": "confirmed"})
    if not core_structure_same:
        issues.append({"code": "core-structure-count-different", "severity": "confirmed"})
    if before_profile["page_break_count"] != after_profile["page_break_count"]:
        issues.append(
            {
                "code": "page-break-count-different",
                "severity": "confirmed",
                "before_page_break_count": before_profile["page_break_count"],
                "after_page_break_count": after_profile["page_break_count"],
            }
        )
    if run_count_ratio < 0.8:
        issues.append(
            {
                "code": "possible-run-flattening",
                "severity": "suspected",
                "message": "after document has more than 20% fewer runs than before",
                "before_run_count": before_runs,
                "after_run_count": after_runs,
                "run_count_ratio": round(run_count_ratio, 4),
            }
        )

    before_texts = before_profile.pop("paragraph_texts")
    after_texts = after_profile.pop("paragraph_texts")
    return {
        "schema_version": "docx-style-invariance/v1",
        "before": str(before_path),
        "after": str(after_path),
        "ok": key_parts_same and core_structure_same and run_count_ratio >= 0.8,
        "summary": {
            "key_parts_same": key_parts_same,
            "core_structure_same": core_structure_same,
            "style_usage_same": style_usage_same,
            "page_breaks_same": before_profile["page_break_count"] == after_profile["page_break_count"],
            "changed_paragraph_count": changed_paragraph_count(before_texts, after_texts),
            "run_count_ratio": round(run_count_ratio, 4),
        },
        "parts": part_results,
        "profiles": {
            "before": before_profile,
            "after": after_profile,
        },
        "issues": issues,
    }


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("before", help="Original/source DOCX")
    parser.add_argument("after", help="Revised/output DOCX")
    parser.add_argument("--parts", nargs="*", default=DEFAULT_PARTS, help="DOCX package parts to hash-compare")
    parser.add_argument("--json", action="store_true", help="Print JSON")
    parser.add_argument("--fail-on-difference", action="store_true", help="Exit non-zero when invariance checks fail")
    return parser


def main() -> int:
    args = build_parser().parse_args()
    report = build_report(Path(args.before).expanduser().resolve(), Path(args.after).expanduser().resolve(), args.parts)
    if args.json:
        print(json.dumps(report, ensure_ascii=False, indent=2))
    else:
        summary = report["summary"]
        print(
            "key_parts_same={key_parts_same} core_structure_same={core_structure_same} "
            "style_usage_same={style_usage_same} changed_paragraph_count={changed_paragraph_count} "
            "run_count_ratio={run_count_ratio}".format(**summary)
        )
        for issue in report["issues"]:
            print(f"{issue['severity']}: {issue['code']}")
    if args.fail_on_difference and not report["ok"]:
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
