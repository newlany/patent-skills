#!/usr/bin/env python3
"""
PostToolUse hook: Reminds agent to register artifacts in manifest.json.
"""
import json
import os
import sys

def main():
    tool_input = os.environ.get("TOOL_INPUT", "{}")
    try:
        data = json.loads(tool_input)
    except json.JSONDecodeError:
        return 0

    file_path = data.get("file_path", "") or data.get("path", "")
    if not file_path:
        return 0

    # Only remind for files in 输出/ directory
    if "输出/" in file_path or "输出\\" in file_path:
        # Determine the artifact kind from path
        kind = "unknown"
        if "过程" in file_path:
            kind = "process"
        elif "定稿" in file_path:
            kind = "final"

        print(f"REMINDER: Register artifact in manifest.json via: python3 patent_workflow.py add-artifact --path \"{file_path}\" --kind \"{kind}\"", file=sys.stderr)

    return 0

if __name__ == "__main__":
    sys.exit(main())
