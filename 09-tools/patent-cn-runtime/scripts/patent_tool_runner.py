#!/usr/bin/env python3
"""Run local patent tools through a single JSON-first registry."""

from __future__ import annotations

import argparse
import json
import shlex
import subprocess
import sys
from pathlib import Path
from typing import Any


REGISTRY_PATH = Path(__file__).with_name("tool_registry.json")
WORKFLOW_SCRIPT = "/Users/chrynos/.codex/skills/patent-entry-drafting/scripts/patent_workflow.py"


def load_registry(path: Path = REGISTRY_PATH) -> dict[str, Any]:
    payload = json.loads(path.read_text(encoding="utf-8"))
    if payload.get("schema_version") != "patent-tool-registry/v1":
        raise SystemExit(f"unsupported registry schema: {path}")
    return payload


def parse_kv(values: list[str] | None) -> dict[str, str]:
    result: dict[str, str] = {}
    for value in values or []:
        if "=" not in value:
            raise SystemExit(f"--arg must use key=value form: {value}")
        key, raw = value.split("=", 1)
        key = key.strip()
        if not key:
            raise SystemExit(f"--arg has empty key: {value}")
        result[key] = raw
    return result


def build_context(args: argparse.Namespace, tool: dict[str, Any]) -> dict[str, str]:
    context: dict[str, str] = {key: str(value) for key, value in tool.get("defaults", {}).items()}
    context.update(parse_kv(args.arg))
    context["python"] = sys.executable
    context["script"] = tool["script"]
    if args.case_dir:
        context["case_dir"] = str(Path(args.case_dir).expanduser().resolve())
    if args.input:
        context["input"] = str(Path(args.input).expanduser().resolve())
    if args.output:
        context["output"] = str(Path(args.output).expanduser().resolve())
    return context


def ensure_required(context: dict[str, str], required: list[str]) -> None:
    missing = [key for key in required if not context.get(key)]
    if missing:
        raise SystemExit("missing required tool arguments: " + ", ".join(missing))


def expand_template(value: str, context: dict[str, str]) -> str:
    try:
        return value.format(**context)
    except KeyError as exc:
        raise SystemExit(f"missing template value: {exc.args[0]}") from exc


def build_argv(tool: dict[str, Any], context: dict[str, str]) -> list[str]:
    split_args = set(tool.get("split_args", []))
    argv: list[str] = []
    for item in tool["argv"]:
        expanded = expand_template(item, context)
        if item.startswith("{") and item.endswith("}") and item[1:-1] in split_args:
            argv.extend(shlex.split(expanded))
        else:
            argv.append(expanded)
    return argv


def parse_stdout(stdout: str, expect_json: bool) -> tuple[Any, str | None]:
    if not stdout.strip():
        return None, None
    try:
        return json.loads(stdout), None
    except json.JSONDecodeError as exc:
        if expect_json:
            return None, f"stdout was not valid JSON: {exc}"
        return None, None


def output_paths(tool: dict[str, Any], context: dict[str, str]) -> dict[str, str]:
    outputs: dict[str, str] = {}
    for key, template in tool.get("outputs", {}).items():
        outputs[key] = expand_template(template, context)
    return outputs


def write_result(path_text: str, payload: dict[str, Any]) -> str:
    path = Path(path_text).expanduser().resolve()
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return str(path)


def log_case_event(case_dir: str, stage: str | None, tool_id: str, payload: dict[str, Any]) -> None:
    metadata = {
        "tool_id": tool_id,
        "ok": payload["ok"],
        "returncode": payload["returncode"],
        "result_output": payload.get("result_output"),
    }
    cmd = [
        sys.executable,
        WORKFLOW_SCRIPT,
        "log-event",
        "--case-dir",
        case_dir,
        "--event",
        "script-run",
        "--script",
        tool_id,
        "--metadata-json",
        json.dumps(metadata, ensure_ascii=False),
        "--json",
    ]
    if stage:
        cmd.extend(["--stage", stage])
    subprocess.run(cmd, capture_output=True, text=True, check=False)


