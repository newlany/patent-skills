from __future__ import annotations

import argparse
from pathlib import Path

from common_docx_xml import NS, get_paragraphs, load_xml_from_docx


def extract_formula_texts(docx_path: Path) -> list[str]:
    root = load_xml_from_docx(docx_path)
    paragraphs = get_paragraphs(root)
    texts: list[str] = []
    for paragraph in paragraphs:
        for math in paragraph.xpath(".//m:oMath | .//m:oMathPara/m:oMath", namespaces=NS):
            text = "".join(math.xpath(".//m:t/text()", namespaces=NS)).replace("\u200b", "").strip()
            if text:
                texts.append(text)
    return texts


def main() -> None:
    parser = argparse.ArgumentParser(description="比较两个 docx 的数学对象数量和公式文本集合。")
    parser.add_argument("baseline_docx", type=Path)
    parser.add_argument("candidate_docx", type=Path)
    parser.add_argument("--report", type=Path, help="可选 Markdown 报告输出路径")
    args = parser.parse_args()

    baseline = extract_formula_texts(args.baseline_docx)
    candidate = extract_formula_texts(args.candidate_docx)

    baseline_set = set(baseline)
    candidate_set = set(candidate)
    missing = sorted(baseline_set - candidate_set)
    added = sorted(candidate_set - baseline_set)

    lines = [
        "# 公式核查报告",
        "",
        f"- 基线文件：`{args.baseline_docx}`",
        f"- 当前文件：`{args.candidate_docx}`",
        f"- 基线公式对象数：`{len(baseline)}`",
        f"- 当前公式对象数：`{len(candidate)}`",
        f"- 基线独立公式文本数：`{len(baseline_set)}`",
        f"- 当前独立公式文本数：`{len(candidate_set)}`",
        f"- 缺失公式文本数：`{len(missing)}`",
        f"- 新增公式文本数：`{len(added)}`",
        "",
    ]

    if missing:
        lines.append("## 缺失公式")
        lines.append("")
        lines.extend(f"- `{item}`" for item in missing)
        lines.append("")
    if added:
        lines.append("## 新增公式")
        lines.append("")
        lines.extend(f"- `{item}`" for item in added)
        lines.append("")
    if not missing and not added:
        lines.append("## 结论")
        lines.append("")
        lines.append("- 未发现公式文本集合层面的遗漏或新增。")
        lines.append("")

    report = "\n".join(lines)
    if args.report:
        args.report.write_text(report, encoding="utf-8")
        print(args.report)
    else:
        print(report)


if __name__ == "__main__":
    main()
