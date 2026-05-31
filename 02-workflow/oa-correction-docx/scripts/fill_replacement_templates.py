#!/usr/bin/env python3
"""Fill replacement-page templates with corrected DOCX content."""

from __future__ import annotations

import argparse
import copy
import json
import posixpath
import re
import sys
import zipfile
from pathlib import Path

from lxml import etree

SCRIPT_DIR = Path(__file__).resolve().parent
if str(SCRIPT_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPT_DIR))

from split_patent_application_docx import (  # noqa: E402
    NS,
    detect_sections,
    read_document,
)


W_NS = "http://schemas.openxmlformats.org/wordprocessingml/2006/main"
R_NS = "http://schemas.openxmlformats.org/officeDocument/2006/relationships"
REL_NS = "http://schemas.openxmlformats.org/package/2006/relationships"
CT_NS = "http://schemas.openxmlformats.org/package/2006/content-types"
REL_Q = f"{{{REL_NS}}}"
CT_Q = f"{{{CT_NS}}}"

DEFAULT_TEMPLATES = {
    "claims": Path("/Users/chrynos/Library/CloudStorage/OneDrive-个人/工作/工作文档/模板/权利要求书替换页.docx"),
    "specification": Path("/Users/chrynos/Library/CloudStorage/OneDrive-个人/工作/工作文档/模板/说明书替换页.docx"),
    "abstract": Path("/Users/chrynos/Library/CloudStorage/OneDrive-个人/工作/工作文档/模板/说明书摘要替换页.docx"),
}
DEFAULT_OUTPUT_NAMES = {
    "claims": "权利要求书替换页.docx",
    "specification": "说明书替换页.docx",
    "abstract": "说明书摘要替换页.docx",
}


def parse_xml(package: zipfile.ZipFile, name: str) -> etree._Element:
    return etree.fromstring(package.read(name))


def serialize(root: etree._Element) -> bytes:
    return etree.tostring(root, xml_declaration=True, encoding="UTF-8", standalone=True)


def body_and_sectpr(root: etree._Element) -> tuple[etree._Element, etree._Element | None]:
    body = root.find("w:body", namespaces=NS)
    if body is None:
        raise ValueError("word/document.xml has no w:body")
    children = list(body)
    sect_pr = children[-1] if children and etree.QName(children[-1]).localname == "sectPr" else None
    return body, sect_pr


def section_blocks(source_docx: Path, section_key: str) -> list[etree._Element]:
    _root, blocks, _sect_pr = read_document(source_docx)
    sections = detect_sections(blocks)
    section = sections[section_key]
    if not section.present or section.start is None or section.end is None:
        raise ValueError(f"Section {section_key} was not detected in {source_docx}")
    return [copy.deepcopy(block) for block in blocks[section.start : section.end]]


def all_body_blocks(source_docx: Path) -> list[etree._Element]:
    _root, blocks, _sect_pr = read_document(source_docx)
    return [copy.deepcopy(block) for block in blocks]


def strip_section_properties(blocks: list[etree._Element]) -> None:
    """Keep replacement pages on the target template's page setup and headers."""
    for block in blocks:
        for sect_pr in list(block.xpath(".//w:sectPr", namespaces=NS)):
            parent = sect_pr.getparent()
            if parent is not None:
                parent.remove(sect_pr)


def referenced_relationship_ids(blocks: list[etree._Element]) -> set[str]:
    ids: set[str] = set()
    for block in blocks:
        for element in block.iter():
            for value in element.attrib.values():
                if isinstance(value, str) and re.fullmatch(r"rId[0-9A-Za-z_-]+", value):
                    ids.add(value)
            for attr in (f"{{{R_NS}}}id", f"{{{R_NS}}}embed", f"{{{R_NS}}}link"):
                value = element.get(attr)
                if value:
                    ids.add(value)
    return ids


def rewrite_relationship_ids(blocks: list[etree._Element], rel_map: dict[str, str]) -> None:
    if not rel_map:
        return
    for block in blocks:
        for element in block.iter():
            for attr, value in list(element.attrib.items()):
                if value in rel_map:
                    element.set(attr, rel_map[value])


def relationship_root(package: zipfile.ZipFile) -> etree._Element:
    return parse_xml(package, "word/_rels/document.xml.rels")


def next_rid(root: etree._Element) -> str:
    used = {
        int(match.group(1))
        for rel in root.findall(f"{REL_Q}Relationship")
        for match in [re.fullmatch(r"rId(\d+)", rel.get("Id", ""))]
        if match
    }
    n = 1
    while n in used:
        n += 1
    return f"rId{n}"


def ensure_relationship(root: etree._Element, rel_type: str, target: str) -> None:
    for rel in root.findall(f"{REL_Q}Relationship"):
        if rel.get("Type") == rel_type and rel.get("Target") == target:
            return
    rel = etree.SubElement(root, f"{REL_Q}Relationship")
    rel.set("Id", next_rid(root))
    rel.set("Type", rel_type)
    rel.set("Target", target)


