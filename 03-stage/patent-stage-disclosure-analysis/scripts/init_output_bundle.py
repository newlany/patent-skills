#!/usr/bin/env python3

from __future__ import annotations

import argparse
from datetime import datetime
from pathlib import Path


FILE_ORDER = [
    "00_交底分析任务索引.md",
    "01_技术交底分析报告.md",
    "02_技术交底逻辑重构与缺陷审查报告.md",
    "03_需要发明人补充说明的问题清单.md",
]


def sanitize_label(value: str) -> str:
    chars = []
    for ch in value.strip():
        if ch.isalnum() or ch in {"-", "_"}:
            chars.append(ch)
        elif ch in {" ", "/", "\\", ":"}:
            chars.append("_")
    cleaned = "".join(chars).strip("_")
    while "__" in cleaned:
        cleaned = cleaned.replace("__", "_")
    return cleaned or "task"


def resolve_paths(source_arg: str, output_dir_arg: str | None) -> tuple[str, Path]:
    source_path = Path(source_arg).expanduser()
    if source_path.exists():
        source_path = source_path.resolve()
        source_display = str(source_path)
        default_output_dir = source_path.parent / "交底分析输出" / source_path.stem
    else:
        source_display = source_arg
        default_output_dir = Path.cwd() / "交底分析输出" / sanitize_label(source_arg)

    if output_dir_arg:
        output_dir = Path(output_dir_arg).expanduser().resolve()
    else:
        output_dir = default_output_dir

    return source_display, output_dir


def load_template(template_dir: Path, filename: str) -> str:
    return (template_dir / filename).read_text(encoding="utf-8")


def render_template(template: str, replacements: dict[str, str]) -> str:
    rendered = template
    for key, value in replacements.items():
        rendered = rendered.replace(key, value)
    return rendered


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Create a standard output bundle for patent disclosure analysis."
    )
    parser.add_argument("--source", required=True, help="Source file path or task label.")
    parser.add_argument(
        "--output-dir",
        help="Optional output directory. Defaults to a folder derived from the source.",
    )
    parser.add_argument(
        "--force",
        action="store_true",
        help="Overwrite existing files in the output bundle.",
    )
    args = parser.parse_args()

    source_display, output_dir = resolve_paths(args.source, args.output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    skill_dir = Path(__file__).resolve().parent.parent
    template_dir = skill_dir / "assets" / "templates"
    created_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    replacements = {
        "__SOURCE__": source_display,
        "__OUTPUT_DIR__": str(output_dir),
        "__CREATED_AT__": created_at,
    }

    for filename in FILE_ORDER:
        target = output_dir / filename
        if target.exists() and not args.force:
            print(f"SKIP {target}")
            continue
        template = load_template(template_dir, filename)
        target.write_text(render_template(template, replacements), encoding="utf-8")
        print(f"WRITE {target}")

    print(f"OUTPUT_DIR {output_dir}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
