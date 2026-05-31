---
name: patent-cn-review
description: "Public orchestrator for reviewing Chinese patent application drafts and filing packages. Use for 成稿审查、形式检查、DOCX/公式/修订痕迹检查、权利要求引用、附图标记、一致性、摘要字数、附图说明、最终 validation report. Dispatches internal QC and document specialists."
---
# CN Patent Review Orchestrator

## Role

This is the user-facing review and QC orchestrator for Chinese patent application drafts.

Use it when the user asks:

- “检查这套申请文件”
- “最终质检”
- “看 DOCX 有没有问题”
- “检查标号、引用关系、附图说明、摘要字数”
- “判断是否可以进入提交包”

## Startup

Always read:

- [references/review-workflow-graph.md](references/review-workflow-graph.md)
- [$patent-cn/references/internal-specialists.md](/Users/chrynos/.codex/skills/patent-cn/references/internal-specialists.md)

Use these internal specialists as needed:

- [$patent-cn-runtime](/Users/chrynos/.codex/skills/patent-cn-runtime/SKILL.md)
- [$patent-support-docx-math](/Users/chrynos/.codex/skills/patent-support-docx-math/SKILL.md)
- [$patent-qc-cn-formality](/Users/chrynos/.codex/skills/patent-qc-cn-formality/SKILL.md)
- [$patent-qc-application-consistency](/Users/chrynos/.codex/skills/patent-qc-application-consistency/SKILL.md)
- [$patent-entry-drafting](/Users/chrynos/.codex/skills/patent-entry-drafting/SKILL.md) only for runtime validation commands

## Runtime Rule

If the draft belongs to a case folder, write normalized tool JSON under `记录/07_质检/工具运行/`, human-readable QC reports under `输出/过程/07_质检/` or `输出/定稿/`, and register them with `patent_workflow.py add-artifact`. Create those folders only when writing the corresponding file.

Recommended first-pass commands:

```bash
python3 /Users/chrynos/.codex/skills/patent-cn-runtime/scripts/patent_tool_runner.py run qc.micro \
  --case-dir <case-dir> \
  --input <draft-file> \
  --result-output <case-dir>/记录/07_质检/工具运行/micro-qc-tool-run.json
```

```bash
python3 /Users/chrynos/.codex/skills/patent-cn-runtime/scripts/patent_tool_runner.py run workflow.validate \
  --case-dir <case-dir> \
  --result-output <case-dir>/记录/07_质检/工具运行/workflow-validate-tool-run.json
```

## DOCX Delivery QC

When a review task changes content but should keep the source formatting and structure, add a style-invariance proof before delivery:

1. Run the normal gates: `unzip -t`, `qc.cn_formality.scan`, `qc.micro`, and `minimax-docx validate --business`.
2. Run DOCX diff and record the headline counts, especially `paragraphs changed`, `styles modified`, and `structural changes`.
3. Compare key DOCX package parts with the runtime style-invariance tool. Store the raw JSON in `记录/07_质检/工具运行/`.

```bash
python3 /Users/chrynos/.codex/skills/patent-cn-runtime/scripts/patent_tool_runner.py run docx.style_invariance \
  --case-dir <case-dir> \
  --input <source-docx> \
  --output <revised-docx> \
  --result-output <case-dir>/记录/07_质检/工具运行/docx-style-invariance-tool-run.json
```

The proof should show key style/theme parts unchanged, no core structural-count drift, page-break counts unchanged, and no large run-count drop. A missing page break is a confirmed delivery blocker unless the user explicitly requested pagination changes. A run-count drop greater than 20% is a suspected run-flattening warning and must be investigated before delivery.

## Output Protocol

Return:

```text
CN REVIEW REPORT
- file/package checked: <path>
- overall status: <pass|needs-fix|blocked>
- drafting status: <drafting-complete|blocked|unknown>
- filing status: <filing-ready|not-ready|unknown>
- confirmed issues: <count>
- suspected issues: <count>
- auto-fix candidates: <count>
- required next action: <one sentence>
```

Group findings as:

- confirmed defects
- suspected issues requiring human review
- safe auto-fix candidates
- filing-package blockers

Do not call a package `filing-ready` unless validation has no hard or soft fail.
