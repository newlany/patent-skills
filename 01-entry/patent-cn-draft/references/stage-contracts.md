# Stage Contracts

Every stage must produce a machine-readable report and a human-readable memo when the stage is substantial.

Use the runtime command whenever possible instead of hand-writing JSON:

```bash
python3 /Users/chrynos/.codex/skills/patent-entry-drafting/scripts/patent_workflow.py stage-report \
  --case-dir <case-dir> \
  --stage 01_disclosure \
  --name disclosure-analysis \
  --status completed \
  --input source.docx \
  --artifact 输出/过程/01_交底分析/交底分析.md \
  --confirmed "确认技术问题与核心方案" \
  --suspected "效果数据仍需发明人确认" \
  --assumption "以当前交底文本为基线" \
  --next-stage checkpoint-a-search \
  --memo-path 输出/过程/01_交底分析/交底分析.md \
  --json
```

By default this writes `记录/<中文阶段名>/报告/<name>-stage-report.json`, registers it in `manifest.json`, and makes `validate` summarize it in `输出/定稿/验证报告.md`. Runtime stage IDs such as `01_disclosure` remain command arguments; they should not be used as new folder names.

## Required JSON Shape

Write stage reports as:

```json
{
  "schema_version": "patent-stage-report/v1",
  "case_id": "case-folder-name",
  "stage": "checkpoint-a-search",
  "runtime_stage": "02_search",
  "status": "completed",
  "created_at": "2026-04-25T00:00:00+08:00",
  "inputs": [],
  "artifacts": [],
  "confirmed_findings": [],
  "suspected_issues": [],
  "assumptions": [],
  "blockers": [],
  "next_stage": "solution-reconstruction"
}
```

Allowed `status` values:

- `completed`
- `needs-review`
- `blocked`
- `skipped`

## Issue Shape

Use this shape for issues:

```json
{
  "severity": "confirmed|suspected|info",
  "code": "claim-forward-citation",
  "location": "权利要求3",
  "message": "权利要求3引用了自身或后续权利要求。",
  "suggestion": "改为引用在先权利要求。"
}
```

## Artifact Registration

After writing a stage report or memo, register it:

```bash
python3 /Users/chrynos/.codex/skills/patent-entry-drafting/scripts/patent_workflow.py add-artifact \
  --case-dir <case-dir> \
  --stage <runtime-stage> \
  --path <relative-path> \
  --kind stage-report \
  --stage-status completed \
  --json
```

## Human Memo

The memo should be short and decision-oriented:

- what was read
- what was concluded
- what is risky or missing
- what changed for the next stage
- whether user confirmation is needed

Do not bury blockers inside prose; also write them into `blockers[]` in the JSON report.

## Validation Aggregation

`patent_workflow.py validate` scans registered stage reports and files named:

- `stage-report.json`
- `*-stage-report.json`
- `stage-reports/*.json`
- `reports/*.json`
- `报告/*.json`

Validation treats:

- invalid or missing registered stage-report files as hard fails
- `status: blocked` or non-empty `blockers[]` as hard fails
- `status: needs-review` as a soft fail
- a completed runtime stage without any stage report as a soft fail
