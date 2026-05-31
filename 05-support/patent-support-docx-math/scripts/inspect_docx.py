#!/usr/bin/env python3
"""Inspect patent-oriented DOCX files without flattening formulas."""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path
from zipfile import ZipFile

from lxml import etree

NS = {
    "m": "http://schemas.openxmlformats.org/officeDocument/2006/math",
    "r": "http://schemas.openxmlformats.org/officeDocument/2006/relationships",
    "w": "http://schemas.openxmlformats.org/wordprocessingml/2006/main",
}

SECTION_PATTERNS = [
    ("title", re.compile(r"^(发明名称[:：]?.*|title)$", re.IGNORECASE)),
    ("abstract", re.compile(r"^(摘要|说明书摘要|abstract)$", re.IGNORECASE)),
    ("field", re.compile(r"^(技术领域|technical field)$", re.IGNORECASE)),
    ("background", re.compile(r"^(背景技术|background)$", re.IGNORECASE)),
    (
        "summary",
        re.compile(
            r"^(发明内容|实用新型内容|发明目的|summary|summary of the invention)$",
            re.IGNORECASE,
        ),
    ),
    (
        "drawings",
        re.compile(
            r"^(附图说明|brief description of the drawings)$",
            re.IGNORECASE,
        ),
    ),
    (
        "embodiment",
        re.compile(
            r"^(具体实施方式|具体实施例|实施例|detailed description)$",
            re.IGNORECASE,
        ),
    ),
    ("claims", re.compile(r"^(权利要求书|权利要求|claims)$", re.IGNORECASE)),
    ("specification", re.compile(r"^(说明书|specification)$", re.IGNORECASE)),
]

STORY_PRIORITY = {
    "word/document.xml": 0,
    "word/footnotes.xml": 1,
    "word/endnotes.xml": 2,
    "word/comments.xml": 3,
}


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()

    path = Path(args.path).expanduser().resolve()
    if path.suffix.lower() != ".docx":
        parser.error("only .docx is supported; normalize .doc to .docx first")
    if not path.exists():
        parser.error(f"file not found: {path}")

    report = inspect_docx(path, args.max_contexts, args.dump_equations)
    if args.json:
        print(json.dumps(report, ensure_ascii=False, indent=2))
    else:
        print(format_report(report))
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Inspect a DOCX package and preserve formula-aware structure."
    )
    parser.add_argument("path", help="Path to a .docx file")
    parser.add_argument(
        "--json",
        action="store_true",
        help="Emit a JSON report instead of human-readable text",
    )
    parser.add_argument(
        "--max-contexts",
        type=int,
        default=8,
        help="Maximum equation contexts to print or include in JSON",
    )
    parser.add_argument(
        "--dump-equations",
        help="Write each equation as XML into the target directory",
    )
    return parser


def inspect_docx(path: Path, max_contexts: int, dump_equations: str | None) -> dict:
    with ZipFile(path) as zf:
        names = set(zf.namelist())
        document_root = parse_xml(zf, "word/document.xml")
        story_parts = list(iter_story_parts(zf, names))

        package_summary = {
            "media_files": len([name for name in names if name.startswith("word/media/")]),
            "embedded_files": len(
                [name for name in names if name.startswith("word/embeddings/")]
            ),
            "has_comments_part": "word/comments.xml" in names,
            "has_footnotes_part": "word/footnotes.xml" in names,
            "has_endnotes_part": "word/endnotes.xml" in names,
            "header_parts": len(
                [name for name in names if name.startswith("word/header")]
            ),
            "footer_parts": len(
                [name for name in names if name.startswith("word/footer")]
            ),
        }

        part_summaries = [summarize_part(name, root) for name, root in story_parts]
        sections = detect_sections(document_root)
        equation_contexts = extract_equation_contexts(document_root, max_contexts)

        dumped = None
        if dump_equations:
            dumped = dump_equations_to_dir(story_parts, Path(dump_equations))

    return {
        "file": str(path),
        "package_summary": package_summary,
        "part_summaries": part_summaries,
        "detected_sections": sections,
        "equation_contexts": equation_contexts,
        "dumped_equations_dir": dumped,
    }


