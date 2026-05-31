# Case Manifest And Validation

Use this structure when a drafting task spans multiple stages. If the user has not provided a case folder, create it under `<project-root>/专利工作区/<中文案件名>` so the project root does not fill with process documents.

## Minimal Initialization

Run:

```bash
python3 /Users/chrynos/.codex/skills/patent-entry-drafting/scripts/patent_workflow.py init \
  --case-dir <case-dir> \
  --title "<case-title>" \
  --source <source-file-or-label> \
  --mode guided \
  --json
```

After initialization, the case folder should contain only:

```text
manifest.json
00_case_status.md
00_case_events.jsonl
```

Do not pre-create admin, archive, stage, output, report, or tool-run folders.

## Directory Policy

Create directories lazily, only when writing a file:

```text
输出/过程/                  # human-readable process artifacts
输出/过程/<中文阶段名>/       # only when grouping multiple stage files helps
输出/定稿/                  # final deliverables and validation reports
记录/<中文阶段名>/报告/       # machine stage reports, metrics, scan summaries
记录/<中文阶段名>/工具运行/   # normalized tool-run JSON
```

Human-readable process files should use Chinese file names, headings, and main prose by default. Keep English only for stable tool contracts, JSON keys, command IDs, source titles, citations, or file names that a script explicitly expects.

Use these stage directory names when a stage folder is needed:

```text
01_交底分析
02_现有技术检索
03_方案重构
04_权利要求
05_说明书
06_附图
07_质检
08_提交包
```

Runtime stage IDs such as `01_disclosure` and `07_qc` remain command arguments and manifest keys. They are not new directory names.

## Artifact Registration

Register user-facing outputs and machine reports:

```bash
python3 /Users/chrynos/.codex/skills/patent-entry-drafting/scripts/patent_workflow.py add-artifact \
  --case-dir <case-dir> \
  --stage 02_search \
  --path 输出/过程/02_现有技术检索/检索纪要A.md \
  --kind search-memo \
  --stage-status completed \
  --json
```

Prefer these paths for common artifacts:

```text
输出/过程/01_交底分析/交底分析.md
输出/过程/02_现有技术检索/检索纪要A.md
输出/过程/02_现有技术检索/检索纪要B.md
输出/过程/02_现有技术检索/参考文献撰写质量.md
输出/过程/03_方案重构/方案重构备忘录.md
输出/过程/04_权利要求/权利要求当前稿.md
输出/过程/05_说明书/说明书当前稿.md
输出/过程/06_附图/附图说明.md
输出/定稿/验证报告.md
输出/定稿/提交清单.md
输出/定稿/申请文件.docx
```

## Events And Metrics

Use stage events for substantial work:

```bash
python3 /Users/chrynos/.codex/skills/patent-entry-drafting/scripts/patent_workflow.py stage-start \
  --case-dir <case-dir> \
  --stage 01_disclosure \
  --json

python3 /Users/chrynos/.codex/skills/patent-entry-drafting/scripts/patent_workflow.py stage-end \
  --case-dir <case-dir> \
  --stage 01_disclosure \
  --status completed \
  --json
```

Write workflow metrics only when needed:

```bash
python3 /Users/chrynos/.codex/skills/patent-entry-drafting/scripts/patent_workflow.py metrics \
  --case-dir <case-dir> \
  --output 记录/07_质检/报告/workflow-metrics.json \
  --json
```

`validate` summarizes current workflow metrics in `输出/定稿/验证报告.md`.

## Stage Reports

Use the stage-report command whenever possible:

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

By default this writes `记录/01_交底分析/报告/disclosure-analysis-stage-report.json`, registers it in `manifest.json`, and makes `validate` summarize it in `输出/定稿/验证报告.md`.

## Validation

Run validation before declaring `drafting-complete` or `filing-ready`:

```bash
python3 /Users/chrynos/.codex/skills/patent-entry-drafting/scripts/patent_workflow.py validate \
  --case-dir <case-dir> \
  --json
```

Validation checks:

- required runtime stages exist in `manifest.json`
- stages `01_disclosure` through `07_qc` are completed or verified before `drafting-complete`
- each required completed stage has registered artifacts
- registered artifacts exist
- registered stage reports are valid `patent-stage-report/v1` JSON
- `status: blocked` or non-empty `blockers[]` is a hard fail
- `status: needs-review` is a soft fail

Validation does not require physical stage directories; empty folders are never evidence of progress.

## Tool-Run Outputs

For normalized tool-run JSON, use Chinese `记录/` paths:

```bash
python3 /Users/chrynos/.codex/skills/patent-cn-runtime/scripts/patent_tool_runner.py run qc.micro \
  --case-dir /path/to/case \
  --input draft.docx \
  --result-output /path/to/case/记录/07_质检/工具运行/micro-qc-tool-run.json
```

For direct helper outputs:

```bash
python3 .../extract_disclosure_text.py input.docx --output 输出/过程/01_交底分析/交底原文.txt --json
python3 .../download_reference_bundle.py US-... --save-dir 记录/02_现有技术检索/参考文献包
python3 .../patent_qc_micro.py check draft.docx --json --output 记录/07_质检/报告/micro-qc.json
```
