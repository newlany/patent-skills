#!/usr/bin/env python3
"""Scan or safely fix CN patent formal defects in DOCX files."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

from patent_formal_lib import (
    fix_docx,
    format_fix_report,
    format_scan_report,
    scan_docx,
)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Check Chinese patent DOC/DOCX files for formality defects and optionally apply safe fixes."
    )
    subparsers = parser.add_subparsers(dest="command", required=True)

    scan_parser = subparsers.add_parser("scan", help="Inspect a patent Word file")
    scan_parser.add_argument("path", help="Path to a .docx file, or a .doc file if LibreOffice is available")
    scan_parser.add_argument("--json", action="store_true", help="Emit JSON instead of a text report")

    fix_parser = subparsers.add_parser("fix", help="Apply safe fixes and write a corrected .docx copy")
    fix_parser.add_argument("path", help="Path to a .docx file, or a .doc file if LibreOffice is available")
    fix_parser.add_argument(
        "--output",
        required=True,
        help="Path to the corrected .docx output",
    )
    fix_parser.add_argument("--json", action="store_true", help="Emit JSON instead of a text report")
    return parser


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()

    if args.command == "scan":
        report = scan_docx(args.path)
        if args.json:
            print(json.dumps(report, ensure_ascii=False, indent=2))
        else:
            print(format_scan_report(report))
        return 0

    if args.command == "fix":
        output_path = Path(args.output).expanduser().resolve()
        report = fix_docx(args.path, output_path)
        if args.json:
            print(json.dumps(report, ensure_ascii=False, indent=2))
        else:
            print(format_fix_report(report))
        return 0

    parser.error(f"unknown command: {args.command}")
    return 2


if __name__ == "__main__":
    sys.exit(main())
