from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parent
if str(SCRIPT_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPT_DIR))

from google_patents_lib import (
    PlaywrightSearchResolver,
    comparison_file_stem,
    comparison_index_from_label,
    download_file,
    extract_original_application_reference,
    extract_references,
    infer_project_dir,
    requests_session,
    resolve_input_files,
    resolve_reference,
    source_application_file_stem,
    write_json,
)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Extract cited patent references from case files and download Google Patents PDFs into the project folder."
    )
    parser.add_argument("inputs", nargs="+", help="Input files or directories. Supported: .docx .pdf .md .txt")
    parser.add_argument(
        "--project-dir",
        type=Path,
        help="Project root for the output folder. Defaults to the common parent of the inputs.",
    )
    parser.add_argument(
        "--output-root",
        type=Path,
        help="Output directory. Defaults to the project root directory.",
    )
    parser.add_argument(
        "--manifest",
        type=Path,
        help="Optional manifest path. If omitted, no manifest file is written.",
    )
    parser.add_argument(
        "--include-unlabeled",
        action="store_true",
        help="Also try patent-like references that do not appear in a citation-style context window.",
    )
    parser.add_argument("--limit", type=int, help="Optional limit on how many extracted references to attempt.")
    parser.add_argument("--timeout", type=int, default=20, help="Network timeout in seconds.")
    parser.add_argument("--overwrite", action="store_true", help="Overwrite PDFs that already exist.")
    parser.add_argument(
        "--skip-original-application",
        action="store_true",
        help="Do not download the original application's published patent PDF.",
    )
    return parser


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()

    input_files = resolve_input_files(args.inputs)
    if not input_files:
        parser.error("No supported input files were found.")

    project_dir = (args.project_dir.resolve() if args.project_dir else infer_project_dir(input_files))
    output_root = (args.output_root.resolve() if args.output_root else project_dir)
    output_root.mkdir(parents=True, exist_ok=True)

    extracted = extract_references(
        input_files,
        citation_only=not args.include_unlabeled,
        comparison_only=True,
    )
    references = extracted["references"]
    if args.limit:
        references = references[: args.limit]
    if not args.skip_original_application:
        original_application = extract_original_application_reference(input_files)
        if original_application:
            references = references + [original_application]

    session = requests_session()
    results: list[dict] = []

    with PlaywrightSearchResolver() as search_resolver:
        for reference in references:
            result: dict = {
                "reference": reference,
                "status": "pending",
            }
            try:
                resolved = resolve_reference(
                    reference,
                    session=session,
                    search_resolver=search_resolver,
                    timeout=args.timeout,
                )
                if not resolved:
                    result["status"] = "not-found"
                    results.append(result)
                    continue

                if reference.get("label") == "原申请文件":
                    target_path = output_root / f"{source_application_file_stem(reference, resolved)}.pdf"
                else:
                    fallback_index = comparison_index_from_label(reference.get("label"))
                    target_path = output_root / f"{comparison_file_stem(reference, resolved, fallback_index=fallback_index)}.pdf"

                if target_path.exists() and not args.overwrite:
                    result["status"] = "exists"
                    result["resolved"] = resolved
                    result["saved_to"] = str(target_path)
                    results.append(result)
                    continue

                download_file(
                    resolved["pdf_url"],
                    target_path,
                    session=session,
                    timeout=max(args.timeout, 30),
                )
                result["status"] = "downloaded"
                result["resolved"] = resolved
                result["saved_to"] = str(target_path)
            except Exception as exc:  # noqa: BLE001
                result["status"] = "error"
                result["error"] = str(exc)
            results.append(result)

    payload = {
        "generated_at": extracted["generated_at"],
        "project_dir": str(project_dir),
        "output_root": str(output_root),
        "citation_only": extracted["citation_only"],
        "input_files": extracted["input_files"],
        "results": results,
        "summary": {
            "references_seen": len(extracted["references"]),
            "references_attempted": len(references),
            "downloaded": sum(1 for item in results if item["status"] == "downloaded"),
            "exists": sum(1 for item in results if item["status"] == "exists"),
            "not_found": sum(1 for item in results if item["status"] == "not-found"),
            "errors": sum(1 for item in results if item["status"] == "error"),
            "original_application_included": any(
                item["reference"].get("label") == "原申请文件"
                for item in results
            ),
        },
    }

    if args.manifest:
        manifest = args.manifest.resolve()
        write_json(manifest, payload)
        payload["manifest"] = str(manifest)

    json.dump(payload, sys.stdout, ensure_ascii=False, indent=2)
    sys.stdout.write("\n")
    return 0 if payload["summary"]["errors"] == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())
