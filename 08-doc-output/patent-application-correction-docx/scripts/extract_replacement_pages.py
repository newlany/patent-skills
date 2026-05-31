#!/usr/bin/env python3
"""Extract patent replacement-page content and optionally render it into a template."""

from __future__ import annotations

import argparse
import copy
import re
import sys
from pathlib import Path
from zipfile import ZIP_DEFLATED, ZipFile

from lxml import etree

W_NS = "http://schemas.openxmlformats.org/wordprocessingml/2006/main"
CT_NS = "http://schemas.openxmlformats.org/package/2006/content-types"
NS = {"w": W_NS}
W = f"{{{W_NS}}}"
CT = f"{{{CT_NS}}}"

DOCX_MAIN_CONTENT_TYPE = (
    "application/vnd.openxmlformats-officedocument.wordprocessingml.document.main+xml"
)
DOTX_MAIN_CONTENT_TYPE = (
    "application/vnd.openxmlformats-officedocument.wordprocessingml.template.main+xml"
)

TOP_LEVEL_PATTERNS = [
    ("abstract-drawings", re.compile(r"^(摘要附图)$", re.IGNORECASE)),
    ("drawings", re.compile(r"^(说明书附图|附图说明|附图)$", re.IGNORECASE)),
    ("claims", re.compile(r"^(权利要求书|权利要求)$", re.IGNORECASE)),
    ("abstract", re.compile(r"^(摘要|说明书摘要)$", re.IGNORECASE)),
    ("specification", re.compile(r"^(说明书)$", re.IGNORECASE)),
]

SECTION_ALIASES = {
    "claims": {"claims"},
    "specification": {"specification"},
    "abstract": {"abstract"},
    "drawings": {"drawings", "abstract-drawings"},
}

STANDALONE_FIGURE_LABEL = re.compile(r"^(图|figure)\s*\d+$", re.IGNORECASE)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Extract a patent replacement-page section from a DOCX."
    )
    parser.add_argument("input", help="Source corrected DOCX file")
    parser.add_argument(
        "--output",
        help="Output DOCX path. Required unless --list-sections is used.",
    )
    parser.add_argument(
        "--template",
        help="Optional DOCX or DOTX template used as the output base package",
    )
    parser.add_argument(
        "--section",
        choices=sorted(SECTION_ALIASES),
        help="Known top-level section to extract",
    )
    parser.add_argument(
        "--start-index",
        type=int,
        help="1-based paragraph index at which extraction starts",
    )
    parser.add_argument(
        "--end-index",
        type=int,
        help="1-based paragraph index at which extraction ends (exclusive)",
    )
    parser.add_argument(
        "--start-text",
        help="Start extraction at the first paragraph whose normalized text contains this value",
    )
    parser.add_argument(
        "--end-text",
        help="End extraction before the first later paragraph whose normalized text contains this value",
    )
    parser.add_argument(
        "--keep-trailing-figure-pages",
        action="store_true",
        help="Keep trailing standalone figure-label pages instead of trimming them in specification mode",
    )
    parser.add_argument(
        "--list-sections",
        action="store_true",
        help="List detected top-level sections and exit",
    )
    return parser


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()

    input_path = Path(args.input).expanduser().resolve()
    if not input_path.exists():
        parser.error(f"file not found: {input_path}")
    if input_path.suffix.lower() != ".docx":
        parser.error("only .docx is supported as the source; normalize .doc first")

    template_path = None
    if args.template:
        template_path = Path(args.template).expanduser().resolve()
        if not template_path.exists():
            parser.error(f"template not found: {template_path}")
        if template_path.suffix.lower() not in {".docx", ".dotx"}:
            parser.error("template must be .docx or .dotx")

    source_tree, source_body = load_document(input_path)
    blocks = body_blocks(source_body)
    paragraphs = collect_body_paragraphs(blocks)
    detected_sections = detect_top_level_sections(paragraphs)

    if args.list_sections:
        print(format_sections(detected_sections))
        return 0

    if not args.output:
        parser.error("--output is required unless --list-sections is used")

    output_path = Path(args.output).expanduser().resolve()
    if output_path.suffix.lower() != ".docx":
        parser.error("output must be a .docx path")

    start_pos, end_pos = resolve_range(args, blocks, paragraphs, detected_sections)
    selected_blocks = blocks[start_pos:end_pos]
    if not selected_blocks:
        parser.error("selected range is empty")

    if template_path:
        ensure_template_safe_selection(selected_blocks)
        output_tree, output_body = load_document(template_path)
        replace_body_with_selection(output_body, selected_blocks)
        save_package(template_path, output_path, output_tree, template_mode=True)
        base_name = template_path.name
    else:
        replace_body_with_selection(source_body, selected_blocks)
        save_package(input_path, output_path, source_tree, template_mode=False)
        base_name = input_path.name

    print(
        f"Extracted {len(selected_blocks)} body block(s) from {input_path.name} "
        f"into {output_path.name} using base {base_name}"
    )
    return 0


