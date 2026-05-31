---
name: patent-method-formula-model
description: "Internal route specialist under patent-cn-draft for formula-heavy, variable-heavy, model-driven, optimization, simulation, objective-function, constraint, or equation-sensitive Chinese method patent drafting. Direct use is allowed only for standalone formula-route revision or older prompts explicitly naming this specialist."
---
# Formula And Model-Driven Method Patent Agent

## New Architecture Role

`patent-cn-draft` is the public drafting orchestrator. This skill is the internal formula/model route specialist and should normally be selected by the orchestrator after file-first classification.

## Skill Position

- 类型：案件类型专科 / formula-model method specialist。
- 中文入口：公式、变量、模型、仿真、优化、目标函数、约束条件、公式敏感 DOCX。
- 上游：应先有交底分析和必要检索；完整撰写由 `patent-cn-draft` 总控。
- 输出：公式保真方案、变量定义、方法步骤、权利要求布局、说明书公式与图例同步。
- 支撑能力：优先使用 `patent-support-docx-math`；可配合 `patent-stage-embodiments`、`patent-stage-invention-content`。
- 边界：仅有少量公式但瓶颈是工艺/实验时，不应选择本路线。

## Overview

Use this skill for formula-heavy and model-driven method patent drafting and revision work. It covers the full path from baseline cleanup and claim layout through background, invention content, detailed embodiments, formula repair, step numbering, and final DOCX QC.

It uses the shared method workflow as its backbone, so the full path also includes disclosure analysis, technical-problem definition, key-technical-means definition, inventive-step judgment, claims, background, invention content, embodiments, figures or flowcharts, and final synchronization. Local materials in this skill should add only formula/model-specific emphasis.

## When To Use

Trigger this skill when the case is driven by formulas, variables, models, simulation outputs, result curves, or mathematically constrained step logic and the user asks to do any of the following:

- review or unify disclosure baselines
- compress or optimize claim layout
- rewrite claim 1 around the inventive technical route
- draft background, invention content, or summary sections
- rewrite the detailed embodiment to follow the claims
- draft or revise embodiments while aligning formulas, figures, figure legends, and comparison labels
- repair formulas, inline math, or patent DOCX structure
- add `S1 / S2.1` style step numbering
- generate or revise method flowcharts

Typical trigger phrases include:

- 方法类案件
- 复杂公式方法案
- 数学模型方法
- 仿真方法
- 优化方法
- 变量约束
- 目标函数
- 敏感度分析
- 参数反演
- 结果曲线
- 权利要求布局
- 权利要求书撰写
- 背景技术
- 技术效果
- 发明内容
- 具体实施方式
- 实施例
- 公式修复
- 附图
- 图例
- 步骤编号

## Shared workflow base

Always use the common full workflow and handoff rules from:

- `../patent-method-runtime-boundary/references/workflow.md`
- `../patent-method-runtime-boundary/references/routing-map.md`
- `../patent-method-runtime-boundary/references/output-contracts.md`
- `../patent-method-runtime-boundary/references/checkpoints.md`

Then read `references/specialization.md` for the formula and model-driven emphasis of this skill.

## Operating Modes

Use one of these three modes:

1. Full workflow mode
   - The user wants the formula/model-driven workflow from the baseline stage onward.
   - Read the shared workflow, shared checkpoints, shared output contracts, and the selected stage file, then apply the local specialization.
2. Single-stage mode
   - The user wants only one stage such as claim layout, invention content, embodiments, figures, or DOCX cleanup.
   - Read the shared routing map, shared output contracts, and the selected stage file, then load local references only as needed.
   - If required prerequisites are missing, state the missing baseline and downstream risk before proceeding.
3. Revision mode
   - The user wants revisions to a previously completed stage.
   - Revise the current stage first.
   - Treat downstream stages as stale until the user confirms whether they should be updated.

## Loading Rules

Always read:

- `../patent-method-runtime-boundary/references/routing-map.md`
- `../patent-method-runtime-boundary/references/output-contracts.md`

