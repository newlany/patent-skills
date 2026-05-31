---
name: patent-method-boundary-alignment
description: "Utility specialist for Chinese method-patent boundary alignment. Use when claims/specification must distinguish runtime method steps from preconditions, offline preparation, existing libraries/models/rule bases/calibration data, or later updates, and synchronize claims, invention content, embodiments, abstract, and flowcharts."
---
# CN Method Patent Boundary Alignment

## Skill Position

- 类型：方法边界校准工具 / method-boundary utility。
- 中文入口：方法步骤边界不清、前置数据/模型/规则库是否写入方法步骤、流程图和权利要求不同步。
- 输入：已有权利要求、发明内容、实施方式、流程图或重构方案。
- 输出：边界调整建议和跨章节同步文本。
- 支撑能力：可配合 `patent-method-runtime-boundary`、`patent-stage-invention-content`、`patent-stage-embodiments`。
- 边界：不作为完整撰写公共入口；只解决方法边界与同步问题。

## Scope

Use this skill for general Chinese method patent cases in which the invention is an execution route, but the disclosure also contains supporting resources that may exist before the method runs, such as historical sample sets, reference libraries, rule bases, trained models, calibration relationships, parameter tables, templates, prior records, or accumulated experience data.

This is a general drafting skill. Do not treat it as a company-specific or institution-specific workflow unless the user explicitly asks to use such a workflow.

## Trigger Phrases

- 方法类案件
- 方法边界
- 前置步骤
- 建库是否写入权利要求
- 标定是否属于方法步骤
- 主权重写
- 整稿同步
- 发明内容和实施例一起改
- 流程图重画
- 摘要同步
- 全文重写

## Core Principle

Before drafting, classify every candidate operation into one of three buckets:

1. pre-established support
2. runtime method step
3. post-run update or optional iteration

Only the runtime chain belongs in the independent method claim unless the disclosure and drafting strategy clearly support broader protection.

## Boundary Test

A candidate operation belongs in the independent method claim only if it satisfies all of the following:

- it is executed when the claimed method runs on the current target object or current batch
- it directly processes the current object, current image, current signal, current data, or current decision state
- its output is used by the next runtime step in the claimed chain
- removing it would change the operative technical route of the current method run, not merely the origin of a supporting basis

If any of the above is missing, do not place that operation in the main step chain by default. Recast it as one of the following:

- a pre-established support used by a runtime step
- a dependent claim feature describing how the support is organized
- an embodiment opening paragraph describing what already exists before execution
- a post-run update step kept outside claim 1 or placed in a dependent claim if needed

## Supporting Resource Rule

When a support resource appears in claim 1, its runtime function must be explicit in the same step or in the immediately following clause.

Typical compliant pattern:

- `基于......建立的X，用于......`
- `从基于......建立的X中匹配......`
- `基于X对当前步骤中的特征/参数/位置进行......`

Typical non-compliant pattern:

- first recite that a library/model/database is built
- later use it without saying what that earlier limitation is doing in the method chain

The point is not merely to mention the support resource. The claim must show why that resource is part of the operative route of the current method run.

## Claim Drafting Workflow

1. Fix the operative method boundary first.
2. Redraw the independent claim around the runtime chain only.
3. If a pre-established support is necessary to the route, fold it into the runtime step that calls it instead of drafting a standalone build step by default.
4. After resetting the chain, renumber every step and update all dependent-claim references.
5. Use dependent claims to hold:
   - support-resource organization
   - support-resource matching dimensions
   - pre-processing details
   - qualification or routing rules
   - output parameter structures
   - coordinate or mapping conversion details
   - recheck, rework, or fallback branches
   - update or write-back mechanisms

## Claim Guardrails

- Do not let claim 1 narrate historical accumulation as though it occurs every time the method executes, unless the disclosure truly defines that as part of each run.
- If a support resource is built from prior samples, prior records, or prior repair results, use that history to define the basis of the resource, then place the actual call to the resource inside the runtime step.
- Do not move technical effects into the claim as substitutes for missing technical steps.
- Do not let the independent claim solve a problem that actually depends on an unclaimed later update mechanism.

