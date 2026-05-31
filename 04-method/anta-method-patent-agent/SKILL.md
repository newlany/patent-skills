---
name: "anta-method-patent-agent"
description: "Use for Anta method patent cases when the user wants the full drafting workflow or any single Anta stage such as disclosure analysis, disclosure reconstruction, core feature analysis, inventive-step analysis, final disclosure, claim layout, claims drafting, background drafting, technical-effects drafting, process-detail drafting, examples design, testing design, or results analysis. Trigger this one skill even when the user names a stage number like stage 3 or stage 8, or asks only for one Anta deliverable such as 背景技术, 权利要求布局, 实施例设计, 测试设计, or 结果分析."
---

# Anta Method Patent Agent

## Scope

Use this skill only for Anta method patent cases. Do not use it for non-Anta matters, device cases, office-action responses, invalidation matters, or general patent drafting unless the user explicitly says to reuse this Anta method workflow.

## Public entry rule

This is the only public Anta workflow skill. If the user asks for any Anta stage by name, by stage number, or by deliverable, stay inside this skill and route internally. Do not rely on the former stage-specific Anta skills as public entry points.

## Trigger phrases

- Full workflow:
  - Anta method case
  - 安踏方法
  - full Anta drafting workflow
  - 从披露分析一路做到结果分析
- Single-stage examples:
  - disclosure analysis
  - disclosure reconstruction
  - core feature analysis
  - inventive-step analysis
  - final disclosure
  - claim layout
  - claims drafting
  - background drafting
  - technical-effects drafting
  - process-detail drafting
  - examples design
  - testing design
  - results analysis
  - 第1阶段 / 第8阶段 / 第11阶段
  - 背景技术
  - 权利要求布局
  - 权利要求书撰写
  - 工艺细化
  - 实施例设计
  - 测试设计
  - 结果分析

## Operating modes

Use one of these three modes:

1. Full workflow mode
   - The user wants the Anta workflow from stage 1 onward.
   - Read `references/workflow.md`, `references/checkpoints.md`, `references/output-contracts.md`, and the selected stage file.
2. Single-stage mode
   - The user wants only one stage such as stage 8 background drafting.
   - Read `references/routing-map.md`, `references/output-contracts.md`, and the selected stage file.
   - If required prerequisites are missing, state the missing baseline and downstream risk before proceeding.
3. Revision mode
   - The user wants revisions to a previously completed stage.
   - Revise the current stage first.
   - Treat downstream stages as stale until the user confirms whether they should be updated.

## Stage loading rule

Always read:

- `references/routing-map.md`
- `references/output-contracts.md`

Then read only the stage file needed for the current request from `references/stages/`.

Read `references/workflow.md` and `references/checkpoints.md` whenever the user is running multiple stages or asks how the workflow fits together.

## Workflow discipline

1. This workflow is only for Anta method patent cases.
2. Each later stage must use the earlier user-confirmed stage as its baseline.
3. Default to one stage at a time, with a stop for user confirmation after each stage.
4. If the user names a later stage directly, do not force the full workflow, but do state any missing prerequisite baseline and risk.
5. Do not draft claims before the final disclosure and feature analysis are fixed.
6. Do not draft examples before the process-detail section is fixed.
7. Do not draft results analysis before the retained result tables are fixed.
8. Keep the entire application on one consistent technical main line.
9. Do not call the former stage-specific Anta skills as separate public skills; those stages are now internalized in this skill's references.

## Stage handoff rule

After each completed stage, present:

1. the completed deliverable
2. key assumptions or unresolved points
3. the recommended next stage
4. a direct request for user confirmation

Do not silently continue to the next stage unless the user explicitly asks for uninterrupted execution.

## References

- `references/workflow.md`
- `references/routing-map.md`
- `references/output-contracts.md`
- `references/checkpoints.md`
- `references/file-naming.md`
- `references/stages/01-disclosure-analysis.md`
- `references/stages/02-disclosure-reconstruction.md`
- `references/stages/03-core-feature-analysis.md`
- `references/stages/04-inventive-step-analysis.md`
- `references/stages/05-final-disclosure.md`
- `references/stages/06-claim-layout.md`
- `references/stages/07-claims-drafting.md`
- `references/stages/08-background-drafting.md`
- `references/stages/09-effects-drafting.md`
- `references/stages/10-process-detail-drafting.md`
- `references/stages/11-examples-design.md`
- `references/stages/12-testing-design.md`
- `references/stages/13-results-analysis.md`
