from __future__ import annotations

import argparse
from pathlib import Path

from lxml import etree

from common_docx_xml import (
    get_body,
    load_xml_from_docx,
    read_json,
    save_docx_with_replacements,
    set_paragraph_text,
)


def main() -> None:
    parser = argparse.ArgumentParser(description="按配置批量修改 docx 中指定段落的文本。")
    parser.add_argument("input_docx", type=Path)
    parser.add_argument("output_docx", type=Path)
    parser.add_argument("config_json", type=Path)
    args = parser.parse_args()

    config = read_json(args.config_json)
    root = load_xml_from_docx(args.input_docx)

    body = get_body(root)
    paragraphs = body.findall("{http://schemas.openxmlformats.org/wordprocessingml/2006/main}p")

    for patch in config["patches"]:
        paragraph = paragraphs[patch["paragraph"] - 1]
        set_paragraph_text(paragraph, patch["text"], clear_math=patch.get("clear_math", True))

    updated_xml = etree.tostring(root, encoding="UTF-8", xml_declaration=True, standalone="yes")
    save_docx_with_replacements(args.input_docx, args.output_docx, {"word/document.xml": updated_xml})
    print(args.output_docx)


if __name__ == "__main__":
    main()
