---
name: patent-entry-oa-response
description: "Internal OA-response workflow engine under patent-cn-response for Chinese patent office-action response work. Direct use is allowed for compatibility or explicit OA-specific prompts involving office-action response, D1/Dx check, distinguishing-feature analysis, claim amendment, inventive-step argument, replacement pages, or response QC. Do not use for new application drafting from a raw disclosure."
---
# Patent OA Response

## New Architecture Role

`patent-cn-response` is the preferred public response orchestrator. This skill is the internal OA-response workflow engine. Direct use is appropriate only for older prompts that explicitly name this skill or for narrowly scoped OA-response work where no higher-level routing is needed.

## Skill Position

- 类型：审查意见答复内部工作流 / OA response workflow engine。
- 中文入口包括审查意见通知书和 D1/Dx 核查；也包括创造性答复、是否改权以及替换页工作。
- 主链条：案件基线 -> 审查意见拆解 -> 对比文件核查 -> 修改策略 -> 创造性主线 -> 答复文本 -> 替换页/QC。
- 常用下游/支撑：
  - `patent-analysis-fixed-patent`
  - `patent-support-google-patents-pdfs`
  - `patent-support-correction-docx`
  - `patent-qc-application-consistency`
  - `patent-support-docx-math`
  - `doc`
  - `pdf`
- 边界：不作为新申请撰写入口；如果只是从交底开始写申请，转 `patent-cn-draft`。

## Overview

This is now the OA-response workflow engine behind the public `patent-cn-response` orchestrator.

Preferred public entrances:

- mixed patent routing: `patent-cn`
- new application drafting: `patent-cn-draft`
- application/final package review: `patent-cn-review`
- OA, correction, and invalidity response work: `patent-cn-response`

## Internal Routing Rule

When `patent-cn-response` selects the OA path, stay inside this skill and route internally. If the user asks only for one OA stage such as 审查意见拆解, D1 核查, 是否修改权利要求, 正式答复起草, or QC, keep the stage work here rather than exposing former stage-specific OA skills as user-facing entries.

## Operating modes

Use one of these modes:

1. Full workflow mode
   - The user wants the OA response from intake through QC.
   - Read `references/routing-map.md`, `references/core/invariants.md`, `references/core/state-model.md`, `references/core/output-contract.md`, `references/workflow.md`, `references/core/checkpoints.md`, and the selected stage file.
   - Read `references/checks/seven-rule-check.md` for inventive-step, amendment strategy with Article 22.3 impact, drafting, or QC work.
   - Read `references/rendering/docx-templates.md` when `.docx` output or replacement pages are required.
2. Single-stage mode
   - The user wants only one stage such as D1 check or amended drafting.
   - Read `references/routing-map.md`, `references/core/invariants.md`, `references/core/state-model.md`, `references/core/output-contract.md`, and the selected stage file.
   - Read `references/core/checkpoints.md` for any strategic judgment stage.
   - Read `references/checks/seven-rule-check.md` for inventive-step, amendment strategy with Article 22.3 impact, drafting, or QC work.
   - Read `references/rendering/docx-templates.md` when `.docx` output or replacement pages are required.
   - If prerequisites are missing, state the missing baseline and risk before proceeding.
3. Drafting-only or QC-only mode
   - The user already has the analysis baseline and wants formal drafting or final QC.
   - Confirm that the effective claim set, distinguishing features, and technical problem baseline are fixed before drafting.
   - Read `references/core/checkpoints.md` to confirm which judgments still need user confirmation before the draft is treated as final.

## Preflight inputs

- office action text
- current application files
- cited prior-art documents if available
- any user constraint on amendment strategy, template use, or response style

If the office action file is available and the cited comparison PDFs or the original application's published PDF are missing from the case folder, first run [$patent-support-google-patents-pdfs](../patent-support-google-patents-pdfs/SKILL.md). Treat this as an automatic preparation step, not a separate user-confirmed action.

## Case Folder Layout

When the case folder comes from `oa-office-action-response`, keep the OA response workflow in the same shallow layout:

```text
<case-folder>/
  01-审查意见/
  02-申请文件/
  03-既往答复/
  04-对比文件/
  05-处理结果/
  06-提交文件/
  记录/
```

- Read the current official notice from `01-审查意见`.
- Read the original application files from `02-申请文件`.
- For a second or later office action, read earlier statements and replacement pages from `03-既往答复`; they may define the current effective claims or specification.
- Save downloaded D1/Dx PDFs in `04-对比文件`.
- Save human-readable extraction, analysis, and stage summaries in `05-处理结果`.
- Save the final 意见陈述 DOCX and replacement-page DOCX files in `06-提交文件`.
- Save stage-report JSON, tool logs, render checks, and other machine traces under `记录/`.

Do not create new legacy `source/`, `work/`, `filing/`, `checks/`, or `oa/` folders. If a legacy case already has them, read those files for compatibility, then write new outputs to the shallow layout.

## Loading rule

Always read:

- `references/routing-map.md`
- `references/core/invariants.md`
- `references/core/state-model.md`
- `references/core/output-contract.md`

Then read only the stage file needed for the current request from `references/stages/`.

Read these whenever the work involves the full workflow or any strategic judgment:

- `references/workflow.md`
- `references/core/checkpoints.md`

Read these when applicable:

- `references/checks/seven-rule-check.md` for inventive-step, amendment strategy with Article 22.3 impact, drafting, or QC work
- `references/rendering/docx-templates.md` when `.docx` output or replacement pages are needed

## Mandatory Opinion-Statement Template Rule

When producing a formal OA 意见陈述 `.docx`, using the correct 意见陈述 template is mandatory.

- If the user, case folder, or local workspace provides an 意见陈述 template, use that file first.
- Known local templates are:
  - `/Users/chrynos/Library/CloudStorage/OneDrive-个人/工作/工作文档/审查意见/意见陈述-有修改.docx`
  - `/Users/chrynos/Library/CloudStorage/OneDrive-个人/工作/工作文档/审查意见/意见陈述-无修改.docx`
- Use `意见陈述-有修改.docx` for an amended OA response and `意见陈述-无修改.docx` for an unamended response.
- Copy the selected template as the working DOCX and fill that copy. Do not create a new DOCX from scratch, and do not only imitate the template's look.
- Preserve the template's section settings, style definitions, numbering definitions, title/salutation skeleton, amendment heading, inventive-step heading, dependent-claim heading, and closing skeleton unless a case-specific correction is necessary.

## Working discipline

- Keep the current effective claim set as the state anchor for all later strategic judgments.
- Treat the preliminary current-claim-1-vs-D1 difference snapshot as amendment-decision input only, not as the final distinguishing-feature set.
- Stop at each confirmation checkpoint before fixing strategic conclusions in the live case state.
- Prefer stable intermediate deliverables before formal drafting.

## References

- `references/routing-map.md`
- `references/workflow.md`
- `references/core/invariants.md`
- `references/core/state-model.md`
- `references/core/checkpoints.md`
- `references/core/output-contract.md`
- `references/checks/seven-rule-check.md`
- `references/rendering/docx-templates.md`
- `references/stages/01-case-baseline.md`
- `references/stages/02-review-breakdown.md`
- `references/stages/03-d1-check.md`
- `references/stages/04-dx-check.md`
- `references/stages/05-claim-amendment.md`
- `references/stages/06-inventive-step.md`
- `references/stages/07-draft-amended.md`
- `references/stages/08-draft-unamended.md`
- `references/stages/09-qc.md`
