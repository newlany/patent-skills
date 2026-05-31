#!/usr/bin/env python3

from __future__ import annotations

import argparse
import json
import os
import shutil
import subprocess
from pathlib import Path

DEFAULT_MARKDOWN_FORMAT = (
    "markdown+tex_math_dollars+tex_math_single_backslash+pipe_tables+fenced_code_blocks+raw_tex"
)


def find_pandoc() -> str | None:
    pandoc = shutil.which("pandoc")
    if pandoc:
        return pandoc

    # Windows winget install typically lands here:
    #   %LOCALAPPDATA%\Pandoc\pandoc.exe
    if os.name == "nt":
        localapp = os.environ.get("LOCALAPPDATA")
        if localapp:
            candidate = Path(localapp) / "Pandoc" / "pandoc.exe"
            if candidate.exists():
                return str(candidate.resolve())

    return None


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Extract a DOCX into Markdown while preserving equations as TeX math."
    )
    parser.add_argument("source", help="Path to the source .docx file")
    parser.add_argument(
        "--output",
        help="Path to the output Markdown file. Defaults next to the source file.",
    )
    parser.add_argument(
        "--format",
        default=DEFAULT_MARKDOWN_FORMAT,
        help=(
            "Pandoc markdown writer format. Defaults to a math-preserving markdown profile."
        ),
    )
    parser.add_argument("--json", action="store_true", help="Emit JSON instead of only the output path.")
    args = parser.parse_args()

    pandoc = find_pandoc()
    if not pandoc:
        raise SystemExit("pandoc is required but was not found in PATH (or LOCALAPPDATA/Pandoc)")

    source = Path(args.source).expanduser().resolve()
    if source.suffix.lower() != ".docx":
        raise SystemExit("source must be a .docx file")
    if not source.exists():
        raise SystemExit(f"file not found: {source}")

    output = (
        Path(args.output).expanduser().resolve()
        if args.output
        else source.with_suffix(".formula.md")
    )
    output.parent.mkdir(parents=True, exist_ok=True)

    subprocess.run(
        [
            pandoc,
            str(source),
            "--to",
            args.format,
            "--wrap",
            "none",
            "--output",
            str(output),
        ],
        check=True,
    )

    if args.json:
        print(
            json.dumps(
                {
                    "input": str(source),
                    "output": str(output),
                    "format": args.format,
                    "pandoc": pandoc,
                    "characters": len(output.read_text(encoding="utf-8")),
                },
                ensure_ascii=False,
                indent=2,
            )
        )
    else:
        print(output)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
