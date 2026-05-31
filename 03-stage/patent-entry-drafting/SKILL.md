---
name: patent-entry-drafting
description: "Internal drafting engine and compatibility entry for Chinese patent application preparation. Prefer patent-cn-draft as the public orchestrator. Use this for older prompts or internal routing from disclosure-to-application drafting workflows: 交底分析、查新、方案重构、权利要求书、说明书撰写."
---
# Patent Drafting Router Agent

## New Architecture Note

`patent-cn-draft` is now the preferred public drafting orchestrator. This skill remains the internal drafting engine and compatibility entry. It should still own route-specific drafting logic, but ordinary users should not need to call it directly.

## Skill Position

- 类型：专利申请撰写内部引擎与兼容入口 / drafting engine and compatibility entry。
- 中文入口：从交底书到申请文件，例如“用撰写流程处理这个交底”“先查新再重构再写权利要求”。
- 主链条：交底读取 -> 交底分析 -> 首轮检索 -> 技术方案重构 -> 复检 -> 创造性判断 -> 权利要求 -> 说明书 -> QC。
- 下游阶段：`patent-stage-disclosure-analysis`、`patent-stage-prior-art-search`、`patent-method-route-helper`、`patent-method-process-route`、`patent-method-formula-model`、`patent-method-runtime-boundary`、`patent-stage-invention-content`、`patent-stage-embodiments`。
- 类型分流：材料制备/配方/工艺方法转 `patent-method-process-route`；控制/识别/匹配/闭环方法转 `patent-method-runtime-boundary`；公式/模型/仿真方法转 `patent-method-formula-model`；材料产品、组合物、层状结构、装置或产品结构暂留在本 skill 的 structural/device/product/material-structure 路线。
- 支撑能力：可调用 `patent-support-docx-math`、`read-chinese-files`、`doc`、`minimax-docx`、`pdf`、`spreadsheet` 等读取和输出工具。
- 边界：不处理 OA 答复、无效、补正-only、单纯格式处理或纯专题研究。

## Overview

This is the internal drafting engine behind the public `patent-cn-draft` orchestrator and a compatibility entry for older prompts.

Use this one skill whenever the task is to move from technical disclosure to drafting-ready patent text, regardless of whether the case turns out to be:

- a process or preparation-heavy method case
- a formula or model-driven method case
- a general runtime-chain or boundary-driven method case
- a structural, device, product, or material-structure case

The user should not need to remember the downstream specialist skills. However, ordinary new drafting work should start from `patent-cn-draft`; route OA response, invalidity, correction-only, pure research, and document-only tasks to their dedicated public orchestrators.

## Internal Engine Rule

For disclosure-to-application drafting work, `patent-cn-draft` should call this engine rather than exposing lower-level specialists such as:

- `patent-entry-router`
- `patent-stage-disclosure-analysis`
- `patent-method-route-helper`
- `patent-method-process-route`
- `patent-method-formula-model`

Those remain available as internal route targets or compatibility paths, but `patent-cn-draft` is the public drafting front door.

## Mandatory Drafting Chain

Unless the user clearly limits the scope, use this chain:

1. disclosure intake and file-first reading
2. disclosure analysis
3. prior-art Checkpoint A
4. technical-solution reconstruction
5. route-specific drafting baseline cleanup
6. prior-art Checkpoint B
7. inventive-step judgment
8. final disclosure or drafting baseline
9. claims
10. background
11. invention content
12. embodiments and examples
13. figures, tables, or DOCX cleanup when needed

Do not jump from raw disclosure directly to claims.

## Case State Rule

For any multi-stage drafting task, initialize and maintain a case folder using:

```bash
python3 scripts/patent_workflow.py init --case-dir <case-dir> --title "<case-title>" --source <source-file-or-label>
```

The workflow uses the public Chinese lazy layout: create the case under `专利工作区/<中文案件名>` when no case folder exists; do not pre-create stage or archive folders; put human process files under `输出/过程/`, final files under `输出/定稿/`, and machine JSON under `记录/<中文阶段名>/报告/` or `记录/<中文阶段名>/工具运行/`. Human-readable process files should use Chinese file names, headings, and main prose by default.

Read [references/case-manifest-and-validation.md](references/case-manifest-and-validation.md) whenever the task involves a full drafting workflow, a handoff between stages, final QC, or a filing package.

If the user asks to run the workflow continuously or produce a full first pass without stopping, read [references/autonomous-mode.md](references/autonomous-mode.md) and initialize or switch the case to `autonomous`. The default remains `guided`.

When the task reaches final package, filing-channel assumptions, or procedural formality questions, read [references/cn-procedural-reference.md](references/cn-procedural-reference.md) and verify current official sources before stating procedural requirements.

After each stage, register the main deliverable with `scripts/patent_workflow.py add-artifact`. Before calling the case complete, run `scripts/patent_workflow.py validate` and use its two-state result:

- `drafting-complete`: draft artifacts are complete and no hard fail remains.
- `filing-ready`: final DOCX/package artifacts are present and no hard or soft fail remains.

Do not describe a case as filing-ready merely because the text draft is complete.

