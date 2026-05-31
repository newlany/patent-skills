---
name: patent-method-runtime-boundary
description: "Internal route specialist and shared method workflow base under patent-cn-draft for Chinese method cases where the bottleneck is runtime step chain, method boundary, preconditions versus runtime steps, state transfer, matching, control, routing, identification, or closed-loop execution."
---
# CN Method Patent Workflow Agent

## New Architecture Role

`patent-cn-draft` is the public drafting orchestrator. This skill is the internal runtime-boundary route specialist and shared method-workflow base for the method-patent family.

## Skill Position

- 类型：案件类型专科 / runtime-boundary method specialist。
- 中文入口：运行步骤链、方法边界、前置条件与运行步骤区分、控制/识别/匹配/闭环方法。
- 上游：应先有交底分析和必要检索；完整撰写由 `patent-cn-draft` 总控。
- 输出：方法边界、步骤链、核心技术手段、权利要求、发明内容、实施方式与流程图同步。
- 支撑能力：必要时调用 `patent-method-boundary-alignment`、`patent-stage-invention-content`、`patent-stage-embodiments`。
- 边界：公式或工艺实验明显支配撰写瓶颈时，应转对应专科。

## Scope

Use this skill for general Chinese method patent cases whose main difficulty lies in the step chain itself, the method boundary, and cross-section synchronization.

This skill is also the shared workflow base for the other method-patent skills in this family. Common stages and common writing standards should live here, while scene-specific skills should keep only their local overlays.

Typical fit:

- control or scheduling methods
- detection, identification, matching, or routing methods
- data-processing or state-transfer methods
- closed-loop execution methods
- cases where pre-established resources, rule bases, models, calibration relations, or historical records must be distinguished from runtime steps

In the new architecture this is an internal route specialist and shared workflow base for method-patent drafting. It is not tied to any specific company, client, school, or project template. `patent-cn-draft` may select it when the case needs either:

1. a full workflow from baseline analysis through final draft packaging
2. one stage of a method-patent case, such as claim layout, invention content, embodiments, figure planning, or final synchronization

This skill may also serve as the provisional intake route when file-based scene classification is still low-confidence. In that case, use the shared baseline stages first, then decide whether the case should stay here or hand off to a more specialized route before major downstream drafting.

## Complete Workflow Coverage

The shared workflow in this skill covers the full core path of a method case:

- disclosure analysis
- prior-art checkpoint A after disclosure analysis
- technical-problem definition
- key-technical-means definition
- prior-art checkpoint B after reconstructed route stabilization
- inventive-step judgment
- claim construction
- background drafting
- invention-content drafting
- embodiments and examples
- figure and flowchart drafting
- abstract and final synchronization

## Internal Routing Rule

This is the general runtime-boundary method specialist behind `patent-cn-draft`. If the orchestrator assigns any stage by name, by stage number, or by deliverable, stay inside this skill and route internally. Do not split the work into multiple user-facing workflow skills.

## Trigger Phrases

- 方法类案件
- 方法类专利
- 全流程撰写
- 披露分析
- 方法边界
- 前置步骤
- 权利要求布局
- 权利要求书撰写
- 背景技术
- 发明内容
- 技术效果
- 具体实施方式
- 实施例
- 附图
- 流程图
- 图例一致性
- 公式修复
- 摘要
- DOCX 清理
- 全文同步

## Operating Modes

Use one of these three modes:

1. Full workflow mode
   - The user wants the method case handled from the baseline stage onward.
   - Read `references/workflow.md`, `references/checkpoints.md`, `references/output-contracts.md`, and the selected stage file.
2. Single-stage mode
   - The user wants only one stage, such as claim layout, invention content, or embodiments.
   - Read `references/routing-map.md`, `references/output-contracts.md`, and the selected stage file.
   - If required prerequisites are missing, state the missing baseline and downstream risk before proceeding.
3. Revision mode
   - The user wants revisions to a previously completed stage.
   - Revise the current stage first.
   - Treat later stages as stale until the user confirms whether they should be updated.

## Stage Loading Rule

Always read:

- `references/routing-map.md`
- `references/output-contracts.md`

Then read only the stage file needed for the current request from `references/stages/`.

Read `references/workflow.md` and `references/checkpoints.md` whenever the user is running multiple stages, asks for a full workflow, or asks how the stages fit together.

## Workflow Discipline