def add_override(content_types: etree._Element, part_name: str, content_type: str) -> None:
    for override in content_types.findall(f"{CT_Q}Override"):
        if override.get("PartName") == part_name:
            return
    override = etree.SubElement(content_types, f"{CT_Q}Override")
    override.set("PartName", part_name)
    override.set("ContentType", content_type)


def add_default(content_types: etree._Element, extension: str, content_type: str) -> None:
    for default in content_types.findall(f"{CT_Q}Default"):
        if default.get("Extension") == extension:
            return
    default = etree.SubElement(content_types, f"{CT_Q}Default")
    default.set("Extension", extension)
    default.set("ContentType", content_type)


def merge_content_type_for_part(
    content_types: etree._Element,
    source_content_types: etree._Element,
    part_name: str,
) -> None:
    for override in source_content_types.findall(f"{CT_Q}Override"):
        if override.get("PartName") == part_name:
            add_override(content_types, part_name, override.get("ContentType", ""))
            return
    extension = part_name.rsplit(".", 1)[-1] if "." in part_name else ""
    if not extension:
        return
    for default in source_content_types.findall(f"{CT_Q}Default"):
        if default.get("Extension") == extension:
            add_default(content_types, extension, default.get("ContentType", ""))
            return


def merge_missing_styles(template_styles: etree._Element, source_styles: etree._Element) -> etree._Element:
    existing = {
        style.get(f"{{{W_NS}}}styleId")
        for style in template_styles.findall("w:style", namespaces=NS)
    }
    for style in source_styles.findall("w:style", namespaces=NS):
        style_id = style.get(f"{{{W_NS}}}styleId")
        if style_id and style_id not in existing:
            template_styles.append(copy.deepcopy(style))
            existing.add(style_id)
    return template_styles


def internal_part_name(target: str) -> str:
    return posixpath.normpath(posixpath.join("word", target)).lstrip("/")


def unique_target(
    target: str,
    template_package: zipfile.ZipFile,
    pending_parts: dict[str, bytes],
    source_bytes: bytes,
) -> str:
    part_name = internal_part_name(target)
    existing = None
    if part_name in pending_parts:
        existing = pending_parts[part_name]
    elif part_name in template_package.namelist():
        existing = template_package.read(part_name)
    if existing is None or existing == source_bytes:
        return target

    directory, basename = posixpath.split(target)
    stem, dot, suffix = basename.partition(".")
    index = 1
    while True:
        candidate_name = f"{stem}-filled-{index}{dot}{suffix}" if dot else f"{stem}-filled-{index}"
        candidate = posixpath.join(directory, candidate_name) if directory else candidate_name
        candidate_part = internal_part_name(candidate)
        if candidate_part not in pending_parts and candidate_part not in template_package.namelist():
            return candidate
        index += 1


def copy_referenced_relationships(
    blocks: list[etree._Element],
    template_package: zipfile.ZipFile,
    source_package: zipfile.ZipFile,
    template_rels: etree._Element,
    content_types: etree._Element,
    source_content_types: etree._Element,
    pending_parts: dict[str, bytes],
) -> None:
    ids = referenced_relationship_ids(blocks)
    if not ids:
        return

    source_rels = relationship_root(source_package)
    source_by_id = {rel.get("Id"): rel for rel in source_rels.findall(f"{REL_Q}Relationship")}
    rel_map: dict[str, str] = {}
    for rid in sorted(ids):
        source_rel = source_by_id.get(rid)
        if source_rel is None:
            continue
        new_rel = etree.SubElement(template_rels, f"{REL_Q}Relationship")
        new_id = next_rid(template_rels)
        new_rel.set("Id", new_id)
        new_rel.set("Type", source_rel.get("Type", ""))
        target = source_rel.get("Target", "")
        if source_rel.get("TargetMode"):
            new_rel.set("TargetMode", source_rel.get("TargetMode", ""))
            new_rel.set("Target", target)
        else:
            source_part = internal_part_name(target)
            if source_part not in source_package.namelist():
                raise ValueError(f"Referenced part is missing from source package: {source_part}")
            source_bytes = source_package.read(source_part)
            target = unique_target(target, template_package, pending_parts, source_bytes)
            target_part = internal_part_name(target)
            pending_parts[target_part] = source_bytes
            merge_content_type_for_part(content_types, source_content_types, "/" + source_part)
            if target_part != source_part:
                merge_content_type_for_part(content_types, source_content_types, "/" + target_part)
            new_rel.set("Target", target)
        rel_map[rid] = new_id
    rewrite_relationship_ids(blocks, rel_map)