def parse_xml(zf: ZipFile, name: str):
    return etree.fromstring(zf.read(name))


def iter_story_parts(zf: ZipFile, names: set[str]):
    story_names = [
        name
        for name in names
        if name.startswith("word/")
        and name.endswith(".xml")
        and (
            name in STORY_PRIORITY
            or Path(name).name.startswith("header")
            or Path(name).name.startswith("footer")
        )
    ]
    for name in sorted(story_names, key=story_sort_key):
        yield name, parse_xml(zf, name)


def story_sort_key(name: str):
    if name in STORY_PRIORITY:
        return (STORY_PRIORITY[name], name)
    if Path(name).name.startswith("header"):
        return (10, name)
    if Path(name).name.startswith("footer"):
        return (11, name)
    return (99, name)


def summarize_part(name: str, root) -> dict:
    return {
        "part": name,
        "paragraphs": len(root.xpath(".//w:p", namespaces=NS)),
        "tables": len(root.xpath(".//w:tbl", namespaces=NS)),
        "drawings": len(root.xpath(".//w:drawing", namespaces=NS)),
        "equations": len(
            root.xpath(
                ".//*[self::m:oMathPara or self::m:oMath[not(ancestor::m:oMathPara)]]",
                namespaces=NS,
            )
        ),
        "equation_paragraphs": len(root.xpath(".//m:oMathPara", namespaces=NS)),
        "embedded_objects": len(root.xpath(".//w:object", namespaces=NS)),
        "tracked_insertions": len(root.xpath(".//w:ins", namespaces=NS)),
        "tracked_deletions": len(root.xpath(".//w:del", namespaces=NS)),
        "comment_refs": len(root.xpath(".//w:commentReference", namespaces=NS)),
        "footnote_refs": len(root.xpath(".//w:footnoteReference", namespaces=NS)),
        "endnote_refs": len(root.xpath(".//w:endnoteReference", namespaces=NS)),
    }


def detect_sections(document_root) -> list[dict]:
    sections = []
    for idx, paragraph in enumerate(
        document_root.xpath("./w:body//w:p", namespaces=NS), start=1
    ):
        text = paragraph_text(paragraph)
        if not text:
            continue
        normalized = normalize_heading(text)
        for label, pattern in SECTION_PATTERNS:
            if pattern.match(normalized):
                sections.append(
                    {
                        "paragraph_index": idx,
                        "label": label,
                        "text": shorten(text, 120),
                        "style": paragraph_style(paragraph),
                    }
                )
                break
    return sections


def extract_equation_contexts(document_root, max_contexts: int) -> list[dict]:
    contexts = []
    for idx, paragraph in enumerate(
        document_root.xpath("./w:body//w:p", namespaces=NS), start=1
    ):
        math_nodes = paragraph.xpath(
            ".//*[self::m:oMathPara or self::m:oMath[not(ancestor::m:oMathPara)]]",
            namespaces=NS,
        )
        if not math_nodes:
            continue
        contexts.append(
            {
                "paragraph_index": idx,
                "style": paragraph_style(paragraph),
                "equation_count": len(math_nodes),
                "text_preview": shorten(paragraph_text(paragraph), 120),
                "equation_previews": [
                    {
                        "text": shorten(extract_math_text(node), 80),
                        "xml_snippet": shorten(compact_xml(node), 220),
                    }
                    for node in math_nodes[:3]
                ],
            }
        )
        if len(contexts) >= max_contexts:
            break
    return contexts


