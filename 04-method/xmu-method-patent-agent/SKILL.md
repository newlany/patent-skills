---
name: xmu-method-patent-agent
description: Use when drafting or revising XMU method-type patent cases, especially requests mentioning 厦大方法案, 方法类案件, 权利要求布局, 权利要求书撰写, 背景技术, 技术效果, 发明内容, 具体实施方式, 实施例, 公式修复, 附图/图例一致性, 步骤编号, 流程图, or DOCX cleanup for method cases containing formulas.
---

# XMU Method Patent Agent

## Overview

Use this skill for XMU method-type patent drafting and revision work. It covers the full path from baseline cleanup and claim layout through background, effects, detailed embodiments, formula repair, step numbering, and final DOCX QC.

## When To Use

Trigger this skill when the user asks to do any of the following for an XMU method case:

- review or unify disclosure baselines
- compress or optimize claim layout
- rewrite claim 1 around the inventive technical route
- draft background, effects, or summary sections
- rewrite the detailed embodiment to follow the claims
- draft or revise embodiments while aligning formulas, figures, figure legends, and comparison labels
- repair formulas, inline math, or patent DOCX structure
- add `S1 / S2.1` style step numbering
- generate or revise method flowcharts

Typical trigger phrases include:

- 厦大方法案
- 方法类案件
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

## Loading Rules

Always read:

- `references/workflow.md`

Read only as needed:

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
6. In effects drafting, explain the difference from traditional methods, why the difference is not obvious, and why it produces stronger technical effects.
7. Do not directly carry internal disclosure labels such as `方案一/方案二/方案三/方案四`, `问题清单`, `本发明方案`, or inventor-facing notes into the patent text unless they are deliberately redefined in patent-suitable language.
8. Before closing, check formulas, figure references, figure legends, step numbering, variable consistency, and whether every labeled element in the drawings is explained in the text.

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
4. Draft background, summary, and effects.
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

- Extract or inspect DOCX with a formula-preserving path. Prefer `patent-docx-math` scripts for inspection/extraction and `minimax-docx` or deterministic OOXML edits for writeback.
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
