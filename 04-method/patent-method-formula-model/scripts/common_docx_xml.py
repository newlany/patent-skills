from __future__ import annotations

import json
import zipfile
from copy import deepcopy
from pathlib import Path
from typing import Any

from lxml import etree


W_NS = "http://schemas.openxmlformats.org/wordprocessingml/2006/main"
M_NS = "http://schemas.openxmlformats.org/officeDocument/2006/math"
R_NS = "http://schemas.openxmlformats.org/officeDocument/2006/relationships"
PKG_REL_NS = "http://schemas.openxmlformats.org/package/2006/relationships"
O_NS = "urn:schemas-microsoft-com:office:office"
V_NS = "urn:schemas-microsoft-com:vml"
CT_NS = "http://schemas.openxmlformats.org/package/2006/content-types"

NS = {
    "w": W_NS,
    "m": M_NS,
    "r": R_NS,
    "pr": PKG_REL_NS,
    "o": O_NS,
    "v": V_NS,
    "ct": CT_NS,
}

XML_SPACE = "{http://www.w3.org/XML/1998/namespace}space"


def read_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def load_xml_from_docx(docx_path: Path, part_name: str = "word/document.xml") -> etree._Element:
    with zipfile.ZipFile(docx_path) as zf:
        return etree.fromstring(zf.read(part_name))


def get_body(root: etree._Element) -> etree._Element:
    body = root.find(f"{{{W_NS}}}body")
    if body is None:
        raise ValueError("Document body not found")
    return body


def get_paragraphs(root: etree._Element) -> list[etree._Element]:
    return root.xpath("//w:body/w:p", namespaces=NS)


def get_text(element: etree._Element) -> str:
    return "".join(element.xpath(".//w:t/text()", namespaces=NS)).replace("\u200b", "").strip()


def has_math(element: etree._Element) -> bool:
    return bool(element.xpath(".//m:oMath | .//m:oMathPara", namespaces=NS))


def has_ole(element: etree._Element) -> bool:
    return bool(element.xpath(".//o:OLEObject | .//w:object", namespaces=NS))


def get_first_text_node(paragraph: etree._Element) -> etree._Element:
    text_nodes = paragraph.xpath(".//w:t", namespaces=NS)
    if not text_nodes:
        raise ValueError("No text node found in paragraph")
    return text_nodes[0]


def set_paragraph_text(paragraph: etree._Element, text: str, clear_math: bool = True) -> None:
    text_nodes = paragraph.xpath(".//w:t", namespaces=NS)
    if not text_nodes:
        raise ValueError("No text node found in paragraph")
    text_nodes[0].text = text
    for node in text_nodes[1:]:
        node.text = ""
    if clear_math:
        for math_node in paragraph.xpath(".//m:oMath | .//m:oMathPara", namespaces=NS):
            parent = math_node.getparent()
            if parent is not None:
                parent.remove(math_node)


def prefix_paragraph_text(paragraph: etree._Element, prefix: str) -> None:
    node = get_first_text_node(paragraph)
    node.text = prefix + (node.text or "")


def first_run_properties(paragraph: etree._Element) -> etree._Element | None:
    rpr = paragraph.find(f"{{{W_NS}}}r/{{{W_NS}}}rPr")
    return deepcopy(rpr) if rpr is not None else None


def make_run(text: str, run_properties: etree._Element | None) -> etree._Element:
    run = etree.Element(f"{{{W_NS}}}r")
    if run_properties is not None:
        run.append(deepcopy(run_properties))
    text_node = etree.SubElement(run, f"{{{W_NS}}}t")
    if text.startswith(" ") or text.endswith(" "):
        text_node.set(XML_SPACE, "preserve")
    text_node.text = text
    return run


def clear_paragraph_content(paragraph: etree._Element) -> None:
    keep = [child for child in paragraph if child.tag == f"{{{W_NS}}}pPr"]
    paragraph[:] = keep


def get_omath(paragraphs: list[etree._Element], paragraph_index: int, omath_index: int = 1) -> etree._Element:
    paragraph = paragraphs[paragraph_index - 1]
    omaths = paragraph.xpath(".//m:oMath | .//m:oMathPara/m:oMath", namespaces=NS)
    if len(omaths) < omath_index:
        raise ValueError(f"Paragraph {paragraph_index} has fewer than {omath_index} math objects")
    return deepcopy(omaths[omath_index - 1])


def save_docx_with_replacements(
    source_docx: Path,
    output_docx: Path,
    replacements: dict[str, bytes],
) -> None:
    with zipfile.ZipFile(source_docx) as zin, zipfile.ZipFile(output_docx, "w", zipfile.ZIP_DEFLATED) as zout:
        written = set()
        for item in zin.infolist():
            data = replacements.get(item.filename, zin.read(item.filename))
            zout.writestr(item, data)
            written.add(item.filename)
        for filename, data in replacements.items():
            if filename not in written:
                zout.writestr(filename, data)