def load_document(path: Path):
    with ZipFile(path) as zf:
        xml_bytes = zf.read("word/document.xml")
    tree = etree.fromstring(xml_bytes)
    body = tree.find("w:body", namespaces=NS)
    if body is None:
        raise SystemExit("word/document.xml does not contain w:body")
    return tree, body


def body_blocks(body) -> list:
    return [child for child in body if child.tag != f"{W}sectPr"]


def collect_body_paragraphs(blocks: list) -> list[dict]:
    paragraphs = []
    for block_index, child in enumerate(blocks):
        if child.tag != f"{W}p":
            continue
        text = paragraph_text(child)
        paragraphs.append(
            {
                "paragraph_index": len(paragraphs) + 1,
                "block_index": block_index,
                "text": text,
                "normalized_text": normalize_text(text),
                "style": paragraph_style(child),
            }
        )
    return paragraphs


def detect_top_level_sections(paragraphs: list[dict]) -> list[dict]:
    sections = []
    for paragraph in paragraphs:
        label = classify_top_level(paragraph["normalized_text"])
        if label:
            sections.append(
                {
                    "label": label,
                    "paragraph_index": paragraph["paragraph_index"],
                    "block_index": paragraph["block_index"],
                    "text": paragraph["text"],
                    "style": paragraph["style"],
                }
            )
    return sections


def classify_top_level(normalized_text: str) -> str | None:
    if not normalized_text:
        return None
    for label, pattern in TOP_LEVEL_PATTERNS:
        if pattern.match(normalized_text):
            return label
    return None


def resolve_range(
    args,
    blocks: list,
    paragraphs: list[dict],
    sections: list[dict],
) -> tuple[int, int]:
    start_pos = 0
    end_pos = len(blocks)

    if args.section:
        named_range = resolve_named_section(args.section, blocks, sections)
        if named_range is None:
            if not any(
                [
                    args.start_index is not None,
                    args.start_text,
                    args.end_index is not None,
                    args.end_text,
                ]
            ):
                raise SystemExit(
                    f"could not detect the '{args.section}' section automatically; "
                    "use --list-sections or manual boundary overrides"
                )
        else:
            start_pos, end_pos = named_range

    if args.start_index is not None:
        start_pos = paragraph_index_to_block(args.start_index, paragraphs)
    elif args.start_text:
        start_pos = find_block_by_text(args.start_text, paragraphs)

    if args.end_index is not None:
        end_pos = paragraph_index_to_block(args.end_index, paragraphs)
    elif args.end_text:
        end_pos = find_block_by_text(args.end_text, paragraphs, start_after=start_pos)

    if (
        args.section == "specification"
        and args.end_index is None
        and not args.end_text
        and not args.keep_trailing_figure_pages
    ):
        end_pos = trim_trailing_figure_pages(blocks, start_pos, end_pos)

    if start_pos >= end_pos:
        raise SystemExit("invalid range: start must be earlier than end")

    return start_pos, end_pos


def resolve_named_section(
    section: str,
    blocks: list,
    sections: list[dict],
) -> tuple[int, int] | None:
    labels = SECTION_ALIASES[section]
    start = next((item for item in sections if item["label"] in labels), None)
    if start is None:
        return None

    end_pos = len(blocks)
    for item in sections:
        if item["block_index"] <= start["block_index"]:
            continue
        if item["label"] not in labels:
            end_pos = item["block_index"]
            break

    return start["block_index"], end_pos


def trim_trailing_figure_pages(
    blocks: list,
    start_pos: int,
    end_pos: int,
) -> int:
    trimmed_end = end_pos
    while trimmed_end > start_pos:
        child = blocks[trimmed_end - 1]
        if child.tag != f"{W}p":
            break
        text = paragraph_text(child).strip()
        has_drawings = bool(
            child.xpath(".//w:drawing | .//w:pict | .//w:object", namespaces=NS)
        )
        removable = (
            not text
            or STANDALONE_FIGURE_LABEL.match(text) is not None
            or (has_drawings and not text)
        )
        if not removable:
            break
        trimmed_end -= 1
    return trimmed_end