Read whenever the user is running multiple stages, asks for a full workflow, or asks how stages fit together:

- `../patent-method-runtime-boundary/references/workflow.md`
- `../patent-method-runtime-boundary/references/checkpoints.md`
- `references/workflow.md`

Read only as needed:

- `references/specialization.md`
  - when formula/model-specific emphasis is needed
- `references/prompts.md`
  - when drafting a stage or reusing a prompt template
- `references/file-handling.md`
  - when modifying `.docx`, repairing formulas, or checking completeness against a base draft

Use bundled scripts from `scripts/` when deterministic OOXML edits are safer than ad hoc manual edits.

## Core Discipline

1. Establish the technical baseline and the wording baseline first.
2. Finalize the claim system before rewriting the detailed embodiment.
3. Keep claims limited to technical solution language, not technical effects.
4. Rewrite the detailed embodiment in claim order, not disclosure order, unless the user explicitly wants otherwise.
5. Preserve every material formula from the baseline; do not flatten formulas to plain text if they should remain Word math objects.
6. When drafting `发明内容`, follow the shared method-style invention-content stage. Make the first effect paragraph explain `feature -> intermediate mechanism/process -> technical consequence`, keep it within the independent-claim scope, and explain step interaction where one step's output becomes the next step's input or basis.
7. Do not directly carry internal disclosure labels such as `方案一/方案二/方案三/方案四`, `问题清单`, `本发明方案`, or inventor-facing notes into the patent text unless they are deliberately redefined in patent-suitable language.
8. Before closing, check formulas, figure references, figure legends, step numbering, variable consistency, and whether every labeled element in the drawings is explained in the text.
9. Prefer this skill when formulas, variable systems, models, or simulation outputs are central to support, clarity, or drafting quality.
10. If the case is instead dominated by raw-material selection, process windows, example ladders, and test-backed process optimization, prefer the process-route skill rather than this one.

## Embodiment Guardrails

When drafting `具体实施方式` or `实施例`:

- Use the claim steps as the backbone. Explain each step in order, then naturally fold dependent-claim features, parameters, formulas, and examples into the relevant step.
- If the user specifies multiple embodiments, keep each embodiment's distinguishing feature clear. If an instruction conflicts with itself, for example one sentence says `双排PTA` but the surrounding request and next clause say `单排PTA`, resolve the conflict from the confirmed case logic and state the correction briefly.
- Avoid small subheadings inside an embodiment when the user asks for natural patent paragraphs. The embodiment may still refer to `S1` to `S7` in prose.
- For each embodiment, explain what the example object is, what figures it uses, how parameters are obtained, how formulas are applied, and how the model output is evaluated.
- Do not introduce a comparison route, parameter source, or formula direction that is absent from the claims or summary. If a disclosure formula conflicts with the adopted/claimed formula, omit the conflicting version and record the reason in the response.

## Figure And Legend Consistency

Treat figures as part of the technical disclosure, not decoration.

- Every figure referenced in the embodiment must be tied to the step or parameter it supports.
- Every important label visible in a figure should be explained in the text, especially ports (`端口`/`波导端口`), boundaries, coordinate axes, sample structures, and result-curve legends.
- If a model figure shows waveguide ports (`波导端口`) or excitation/receiving ports, describe their locations, cross-section orientation, excitation/receiving role, relation to `S21`/`S11`, and that they are simulation boundary settings rather than material-model or area-ratio calculation steps.
- If result figures retain legacy comparison labels, replace internal labels with neutral patent labels and define them before analyzing the curves. Recommended mapping:
  - `实验` -> `实验结果`
  - `方案2` -> `第一对照仿真结果`
  - `方案3` -> `第二对照仿真结果`
  - `方案4` -> `本实施例仿真结果`
