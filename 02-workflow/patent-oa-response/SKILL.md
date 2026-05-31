---
name: "patent-oa-response"
description: "Use for Chinese patent office-action response work when the user wants the full OA workflow or any single stage such as case baseline, office-action breakdown, D1 check, Dx check, claim amendment decision, inventive-step synthesis, amended drafting, unamended drafting, replacement-page generation, or QC. Trigger this one skill even when the user asks only for D1核查, D2/D3核查, 是否改权, 修改后答复, 不修改答复, 审查意见拆解, 创造性主线, or 审查意见答复 QC."
---

# Patent OA Response

## Public entry rule

This is the only public skill for the CN OA response workflow. If the user asks only for one stage such as 审查意见拆解, D1 核查, 是否修改权利要求, 正式答复起草, or QC, stay inside this skill and route internally. Do not call the former stage-specific OA skills as separate public skills.

## Operating modes

Use one of these modes:

1. Full workflow mode
   - The user wants the OA response from intake through QC.
   - Read `references/routing-map.md`, `references/core/invariants.md`, `references/core/state-model.md`, `references/core/output-contract.md`, `references/workflow.md`, `references/core/checkpoints.md`, and the selected stage file.
   - Read `references/checks/seven-rule-check.md` for inventive-step or QC work.
   - Read `references/rendering/docx-templates.md` when `.docx` output or replacement pages are required.
2. Single-stage mode
   - The user wants only one stage such as D1 check or amended drafting.
   - Read `references/routing-map.md`, `references/core/invariants.md`, `references/core/state-model.md`, `references/core/output-contract.md`, and the selected stage file.
   - Read `references/core/checkpoints.md` for any strategic judgment stage.
   - Read `references/checks/seven-rule-check.md` for inventive-step or QC work.
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

If the office action file is available and the cited comparison PDFs or the original application's published PDF are missing from the case folder, first run [$download-google-patents-pdfs](../download-google-patents-pdfs/SKILL.md). Treat this as an automatic preparation step, not a separate user-confirmed action.

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

- `references/checks/seven-rule-check.md` for inventive-step or QC work
- `references/rendering/docx-templates.md` when `.docx` output or replacement pages are needed

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