def paragraph_index_to_block(paragraph_index: int, paragraphs: list[dict]) -> int:
    match = next(
        (item for item in paragraphs if item["paragraph_index"] == paragraph_index),
        None,
    )
    if match is None:
        raise SystemExit(f"paragraph index out of range: {paragraph_index}")
    return match["block_index"]


def find_block_by_text(
    target: str,
    paragraphs: list[dict],
    start_after: int | None = None,
) -> int:
    normalized_target = normalize_text(target)
    for paragraph in paragraphs:
        if start_after is not None and paragraph["block_index"] <= start_after:
            continue
        if normalized_target and normalized_target in paragraph["normalized_text"]:
            return paragraph["block_index"]
    raise SystemExit(f"could not find paragraph text: {target}")


def ensure_template_safe_selection(selected_blocks: list) -> None:
    media_xpath = (
        ".//w:drawing | .//w:object | .//w:pict | .//w:footnoteReference | "
        ".//w:endnoteReference | .//w:commentReference"
    )
    for child in selected_blocks:
        if child.xpath(media_xpath, namespaces=NS):
            raise SystemExit(
                "template mode currently supports text-only claim/specification ranges; "
                "remove figures or use a manual non-template workflow for that range"
            )


def replace_body_with_selection(body, selected_blocks: list) -> None:
    original_sectpr = body.find("w:sectPr", namespaces=NS)
    for child in list(body):
        body.remove(child)

    for child in selected_blocks:
        body.append(copy.deepcopy(child))

    if original_sectpr is not None:
        body.append(copy.deepcopy(original_sectpr))


def save_package(base_path: Path, output: Path, tree, template_mode: bool) -> None:
    output.parent.mkdir(parents=True, exist_ok=True)
    document_bytes = etree.tostring(
        tree,
        encoding="UTF-8",
        xml_declaration=True,
        standalone="yes",
    )

    with ZipFile(base_path) as src_zip, ZipFile(
        output, "w", compression=ZIP_DEFLATED
    ) as out_zip:
        for item in src_zip.infolist():
            if item.filename == "word/document.xml":
                data = document_bytes
            elif template_mode and item.filename == "[Content_Types].xml":
                data = convert_template_content_types(src_zip.read(item.filename))
            else:
                data = src_zip.read(item.filename)
            out_zip.writestr(item, data)


def convert_template_content_types(content_types_bytes: bytes) -> bytes:
    tree = etree.fromstring(content_types_bytes)
    changed = False
    for override in tree.findall(f"{CT}Override"):
        if override.get("PartName") == "/word/document.xml":
            if override.get("ContentType") == DOTX_MAIN_CONTENT_TYPE:
                override.set("ContentType", DOCX_MAIN_CONTENT_TYPE)
                changed = True
    if not changed:
        return content_types_bytes
    return etree.tostring(
        tree,
        encoding="UTF-8",
        xml_declaration=True,
        standalone="yes",
    )


def paragraph_text(paragraph) -> str:
    text_nodes = paragraph.xpath(".//w:t/text() | .//w:delText/text()", namespaces=NS)
    return "".join(text_nodes).strip()


def paragraph_style(paragraph) -> str | None:
    style = paragraph.find("./w:pPr/w:pStyle", namespaces=NS)
    if style is None:
        return None
    return style.get(f"{W}val") or style.get("val")


def normalize_text(text: str) -> str:
    normalized = text.strip().lower()
    normalized = re.sub(r"\s+", "", normalized)
    normalized = re.sub(r"[()（）\[\]【】,，.。:：;；、\-—_]", "", normalized)
    return normalized


def format_sections(sections: list[dict]) -> str:
    if not sections:
        return "No top-level patent sections detected."
    lines = []
    for item in sections:
        preview = item["text"] or "<empty>"
        style = item["style"] or "-"
        lines.append(
            f"{item['paragraph_index']:>4} | {item['block_index']:>4} | "
            f"{item['label']:<16} | {style:<12} | {preview}"
        )
    return "\n".join(lines)


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except KeyboardInterrupt:
        sys.exit(130)