def dump_equations_to_dir(story_parts, output_dir: Path) -> str:
    output_dir = output_dir.expanduser().resolve()
    output_dir.mkdir(parents=True, exist_ok=True)
    manifest = []
    counter = 1

    for part_name, root in story_parts:
        paragraphs = root.xpath(".//w:p", namespaces=NS)
        for paragraph_index, paragraph in enumerate(paragraphs, start=1):
            math_nodes = paragraph.xpath(
                ".//*[self::m:oMathPara or self::m:oMath[not(ancestor::m:oMathPara)]]",
                namespaces=NS,
            )
            for node in math_nodes:
                filename = f"equation-{counter:04d}.xml"
                path = output_dir / filename
                path.write_text(
                    etree.tostring(node, encoding="unicode", pretty_print=True),
                    encoding="utf-8",
                )
                manifest.append(
                    {
                        "id": counter,
                        "file": filename,
                        "part": part_name,
                        "paragraph_index": paragraph_index,
                        "paragraph_text": shorten(paragraph_text(paragraph), 200),
                        "math_text": extract_math_text(node),
                    }
                )
                counter += 1

    (output_dir / "manifest.json").write_text(
        json.dumps(manifest, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )
    return str(output_dir)


def paragraph_text(paragraph) -> str:
    pieces = []
    for node in paragraph.iter():
        if not isinstance(node.tag, str):
            continue
        local = etree.QName(node).localname
        if local in {"t", "delText"} and node.text:
            pieces.append(node.text)
        elif local in {"tab"}:
            pieces.append("\t")
        elif local in {"br", "cr"}:
            pieces.append("\n")
    text = "".join(pieces)
    text = text.replace("\t", " ").replace("\n", " ")
    return re.sub(r"\s+", " ", text).strip()


def paragraph_style(paragraph) -> str | None:
    style = paragraph.find("./w:pPr/w:pStyle", namespaces=NS)
    if style is None:
        return None
    return style.get(f"{{{NS['w']}}}val")


def extract_math_text(node) -> str:
    texts = node.xpath(".//m:t/text() | .//w:t/text()", namespaces=NS)
    if not texts:
        texts = node.xpath(".//text()")
    return re.sub(r"\s+", " ", "".join(texts)).strip()


def compact_xml(node) -> str:
    xml = etree.tostring(node, encoding="unicode", with_tail=False)
    return re.sub(r"\s+", " ", xml).strip()


def normalize_heading(text: str) -> str:
    stripped = re.sub(r"\s+", "", text)
    return stripped.strip("：:()（）.。")


def shorten(text: str, limit: int) -> str:
    if len(text) <= limit:
        return text
    return text[: limit - 3] + "..."


def format_report(report: dict) -> str:
    lines = [
        f"File: {report['file']}",
        "",
        "Package summary:",
    ]
    for key, value in report["package_summary"].items():
        lines.append(f"  {key}: {value}")

    lines.extend(["", "Story parts:"])
    for part in report["part_summaries"]:
        lines.append(
            "  {part}: p={paragraphs} tbl={tables} draw={drawings} "
            "eq={equations} eqp={equation_paragraphs} ole={embedded_objects} "
            "ins={tracked_insertions} del={tracked_deletions} comments={comment_refs} "
            "fn={footnote_refs} en={endnote_refs}".format(**part)
        )

    lines.extend(["", "Detected sections:"])
    if report["detected_sections"]:
        for item in report["detected_sections"]:
            lines.append(
                f"  p{item['paragraph_index']}: {item['label']} "
                f"(style={item['style'] or '-'}) {item['text']}"
            )
    else:
        lines.append("  <none detected>")

    lines.extend(["", "Equation contexts:"])
    if report["equation_contexts"]:
        for item in report["equation_contexts"]:
            lines.append(
                f"  p{item['paragraph_index']} style={item['style'] or '-'} "
                f"eq={item['equation_count']} text={item['text_preview'] or '<empty>'}"
            )
            for preview in item["equation_previews"]:
                math_text = preview["text"] or "<no plain text>"
                lines.append(f"    math: {math_text}")
                lines.append(f"    xml : {preview['xml_snippet']}")
    else:
        lines.append("  <none detected>")

    if report["dumped_equations_dir"]:
        lines.extend(["", f"Dumped equations: {report['dumped_equations_dir']}"])

    return "\n".join(lines)


if __name__ == "__main__":
    sys.exit(main())
