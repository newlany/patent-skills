#!/usr/bin/env python3
"""
PreToolUse hook: Enforces patent workflow stage ordering.
Blocks writes to later stages if earlier stages are incomplete.
"""
import json
import os
import sys

def find_manifest(file_path):
    """Walk up from file_path to find manifest.json."""
    current = os.path.dirname(file_path)
    for _ in range(10):
        manifest = os.path.join(current, "manifest.json")
        if os.path.exists(manifest):
            return manifest
        parent = os.path.dirname(current)
        if parent == current:
            break
        current = parent
    return None

def get_stage_from_path(file_path):
    """Determine which stage a file belongs to based on path."""
    path_lower = file_path.lower()
    if any(x in path_lower for x in ["01_交底", "01_disclosure", "交底分析"]):
        return "disclosure"
    elif any(x in path_lower for x in ["02_现有技术", "02_search", "检索", "现有技术"]):
        return "search"
    elif any(x in path_lower for x in ["03_方案", "03_reconstruction", "重构"]):
        return "reconstruction"
    elif any(x in path_lower for x in ["04_权利要求", "04_claims", "权利要求书"]):
        return "claims"
    elif any(x in path_lower for x in ["05_说明书", "05_specification", "说明书"]):
        return "specification"
    elif any(x in path_lower for x in ["06_附图", "06_figures", "附图"]):
        return "figures"
    elif any(x in path_lower for x in ["07_质检", "07_qc", "质检"]):
        return "qc"
    return None

STAGE_ORDER = ["disclosure", "search", "reconstruction", "claims", "specification", "figures", "qc"]

STAGE_DEPENDENCIES = {
    "search": ["disclosure"],
    "reconstruction": ["disclosure", "search"],
    "claims": ["disclosure", "search", "reconstruction"],
    "specification": ["disclosure", "search", "reconstruction", "claims"],
    "figures": ["disclosure", "search", "reconstruction", "claims", "specification"],
    "qc": ["disclosure", "search", "reconstruction", "claims", "specification"],
}

def main():
    # Read environment variables set by Claude Code hooks
    tool_input = os.environ.get("TOOL_INPUT", "{}")
    try:
        data = json.loads(tool_input)
    except json.JSONDecodeError:
        return 0

    file_path = data.get("file_path", "") or data.get("path", "")
    if not file_path:
        return 0

    # Only check files in 输出/ directory
    if "输出/" not in file_path and "输出\\" not in file_path:
        return 0

    stage = get_stage_from_path(file_path)
    if not stage:
        return 0

    manifest_path = find_manifest(file_path)
    if not manifest_path:
        return 0  # No manifest, can't enforce

    try:
        with open(manifest_path, "r") as f:
            manifest = json.load(f)
    except (json.JSONDecodeError, IOError):
        return 0

    stages = manifest.get("stages", {})
    dependencies = STAGE_DEPENDENCIES.get(stage, [])

    for dep in dependencies:
        dep_status = stages.get(dep, {}).get("status", "pending")
        if dep_status != "completed":
            print(f"BLOCKED: Cannot write to stage '{stage}' because dependency '{dep}' is '{dep_status}'. Complete '{dep}' first.", file=sys.stderr)
            return 1

    return 0

if __name__ == "__main__":
    sys.exit(main())
