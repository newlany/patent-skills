from __future__ import annotations

import argparse
from copy import deepcopy
from pathlib import Path

from lxml import etree

from common_docx_xml import (
    clear_paragraph_content,
    first_run_properties,
    get_omath,
    get_paragraphs,
    load_xml_from_docx,
    make_run,
    read_json,
    save_docx_with_replacements,
)


def set_segments(
    paragraph: etree._Element,
    segments: list[list[str]],
    formula_map: dict[str, etree._Element],
    run_properties: etree._Element | None,
) -> None:
    clear_paragraph_content(paragraph)
    for kind, value in segments:
        if kind == "text":
            paragraph.append(make_run(value, run_properties))
        elif kind == "math":
            paragraph.append(deepcopy(formula_map[value]))
        else:
            raise ValueError(f"Unknown segment kind: {kind}")


def main() -> None:
    parser = argparse.ArgumentParser(description="按配置修复 docx 中的内联数学对象。")
    parser.add_argument("input_docx", type=Path)
    parser.add_argument("output_docx", type=Path)
    parser.add_argument("config_json", type=Path)
    args = parser.parse_args()

    config = read_json(args.config_json)
    main_root = load_xml_from_docx(args.input_docx)
    main_paragraphs = get_paragraphs(main_root)

    source_paragraphs: dict[str, list[etree._Element]] = {"input": main_paragraphs}
    for alias, doc_path in config.get("external_docs", {}).items():
        source_paragraphs[alias] = get_paragraphs(load_xml_from_docx(Path(doc_path)))

    run_properties = first_run_properties(main_paragraphs[config["style_paragraph"] - 1])

    formula_map: dict[str, etree._Element] = {}
    for name, spec in config["formulas"].items():
        paragraphs = source_paragraphs[spec["doc"]]
        formula_map[name] = get_omath(paragraphs, spec["paragraph"], spec.get("omath", 1))

    for patch in config["patches"]:
        paragraph = main_paragraphs[patch["paragraph"] - 1]
        set_segments(paragraph, patch["segments"], formula_map, run_properties)

    updated_xml = etree.tostring(main_root, encoding="UTF-8", xml_declaration=True, standalone="yes")
    save_docx_with_replacements(args.input_docx, args.output_docx, {"word/document.xml": updated_xml})
    print(args.output_docx)


if __name__ == "__main__":
    main()