## Invention Content Alignment

After the claim boundary is fixed, rewrite `发明内容` to the same boundary.

Required moves:

1. Keep the purpose paragraph aligned to the defect solved by the runtime chain.
2. If the prior art already has a known upstream route, acknowledge that route fairly before `申请人发现`.
3. Make the `申请人发现` paragraph explain why the defect arises in actual use, not merely repeat the defect.
4. Draft the main solution paragraph in claim order.
5. In the first effect paragraph, explain how information, position, state, parameter, or decision results are passed from one runtime step to the next.
6. Do not attribute the main inventive effect to preconditions or post-run updates that are not part of claim 1.

Preferred-feature paragraphs may still cover support-resource structure, fallback logic, or update logic, but each paragraph must stay aligned with the relevant dependent feature.

## Embodiment Workflow

For `具体实施方式` or `实施例`, use this order unless the user instructs otherwise:

1. state that the embodiment relates to the method
2. state the application scene
3. state which supporting resources, devices, data, or mappings are already available before execution
4. list the runtime steps
5. explain the runtime steps in order
6. integrate dependent features into the relevant step explanations
7. end with one concrete running example

## Embodiment Rules

- The embodiment opening should clearly separate preconditions from method steps.
- Do not reintroduce a pre-established support as though it were a runtime step after claim 1 has already been narrowed.
- Explain every step as an executable route: input, operation, condition, and output for the next step.
- Define custom terms where they first appear. Prefer direct sentence forms such as `其中，X是指......`.
- If the user wants natural patent prose, avoid claim-like repetition and avoid unnecessary `所述` inside the embodiment.
- The final concrete example should show how the pre-established support is called during execution, not how it was historically accumulated.

## Figures And Abstract

Method cases do not automatically require product or equipment figures.

Default figure planning rule:

- if the inventive point is the runtime method chain, start from a flowchart
- add structural or equipment figures only when they are truly needed to explain a claimed step or a term that cannot be understood from the prose alone

If the method boundary has been reset, update these materials together:

- flowchart
- figure legend
- abstract
- abstract figure

None of them should preserve stale steps from the superseded claim chain.

## Cross-Section Synchronization Checklist

After any boundary reset, check all of the following against the same operative chain:

- independent claim step order
- dependent-claim references and step references
- main solution paragraph in `发明内容`
- first technical-effect paragraph
- embodiment step list
- embodiment detailed explanations
- concrete running example
- abstract
- figure legend
- flowchart

If one section still reflects the old chain, treat the whole draft as inconsistent.

## Style Rules

- Prefer natural causal sentences over repeated noun lists separated by `、`.
- Explain technical effects through `feature -> mechanism/process -> result`.
- Keep problem statements tied to the actual claimed route.
- Define recurring terms directly and consistently.
- Avoid label-only openings such as `技术方案一` before the main solution paragraph unless the user specifically asks for that structure.
- If the user is trying to reduce AI-like writing, avoid stock formulas such as `所谓` or `这里所称` when a direct definition is enough.

## DOCX Handling

When the deliverable is a Word file:

- create a new copy unless the user explicitly asks to overwrite
- update claims, invention content, embodiment, abstract, and figures together when the method boundary changes
- validate package integrity after writing
- run at least one text scan for stale old steps, stale term definitions, or cross-section inconsistency

## Final Checks

Before finishing, confirm:

- no pre-established support is accidentally left as a standalone runtime step in claim 1
- every support resource recited in claim 1 has an explicit runtime function
- the embodiment opening clearly states what already exists before execution
- the flowchart shows the current runtime chain rather than an obsolete fuller chain
- the abstract follows the same step boundary as claim 1
- no section claims to solve a problem that the adopted method chain cannot actually solve
