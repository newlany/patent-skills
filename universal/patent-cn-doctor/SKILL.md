---
name: patent-cn-doctor
version: 2.0.0
description: |
  Public health-check entry for the local Chinese patent workflow. Checks whether the patent system,
  tool/specialist registries, BigQuery, Google Patents bundle scripts, LibreOffice, DOCX math inspection,
  flowchart renderer, Word template, Python dependencies, and JSON workflow tools are ready.
  Trigger phrases: "doctor", "健康检查", "系统检查", "能不能跑", "health", "status".
user-invocable: true
allowed-tools:
  - Read
  - Bash
  - Grep
  - Glob
---
# CN Patent System Doctor

## Role

Health-check entry for the local Chinese patent workflow.

Use when:
- User asks "检查专利系统能不能跑"
- User says "doctor" or "health/status"
- Before starting a new case to verify dependencies

## Checks

Quick check:
```bash
python3 /Users/chrynos/.codex/skills/patent-cn-runtime/scripts/patent_tool_runner.py run workflow.doctor
```

Deep check:
```bash
python3 /Users/chrynos/.codex/skills/patent-entry-drafting/scripts/patent_workflow.py doctor --deep --json
```

## Output

```
PATENT SYSTEM STATUS
- overall: ready|ready-with-warnings|blocked
- required missing: <count>
- optional missing: <count>
- blockers: <list>
- warnings: <list>
- next fix: <suggestion>
```