1. Establish the technical baseline before drafting legal text.
2. When the downstream goal is patentability judgment, technical-solution reconstruction, or claim drafting, run a first prior-art search after disclosure analysis and before reconstruction.
3. Use the first search to decide which technical route should be repaired, narrowed, or abandoned.
4. If the disclosure mixes runtime steps with preconditions, offline preparation, pre-established resources, or later updates, run the method-boundary stage before claim layout.
5. After reconstruction, method-boundary alignment, and core-feature stabilization, run a second prior-art recheck around the reconstructed route before inventive-step judgment.
6. Finalize the main technical route only after the second search and the inventive-step report are both stable.
7. Draft specification sections from the fixed claim baseline rather than from a stale disclosure narrative.
8. Keep figures, flowcharts, abstract, and embodiments synchronized with the adopted claim chain.
9. When formulas or native Word math objects matter, preserve them and validate the edited document package.
10. Do not carry company-specific or institution-specific drafting habits into this general workflow unless the user explicitly asks to reuse them.
11. Prefer this skill when the core issue is method-boundary alignment or whole-draft synchronization.
12. If the case is dominated by complex formulas, variables, or simulation outputs, prefer the formula-heavy method skill.
13. If the case is dominated by raw materials, process windows, examples, testing, and results tables, prefer the process-route method skill.
14. In background drafting by default, write only the existing technical background and the observable prior-art phenomena; do not analyze why the phenomena arise there unless the user explicitly asks for a different style.
15. In invention-content drafting by default, move the cause analysis into the opening `申请人发现` part, then explain the adopted solution in claim order, and make the main effect paragraphs clarify how the inventive key means work and how the step chain or execution objects cooperate.
16. When the user asks for Word-template packaging or final patent-form output, use the public `patent-cn` application template `templates/专利撰写模板文件.docx` unless the user provides another template, and fill only the corresponding body sections while preserving the template's existing font, size, spacing, headers, footers, and non-body layout.
17. When the user asks to reduce AI-like writing style in background, invention content, or embodiments, prefer shorter sentences, reduce dense stacks joined by `、`, and keep the prose direct and restrained without making it choppy.
18. If a later dependent claim narrows how a pre-existing support resource is updated or refreshed after the main runtime chain, keep that feature in the resource-update register and do not automatically promote it into a new main step, new main effect layer, or extra numbered embodiment step unless the independent claim itself includes that step.
19. In embodiment drafting for control or execution methods, after one brief scene paragraph first restate the fixed runtime chain such as `S1-S6`, then explain the steps in order; do not stop at functional naming of devices or self-defined terms, and do not front-load a glossary. Instead, explain the meaning of each term when first used in the detailed step explanation, explain any subordinate terms introduced there, explain how self-defined quantities are measured, extracted, calculated, or represented, and explain how the physical controller, sensor, drive, valve, guide, or actuator concretely implements the claimed operation in industrial use. In Chinese drafting paragraphs, avoid double quotes by default and vary definition lead-ins rather than repeating one rigid phrase.

## Stage Handoff Rule

After each completed stage, present:

1. the completed deliverable
2. the baseline used
3. key assumptions or unresolved points
4. the recommended next stage
5. a direct request for user confirmation

Do not silently continue to the next stage unless the user explicitly asks for uninterrupted execution.

## References

## Reusable Assets

- `/Users/chrynos/.codex/skills/patent-cn/templates/专利撰写模板文件.docx`
  - Canonical patent drafting template for final Word output.
  - Use when the user asks to fill claims/specification content into a formal patent template.
  - Create a working `.docx` copy from the template, then replace only the target body text.
  - Do not alter the template's existing typography, page setup, headers, footers, numbering shell, or other non-body formatting unless the user explicitly asks.

- `references/workflow.md`
- `references/routing-map.md`
- `references/output-contracts.md`
- `references/checkpoints.md`
- `references/stages/01-disclosure-analysis.md`
- `references/stages/02-disclosure-reconstruction.md`
- `references/stages/03-method-boundary-alignment.md`
- `references/stages/04-core-feature-analysis.md`
- `references/stages/05-inventive-step-analysis.md`
- `references/stages/06-final-disclosure.md`
- `references/stages/07-claim-layout.md`
- `references/stages/08-claims-drafting.md`
- `references/stages/09-background-drafting.md`
- `references/stages/10-invention-content-drafting.md`
- `references/stages/11-embodiments-and-examples.md`
- `references/stages/12-figures-flowcharts-and-legends.md`
- `references/stages/13-formulas-and-docx-cleanup.md`
- `references/stages/14-testing-design.md`
- `references/stages/15-results-analysis.md`
- `references/stages/16-abstract-and-final-synchronization.md`
