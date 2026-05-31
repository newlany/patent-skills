from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parent
if str(SCRIPT_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPT_DIR))

from google_patents_lib import (
    comparison_file_stem,
    download_file,
    file_stem_for_reference,
    resolve_reference,
    requests_session,
    source_application_file_stem,
)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Resolve a Google Patents result and download its PDF."
    )
    parser.add_argument("--publication", action="append", default=[], help="Publication number. Repeatable.")
    parser.add_argument("--application", action="append", default=[], help="Application number. Repeatable.")
    parser.add_argument("--title", help="Patent title or topic for Google Patents search fallback.")
    parser.add_argument("--label", help="Optional label such as D1 or 证据1.")
    parser.add_argument("--category", default="other", choices=["comparison", "evidence", "other"])
    parser.add_argument("--output", type=Path, required=True, help="Destination PDF path.")
    parser.add_argument("--timeout", type=int, default=20, help="Network timeout in seconds.")
    parser.add_argument("--overwrite", action="store_true", help="Overwrite the existing file if present.")
    return parser


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()

    reference = {
        "label": args.label,
        "category": args.category,
        "publication_numbers": args.publication,
        "application_numbers": args.application,
        "title": args.title,
    }
    if not any([args.publication, args.application, args.title]):
        parser.error("Provide at least one of --publication, --application, or --title.")

    session = requests_session()
    resolved = resolve_reference(reference, session=session, timeout=args.timeout)
    if not resolved:
        payload = {
            "status": "not-found",
            "reference": reference,
        }
        json.dump(payload, sys.stdout, ensure_ascii=False, indent=2)
        sys.stdout.write("\n")
        return 2

    output_path = args.output.resolve()
    if output_path.suffix.lower() != ".pdf":
        if args.label == "原申请文件":
            stem = source_application_file_stem(reference, resolved)
        elif args.category == "comparison":
            stem = comparison_file_stem(reference, resolved)
        else:
            stem = file_stem_for_reference(reference, resolved)
        output_path = output_path / f"{stem}.pdf"

    if output_path.exists() and not args.overwrite:
        payload = {
            "status": "exists",
            "reference": reference,
            "resolved": resolved,
            "saved_to": str(output_path),
        }
        json.dump(payload, sys.stdout, ensure_ascii=False, indent=2)
        sys.stdout.write("\n")
        return 0

    download_file(resolved["pdf_url"], output_path, session=session, timeout=max(args.timeout, 30))
    payload = {
        "status": "downloaded",
        "reference": reference,
        "resolved": resolved,
        "saved_to": str(output_path),
    }
    json.dump(payload, sys.stdout, ensure_ascii=False, indent=2)
    sys.stdout.write("\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
