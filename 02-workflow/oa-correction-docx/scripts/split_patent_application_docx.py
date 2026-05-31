#!/usr/bin/env python3
"""Split a combined Chinese patent application DOCX into five filing DOCX files."""

from __future__ import annotations

import argparse
import copy
import json
import re
import sys
import zipfile
from dataclasses import dataclass
from pathlib import Path

from lxml import etree


W_NS = "http://schemas.openxmlformats.org/wordprocessingml/2006/main"
NS = {"w": W_NS}
OUTPUT_NAMES = {
    "claims": "权利要求书.docx",
    "specification": "说明书.docx",
    "drawings": "说明书附图.docx",
    "abstract": "说明书摘要.docx",
    "abstract_drawings": "摘要附图.docx",
}


@dataclass
class Section:
    key: str
    start: int | None
    end: int | None
    confidence: str
    note: str = ""

    @property
    def present(self) -> bool:
        return self.start is not None and self.end is not None and self.end > self.start


def local_name(element: etree._Element) -> str:
    return etree.QName(element).localname


def block_text(block: etree._Element) -> str:
    text = "".join(block.xpath(".//w:t/text()", namespaces=NS))
    return re.sub(r"\s+", "", text)


def block_has_image(block: etree._Element) -> bool:
    return bool(
        block.xpath(
            ".//*[local-name()='drawing' or local-name()='pict' or local-name()='object']"
        )
    )


def punctuation_only(text: str) -> bool:
    return bool(text) and re.fullmatch(r"[。．.]+", text) is not None


def nonempty_indices(blocks: list[etree._Element]) -> list[int]:
    return [i for i, block in enumerate(blocks) if block_text(block) or block_has_image(block)]


def previous_nonempty(blocks: list[etree._Element], before: int) -> int | None:
    for i in range(before - 1, -1, -1):
        text = block_text(blocks[i])
        if text and not punctuation_only(text):
            return i
    return None


def next_nonempty(blocks: list[etree._Element], after: int) -> int | None:
    for i in range(after, len(blocks)):
        if block_text(blocks[i]) or block_has_image(blocks[i]):
            return i
    return None


def first_text_index(blocks: list[etree._Element], pattern: str, start: int = 0) -> int | None:
    regex = re.compile(pattern)
    for i in range(start, len(blocks)):
        if regex.search(block_text(blocks[i])):
            return i
    return None


def figure_label(text: str) -> bool:
    return re.fullmatch(r"图[0-9一二三四五六七八九十百]+", text) is not None


def has_nearby_image(blocks: list[etree._Element], index: int, window: int = 4) -> bool:
    for i in range(index, min(len(blocks), index + window)):
        if block_has_image(blocks[i]):
            return True
    return False


def find_spec_start(blocks: list[etree._Element]) -> tuple[int | None, str]:
    heading = first_text_index(blocks, r"^(说明书|说明书正文)$")
    if heading is not None:
        return heading, "explicit specification heading"

    tech = first_text_index(blocks, r"^技术领域$")
    if tech is not None:
        title = previous_nonempty(blocks, tech)
        if title is not None:
            return title, "title immediately before 技术领域"
        return tech, "技术领域 heading"

    return None, "not detected"


def find_claims_start(blocks: list[etree._Element], spec_start: int | None) -> tuple[int | None, str]:
    heading = first_text_index(blocks, r"^权利要求书$")
    if heading is not None and (spec_start is None or heading < spec_start):
        return heading, "explicit claims heading"

    stop = spec_start if spec_start is not None else len(blocks)
    for i in range(stop):
        text = block_text(blocks[i])
        if "其特征是" in text:
            return i, "first claim-like paragraph"
    for i in range(stop):
        if "如权利要求" in block_text(blocks[i]):
            return i, "dependent claim paragraph"
    return None, "not detected"


