from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parent
if str(SCRIPT_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPT_DIR))

from google_patents_lib import (
    extract_original_application_reference,
    extract_references,
    resolve_input_files,
    write_json,
)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Extract comparison-document references and the original application from office actions and similar files."
    )
    parser.add_argument("inputs", nargs="+", help="Input files or directories. Supported: .docx .pdf .md .txt")
    parser.add_argument(
        "--output",
        type=Path,
        help="Optional JSON output path. Defaults to stdout only.",
    )
    parser.add_argument(
        "--include-unlabeled",
        action="store_true",
        help="Broaden the comparison-document pass when the source file OCR is especially noisy.",
    )
    parser.add_argument(
        "--skip-original-application",
        action="store_true",
        help="Do not include the original application's published patent document reference.",
    )
    return parser


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()

    input_files = resolve_input_files(args.inputs)
    if not input_files:
        parser.error("No supported input files were found.")

    payload = extract_references(
        input_files=input_files,
        citation_only=not args.include_unlabeled,
        comparison_only=True,
    )
    if not args.skip_original_application:
        original_application = extract_original_application_reference(input_files)
        if original_application:
            payload["references"].append(original_application)

    if args.output:
        write_json(args.output.resolve(), payload)

    json.dump(payload, sys.stdout, ensure_ascii=False, indent=2)
    sys.stdout.write("\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
