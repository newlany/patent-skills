#!/usr/bin/env python3
"""Replace DOCX paragraph text while preserving paragraph run templates."""

from __future__ import annotations

import argparse
import copy
import json
import sys
import zipfile
from pathlib import Path
from xml.etree import ElementTree as ET


NS = {"w": "http://schemas.openxmlformats.org/wordprocessingml/2006/main"}
W = NS["w"]
XML_SPACE = "{http://www.w3.org/XML/1998/namespace}space"
PRESERVABLE_RUN_CHILDREN = {
    f"{{{W}}}rPr",
    f"{{{W}}}t",
    f"{{{W}}}br",
    f"{{{W}}}tab",
    f"{{{W}}}cr",
    f"{{{W}}}lastRenderedPageBreak",
    f"{{{W}}}noBreakHyphen",
    f"{{{W}}}softHyphen",
}

PREFIXES = {
    "w": W,
    "r": "http://schemas.openxmlformats.org/officeDocument/2006/relationships",
    "m": "http://schemas.openxmlformats.org/officeDocument/2006/math",
    "wp": "http://schemas.openxmlformats.org/drawingml/2006/wordprocessingDrawing",
    "a": "http://schemas.openxmlformats.org/drawingml/2006/main",
    "pic": "http://schemas.openxmlformats.org/drawingml/2006/picture",
    "mc": "http://schemas.openxmlformats.org/markup-compatibility/2006",
    "w14": "http://schemas.microsoft.com/office/word/2010/wordml",
    "w15": "http://schemas.microsoft.com/office/word/2012/wordml",
}

for prefix, uri in PREFIXES.items():
    ET.register_namespace(prefix, uri)


def qn(local: str) -> str:
    return f"{{{W}}}{local}"


def paragraph_text(paragraph: ET.Element) -> str:
    return "".join(node.text or "" for node in paragraph.findall(".//w:t", NS))


def is_plain_text_paragraph(paragraph: ET.Element) -> bool:
    """Only rebuild text paragraphs; preserve simple inline breaks/tabs, reject fields/drawings."""
    for child in list(paragraph):
        if child.tag not in {qn("pPr"), qn("r")}:
            return False
        if child.tag == qn("r"):
            for run_child in list(child):
                if run_child.tag not in PRESERVABLE_RUN_CHILDREN:
                    return False
    return True


def clone_run_templates(paragraph: ET.Element) -> list[dict[str, object]]:
    templates: list[dict[str, object]] = []
    for run in paragraph.findall("w:r", NS):
        run_properties = run.find("w:rPr", NS)
        tokens: list[tuple[str, object]] = []
        text_length = 0
        for child in list(run):
            if child.tag == qn("rPr"):
                continue
            if child.tag == qn("t"):
                length = len(child.text or "")
                text_length += length
                tokens.append(("text", length))
            else:
                tokens.append(("element", copy.deepcopy(child)))
        templates.append(
            {
                "rpr": copy.deepcopy(run_properties) if run_properties is not None else None,
                "text_length": text_length,
                "tokens": tokens,
            }
        )
    return templates


def set_text_preserving_runs(paragraph: ET.Element, text: str) -> None:
    paragraph_properties = paragraph.find("w:pPr", NS)
    run_templates = clone_run_templates(paragraph)

    if not run_templates:
        run_templates.append({"rpr": None, "text_length": len(text), "tokens": [("text", len(text))]})

    for child in list(paragraph):
        if child is not paragraph_properties:
            paragraph.remove(child)

    remaining = text
    text_run_indexes = [idx for idx, template in enumerate(run_templates) if int(template["text_length"]) > 0]
    final_text_run_index = text_run_indexes[-1] if text_run_indexes else len(run_templates) - 1
    emitted_text = False
    for index, template in enumerate(run_templates):
        old_length = int(template["text_length"])
        if old_length <= 0:
            chunk = remaining
        elif index == final_text_run_index:
            chunk = remaining
            remaining = ""
        else:
            take = min(len(remaining), old_length)
            chunk = remaining[:take]
            remaining = remaining[take:]
        run = ET.SubElement(paragraph, qn("r"))
        run_properties = template["rpr"]
        if run_properties is not None:
            run.append(run_properties)
        text_remaining = chunk
        text_token_positions = [
            token_index for token_index, token in enumerate(template["tokens"]) if token[0] == "text"
        ]
        for token_index, token in enumerate(template["tokens"]):
            token_kind, token_value = token
            if token_kind == "element":
                run.append(copy.deepcopy(token_value))
                continue
            if token_index == text_token_positions[-1]:
                token_text = text_remaining
                text_remaining = ""
            else:
                take = min(len(text_remaining), int(token_value))
                token_text = text_remaining[:take]
                text_remaining = text_remaining[take:]
            text_node = ET.SubElement(run, qn("t"))
            text_node.set(XML_SPACE, "preserve")
            text_node.text = token_text
            emitted_text = True
    if remaining or not emitted_text:
        run = ET.SubElement(paragraph, qn("r"))
        text_node = ET.SubElement(run, qn("t"))
        text_node.set(XML_SPACE, "preserve")
        text_node.text = remaining or text