def fill_one(
    template_docx: Path,
    source_docx: Path,
    output_docx: Path,
    blocks: list[etree._Element],
) -> dict[str, object]:
    if not template_docx.exists():
        raise FileNotFoundError(f"Template not found: {template_docx}")
    if not source_docx.exists():
        raise FileNotFoundError(f"Source not found: {source_docx}")

    strip_section_properties(blocks)
    output_docx.parent.mkdir(parents=True, exist_ok=True)
    with zipfile.ZipFile(template_docx, "r") as template_package, zipfile.ZipFile(source_docx, "r") as source_package:
        template_root = parse_xml(template_package, "word/document.xml")
        template_body, template_sect_pr = body_and_sectpr(template_root)
        if template_sect_pr is None:
            raise ValueError(f"Template has no section properties: {template_docx}")

        for child in list(template_body):
            template_body.remove(child)
        for block in blocks:
            template_body.append(block)
        template_body.append(copy.deepcopy(template_sect_pr))

        template_rels = relationship_root(template_package)
        content_types = parse_xml(template_package, "[Content_Types].xml")
        source_content_types = parse_xml(source_package, "[Content_Types].xml")
        pending_parts: dict[str, bytes] = {}

        copy_referenced_relationships(
            blocks,
            template_package,
            source_package,
            template_rels,
            content_types,
            source_content_types,
            pending_parts,
        )

        has_numbering = any(block.xpath(".//w:numPr", namespaces=NS) for block in blocks)
        styles_xml = None
        if "word/styles.xml" in template_package.namelist() and "word/styles.xml" in source_package.namelist():
            styles_xml = serialize(
                merge_missing_styles(
                    parse_xml(template_package, "word/styles.xml"),
                    parse_xml(source_package, "word/styles.xml"),
                )
            )

        numbering_xml = None
        if has_numbering:
            if "word/numbering.xml" not in source_package.namelist():
                raise ValueError("Source content uses numbering, but source package has no word/numbering.xml")
            numbering_xml = source_package.read("word/numbering.xml")
            add_override(
                content_types,
                "/word/numbering.xml",
                "application/vnd.openxmlformats-officedocument.wordprocessingml.numbering+xml",
            )
            ensure_relationship(
                template_rels,
                "http://schemas.openxmlformats.org/officeDocument/2006/relationships/numbering",
                "numbering.xml",
            )

        replacements = {
            "word/document.xml": serialize(template_root),
            "word/_rels/document.xml.rels": serialize(template_rels),
            "[Content_Types].xml": serialize(content_types),
        }
        if styles_xml is not None:
            replacements["word/styles.xml"] = styles_xml
        if numbering_xml is not None:
            replacements["word/numbering.xml"] = numbering_xml

        with zipfile.ZipFile(output_docx, "w", zipfile.ZIP_DEFLATED) as target:
            written = set()
            for item in template_package.infolist():
                if item.filename in replacements:
                    target.writestr(item, replacements[item.filename])
                else:
                    target.writestr(item, template_package.read(item.filename))
                written.add(item.filename)
            for name, data in {**pending_parts, **replacements}.items():
                if name not in written:
                    target.writestr(name, data)
                    written.add(name)

    return {
        "output": str(output_docx),
        "template": str(template_docx),
        "source": str(source_docx),
        "blockCount": len(blocks),
        "numberingCopied": bool(numbering_xml),
    }


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Fill 权利要求书/说明书/说明书摘要 replacement-page templates with corrected application content."
    )
    parser.add_argument("--corrected-docx", type=Path, help="Corrected combined application DOCX. Claims, specification, and abstract sections are detected from it.")
    parser.add_argument("--claims-source", type=Path, help="Source DOCX containing only claims. Overrides claims extraction from --corrected-docx.")
    parser.add_argument("--spec-source", type=Path, help="Source DOCX containing only specification. Overrides specification extraction from --corrected-docx.")
    parser.add_argument("--abstract-source", type=Path, help="Source DOCX containing only abstract. Overrides abstract extraction from --corrected-docx.")
    parser.add_argument("--claims-template", type=Path, default=DEFAULT_TEMPLATES["claims"])
    parser.add_argument("--spec-template", type=Path, default=DEFAULT_TEMPLATES["specification"])
    parser.add_argument("--abstract-template", type=Path, default=DEFAULT_TEMPLATES["abstract"])
    parser.add_argument("--output-dir", type=Path, required=True)
    parser.add_argument("--prefix", default="")
    parser.add_argument("--only", choices=["claims", "specification", "abstract", "both", "all"], default="both")
    args = parser.parse_args()

    if args.only == "both":
        wanted = ["claims", "specification"]
    elif args.only == "all":
        wanted = ["claims", "specification", "abstract"]
    else:
        wanted = [args.only]
    outputs: list[dict[str, object]] = []

    for key in wanted:
        if key == "claims":
            template = args.claims_template
            source = args.claims_source or args.corrected_docx
            explicit_source = args.claims_source
        elif key == "specification":
            template = args.spec_template
            source = args.spec_source or args.corrected_docx
            explicit_source = args.spec_source
        else:
            template = args.abstract_template
            source = args.abstract_source or args.corrected_docx
            explicit_source = args.abstract_source
        if source is None:
            print(f"Source is required for {key}. Pass --corrected-docx or an explicit source DOCX.", file=sys.stderr)
            return 2
        blocks = all_body_blocks(source) if explicit_source else section_blocks(source, key)
        output_name = DEFAULT_OUTPUT_NAMES[key]
        if args.prefix:
            output_name = f"{args.prefix}-{output_name}"
        outputs.append(fill_one(template, source, args.output_dir / output_name, blocks))

    print(json.dumps({"written": outputs}, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