- Define the neutral labels in the embodiment. Example pattern: `实验结果` means the measured response curve of the real sample under the corresponding condition; `第一对照仿真结果` and `第二对照仿真结果` are only for comparison and are not required steps of the claimed method; `本实施例仿真结果` is produced by the claimed step chain.
- If a result curve is described as `本实施例仿真结果`, ensure the prose ties it back to the current embodiment's parameter path, such as overall diagnosis -> area-ratio conversion -> material-model parameter -> discrete-geometry simulation.

## Working Pattern

For full-case work:

1. Unify baseline documents and eliminate wording conflicts.
2. Build or compress the claims system.
3. Strengthen the inventive technical route in claim 1.
4. Draft background, invention content, and summary sections.
5. Rewrite the detailed embodiment to track the claims.
6. Normalize drawing labels and comparison-result labels into patent-suitable terms.
7. Repair formulas and inline math objects.
8. Add step labels and flowcharts if helpful.
9. Run a final completeness check against the baseline draft.

For single-stage work:

1. State which current file is the operative baseline.
2. Do the requested stage only.
3. Warn briefly if later sections may now be stale.

## Formula And DOCX QC

For formula-heavy method cases:

- Extract or inspect DOCX with a formula-preserving path. Prefer `patent-support-docx-math` scripts for inspection/extraction and `minimax-docx` or deterministic OOXML edits for writeback.
- After writing, compare the current draft against the claims and technical disclosure for formula completeness. All claim formulas should appear in the detailed embodiment unless the section intentionally defers them elsewhere.
- If formulas from the disclosure are omitted, classify the omission in the response, for example: conflicting with adopted claim formula, image-only duplicate, internal comparison label removed, or purely explanatory arithmetic already incorporated into a larger formula.
- Confirm generated deliverables have native Word math objects, no unexpected embedded objects, no tracked changes/comments in a clean draft, and no accidental plain-text flattening of important formulas.
- Run a final text scan for stale internal terms such as `方案四`, `问题清单`, old figure numbers, and embodiment object confusion such as `单排`/`双排` mismatch.

## Scripts

Bundled scripts are available for:

- file inventory
- paragraph patching
- section copying between DOCX files
- inline math patching
- step label insertion
- formula completeness audit

Read `references/file-handling.md` before using them.

## References

- `../patent-method-runtime-boundary/references/workflow.md`
- `../patent-method-runtime-boundary/references/routing-map.md`
- `../patent-method-runtime-boundary/references/output-contracts.md`
- `../patent-method-runtime-boundary/references/checkpoints.md`
- `../patent-method-runtime-boundary/references/stages/01-disclosure-analysis.md`
- `../patent-method-runtime-boundary/references/stages/02-disclosure-reconstruction.md`
- `../patent-method-runtime-boundary/references/stages/03-method-boundary-alignment.md`
- `../patent-method-runtime-boundary/references/stages/04-core-feature-analysis.md`
- `../patent-method-runtime-boundary/references/stages/05-inventive-step-analysis.md`
- `../patent-method-runtime-boundary/references/stages/06-final-disclosure.md`
- `../patent-method-runtime-boundary/references/stages/07-claim-layout.md`
- `../patent-method-runtime-boundary/references/stages/08-claims-drafting.md`
- `../patent-method-runtime-boundary/references/stages/09-background-drafting.md`
- `../patent-method-runtime-boundary/references/stages/10-invention-content-drafting.md`
- `../patent-method-runtime-boundary/references/stages/11-embodiments-and-examples.md`
- `../patent-method-runtime-boundary/references/stages/12-figures-flowcharts-and-legends.md`
- `../patent-method-runtime-boundary/references/stages/13-formulas-and-docx-cleanup.md`
- `../patent-method-runtime-boundary/references/stages/14-testing-design.md`
- `../patent-method-runtime-boundary/references/stages/15-results-analysis.md`
- `../patent-method-runtime-boundary/references/stages/16-abstract-and-final-synchronization.md`
- `references/workflow.md`
- `references/specialization.md`
- `references/prompts.md`
- `references/file-handling.md`