def find_drawings_start(blocks: list[etree._Element], spec_start: int | None) -> tuple[int | None, str]:
    search_from = spec_start or 0
    impl = first_text_index(blocks, r"^具体实施方式$", search_from)
    if impl is not None:
        search_from = impl + 1

    for i in range(search_from, len(blocks)):
        if figure_label(block_text(blocks[i])) and has_nearby_image(blocks, i):
            if i > search_from and block_has_image(blocks[i - 1]) and not block_text(blocks[i - 1]):
                return i - 1, "image immediately before figure label"
            return i, "figure label followed by image"

    for i in range(search_from, len(blocks)):
        if block_has_image(blocks[i]):
            return i, "first image after specification text"

    return None, "not detected"


def find_abstract_range(
    blocks: list[etree._Element], claims_start: int | None
) -> tuple[int | None, int | None, str]:
    heading = first_text_index(blocks, r"^(说明书摘要|摘要)$")
    if heading is not None:
        end = claims_start if claims_start is not None and claims_start > heading else len(blocks)
        return heading, end, "explicit abstract heading"

    if claims_start is None:
        return None, None, "claims start not detected"

    first = next_nonempty(blocks, 0)
    if first is not None and first < claims_start:
        return first, claims_start, "content before claims"

    return None, None, "not detected"


def find_abstract_drawing_range(
    blocks: list[etree._Element],
    drawings_start: int | None,
    drawings_end: int | None,
    abstract_start: int | None,
    abstract_end: int | None,
) -> tuple[int | None, int | None, str]:
    if abstract_start is not None and abstract_end is not None:
        for i in range(abstract_start, abstract_end):
            if block_has_image(blocks[i]):
                return i, i + 1, "image inside abstract section"

    if drawings_start is None or drawings_end is None or drawings_end <= drawings_start:
        return None, None, "drawings not detected"

    end = drawings_end
    for i in range(drawings_start + 1, drawings_end):
        if figure_label(block_text(blocks[i])):
            end = i
            break
    return drawings_start, end, "first detected drawing"


def trim_range(blocks: list[etree._Element], start: int | None, end: int | None) -> tuple[int | None, int | None]:
    if start is None or end is None:
        return None, None
    while start < end and not (block_text(blocks[start]) or block_has_image(blocks[start])):
        start += 1
    while end > start and not (block_text(blocks[end - 1]) or block_has_image(blocks[end - 1])):
        end -= 1
    return start, end


def detect_sections(blocks: list[etree._Element]) -> dict[str, Section]:
    spec_start, spec_note = find_spec_start(blocks)
    claims_start, claims_note = find_claims_start(blocks, spec_start)
    drawings_start, drawings_note = find_drawings_start(blocks, spec_start)

    claims_end = spec_start if spec_start is not None else drawings_start
    if claims_start is not None and claims_end is None:
        claims_end = len(blocks)

    spec_end = drawings_start if drawings_start is not None else len(blocks)
    abstract_start, abstract_end, abstract_note = find_abstract_range(blocks, claims_start)
    abstract_drawing_start, abstract_drawing_end, abstract_drawing_note = find_abstract_drawing_range(
        blocks,
        drawings_start,
        len(blocks) if drawings_start is not None else None,
        abstract_start,
        abstract_end,
    )

    ranges = {
        "abstract": (abstract_start, abstract_end, abstract_note),
        "claims": (claims_start, claims_end, claims_note),
        "specification": (spec_start, spec_end, spec_note),
        "drawings": (drawings_start, len(blocks) if drawings_start is not None else None, drawings_note),
        "abstract_drawings": (
            abstract_drawing_start,
            abstract_drawing_end,
            abstract_drawing_note,
        ),
    }

    sections: dict[str, Section] = {}
    for key, (start, end, note) in ranges.items():
        start, end = trim_range(blocks, start, end)
        confidence = "high" if start is not None and end is not None and end > start else "missing"
        sections[key] = Section(key=key, start=start, end=end, confidence=confidence, note=note)
    return sections


