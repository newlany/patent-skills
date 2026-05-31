#!/usr/bin/env python3
"""
Stop hook: Blocks completion if agent declares filing-ready/drafting-complete without validation.
"""
import json
import os
import re
import sys

def main():
    agent_output = os.environ.get("AGENT_OUTPUT", "")

    # Check for completion declarations
    completion_patterns = [
        r"filing-ready",
        r"drafting-complete",
        r"申请文件.*完成",
        r"撰写.*完成",
        r"答复.*完成",
    ]

    is_declaring_completion = any(re.search(p, agent_output, re.IGNORECASE) for p in completion_patterns)

    if not is_declaring_completion:
        return 0

    # Check if validation was mentioned
    validation_patterns = [
        r"validate",
        r"validation",
        r"验证",
        r"质检",
        r"QC",
        r"patent_workflow\.py.*validate",
    ]

    has_validation = any(re.search(p, agent_output, re.IGNORECASE) for p in validation_patterns)

    if not has_validation:
        print("BLOCKED: Agent declared completion without mentioning validation. Run 'python3 patent_workflow.py validate --case-dir <dir> --json' first.", file=sys.stderr)
        return 1

    return 0

if __name__ == "__main__":
    sys.exit(main())
