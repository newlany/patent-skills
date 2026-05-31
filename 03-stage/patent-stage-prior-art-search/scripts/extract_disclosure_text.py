#!/usr/bin/env python3
"""
Extract plain text from common disclosure file formats for novelty-search intake.

Supported directly:
- .txt / .md / .markdown
- .doc / .docx / .rtf / .odt via macOS textutil, with soffice fallback for .doc
- .pdf via pdftotext when available
"""

from __future__ import annotations

import argparse
import json
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path


TEXT_SUFFIXES = {".txt", ".md", ".markdown"}
WORD_SUFFIXES = {".doc", ".docx", ".rtf", ".odt"}


def _run_command(command: list[str]) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        command,
        capture_output=True,
        text=True,
        check=False,
    )


def _extract_with_textutil(path: Path) -> str:
    result = _run_command(
        ["/usr/bin/textutil", "-convert", "txt", "-stdout", str(path)]
    )
    if result.returncode != 0:
        raise RuntimeError(result.stderr.strip() or "textutil conversion failed")
    return result.stdout


def _extract_pdf(path: Path) -> str:
    pdftotext = shutil.which("pdftotext")
    if not pdftotext:
        raise RuntimeError("pdftotext is not installed")
    result = _run_command([pdftotext, "-layout", str(path), "-"])
    if result.returncode != 0:
        raise RuntimeError(result.stderr.strip() or "pdftotext extraction failed")
    return result.stdout


def _convert_doc_with_soffice(path: Path) -> Path:
    soffice = shutil.which("soffice")
    if not soffice:
        raise RuntimeError("soffice is not installed")

    temp_dir = Path(tempfile.mkdtemp(prefix="patent-intake-"))
    result = _run_command(
        [
            soffice,
            "--headless",
            "--convert-to",
            "docx",
            "--outdir",
            str(temp_dir),
            str(path),
        ]
    )
    if result.returncode != 0:
        raise RuntimeError(result.stderr.strip() or "soffice conversion failed")

    converted = temp_dir / f"{path.stem}.docx"
    if not converted.exists():
        raise RuntimeError("soffice did not produce a docx file")
    return converted


def extract_text(path: Path) -> tuple[str, str]:
    suffix = path.suffix.lower()

    if suffix in TEXT_SUFFIXES:
        return path.read_text(encoding="utf-8", errors="ignore"), "plain-text"

    if suffix in WORD_SUFFIXES:
        try:
            return _extract_with_textutil(path), "textutil"
        except RuntimeError:
            if suffix != ".doc":
                raise
            converted = _convert_doc_with_soffice(path)
            return _extract_with_textutil(converted), "soffice+textutil"

    if suffix == ".pdf":
        return _extract_pdf(path), "pdftotext"

    raise RuntimeError(f"Unsupported file type: {suffix or '<no suffix>'}")


def main() -> int:
    parser = argparse.ArgumentParser(description="Extract disclosure text")
    parser.add_argument("input", help="Path to disclosure file")
    parser.add_argument(
        "--output",
        help="Optional output text file path",
    )
    parser.add_argument(
        "--json",
        action="store_true",
        help="Print metadata as JSON instead of raw text",
    )
    args = parser.parse_args()

    input_path = Path(args.input).expanduser().resolve()
    if not input_path.exists():
        raise SystemExit(f"File not found: {input_path}")

    text, method = extract_text(input_path)
    text = text.strip()

    if args.output:
        output_path = Path(args.output).expanduser().resolve()
        output_path.parent.mkdir(parents=True, exist_ok=True)
        output_path.write_text(text, encoding="utf-8")
    else:
        output_path = None

    if args.json:
        payload = {
            "input": str(input_path),
            "method": method,
            "characters": len(text),
            "output": str(output_path) if output_path else None,
            "preview": text[:300],
        }
        json.dump(payload, sys.stdout, ensure_ascii=False, indent=2)
        sys.stdout.write("\n")
    else:
        sys.stdout.write(text)
        if text and not text.endswith("\n"):
            sys.stdout.write("\n")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
