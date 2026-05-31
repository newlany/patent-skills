#!/usr/bin/env python3
"""Shared workflow utilities for local Chinese patent drafting cases.

This script keeps case folders, manifests, validation reports, and environment
checks consistent across the patent drafting skills. It intentionally uses only
the Python standard library so it can run before project-specific environments
are ready.
"""

from __future__ import annotations

import argparse
import json
import os
import platform
import shutil
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


SCHEMA_VERSION = "patent-workflow-manifest/v1"
STAGE_REPORT_SCHEMA_VERSION = "patent-stage-report/v1"
EVENT_LOG_NAME = "00_case_events.jsonl"
USER_OUTPUT_DIR = "输出"
PROCESS_OUTPUT_DIR = "输出/过程"
FINAL_OUTPUT_DIR = "输出/定稿"
RECORD_DIR = "记录"
REPORTS_DIR = "报告"
TOOL_RUNS_DIR = "工具运行"
LEGACY_CASE_SUPPORT_DIRS = [
    "00_admin",
    "00_admin/decisions",
    "00_admin/source-inventory",
    "99_archive",
]
LEGACY_STAGE_SUBDIRS = [
    "inputs",
    "work",
    "reports",
    "outputs",
    "tool-runs",
    "archive",
]
STAGE_DIR_NAMES = {
    "01_disclosure": "01_交底分析",
    "02_search": "02_现有技术检索",
    "03_reconstruction": "03_方案重构",
    "04_claims": "04_权利要求",
    "05_specification": "05_说明书",
    "06_figures": "06_附图",
    "07_qc": "07_质检",
    "08_filing_package": "08_提交包",
}
DEFAULT_STAGES = [
    ("01_disclosure", "交底分析"),
    ("02_search", "现有技术检索"),
    ("03_reconstruction", "方案重构"),
    ("04_claims", "权利要求"),
    ("05_specification", "说明书"),
    ("06_figures", "附图"),
    ("07_qc", "质检"),
    ("08_filing_package", "提交包"),
]
DRAFTING_REQUIRED_STAGES = [
    "01_disclosure",
    "02_search",
    "03_reconstruction",
    "04_claims",
    "05_specification",
    "06_figures",
    "07_qc",
]
COMPLETED_STATUSES = {"completed", "verified"}
STAGE_STATUSES = {"pending", "in-progress", "completed", "verified", "blocked"}
STAGE_REPORT_STATUSES = {"completed", "needs-review", "blocked", "skipped"}
METRIC_EVENT_TYPES = {"script-run", "dependency-call", "manual-interruption"}


def now_iso() -> str:
    return datetime.now(timezone.utc).astimezone().isoformat(timespec="seconds")


def repo_root() -> Path:
    return Path(__file__).resolve().parents[1]


def skills_root() -> Path:
    return repo_root().parent


def rel_to(path: Path, base: Path) -> str:
    try:
        return str(path.resolve().relative_to(base.resolve()))
    except ValueError:
        return str(path.resolve())


def safe_slug(text: str) -> str:
    slug = "".join(char if char.isalnum() or char in {"-", "_"} else "-" for char in text.strip())
    slug = "-".join(part for part in slug.split("-") if part)
    return slug or "stage"


def stage_dir_name(stage: str) -> str:
    return STAGE_DIR_NAMES.get(stage, stage)


def stage_record_dir(case_dir: Path, stage: str) -> Path:
    return case_dir / RECORD_DIR / stage_dir_name(stage)


def validation_report_path(case_dir: Path) -> Path:
    return case_dir / FINAL_OUTPUT_DIR / "验证报告.md"


def load_manifest(case_dir: Path) -> dict[str, Any]:
    manifest_path = case_dir / "manifest.json"
    if not manifest_path.exists():
        raise SystemExit(f"manifest not found: {manifest_path}")
    return json.loads(manifest_path.read_text(encoding="utf-8"))


