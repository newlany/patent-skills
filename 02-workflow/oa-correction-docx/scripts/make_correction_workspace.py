#!/usr/bin/env python3
"""Create a stable workspace path for an OA correction matter."""

from __future__ import annotations

import argparse
import json
import re
import shlex
import unicodedata
from pathlib import Path


DEFAULT_ROOT = Path("/Users/chrynos/专利工作区/日常工作/补正处理")
DEFAULT_CUSTOMER_CASE_NO = "客户案号待补"
SUBDIRS = {
    "downloadRoot": "source",
    "workDir": "work",
    "replacementDir": "replacement-pages",
    "checksDir": "checks",
    "oaDir": "oa",
}


def clean_part(value: str | None, fallback: str, limit: int = 80) -> str:
    text = unicodedata.normalize("NFKC", str(value or "").strip())
    text = re.sub(r"[\x00-\x1f\x7f/:\\]+", "_", text)
    text = re.sub(r"[<>|?*\"]+", "_", text)
    text = re.sub(r"\s+", "", text)
    text = text.strip(" ._-")
    if not text:
        text = fallback
    if len(text) > limit:
        text = text[:limit].rstrip(" ._-")
    return text


def build_paths(args: argparse.Namespace) -> dict[str, str]:
    case_volume = clean_part(args.case_volume, "Z案号待补", 40)
    case_name = clean_part(args.case_name, "案件名称待补")
    customer_name = clean_part(args.customer_name, "客户名称待补")
    customer_case_no = clean_part(
        args.customer_case_no or DEFAULT_CUSTOMER_CASE_NO,
        DEFAULT_CUSTOMER_CASE_NO,
        60,
    )
    app_no = clean_part(args.app_no, "申请号待补", 60)

    folder_name = "-".join(
        [
            "补正",
            case_volume,
            case_name,
            customer_name,
            customer_case_no,
            app_no,
        ]
    )
    root = Path(args.root).expanduser()
    case_dir = root / folder_name
    paths = {
        "root": str(root),
        "folderName": folder_name,
        "caseDir": str(case_dir),
        "caseVolume": case_volume,
        "caseName": case_name,
        "customerName": customer_name,
        "customerCaseNo": customer_case_no,
        "appNo": app_no,
        "sourceDirAfterDownload": str(case_dir / SUBDIRS["downloadRoot"] / case_volume),
    }
    for key, subdir in SUBDIRS.items():
        paths[key] = str(case_dir / subdir)
    return paths


def create_dirs(paths: dict[str, str]) -> None:
    Path(paths["root"]).mkdir(parents=True, exist_ok=True)
    for key in ("downloadRoot", "workDir", "replacementDir", "checksDir", "oaDir"):
        Path(paths[key]).mkdir(parents=True, exist_ok=True)


def print_shell(paths: dict[str, str]) -> None:
    mapping = {
        "CORRECTION_ROOT": paths["root"],
        "CASE_DIR": paths["caseDir"],
        "DOWNLOAD_ROOT": paths["downloadRoot"],
        "SOURCE_DIR": paths["sourceDirAfterDownload"],
        "WORK_DIR": paths["workDir"],
        "REPLACEMENT_DIR": paths["replacementDir"],
        "CHECKS_DIR": paths["checksDir"],
        "OA_DIR": paths["oaDir"],
    }
    for key, value in mapping.items():
        print(f"export {key}={shlex.quote(value)}")


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Create a correction workspace folder with a stable case-based name.",
    )
    parser.add_argument("--root", default=str(DEFAULT_ROOT))
    parser.add_argument("--case-volume", required=True)
    parser.add_argument("--case-name", required=True)
    parser.add_argument("--customer-name", required=True)
    parser.add_argument("--customer-case-no", default=DEFAULT_CUSTOMER_CASE_NO)
    parser.add_argument("--app-no", required=True)
    parser.add_argument("--create", action="store_true")
    parser.add_argument("--format", choices=("text", "json", "shell"), default="text")
    args = parser.parse_args()

    paths = build_paths(args)
    if args.create:
        create_dirs(paths)

    if args.format == "json":
        print(json.dumps(paths, ensure_ascii=False, indent=2))
    elif args.format == "shell":
        print_shell(paths)
    else:
        for key, value in paths.items():
            print(f"{key}: {value}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
