#!/usr/bin/env python3

from __future__ import annotations

import argparse
import shutil
import subprocess
from pathlib import Path


DEFAULT_FILES = [
    "01_技术交底分析报告.md",
    "02_技术交底逻辑重构与缺陷审查报告.md",
    "03_需要发明人补充说明的问题清单.md",
]
DEFAULT_PANDOC_FROM = (
    "markdown+tex_math_dollars+tex_math_single_backslash+pipe_tables+fenced_code_blocks+raw_tex"
)


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Export a patent disclosure Markdown bundle to DOCX files."
    )
    parser.add_argument(
        "--output-dir",
        required=True,
        help="Directory containing the Markdown bundle.",
    )
    parser.add_argument(
        "--files",
        nargs="*",
        help="Optional subset of Markdown filenames to export.",
    )
    parser.add_argument(
        "--overwrite",
        action="store_true",
        help="Overwrite existing DOCX files.",
    )
    parser.add_argument(
        "--from-format",
        default=DEFAULT_PANDOC_FROM,
        help=(
            "Pandoc reader format for Markdown inputs. "
            "Defaults to a math-preserving markdown profile."
        ),
    )
    args = parser.parse_args()

    output_dir = Path(args.output_dir).expanduser().resolve()
    if not output_dir.is_dir():
        raise SystemExit(f"output directory not found: {output_dir}")

    pandoc = shutil.which("pandoc")
    if not pandoc:
        raise SystemExit("pandoc is required but was not found in PATH")

    files = args.files or DEFAULT_FILES
    for name in files:
        md_path = output_dir / name
        if not md_path.exists():
            print(f"SKIP {md_path} (missing)")
            continue

        docx_path = md_path.with_suffix(".docx")
        if docx_path.exists() and not args.overwrite:
            print(f"SKIP {docx_path} (exists)")
            continue

        subprocess.run(
            [
                pandoc,
                str(md_path),
                "--from",
                args.from_format,
                "--to",
                "docx",
                "--resource-path",
                str(output_dir),
                "--output",
                str(docx_path),
            ],
            check=True,
        )
        print(f"WRITE {docx_path}")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
