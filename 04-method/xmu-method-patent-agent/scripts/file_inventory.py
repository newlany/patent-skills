from __future__ import annotations

import argparse
from pathlib import Path


def build_report(root: Path) -> str:
    lines = [f"# 案件文件清单", "", f"- 根目录：`{root}`", ""]
    for path in sorted(root.rglob("*")):
        if path.name.startswith("~$"):
            continue
        rel = path.relative_to(root)
        kind = "目录" if path.is_dir() else "文件"
        lines.append(f"- `{rel}` ({kind})")
    lines.append("")
    return "\n".join(lines)


def main() -> None:
    parser = argparse.ArgumentParser(description="递归生成案件文件清单 Markdown。")
    parser.add_argument("root", type=Path, help="案件根目录")
    parser.add_argument("output", type=Path, help="输出 Markdown 路径")
    args = parser.parse_args()

    report = build_report(args.root.resolve())
    args.output.write_text(report, encoding="utf-8")
    print(args.output)


if __name__ == "__main__":
    main()

