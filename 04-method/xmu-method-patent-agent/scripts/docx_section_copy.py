from __future__ import annotations

import argparse
import zipfile
from copy import deepcopy
from pathlib import Path

from lxml import etree

from common_docx_xml import (
    CT_NS,
    NS,
    PKG_REL_NS,
    R_NS,
    W_NS,
    get_body,
    get_text,
)


def has_payload(element: etree._Element) -> bool:
    return bool(
        get_text(element)
        or element.xpath(".//*[local-name()='oMath' or local-name()='oMathPara']")
        or element.xpath(".//*[local-name()='OLEObject']")
        or element.tag == f"{{{W_NS}}}tbl"
    )


def next_rid(existing_ids: set[str]) -> str:
    nums = [int(rid[3:]) for rid in existing_ids if rid.startswith("rId") and rid[3:].isdigit()]
    candidate = max(nums, default=0) + 1
    while f"rId{candidate}" in existing_ids:
        candidate += 1
    rid = f"rId{candidate}"
    existing_ids.add(rid)
    return rid


def main() -> None:
    parser = argparse.ArgumentParser(description="在两个标题之间复制 docx 章节，同时复制关系和嵌入对象。")
    parser.add_argument("source_docx", type=Path)
    parser.add_argument("target_docx", type=Path)
    parser.add_argument("output_docx", type=Path)
    parser.add_argument("--source-start", required=True, help="源文档起始标题文本")
    parser.add_argument("--source-end", required=True, help="源文档结束标题文本")
    parser.add_argument("--target-start", required=True, help="目标文档起始标题文本")
    parser.add_argument("--target-end", required=True, help="目标文档结束标题文本")
    args = parser.parse_args()

    with zipfile.ZipFile(args.source_docx) as zs, zipfile.ZipFile(args.target_docx) as zt:
        source_doc = etree.fromstring(zs.read("word/document.xml"))
        target_doc = etree.fromstring(zt.read("word/document.xml"))
        source_body = get_body(source_doc)
        target_body = get_body(target_doc)

        source_children = list(source_body)
        target_children = list(target_body)

        source_start_node = next(node for node in source_children if get_text(node) == args.source_start)
        source_end_node = next(node for node in source_children if get_text(node) == args.source_end)
        target_start_node = next(node for node in target_children if get_text(node) == args.target_start)
        target_end_node = next(node for node in target_children if get_text(node) == args.target_end)

        source_start = source_children.index(source_start_node) + 1
        source_end = source_children.index(source_end_node)
        copied_children = [deepcopy(child) for child in source_children[source_start:source_end]]
        while copied_children and not has_payload(copied_children[-1]):
            copied_children.pop()

        target_start = target_children.index(target_start_node) + 1
        target_end = target_children.index(target_end_node)
        for child in target_children[target_start:target_end]:
            target_body.remove(child)
        for offset, child in enumerate(copied_children):
            target_body.insert(target_start + offset, child)

        target_rels = etree.fromstring(zt.read("word/_rels/document.xml.rels"))
        source_rels = etree.fromstring(zs.read("word/_rels/document.xml.rels"))
        source_rel_map = {rel.get("Id"): rel for rel in source_rels.findall(f"{{{PKG_REL_NS}}}Relationship")}
        existing_ids = {rel.get("Id") for rel in target_rels.findall(f"{{{PKG_REL_NS}}}Relationship")}

        inserted_nodes = list(target_body)[target_start:target_start + len(copied_children)]
        used_old_rids: list[str] = []
        for node in inserted_nodes:
            used_old_rids.extend(node.xpath(".//@r:id", namespaces=NS))
        used_old_rids = [rid for rid in dict.fromkeys(used_old_rids) if rid in source_rel_map]

        rid_map: dict[str, str] = {}
        extra_parts: dict[str, bytes] = {}
        for old_rid in used_old_rids:
            source_rel = source_rel_map[old_rid]
            new_rid = next_rid(existing_ids)
            rid_map[old_rid] = new_rid
            new_rel = deepcopy(source_rel)
            new_rel.set("Id", new_rid)
            target_rels.append(new_rel)
            target_name = source_rel.get("Target")
            if target_name and not target_name.startswith("/"):
                part_name = f"word/{target_name}"
                extra_parts[part_name] = zs.read(part_name)

        for node in inserted_nodes:
            for owner in node.xpath(".//*[@r:id]", namespaces=NS):
                old_rid = owner.get(f"{{{R_NS}}}id")
                if old_rid in rid_map:
                    owner.set(f"{{{R_NS}}}id", rid_map[old_rid])

        content_types = etree.fromstring(zt.read("[Content_Types].xml"))
        source_content_types = etree.fromstring(zs.read("[Content_Types].xml"))
        existing_defaults = {
            default.get("Extension"): default for default in content_types.findall(f"{{{CT_NS}}}Default")
        }
        source_defaults = {
            default.get("Extension"): default for default in source_content_types.findall(f"{{{CT_NS}}}Default")
        }
        for part_name in extra_parts:
            ext = Path(part_name).suffix.lstrip(".").lower()
            if ext and ext not in existing_defaults and ext in source_defaults:
                content_types.append(deepcopy(source_defaults[ext]))

        updated_doc = etree.tostring(target_doc, encoding="UTF-8", xml_declaration=True, standalone="yes")
        updated_rels = etree.tostring(target_rels, encoding="UTF-8", xml_declaration=True, standalone="yes")
        updated_ct = etree.tostring(content_types, encoding="UTF-8", xml_declaration=True, standalone="yes")

        with zipfile.ZipFile(args.output_docx, "w", zipfile.ZIP_DEFLATED) as zout:
            written = set()
            for item in zt.infolist():
                if item.filename == "word/document.xml":
                    data = updated_doc
                elif item.filename == "word/_rels/document.xml.rels":
                    data = updated_rels
                elif item.filename == "[Content_Types].xml":
                    data = updated_ct
                else:
                    data = zt.read(item.filename)
                zout.writestr(item, data)
                written.add(item.filename)
            for part_name, data in extra_parts.items():
                if part_name not in written:
                    zout.writestr(part_name, data)

    print(args.output_docx)


if __name__ == "__main__":
    main()