def cmd_list(args: argparse.Namespace) -> int:
    registry = load_registry(Path(args.registry) if args.registry else REGISTRY_PATH)
    tools = registry["tools"]
    payload = {
        "schema_version": registry["schema_version"],
        "tools": [
            {
                "id": tool_id,
                "category": spec.get("category"),
                "stage": spec.get("stage"),
                "description": spec.get("description"),
                "required": spec.get("required", []),
            }
            for tool_id, spec in sorted(tools.items())
        ],
    }
    print(json.dumps(payload, ensure_ascii=False, indent=2))
    return 0


def cmd_describe(args: argparse.Namespace) -> int:
    registry = load_registry(Path(args.registry) if args.registry else REGISTRY_PATH)
    tool = registry["tools"].get(args.tool)
    if not tool:
        raise SystemExit(f"unknown tool: {args.tool}")
    payload = {"tool_id": args.tool, **tool}
    print(json.dumps(payload, ensure_ascii=False, indent=2))
    return 0


def cmd_run(args: argparse.Namespace) -> int:
    registry = load_registry(Path(args.registry) if args.registry else REGISTRY_PATH)
    tool = registry["tools"].get(args.tool)
    if not tool:
        raise SystemExit(f"unknown tool: {args.tool}")

    context = build_context(args, tool)
    ensure_required(context, tool.get("required", []))
    argv = build_argv(tool, context)

    completed = subprocess.run(
        argv,
        capture_output=True,
        text=True,
        timeout=args.timeout,
        check=False,
    )
    stdout_json, parse_error = parse_stdout(completed.stdout, bool(tool.get("stdout_json")))
    payload: dict[str, Any] = {
        "schema_version": "patent-tool-run/v1",
        "tool_id": args.tool,
        "category": tool.get("category"),
        "stage": args.stage or tool.get("stage"),
        "ok": completed.returncode == 0 and not parse_error,
        "returncode": completed.returncode,
        "command": argv,
        "stdout_json": stdout_json,
        "stdout": completed.stdout if stdout_json is None else None,
        "stderr": completed.stderr,
        "parse_error": parse_error,
        "outputs": output_paths(tool, context),
    }
    if args.case_dir:
        payload["case_dir"] = context["case_dir"]
    if args.result_output:
        result_path = write_result(args.result_output, payload)
        payload["result_output"] = result_path
    if args.case_dir and not args.no_log:
        log_case_event(context["case_dir"], args.stage or tool.get("stage"), args.tool, payload)

    print(json.dumps(payload, ensure_ascii=False, indent=2))
    return 0 if payload["ok"] else 1


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Run patent tools through tool_registry.json.")
    parser.add_argument("--registry", help="Override registry JSON path.")
    sub = parser.add_subparsers(dest="command", required=True)

    list_parser = sub.add_parser("list", help="List registered tools.")
    list_parser.set_defaults(func=cmd_list)

    describe = sub.add_parser("describe", help="Describe one registered tool.")
    describe.add_argument("tool")
    describe.set_defaults(func=cmd_describe)

    run = sub.add_parser("run", help="Run one registered tool.")
    run.add_argument("tool")
    run.add_argument("--case-dir")
    run.add_argument("--stage")
    run.add_argument("--input")
    run.add_argument("--output")
    run.add_argument("--result-output", help="Write normalized run JSON to this path.")
    run.add_argument("--arg", action="append", help="Extra key=value template argument; repeatable.")
    run.add_argument("--timeout", type=int, default=120)
    run.add_argument("--no-log", action="store_true", help="Do not log script-run to the case event log.")
    run.set_defaults(func=cmd_run)
    return parser


def main() -> int:
    args = build_parser().parse_args()
    return args.func(args)


if __name__ == "__main__":
    raise SystemExit(main())