def read_document(input_docx: Path) -> tuple[etree._Element, list[etree._Element], etree._Element | None]:
    with zipfile.ZipFile(input_docx) as package:
        root = etree.fromstring(package.read("word/document.xml"))

    body = root.find("w:body", namespaces=NS)
    if body is None:
        raise ValueError("word/document.xml has no w:body")

    children = list(body)
    sect_pr = children[-1] if children and local_name(children[-1]) == "sectPr" else None
    blocks = children[:-1] if sect_pr is not None else children
    return root, blocks, sect_pr


def write_part(
    input_docx: Path,
    output_docx: Path,
    root: etree._Element,
    blocks: list[etree._Element],
    sect_pr: etree._Element | None,
    section: Section,
) -> None:
    if not section.present:
        raise ValueError(f"Section {section.key} is missing")

    output_root = copy.deepcopy(root)
    output_body = output_root.find("w:body", namespaces=NS)
    if output_body is None:
        raise ValueError("word/document.xml has no w:body")
    for child in list(output_body):
        output_body.remove(child)

    assert section.start is not None and section.end is not None
    for block in blocks[section.start : section.end]:
        output_body.append(copy.deepcopy(block))
    if sect_pr is not None:
        output_body.append(copy.deepcopy(sect_pr))

    xml = etree.tostring(
        output_root,
        xml_declaration=True,
        encoding="UTF-8",
        standalone=True,
    )

    output_docx.parent.mkdir(parents=True, exist_ok=True)
    with zipfile.ZipFile(input_docx, "r") as source, zipfile.ZipFile(
        output_docx, "w", zipfile.ZIP_DEFLATED
    ) as target:
        for item in source.infolist():
            if item.filename == "word/document.xml":
                target.writestr(item, xml)
            else:
                target.writestr(item, source.read(item.filename))


def section_summary(blocks: list[etree._Element], section: Section) -> dict[str, object]:
    preview = ""
    has_image = False
    if section.present:
        assert section.start is not None and section.end is not None
        for block in blocks[section.start : section.end]:
            if not preview:
                preview = block_text(block)[:80]
            has_image = has_image or block_has_image(block)
    return {
        "key": section.key,
        "present": section.present,
        "start": section.start,
        "end": section.end,
        "block_count": (section.end - section.start) if section.present else 0,
        "confidence": section.confidence,
        "note": section.note,
        "has_image": has_image,
        "preview": preview,
    }


def output_path(output_dir: Path, prefix: str | None, key: str) -> Path:
    name = OUTPUT_NAMES[key]
    if prefix:
        name = f"{prefix}-{name}"
    return output_dir / name


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Split a combined Chinese patent application DOCX into five filing DOCX files."
    )
    parser.add_argument("input_docx", type=Path)
    parser.add_argument("--output-dir", type=Path, default=Path("split"))
    parser.add_argument("--prefix", default="")
    parser.add_argument("--list-sections", action="store_true")
    parser.add_argument("--allow-missing", action="store_true")
    args = parser.parse_args()

    if not args.input_docx.exists():
        print(f"Input DOCX not found: {args.input_docx}", file=sys.stderr)
        return 2

    root, blocks, sect_pr = read_document(args.input_docx)
    sections = detect_sections(blocks)

    if args.list_sections:
        print(
            json.dumps(
                [section_summary(blocks, sections[key]) for key in OUTPUT_NAMES],
                ensure_ascii=False,
                indent=2,
            )
        )
        return 0

    missing = [key for key in OUTPUT_NAMES if not sections[key].present]
    if missing and not args.allow_missing:
        print(
            "Missing sections: " + ", ".join(missing) + ". Re-run with --list-sections.",
            file=sys.stderr,
        )
        return 3

    written: list[str] = []
    for key in OUTPUT_NAMES:
        section = sections[key]
        if not section.present:
            continue
        path = output_path(args.output_dir, args.prefix or None, key)
        write_part(args.input_docx, path, root, blocks, sect_pr, section)
        written.append(str(path))

    print(json.dumps({"written": written, "missing": missing}, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
