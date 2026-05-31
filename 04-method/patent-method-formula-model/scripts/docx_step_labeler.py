from __future__ import annotations

import argparse
from pathlib import Path

from lxml import etree

from common_docx_xml import get_paragraphs, prefix_paragraph_text, read_json, save_docx_with_replacements, load_xml_from_docx


def main() -> None:
    parser = argparse.ArgumentParser(description="给指定段落补步骤编号。")
    parser.add_argument("input_docx", type=Path)
    parser.add_argument("output_docx", type=Path)
    parser.add_argument("config_json", type=Path)
    args = parser.parse_args()

    config = read_json(args.config_json)
    root = load_xml_from_docx(args.input_docx)
    paragraphs = get_paragraphs(root)

    for index_str, prefix in config["step_labels"].items():
        prefix_paragraph_text(paragraphs[int(index_str) - 1], prefix)

    updated_xml = etree.tostring(root, encoding="UTF-8", xml_declaration=True, standalone="yes")
    save_docx_with_replacements(args.input_docx, args.output_docx, {"word/document.xml": updated_xml})
    print(args.output_docx)


if __name__ == "__main__":
    main()