def save_manifest(case_dir: Path, manifest: dict[str, Any]) -> None:
    manifest["updated_at"] = now_iso()
    (case_dir / "manifest.json").write_text(
        json.dumps(manifest, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )


EXECUTION_MODES = {"guided", "autonomous"}


def default_metrics() -> dict[str, Any]:
    return {
        "events_count": 0,
        "script_runs_count": 0,
        "dependency_calls_count": 0,
        "manual_interruptions_count": 0,
        "stage_durations_seconds": {},
        "last_event_at": None,
        "last_validation": None,
    }


def default_manifest(
    case_dir: Path,
    title: str | None,
    source: str | None,
    execution_mode: str = "guided",
) -> dict[str, Any]:
    created = now_iso()
    if execution_mode not in EXECUTION_MODES:
        raise ValueError(f"unknown execution mode: {execution_mode}")
    return {
        "schema_version": SCHEMA_VERSION,
        "case_id": case_dir.name,
        "title": title or case_dir.name,
        "source": source,
        "execution_mode": execution_mode,
        "layout": {
            "project_workspace_dir": "专利工作区",
            "directory_policy": "lazy-create-only-parents-for-written-files",
            "user_output_dir": USER_OUTPUT_DIR,
            "process_output_dir": PROCESS_OUTPUT_DIR,
            "final_output_dir": FINAL_OUTPUT_DIR,
            "record_dir": RECORD_DIR,
            "report_dir": REPORTS_DIR,
            "tool_run_dir": TOOL_RUNS_DIR,
            "stage_record_dirs": STAGE_DIR_NAMES,
            "legacy_project_workspace_dir": "patent-workspace",
            "legacy_support_dirs": LEGACY_CASE_SUPPORT_DIRS,
            "legacy_stage_subdirs": LEGACY_STAGE_SUBDIRS,
        },
        "created_at": created,
        "updated_at": created,
        "status": {
            "drafting": "in-progress",
            "filing": "not-ready",
            "hard_fail_count": 0,
            "soft_fail_count": 0,
        },
        "stages": {
            key: {
                "label": label,
                "status": "pending",
                "artifacts": [],
                "notes": [],
                "updated_at": None,
            }
            for key, label in DEFAULT_STAGES
        },
        "checks": [],
        "metrics": default_metrics(),
    }


def ensure_case_dirs(case_dir: Path) -> None:
    case_dir.mkdir(parents=True, exist_ok=True)


def write_status(case_dir: Path, manifest: dict[str, Any]) -> None:
    lines = [
        "# Patent Case Status",
        "",
        f"- case_id: `{manifest.get('case_id', case_dir.name)}`",
        f"- title: {manifest.get('title') or ''}",
        f"- source: {manifest.get('source') or ''}",
        f"- execution_mode: `{manifest.get('execution_mode', 'guided')}`",
        f"- event_log: `{EVENT_LOG_NAME}`",
        f"- drafting_status: `{manifest.get('status', {}).get('drafting', 'unknown')}`",
        f"- filing_status: `{manifest.get('status', {}).get('filing', 'unknown')}`",
        f"- updated_at: `{manifest.get('updated_at', '')}`",
        "",
        "## Stages",
        "",
        "| Stage | Status | Artifacts |",
        "|---|---:|---:|",
    ]
    for key, stage in manifest.get("stages", {}).items():
        lines.append(
            f"| `{key}` | `{stage.get('status', 'pending')}` | {len(stage.get('artifacts', []))} |"
        )
    lines.append("")
    lines.append("## Next Use")
    lines.append("")
    lines.append(
        "Use `python3 /Users/chrynos/.codex/skills/patent-entry-drafting/scripts/patent_workflow.py validate --case-dir <case-dir>` before declaring the case complete."
    )
    (case_dir / "00_case_status.md").write_text("\n".join(lines) + "\n", encoding="utf-8")


def emit(payload: dict[str, Any], as_json: bool) -> None:
    if as_json:
        print(json.dumps(payload, ensure_ascii=False, indent=2))
        return
    status = payload.get("status") or payload.get("overall") or payload.get("result") or "ok"
    print(f"{status}: {payload.get('message', '')}".strip())
    if payload.get("path"):
        print(payload["path"])


def event_log_path(case_dir: Path) -> Path:
    return case_dir / EVENT_LOG_NAME


def append_event(
    case_dir: Path,
    manifest: dict[str, Any],
    event_type: str,
    *,
    stage: str | None = None,
    severity: str = "info",
    message: str | None = None,
    data: dict[str, Any] | None = None,
) -> dict[str, Any]:
    event = {
        "created_at": now_iso(),
        "event": event_type,
        "severity": severity,
    }
    if stage:
        event["stage"] = stage
    if message:
        event["message"] = message
    if data:
        event["data"] = data

    log_path = event_log_path(case_dir)
    log_path.parent.mkdir(parents=True, exist_ok=True)
    with log_path.open("a", encoding="utf-8") as fh:
        fh.write(json.dumps(event, ensure_ascii=False, sort_keys=True) + "\n")

    metrics = manifest.setdefault("metrics", default_metrics())
    metrics["events_count"] = int(metrics.get("events_count") or 0) + 1
    metrics["last_event_at"] = event["created_at"]
    if event_type == "script-run":
        metrics["script_runs_count"] = int(metrics.get("script_runs_count") or 0) + 1
    elif event_type == "dependency-call":
        metrics["dependency_calls_count"] = int(metrics.get("dependency_calls_count") or 0) + 1
    elif event_type == "manual-interruption":
        metrics["manual_interruptions_count"] = int(metrics.get("manual_interruptions_count") or 0) + 1
    return event


def parse_iso(text: str | None) -> datetime | None:
    if not text:
        return None
    try:
        return datetime.fromisoformat(text)
    except ValueError:
        return None


def stage_duration_seconds(stage: dict[str, Any], finished_at: str) -> int | None:
    started = parse_iso(stage.get("started_at"))
    finished = parse_iso(finished_at)
    if not started or not finished:
        return None
    seconds = round((finished - started).total_seconds())
    return max(seconds, 0)


def summarize_metrics(case_dir: Path, manifest: dict[str, Any]) -> dict[str, Any]:
    metrics = manifest.get("metrics") or {}
    stages = {}
    for key, stage in manifest.get("stages", {}).items():
        stages[key] = {
            "status": stage.get("status", "pending"),
            "started_at": stage.get("started_at"),
            "finished_at": stage.get("finished_at"),
            "duration_seconds": stage.get("duration_seconds"),
            "artifact_count": len(stage.get("artifacts", [])),
        }
    return {
        "case_id": manifest.get("case_id", case_dir.name),
        "event_log": str(event_log_path(case_dir)),
        "events_count": int(metrics.get("events_count") or 0),
        "script_runs_count": int(metrics.get("script_runs_count") or 0),
        "dependency_calls_count": int(metrics.get("dependency_calls_count") or 0),
        "manual_interruptions_count": int(metrics.get("manual_interruptions_count") or 0),
        "last_event_at": metrics.get("last_event_at"),
        "last_validation": metrics.get("last_validation"),
        "stages": stages,
    }


def parse_json_object_arg(text: str, arg_name: str) -> dict[str, Any]:
    try:
        payload = json.loads(text)
    except json.JSONDecodeError as exc:
        raise SystemExit(f"invalid {arg_name}: {exc}") from exc
    if not isinstance(payload, dict):
        raise SystemExit(f"{arg_name} must be a JSON object")
    return payload


def issue_items(values: list[str] | None, severity: str) -> list[dict[str, str]]:
    return [
        {
            "severity": severity,
            "code": "manual",
            "message": value,
        }
        for value in (values or [])
    ]


def stage_report_default_path(case_dir: Path, stage: str, name: str | None) -> Path:
    stage_dir = stage_record_dir(case_dir, stage) / REPORTS_DIR
    if name:
        return stage_dir / f"{safe_slug(name)}-stage-report.json"
    return stage_dir / "stage-report.json"


def upsert_artifact(stage: dict[str, Any], artifact: dict[str, Any]) -> None:
    artifacts = stage.setdefault("artifacts", [])
    for existing in artifacts:
        if existing.get("path") == artifact.get("path") and existing.get("kind") == artifact.get("kind"):
            existing.update(artifact)
            return
    artifacts.append(artifact)


def collect_stage_reports(case_dir: Path, manifest: dict[str, Any]) -> tuple[list[dict[str, Any]], list[dict[str, str]]]:
    candidates: dict[Path, str] = {}
    for key, _ in DEFAULT_STAGES:
        for stage_dir in (stage_record_dir(case_dir, key), case_dir / key):
            for pattern in (
                "stage-report.json",
                "*-stage-report.json",
                "stage-reports/*.json",
                "reports/*.json",
                f"{REPORTS_DIR}/*.json",
            ):
                for path in stage_dir.glob(pattern):
                    candidates[path.resolve()] = key

    for key, stage in manifest.get("stages", {}).items():
        for artifact in stage.get("artifacts", []):
            if artifact.get("kind") != "stage-report":
                continue
            path_text = artifact.get("path")
            if not path_text:
                continue
            path = Path(path_text)
            if not path.is_absolute():
                path = case_dir / path
            candidates[path.resolve()] = key

    reports: list[dict[str, Any]] = []
    errors: list[dict[str, str]] = []
    for path, fallback_stage in sorted(candidates.items(), key=lambda item: str(item[0])):
        rel_path = rel_to(path, case_dir)
        if not path.exists():
            errors.append({"code": "stage-report-missing", "message": f"Stage report does not exist: {rel_path}"})
            continue
        try:
            payload = json.loads(path.read_text(encoding="utf-8"))
        except json.JSONDecodeError as exc:
            errors.append({"code": "stage-report-invalid-json", "message": f"Invalid stage report JSON {rel_path}: {exc}"})
            continue
        if not isinstance(payload, dict):
            errors.append({"code": "stage-report-not-object", "message": f"Stage report is not a JSON object: {rel_path}"})
            continue
        if payload.get("schema_version") != STAGE_REPORT_SCHEMA_VERSION:
            errors.append({"code": "stage-report-schema", "message": f"Unexpected stage report schema in {rel_path}"})
            continue
        payload["_path"] = rel_path
        payload.setdefault("runtime_stage", fallback_stage)
        reports.append(payload)
    return reports, errors


def cmd_init(args: argparse.Namespace) -> int:
    case_dir = Path(args.case_dir).expanduser().resolve()
    ensure_case_dirs(case_dir)
    manifest_path = case_dir / "manifest.json"
    if manifest_path.exists() and not args.force:
        manifest = load_manifest(case_dir)
        result = {
            "status": "exists",
            "message": "case manifest already exists",
            "case_dir": str(case_dir),
            "manifest": str(manifest_path),
        }
        emit(result, args.json)
        return 0

    manifest = default_manifest(case_dir, args.title, args.source, args.mode)
    append_event(
        case_dir,
        manifest,
        "case-initialized",
        message="case folder initialized",
        data={"execution_mode": manifest["execution_mode"]},
    )
    save_manifest(case_dir, manifest)
    write_status(case_dir, manifest)
    result = {
        "status": "initialized",
        "message": "case folder initialized",
        "case_dir": str(case_dir),
        "manifest": str(manifest_path),
        "status_file": str(case_dir / "00_case_status.md"),
        "execution_mode": manifest["execution_mode"],
        "layout": manifest.get("layout", {}),
        "stages": list(manifest["stages"].keys()),
    }
    emit(result, args.json)
    return 0


def cmd_set_mode(args: argparse.Namespace) -> int:
    case_dir = Path(args.case_dir).expanduser().resolve()
    manifest = load_manifest(case_dir)
    previous = manifest.get("execution_mode", "guided")
    manifest["execution_mode"] = args.mode
    append_event(
        case_dir,
        manifest,
        "mode-updated",
        message=f"execution mode changed from {previous} to {args.mode}",
        data={"previous_mode": previous, "execution_mode": args.mode},
    )
    save_manifest(case_dir, manifest)
    write_status(case_dir, manifest)
    emit(
        {
            "status": "mode-updated",
            "message": f"execution mode changed from {previous} to {args.mode}",
            "case_dir": str(case_dir),
            "previous_mode": previous,
            "execution_mode": args.mode,
        },
        args.json,
    )
    return 0


def cmd_add_artifact(args: argparse.Namespace) -> int:
    case_dir = Path(args.case_dir).expanduser().resolve()
    manifest = load_manifest(case_dir)
    stage_key = args.stage
    stages = manifest.setdefault("stages", {})
    if stage_key not in stages:
        raise SystemExit(f"unknown stage: {stage_key}")

    artifact_path = Path(args.path).expanduser()
    if not artifact_path.is_absolute():
        artifact_path = (case_dir / artifact_path).resolve()
    artifact = {
        "path": rel_to(artifact_path, case_dir),
        "kind": args.kind,
        "label": args.label,
        "status": args.status,
        "exists": artifact_path.exists(),
        "updated_at": now_iso(),
    }
    if args.note:
        artifact["note"] = args.note

    stage = stages[stage_key]
    stage.setdefault("artifacts", []).append(artifact)
    stage["status"] = args.stage_status or stage.get("status") or "in-progress"
    stage["updated_at"] = now_iso()
    append_event(
        case_dir,
        manifest,
        "artifact-added",
        stage=stage_key,
        message=f"registered {artifact['path']}",
        data={"artifact": artifact},
    )
    save_manifest(case_dir, manifest)
    write_status(case_dir, manifest)
    emit(
        {
            "status": "artifact-added",
            "message": f"registered {artifact['path']}",
            "case_dir": str(case_dir),
            "artifact": artifact,
        },
        args.json,
    )
    return 0


def cmd_stage_start(args: argparse.Namespace) -> int:
    case_dir = Path(args.case_dir).expanduser().resolve()
    manifest = load_manifest(case_dir)
    stage = manifest.setdefault("stages", {}).get(args.stage)
    if not stage:
        raise SystemExit(f"unknown stage: {args.stage}")
    started_at = now_iso()
    stage["status"] = "in-progress"
    stage["started_at"] = started_at
    stage.pop("finished_at", None)
    stage.pop("duration_seconds", None)
    stage["updated_at"] = started_at
    event = append_event(
        case_dir,
        manifest,
        "stage-start",
        stage=args.stage,
        message=args.note or f"stage started: {args.stage}",
    )
    save_manifest(case_dir, manifest)
    write_status(case_dir, manifest)
    emit(
        {
            "status": "stage-started",
            "case_dir": str(case_dir),
            "stage": args.stage,
            "started_at": started_at,
            "event": event,
        },
        args.json,
    )
    return 0


def cmd_stage_end(args: argparse.Namespace) -> int:
    case_dir = Path(args.case_dir).expanduser().resolve()
    manifest = load_manifest(case_dir)
    stage = manifest.setdefault("stages", {}).get(args.stage)
    if not stage:
        raise SystemExit(f"unknown stage: {args.stage}")
    finished_at = now_iso()
    duration = stage_duration_seconds(stage, finished_at)
    stage["status"] = args.status
    stage["finished_at"] = finished_at
    if duration is not None:
        stage["duration_seconds"] = duration
        metrics = manifest.setdefault("metrics", default_metrics())
        metrics.setdefault("stage_durations_seconds", {})[args.stage] = duration
    stage["updated_at"] = finished_at
    event = append_event(
        case_dir,
        manifest,
        "stage-end",
        stage=args.stage,
        severity="warning" if args.status == "blocked" else "info",
        message=args.note or f"stage ended: {args.stage}",
        data={"stage_status": args.status, "duration_seconds": duration},
    )
    save_manifest(case_dir, manifest)
    write_status(case_dir, manifest)
    emit(
        {
            "status": "stage-ended",
            "case_dir": str(case_dir),
            "stage": args.stage,
            "stage_status": args.status,
            "finished_at": finished_at,
            "duration_seconds": duration,
            "event": event,
        },
        args.json,
    )
    return 0


def cmd_log_event(args: argparse.Namespace) -> int:
    case_dir = Path(args.case_dir).expanduser().resolve()
    manifest = load_manifest(case_dir)
    data: dict[str, Any] = {}
    if args.script:
        data["script"] = args.script
    if args.dependency:
        data["dependency"] = args.dependency
    if args.metadata_json:
        try:
            parsed = json.loads(args.metadata_json)
        except json.JSONDecodeError as exc:
            raise SystemExit(f"invalid --metadata-json: {exc}") from exc
        if not isinstance(parsed, dict):
            raise SystemExit("--metadata-json must be a JSON object")
        data.update(parsed)
    event = append_event(
        case_dir,
        manifest,
        args.event,
        stage=args.stage,
        severity=args.severity,
        message=args.message,
        data=data or None,
    )
    save_manifest(case_dir, manifest)
    write_status(case_dir, manifest)
    emit(
        {
            "status": "event-logged",
            "case_dir": str(case_dir),
            "event": event,
            "metrics": manifest.get("metrics", {}),
        },
        args.json,
    )
    return 0


def cmd_metrics(args: argparse.Namespace) -> int:
    case_dir = Path(args.case_dir).expanduser().resolve()
    manifest = load_manifest(case_dir)
    payload = summarize_metrics(case_dir, manifest)
    if args.output:
        output = Path(args.output).expanduser()
        if not output.is_absolute():
            output = case_dir / output
        output.parent.mkdir(parents=True, exist_ok=True)
        output.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        payload["output"] = str(output)
    emit(payload, args.json)
    return 0


def cmd_stage_report(args: argparse.Namespace) -> int:
    case_dir = Path(args.case_dir).expanduser().resolve()
    manifest = load_manifest(case_dir)
    stage = manifest.setdefault("stages", {}).get(args.stage)
    if not stage:
        raise SystemExit(f"unknown stage: {args.stage}")

    output = Path(args.output).expanduser() if args.output else stage_report_default_path(case_dir, args.stage, args.name)
    if not output.is_absolute():
        output = case_dir / output
    output.parent.mkdir(parents=True, exist_ok=True)

    created_at = now_iso()
    payload = {
        "schema_version": STAGE_REPORT_SCHEMA_VERSION,
        "case_id": manifest.get("case_id", case_dir.name),
        "stage": args.name or args.stage,
        "runtime_stage": args.stage,
        "status": args.status,
        "created_at": created_at,
        "inputs": args.input or [],
        "artifacts": args.artifact or [],
        "confirmed_findings": issue_items(args.confirmed, "confirmed"),
        "suspected_issues": issue_items(args.suspected, "suspected"),
        "assumptions": args.assumption or [],
        "blockers": args.blocker or [],
        "next_stage": args.next_stage,
    }
    if args.memo_path:
        payload["memo_path"] = args.memo_path
    if args.metadata_json:
        payload["metadata"] = parse_json_object_arg(args.metadata_json, "--metadata-json")

    output.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    report_rel = rel_to(output, case_dir)
    artifact = {
        "path": report_rel,
        "kind": "stage-report",
        "label": args.name or f"{args.stage} stage report",
        "status": args.status,
        "exists": output.exists(),
        "updated_at": created_at,
    }
    upsert_artifact(stage, artifact)
    status_map = {
        "completed": "completed",
        "needs-review": "in-progress",
        "blocked": "blocked",
        "skipped": "completed",
    }
    stage["status"] = status_map[args.status]
    stage["updated_at"] = created_at
    append_event(
        case_dir,
        manifest,
        "stage-report-written",
        stage=args.stage,
        severity="warning" if args.status in {"blocked", "needs-review"} else "info",
        message=f"stage report written: {report_rel}",
        data={"report": report_rel, "status": args.status},
    )
    save_manifest(case_dir, manifest)
    write_status(case_dir, manifest)
    emit(
        {
            "status": "stage-report-written",
            "case_dir": str(case_dir),
            "report": str(output),
            "stage_report": payload,
        },
        args.json,
    )
    return 0


def stage_is_complete(stage: dict[str, Any]) -> bool:
    return stage.get("status") in COMPLETED_STATUSES


def collect_validation(case_dir: Path, manifest: dict[str, Any]) -> tuple[list[dict], list[dict]]:
    hard: list[dict[str, str]] = []
    soft: list[dict[str, str]] = []
    stages = manifest.get("stages", {})
    stage_reports, stage_report_errors = collect_stage_reports(case_dir, manifest)
    hard.extend(stage_report_errors)

    for key in DRAFTING_REQUIRED_STAGES:
        stage = stages.get(key)
        if not stage:
            hard.append({"code": "missing-stage", "message": f"Manifest missing stage: {key}"})
            continue
        if not stage_is_complete(stage):
            hard.append({"code": "stage-not-complete", "message": f"Stage is not completed: {key}"})
        if not stage.get("artifacts"):
            hard.append({"code": "stage-no-artifact", "message": f"No artifact registered for: {key}"})

    reports_by_runtime_stage: dict[str, list[dict[str, Any]]] = {}
    for report in stage_reports:
        reports_by_runtime_stage.setdefault(str(report.get("runtime_stage") or ""), []).append(report)
        if report.get("status") == "blocked" or report.get("blockers"):
            hard.append(
                {
                    "code": "stage-report-blocked",
                    "message": f"Stage report has blockers: {report.get('_path', report.get('stage', 'unknown'))}",
                }
            )
        elif report.get("status") == "needs-review":
            soft.append(
                {
                    "code": "stage-report-needs-review",
                    "message": f"Stage report needs review: {report.get('_path', report.get('stage', 'unknown'))}",
                }
            )

    for key in DRAFTING_REQUIRED_STAGES:
        stage = stages.get(key)
        if stage_is_complete(stage or {}) and key not in reports_by_runtime_stage:
            soft.append({"code": "stage-report-missing", "message": f"No stage-report JSON found for completed stage: {key}"})

    for key, stage in stages.items():
        for artifact in stage.get("artifacts", []):
            path_text = artifact.get("path")
            if not path_text:
                hard.append({"code": "artifact-no-path", "message": f"Artifact without path in {key}"})
                continue
            artifact_path = Path(path_text)
            if not artifact_path.is_absolute():
                artifact_path = case_dir / artifact_path
            if not artifact_path.exists():
                hard.append(
                    {
                        "code": "artifact-missing",
                        "message": f"Registered artifact does not exist: {path_text}",
                    }
                )

    if not list(case_dir.rglob("*.docx")):
        soft.append({"code": "no-docx", "message": "No DOCX deliverable found in the case folder."})
    figure_dirs = [
        case_dir / PROCESS_OUTPUT_DIR / STAGE_DIR_NAMES["06_figures"],
        case_dir / FINAL_OUTPUT_DIR / STAGE_DIR_NAMES["06_figures"],
        case_dir / "06_figures",
    ]
    existing_figure_dirs = [path for path in figure_dirs if path.exists()]
    figure_assets: list[Path] = []
    for path in existing_figure_dirs:
        figure_assets.extend(path.rglob("*.svg"))
        figure_assets.extend(path.rglob("*.png"))
        figure_assets.extend(path.rglob("*.pdf"))
    if existing_figure_dirs and not figure_assets:
        soft.append({"code": "no-figure-asset", "message": "No SVG/PNG/PDF figure asset found in figure folders."})
    filing_stage = stages.get("08_filing_package", {})
    if not stage_is_complete(filing_stage):
        soft.append(
            {
                "code": "filing-package-not-complete",
                "message": "08_filing_package is not completed; drafting may be complete but filing-ready is not reached.",
            }
        )
    return hard, soft


def write_validation_report(
    case_dir: Path,
    manifest: dict[str, Any],
    hard: list[dict],
    soft: list[dict],
) -> Path:
    report_path = validation_report_path(case_dir)
    report_path.parent.mkdir(parents=True, exist_ok=True)
    lines = [
        "# Validation Report",
        "",
        f"- case_id: `{manifest.get('case_id', case_dir.name)}`",
        f"- title: {manifest.get('title') or ''}",
        f"- generated_at: `{now_iso()}`",
        f"- execution_mode: `{manifest.get('execution_mode', 'guided')}`",
        f"- drafting_status: `{manifest.get('status', {}).get('drafting', 'unknown')}`",
        f"- filing_status: `{manifest.get('status', {}).get('filing', 'unknown')}`",
        f"- hard_fail_count: {len(hard)}",
        f"- soft_fail_count: {len(soft)}",
        "",
        "## Hard Fails",
        "",
    ]
    if hard:
        for item in hard:
            lines.append(f"- `{item['code']}`: {item['message']}")
    else:
        lines.append("- None")
    lines.extend(["", "## Soft Fails", ""])
    if soft:
        for item in soft:
            lines.append(f"- `{item['code']}`: {item['message']}")
    else:
        lines.append("- None")
    metrics = summarize_metrics(case_dir, manifest)
    lines.extend(["", "## Stage Summary", "", "| Stage | Status | Artifacts |", "|---|---:|---:|"])
    for key, stage in manifest.get("stages", {}).items():
        lines.append(
            f"| `{key}` | `{stage.get('status', 'pending')}` | {len(stage.get('artifacts', []))} |"
        )
    stage_reports, stage_report_errors = collect_stage_reports(case_dir, manifest)
    lines.extend(
        [
            "",
            "## Stage Reports",
            "",
            "| Report | Runtime Stage | Status | Confirmed | Suspected | Assumptions | Blockers | Next Stage |",
            "|---|---|---:|---:|---:|---:|---:|---|",
        ]
    )
    if stage_reports:
        for report in stage_reports:
            lines.append(
                "| `{path}` | `{runtime}` | `{status}` | {confirmed} | {suspected} | {assumptions} | {blockers} | {next_stage} |".format(
                    path=report.get("_path", ""),
                    runtime=report.get("runtime_stage", ""),
                    status=report.get("status", ""),
                    confirmed=len(report.get("confirmed_findings") or []),
                    suspected=len(report.get("suspected_issues") or []),
                    assumptions=len(report.get("assumptions") or []),
                    blockers=len(report.get("blockers") or []),
                    next_stage=report.get("next_stage") or "",
                )
            )
    else:
        lines.append("| None |  |  |  |  |  |  |  |")
    if stage_report_errors:
        lines.extend(["", "### Stage Report Errors", ""])
        for item in stage_report_errors:
            lines.append(f"- `{item['code']}`: {item['message']}")
    lines.extend(
        [
            "",
            "## Workflow Metrics",
            "",
            f"- event_log: `{EVENT_LOG_NAME}`",
            f"- events_count: {metrics['events_count']}",
            f"- script_runs_count: {metrics['script_runs_count']}",
            f"- dependency_calls_count: {metrics['dependency_calls_count']}",
            f"- manual_interruptions_count: {metrics['manual_interruptions_count']}",
            f"- last_event_at: `{metrics.get('last_event_at') or ''}`",
            "",
            "| Stage | Duration Seconds |",
            "|---|---:|",
        ]
    )
    for key, stage_metrics in metrics["stages"].items():
        duration = stage_metrics.get("duration_seconds")
        lines.append(f"| `{key}` | {duration if duration is not None else ''} |")
    report_path.write_text("\n".join(lines) + "\n", encoding="utf-8")
    return report_path


def register_validation_artifact(case_dir: Path, manifest: dict[str, Any], report_path: Path) -> None:
    qc_stage = manifest.setdefault("stages", {}).setdefault(
        "07_qc",
        {"label": "质检", "status": "pending", "artifacts": [], "notes": []},
    )
    report_rel = rel_to(report_path, case_dir)
    if not any(item.get("path") == report_rel for item in qc_stage.setdefault("artifacts", [])):
        qc_stage["artifacts"].append(
            {
                "path": report_rel,
                "kind": "validation-report",
                "label": "验证报告",
                "status": "generated",
                "exists": report_path.exists(),
                "updated_at": now_iso(),
            }
        )
    else:
        for item in qc_stage["artifacts"]:
            if item.get("path") == report_rel:
                item["exists"] = report_path.exists()
                item["updated_at"] = now_iso()
    qc_stage["updated_at"] = now_iso()


def apply_validation_status(manifest: dict[str, Any], hard: list[dict], soft: list[dict]) -> None:
    status = manifest.setdefault("status", {})
    status["hard_fail_count"] = len(hard)
    status["soft_fail_count"] = len(soft)
    status["drafting"] = "drafting-complete" if not hard else "blocked"
    status["filing"] = "filing-ready" if not hard and not soft else "not-ready"
    manifest.setdefault("metrics", default_metrics())["last_validation"] = {
        "updated_at": now_iso(),
        "hard_fail_count": len(hard),
        "soft_fail_count": len(soft),
        "drafting_status": status["drafting"],
        "filing_status": status["filing"],
    }


def cmd_validate(args: argparse.Namespace) -> int:
    case_dir = Path(args.case_dir).expanduser().resolve()
    manifest = load_manifest(case_dir)
    hard, soft = collect_validation(case_dir, manifest)
    apply_validation_status(manifest, hard, soft)
    report_path = write_validation_report(case_dir, manifest, hard, soft)
    register_validation_artifact(case_dir, manifest, report_path)

    append_event(
        case_dir,
        manifest,
        "validation-run",
        severity="warning" if hard else "info",
        message="validation report generated",
        data={
            "hard_fail_count": len(hard),
            "soft_fail_count": len(soft),
            "drafting_status": manifest["status"]["drafting"],
            "filing_status": manifest["status"]["filing"],
        },
    )
    save_manifest(case_dir, manifest)
    write_status(case_dir, manifest)
    payload = {
        "status": manifest["status"]["drafting"],
        "case_dir": str(case_dir),
        "report": str(report_path),
        "hard_fails": hard,
        "soft_fails": soft,
        "filing_status": manifest["status"]["filing"],
    }
    emit(payload, args.json)
    return 1 if hard and args.fail_on_hard else 0


def which_any(names: list[str]) -> str | None:
    for name in names:
        hit = shutil.which(name)
        if hit:
            return hit
    return None


def import_check(module: str) -> bool:
    code = f"import {module}"
    return subprocess.run([sys.executable, "-c", code], capture_output=True).returncode == 0


def doctor_checks(deep: bool = False) -> list[dict[str, Any]]:
    root = skills_root()
    checks: list[dict[str, Any]] = []

    def add(name: str, ok: bool, severity: str, detail: str) -> None:
        checks.append({"name": name, "ok": bool(ok), "severity": severity, "detail": detail})

    add("python-version", sys.version_info >= (3, 10), "required", platform.python_version())
    add("python-executable", bool(sys.executable), "required", sys.executable)

    required_files = {
        "workflow-script": root / "patent-entry-drafting/scripts/patent_workflow.py",
        "qc-micro-script": root / "patent-entry-drafting/scripts/patent_qc_micro.py",
        "tool-registry": root / "patent-cn-runtime/scripts/tool_registry.json",
        "specialist-registry": root / "patent-cn-runtime/scripts/specialist_registry.json",
        "tool-runner": root / "patent-cn-runtime/scripts/patent_tool_runner.py",
        "prior-art-bigquery-script": root / "patent-stage-prior-art-search/scripts/bigquery_search.py",
        "google-patents-fetch-script": root / "patent-stage-prior-art-search/scripts/google_patents_fetch.py",
        "reference-bundle-script": root / "patent-stage-prior-art-search/scripts/download_reference_bundle.py",
        "docx-inspect-script": root / "patent-support-docx-math/scripts/inspect_docx.py",
        "cn-formality-script": root / "patent-qc-cn-formality/scripts/check_patent_formal.py",
        "application-consistency-script": root
        / "patent-qc-application-consistency/scripts/patent_doc_tools.py",
    }
    for name, path in required_files.items():
        add(name, path.exists(), "required", str(path))

    optional_files = {
        "flowchart-renderer": root / "patent-drawing-generator/scripts/patent-flowchart",
        "word-template": root / "patent-cn/templates/专利撰写模板文件.docx",
        "oa-response-template-amended": root
        / "patent-entry-oa-response/assets/templates/意见陈述-有修改.docx",
        "oa-response-template-unamended": root
        / "patent-entry-oa-response/assets/templates/意见陈述-无修改.docx",
    }
    for name, path in optional_files.items():
        add(name, path.exists(), "optional", str(path))

    add("libreoffice", bool(which_any(["soffice", "libreoffice"])), "optional", which_any(["soffice", "libreoffice"]) or "not found")
    add("gcloud", bool(which_any(["gcloud"])), "optional", which_any(["gcloud"]) or "not found")
    add("GOOGLE_CLOUD_PROJECT", bool(os.environ.get("GOOGLE_CLOUD_PROJECT")), "optional", os.environ.get("GOOGLE_CLOUD_PROJECT", "not set"))
    add("lxml-import", import_check("lxml"), "required", "Python import lxml")
    add("pillow-import", import_check("PIL"), "optional", "Python import PIL for flowchart rendering")

    if deep:
        bq_script = required_files["prior-art-bigquery-script"]
        if bq_script.exists():
            result = subprocess.run(
                [sys.executable, str(bq_script), "doctor"],
                capture_output=True,
                text=True,
                timeout=20,
            )
            add("bigquery-doctor", result.returncode == 0, "optional", result.stdout.strip()[:500])
    return checks


def cmd_doctor(args: argparse.Namespace) -> int:
    checks = doctor_checks(args.deep)
    required_missing = [item for item in checks if item["severity"] == "required" and not item["ok"]]
    optional_missing = [item for item in checks if item["severity"] == "optional" and not item["ok"]]
    overall = "blocked" if required_missing else ("ready-with-warnings" if optional_missing else "ready")
    payload = {
        "overall": overall,
        "required_missing": len(required_missing),
        "optional_missing": len(optional_missing),
        "checks": checks,
    }
    if args.json:
        print(json.dumps(payload, ensure_ascii=False, indent=2))
    else:
        print(f"overall: {overall}")
        for item in checks:
            marker = "OK" if item["ok"] else "MISS"
            print(f"{marker} [{item['severity']}] {item['name']}: {item['detail']}")
    return 1 if required_missing and args.fail_on_required else 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Manage local patent workflow case state.")
    sub = parser.add_subparsers(dest="command", required=True)

    init = sub.add_parser("init", help="Initialize a patent case folder with manifest and status files.")
    init.add_argument("--case-dir", required=True)
    init.add_argument("--title")
    init.add_argument("--source")
    init.add_argument("--mode", choices=sorted(EXECUTION_MODES), default="guided")
    init.add_argument("--force", action="store_true")
    init.add_argument("--json", action="store_true")
    init.set_defaults(func=cmd_init)

    set_mode = sub.add_parser("set-mode", help="Update the case execution mode.")
    set_mode.add_argument("--case-dir", required=True)
    set_mode.add_argument("--mode", choices=sorted(EXECUTION_MODES), required=True)
    set_mode.add_argument("--json", action="store_true")
    set_mode.set_defaults(func=cmd_set_mode)

    stage_start = sub.add_parser("stage-start", help="Mark a workflow stage as started.")
    stage_start.add_argument("--case-dir", required=True)
    stage_start.add_argument("--stage", required=True, choices=[key for key, _ in DEFAULT_STAGES])
    stage_start.add_argument("--note")
    stage_start.add_argument("--json", action="store_true")
    stage_start.set_defaults(func=cmd_stage_start)

    stage_end = sub.add_parser("stage-end", help="Mark a workflow stage as ended.")
    stage_end.add_argument("--case-dir", required=True)
    stage_end.add_argument("--stage", required=True, choices=[key for key, _ in DEFAULT_STAGES])
    stage_end.add_argument("--status", required=True, choices=sorted(STAGE_STATUSES - {"pending"}))
    stage_end.add_argument("--note")
    stage_end.add_argument("--json", action="store_true")
    stage_end.set_defaults(func=cmd_stage_end)

    log_event = sub.add_parser("log-event", help="Append a structured event to the case log.")
    log_event.add_argument("--case-dir", required=True)
    log_event.add_argument("--event", required=True, help="Event name, e.g. script-run, dependency-call, manual-interruption.")
    log_event.add_argument("--stage", choices=[key for key, _ in DEFAULT_STAGES])
    log_event.add_argument("--severity", choices=["info", "warning", "error"], default="info")
    log_event.add_argument("--message")
    log_event.add_argument("--script")
    log_event.add_argument("--dependency")
    log_event.add_argument("--metadata-json", help="Additional JSON object to store under event data.")
    log_event.add_argument("--json", action="store_true")
    log_event.set_defaults(func=cmd_log_event)

    metrics = sub.add_parser("metrics", help="Summarize workflow event and stage metrics.")
    metrics.add_argument("--case-dir", required=True)
    metrics.add_argument("--output", help="Optional JSON output path, relative to case dir if not absolute.")
    metrics.add_argument("--json", action="store_true")
    metrics.set_defaults(func=cmd_metrics)

    stage_report = sub.add_parser("stage-report", help="Write a standard stage-report JSON and register it.")
    stage_report.add_argument("--case-dir", required=True)
    stage_report.add_argument("--stage", required=True, choices=[key for key, _ in DEFAULT_STAGES])
    stage_report.add_argument("--name", help="Logical stage name; also used in the default filename.")
    stage_report.add_argument("--status", required=True, choices=sorted(STAGE_REPORT_STATUSES))
    stage_report.add_argument("--input", action="append", help="Input artifact/path/label; repeatable.")
    stage_report.add_argument("--artifact", action="append", help="Output artifact/path/label; repeatable.")
    stage_report.add_argument("--confirmed", action="append", help="Confirmed finding message; repeatable.")
    stage_report.add_argument("--suspected", action="append", help="Suspected issue message; repeatable.")
    stage_report.add_argument("--assumption", action="append", help="Assumption text; repeatable.")
    stage_report.add_argument("--blocker", action="append", help="Blocker text; repeatable.")
    stage_report.add_argument("--next-stage")
    stage_report.add_argument("--memo-path", help="Human-readable memo path, preferably relative to case dir.")
    stage_report.add_argument("--metadata-json", help="Additional JSON object stored under metadata.")
    stage_report.add_argument("--output", help="Optional JSON output path; defaults to 记录/<中文阶段>/报告/<name>-stage-report.json.")
    stage_report.add_argument("--json", action="store_true")
    stage_report.set_defaults(func=cmd_stage_report)

    artifact = sub.add_parser("add-artifact", help="Register a stage artifact in manifest.json.")
    artifact.add_argument("--case-dir", required=True)
    artifact.add_argument("--stage", required=True, choices=[key for key, _ in DEFAULT_STAGES])
    artifact.add_argument("--path", required=True)
    artifact.add_argument("--kind", required=True)
    artifact.add_argument("--label")
    artifact.add_argument("--status", default="ready")
    artifact.add_argument("--stage-status", choices=sorted(STAGE_STATUSES))
    artifact.add_argument("--note")
    artifact.add_argument("--json", action="store_true")
    artifact.set_defaults(func=cmd_add_artifact)

    validate = sub.add_parser("validate", help="Generate validation-report.md and update case status.")
    validate.add_argument("--case-dir", required=True)
    validate.add_argument("--fail-on-hard", action="store_true")
    validate.add_argument("--json", action="store_true")
    validate.set_defaults(func=cmd_validate)

    doctor = sub.add_parser("doctor", help="Check local patent workflow dependencies.")
    doctor.add_argument("--deep", action="store_true", help="Run slower external doctors where available.")
    doctor.add_argument("--fail-on-required", action="store_true")
    doctor.add_argument("--json", action="store_true")
    doctor.set_defaults(func=cmd_doctor)

    return parser


def main() -> int:
    args = build_parser().parse_args()
    return args.func(args)


if __name__ == "__main__":
    raise SystemExit(main())
