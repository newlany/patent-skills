# Case Workspace Layout

Use this layout whenever a patent workflow produces more than one artifact. The goal is to keep the user's project root clean, avoid empty folders, and keep all new directory names in Chinese.

## Project Root Rule

Do not write process documents directly into the project root. Unless the user gives an existing case folder containing `manifest.json`, create or use:

```text
<project-root>/
└── 专利工作区/
    └── <中文案件名>/
```

The project root should contain only the user's source materials and the single `专利工作区/` folder created by the workflow.

## Lazy Creation Rule

Each case folder is the `--case-dir` passed to `patent_workflow.py init`. Initialization should create only the case folder and root ledger files:

```text
<case-dir>/
├── manifest.json
├── 00_case_status.md
└── 00_case_events.jsonl
```

Do not pre-create stage, admin, archive, report, output, or tool-run directories. Create only the immediate parent directories needed by the actual file being written.

## User-Facing Outputs

Use one reviewable `输出/` tree:

```text
输出/
├── 过程/
│   └── <中文阶段名>/      # create only when grouping multiple stage files helps
└── 定稿/
```

- `输出/过程/`: disclosure analysis, search memos, strategy notes, interim claims/spec text, review checklists, OA outlines, correction notes.
- `输出/定稿/`: final claims/specification text, DOCX/PDF deliverables, replacement pages, final responses, invalidity/hearing materials, filing-readiness reports, validation reports.

Keep `输出/过程/` flat when there are only one or two process files. Add a numbered Chinese stage folder only when it prevents clutter.

## Machine Records

Use `记录/` only when a machine-readable artifact exists:

```text
记录/
└── <中文阶段名>/
    ├── 报告/      # stage-report JSON, metrics, scan summaries
    └── 工具运行/  # normalized patent-tool-run/v1 JSON
```

Do not mirror every stage into `记录/`; create a stage folder only when that stage actually has a report or tool-run JSON.

## Stage Names

When a stage folder is needed, use these Chinese names:

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

Runtime stage IDs such as `01_disclosure` and `07_qc` remain valid command arguments and manifest keys. They are not directory names for new artifacts.

## Canonical Outputs

Prefer these paths for new drafting cases, creating only the parents for files that actually exist:

```text
输出/过程/01_交底分析/交底分析.md
记录/01_交底分析/报告/disclosure-analysis-stage-report.json
输出/过程/02_现有技术检索/检索纪要A.md
输出/过程/02_现有技术检索/检索纪要B.md
输出/过程/02_现有技术检索/参考文献撰写质量.md
输出/过程/03_方案重构/方案重构备忘录.md
输出/过程/03_方案重构/创造性策略.md
输出/过程/04_权利要求/权利要求当前稿.md
输出/过程/05_说明书/说明书当前稿.md
输出/过程/06_附图/附图说明.md
输出/过程/06_附图/*.svg
输出/定稿/验证报告.md
记录/07_质检/工具运行/*-tool-run.json
输出/定稿/提交清单.md
输出/定稿/申请文件.docx
```

If an old skill expects a legacy path such as `04_claims/outputs/claims-current.md`, keep that old file only as a compatibility copy or register the new Chinese path in `manifest.json`.

## Naming Rules

- Use Chinese directory names for all new folders.
- Use Chinese file names, headings, and main prose for human-readable process files by default.
- Keep machine file names stable when tools already expect them, such as `workflow-validate-tool-run.json`.
- Use short Chinese names for human-facing Markdown, DOCX, PDF, and checklist files.
- Add version suffixes only for competing baselines: `权利要求-v01.md`, `权利要求-v02.md`.
- Keep the active baseline named clearly, such as `权利要求当前稿.md`.
- Register every user-facing output or machine report with `patent_workflow.py add-artifact` or `stage-report`.