For long-running workflows, record stage events and metrics:

```bash
python3 scripts/patent_workflow.py stage-start --case-dir <case-dir> --stage 01_disclosure --json
python3 scripts/patent_workflow.py log-event --case-dir <case-dir> --event script-run --stage 01_disclosure --script extract_disclosure_text.py --json
python3 scripts/patent_workflow.py stage-report --case-dir <case-dir> --stage 01_disclosure --name disclosure-analysis --status completed --json
python3 scripts/patent_workflow.py stage-end --case-dir <case-dir> --stage 01_disclosure --status completed --json
```

The event log is stored as `00_case_events.jsonl`, stage reports use `patent-stage-report/v1`, and validation reports include both stage-report and workflow-metrics summaries.

For environment checks, use:

```bash
python3 scripts/patent_workflow.py doctor --json
```

For deterministic first-pass QC before specialist review, use:

```bash
python3 scripts/patent_qc_micro.py check <draft-file> --json --output <case-dir>/记录/07_质检/报告/micro-qc.json
```

## Startup Rule

Always read:

- [references/route-families.md](references/route-families.md)

When the work reaches inventive-step judgment, claim-scope strategy, or rights-claim drafting/revision, also read:

- [references/problem-based-inventive-claim-drafting.md](references/problem-based-inventive-claim-drafting.md)

When the work reaches embodiment drafting or revision for a structural, device, assembly, product, component-relation, or layered-structure case, also read:

- [$patent-cn-draft/references/structural-embodiment-drafting.md](/Users/chrynos/.codex/skills/patent-cn-draft/references/structural-embodiment-drafting.md)

Then use these companion skills as needed:

- [$patent-stage-disclosure-analysis](/Users/chrynos/.codex/skills/patent-stage-disclosure-analysis/SKILL.md) for disclosure analysis
- [$patent-stage-prior-art-search](/Users/chrynos/.codex/skills/patent-stage-prior-art-search/SKILL.md) for Checkpoint A and Checkpoint B
- [$patent-method-process-route](/Users/chrynos/.codex/skills/patent-method-process-route/SKILL.md) for process-route or preparation-heavy method cases
- [$patent-method-formula-model](/Users/chrynos/.codex/skills/patent-method-formula-model/SKILL.md) for formula or model-driven method cases
- [$patent-method-runtime-boundary](/Users/chrynos/.codex/skills/patent-method-runtime-boundary/SKILL.md) for general runtime-chain or boundary-driven method cases
- [$patent-stage-invention-content](/Users/chrynos/.codex/skills/patent-stage-invention-content/SKILL.md) when section-only invention-content drafting support is useful
- [$patent-support-docx-math](/Users/chrynos/.codex/skills/patent-support-docx-math/SKILL.md) when DOCX formulas, tracked changes, or layout-sensitive files matter
- [$patent-qc-application-consistency](/Users/chrynos/.codex/skills/patent-qc-application-consistency/SKILL.md) for numerals, consistency, and drafting cleanup

## File-First Classification Rule

Always read the disclosure content before choosing the route.

Do not classify only from:

- applicant name
- project folder
- user shorthand
- file title

Treat user hints such as `安踏`, `厦大`, `宏发`, or `科华` as supporting signals only, unless the user explicitly instructs otherwise.

## Route Selection Rule

Classify by the hardest part to draft correctly.

Use one of these route outcomes:

1. structural or device route
   - default route when no method family clearly dominates
   - stay inside this skill for the common drafting chain and use utilities as needed
2. process-route or preparation-heavy method route
   - hand off into `patent-method-process-route`
3. formula or model-driven method route
   - hand off into `patent-method-formula-model`
4. general runtime-chain or boundary-driven method route
   - hand off into `patent-method-runtime-boundary`

If the user explicitly says `安踏` and also says the case needs `方案重构`, treat that as a strong signal that reconstruction and art-aware narrowing are mandatory. Still confirm from the file whether the technical burden is truly process-route-heavy before choosing the Anta route.

## Uncertainty Rule

Use these confidence levels:

- high confidence: one route clearly dominates
- medium confidence: mixed signals, but one route still controls the next drafting step
- low confidence: two or more routes would lead to materially different next steps

If confidence is high or medium, route automatically and continue.

If confidence is low, stop and ask the user before going further. In that stop message, include:

1. the two or three plausible routes
2. why each route is plausible from the disclosure
3. which underlying skill each route would use
4. what downstream difference makes the choice matter

Do not silently choose a low-confidence route.

## Output Protocol

When this skill routes a case, state:

```text
DRAFT ROUTE
- selected route: <route>
- confidence: <high|medium|low>
- underlying workflow: <skill or internal route>
- companions: <skill-1>, <skill-2>
- chain: disclosure analysis -> Checkpoint A -> reconstruction -> Checkpoint B -> inventive-step -> drafting
```

Then continue with the chosen workflow instead of stopping at classification, unless the route confidence is low.

## Boundaries

- This is for drafting work, not OA response.
- This is for drafting work, not invalidity analysis or response.
- If the user only wants prior-art search and not drafting, `patent-stage-prior-art-search` may be used directly.
