#!/usr/bin/env python3
"""Convert Word files for normalization or visual review."""

from __future__ import annotations

import argparse
import json
import shutil
import subprocess
import sys
from pathlib import Path


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()

    input_path = Path(args.path).expanduser().resolve()
    if not input_path.exists():
        parser.error(f"file not found: {input_path}")

    if args.render_preview and args.to != "pdf":
        parser.error("--render-preview requires --to pdf")

    office = find_executable(
        ["libreoffice", "soffice", "/Applications/LibreOffice.app/Contents/MacOS/soffice"]
    )
    if not office:
        parser.error("LibreOffice/soffice not found; install LibreOffice first")

    output_dir = Path(args.output_dir).expanduser().resolve()
    output_dir.mkdir(parents=True, exist_ok=True)

    converted = convert_file(office, input_path, output_dir, args.to)
    previews = []
    if args.render_preview:
        pdftoppm = find_executable(["pdftoppm", "/opt/homebrew/bin/pdftoppm"])
        if not pdftoppm:
            parser.error("pdftoppm not found; install poppler or omit --render-preview")
        previews = render_previews(
            pdftoppm,
            converted,
            output_dir,
            dpi=args.dpi,
            first_page=args.first_page,
            last_page=args.last_page,
        )

    result = {
        "input": str(input_path),
        "converter": office,
        "output": str(converted),
        "previews": [str(path) for path in previews],
    }

    if args.json:
        print(json.dumps(result, ensure_ascii=False, indent=2))
    else:
        print(f"Input: {result['input']}")
        print(f"Converter: {result['converter']}")
        print(f"Output: {result['output']}")
        if previews:
            print("Preview images:")
            for path in previews:
                print(f"  {path}")

    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Convert .doc/.docx files with LibreOffice for normalization or review."
    )
    parser.add_argument("path", help="Path to a .doc or .docx file")
    parser.add_argument(
        "--to",
        choices=["docx", "pdf"],
        default="pdf",
        help="Target format",
    )
    parser.add_argument(
        "--output-dir",
        default="tmp/docx-review",
        help="Directory for converted output",
    )
    parser.add_argument(
        "--render-preview",
        action="store_true",
        help="Render PDF pages to PNG with pdftoppm after conversion",
    )
    parser.add_argument("--dpi", type=int, default=144, help="PNG render resolution")
    parser.add_argument("--first-page", type=int, help="First page to render")
    parser.add_argument("--last-page", type=int, help="Last page to render")
    parser.add_argument("--json", action="store_true", help="Emit machine-readable JSON")
    return parser


def find_executable(candidates: list[str]) -> str | None:
    for candidate in candidates:
        resolved = shutil.which(candidate)
        if resolved:
            return resolved
        path = Path(candidate)
        if path.exists():
            return str(path)
    return None


def convert_file(office: str, input_path: Path, output_dir: Path, target: str) -> Path:
    cmd = [
        office,
        "--headless",
        "--convert-to",
        target,
        "--outdir",
        str(output_dir),
        str(input_path),
    ]
    completed = subprocess.run(cmd, capture_output=True, text=True)
    if completed.returncode != 0:
        raise SystemExit(completed.stderr.strip() or completed.stdout.strip() or "conversion failed")

    expected = output_dir / f"{input_path.stem}.{target}"
    if expected.exists():
        return expected

    candidates = sorted(
        output_dir.glob(f"{input_path.stem}*.{target}"),
        key=lambda path: path.stat().st_mtime,
        reverse=True,
    )
    if candidates:
        return candidates[0]

    raise SystemExit(
        completed.stdout.strip()
        or f"conversion reported success but no .{target} output was found"
    )


def render_previews(
    pdftoppm: str,
    pdf_path: Path,
    output_dir: Path,
    dpi: int,
    first_page: int | None,
    last_page: int | None,
) -> list[Path]:
    prefix = output_dir / f"{pdf_path.stem}-page"
    cmd = [pdftoppm, "-png", "-r", str(dpi)]
    if first_page is not None:
        cmd.extend(["-f", str(first_page)])
    if last_page is not None:
        cmd.extend(["-l", str(last_page)])
    cmd.extend([str(pdf_path), str(prefix)])

    completed = subprocess.run(cmd, capture_output=True, text=True)
    if completed.returncode != 0:
        raise SystemExit(completed.stderr.strip() or completed.stdout.strip() or "preview render failed")

    previews = sorted(output_dir.glob(f"{pdf_path.stem}-page-*.png"))
    if not previews:
        raise SystemExit("preview render completed but no PNG files were found")
    return previews


if __name__ == "__main__":
    sys.exit(main())