def load_replacements(path: Path) -> list[dict[str, str]]:
    payload = json.loads(path.read_text(encoding="utf-8"))
    if isinstance(payload, list):
        replacements = payload
    elif isinstance(payload, dict):
        replacements = payload.get("paragraph_replacements") or payload.get("replacements") or []
    else:
        raise SystemExit("replacement JSON must be an object or a list")

    normalized: list[dict[str, str]] = []
    for index, item in enumerate(replacements, start=1):
        if not isinstance(item, dict) or "old" not in item or "new" not in item:
            raise SystemExit(f"replacement #{index} must contain old/new")
        normalized.append({"old": str(item["old"]), "new": str(item["new"])})
    return normalized


def apply_replacements(
    root: ET.Element,
    replacements: list[dict[str, str]],
    *,
    strip_match: bool,
    strict: bool,
) -> dict[str, object]:
    match_counts = [0 for _ in replacements]
    modified = 0
    skipped_complex: list[dict[str, object]] = []

    for paragraph_index, paragraph in enumerate(root.findall(".//w:p", NS), start=1):
        current_text = paragraph_text(paragraph)
        comparable_text = current_text.strip() if strip_match else current_text
        for replacement_index, replacement in enumerate(replacements):
            old = replacement["old"].strip() if strip_match else replacement["old"]
            if comparable_text != old:
                continue
            match_counts[replacement_index] += 1
            if not is_plain_text_paragraph(paragraph):
                skipped_complex.append(
                    {
                        "paragraph_index": paragraph_index,
                        "replacement_index": replacement_index + 1,
                        "text_preview": current_text[:80],
                    }
                )
                if strict:
                    raise SystemExit(
                        f"matched paragraph {paragraph_index} is complex; refusing to rebuild runs"
                    )
                break
            set_text_preserving_runs(paragraph, replacement["new"])
            modified += 1
            break

    missing = [
        {"replacement_index": index + 1, "old_preview": replacements[index]["old"][:80]}
        for index, count in enumerate(match_counts)
        if count == 0
    ]
    if strict and missing:
        raise SystemExit(f"{len(missing)} replacement(s) did not match")

    return {
        "requested": len(replacements),
        "matched": sum(match_counts),
        "modified": modified,
        "missing": missing,
        "skipped_complex": skipped_complex,
    }


def rewrite_docx(input_path: Path, output_path: Path, document_xml: bytes) -> None:
    output_path.parent.mkdir(parents=True, exist_ok=True)
    with zipfile.ZipFile(input_path, "r") as zin, zipfile.ZipFile(output_path, "w", zipfile.ZIP_DEFLATED) as zout:
        for info in zin.infolist():
            payload = document_xml if info.filename == "word/document.xml" else zin.read(info.filename)
            zout.writestr(info, payload)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("input", help="Source .docx file")
    parser.add_argument("--output", required=True, help="Output .docx file")
    parser.add_argument("--replacements-json", required=True, help="JSON file with paragraph_replacements")
    parser.add_argument("--strip-match", action="store_true", help="Compare old paragraph text after strip()")
    parser.add_argument("--strict", action="store_true", help="Fail on missing or complex matched paragraphs")
    parser.add_argument("--json", action="store_true", help="Print JSON summary")
    return parser


def main() -> int:
    args = build_parser().parse_args()
    input_path = Path(args.input).expanduser().resolve()
    output_path = Path(args.output).expanduser().resolve()
    replacements_path = Path(args.replacements_json).expanduser().resolve()

    replacements = load_replacements(replacements_path)
    with zipfile.ZipFile(input_path, "r") as package:
        root = ET.fromstring(package.read("word/document.xml"))

    summary = apply_replacements(root, replacements, strip_match=args.strip_match, strict=args.strict)
    document_xml = ET.tostring(root, encoding="utf-8", xml_declaration=True)
    rewrite_docx(input_path, output_path, document_xml)

    payload = {
        "schema_version": "docx-preserve-runs-replace/v1",
        "input": str(input_path),
        "output": str(output_path),
        **summary,
    }
    if args.json:
        print(json.dumps(payload, ensure_ascii=False, indent=2))
    else:
        print(f"modified={summary['modified']} matched={summary['matched']} output={output_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
