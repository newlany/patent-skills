---
name: patent-cn-doctor
description: "Public health-check entry for the local Chinese patent workflow. Use when the user asks to check whether the patent system, tool/specialist registries, BigQuery, Google Patents bundle scripts, LibreOffice, DOCX math inspection, flowchart renderer, Word template, Python dependencies, or JSON workflow tools are ready."
---
# CN Patent Doctor

## Role

This is the public system-health entry for the local patent workflow.

Use it when the user asks:

- “检查专利系统能不能跑”
- “doctor”
- “health/status”
- “BigQuery、LibreOffice、DOCX、流程图工具、tool registry、specialist registry 是否正常”

## Command

Run:

```bash
python3 /Users/chrynos/.codex/skills/patent-cn-runtime/scripts/patent_tool_runner.py run workflow.doctor
```

Use `--deep` when the user wants slower external checks:

```bash
python3 /Users/chrynos/.codex/skills/patent-entry-drafting/scripts/patent_workflow.py doctor --deep --json
```

## Report Format

Return:

```text
CN PATENT DOCTOR
- overall: <ready|ready-with-warnings|blocked>
- required missing: <count>
- optional missing: <count>
- required blockers: <short list>
- optional warnings: <short list>
- next fix: <one sentence>
```

Do not hide missing required dependencies. Missing optional dependencies should be framed as capability limitations, not fatal failures.
