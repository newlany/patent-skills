---
name: patent-method-process-route
description: "Internal route specialist under patent-cn-draft for process-route, preparation-heavy, material, formulation, treatment, manufacturing, parameter-window, test-backed Chinese method patent drafting. Direct use is allowed only for standalone route revision or older prompts explicitly naming this process-route specialist."
---
# Preparation And Process-Route Method Patent Agent

## New Architecture Role

`patent-cn-draft` is the public drafting orchestrator. This skill is the internal process-route specialist for `03_reconstruction`, claims, specification, examples, and testing emphasis after disclosure analysis and search baselines exist.

## Skill Position

- 类型：案件类型专科 / process-route method specialist。
- 中文入口：制备方法、工艺路线、材料配方、处理窗口、测试结果、实施例/对比例为核心的案件。
- 上游：应先有交底分析和必要检索；完整撰写由 `patent-cn-draft` 总控。
- 输出：工艺主线、权利要求布局、实施例/对比例、测试设计和效果表达。
- 支撑能力：可调用 `patent-stage-embodiments`、`patent-stage-invention-content`、`patent-support-docx-math`、`spreadsheet`。
- 边界：不要因为文件来自某客户就自动选择；必须按实际撰写瓶颈判断。

## Scope

Use this skill for Chinese method patent cases whose main difficulty lies in a concrete process chain, such as raw-material selection, feed order, equipment cooperation, process windows, treatment sequence, example design, testing design, and results analysis.

Typical fit:

- material preparation methods
- manufacturing or treatment methods
- formulation or compounding methods
- process-parameter optimization methods
- experimentally verified process methods with examples, comparative examples, and result tables

Legacy internal naming is retained for compatibility, but the applicable scene is process-route and preparation-heavy method drafting rather than a client-specific workflow.

## Internal Routing Rule

This is the process-route specialist behind `patent-cn-draft`. If the orchestrator assigns any route-specific stage by name, by stage number, or by deliverable, stay inside this skill and route internally. Do not expose former stage-specific variants as user-facing entry points.

## Shared workflow base

Always use the common full workflow and handoff rules from:

- `../patent-method-runtime-boundary/references/workflow.md`
- `../patent-method-runtime-boundary/references/routing-map.md`
- `../patent-method-runtime-boundary/references/output-contracts.md`
- `../patent-method-runtime-boundary/references/checkpoints.md`

Then read `references/specialization.md` for the process-route-heavy emphasis of this skill.

## Complete workflow coverage

Through the shared workflow base, this skill covers the full method-case path, including disclosure analysis, technical-problem definition, key-technical-means definition, inventive-step judgment, claims, background, invention content, embodiments, figures or flowcharts, testing, results analysis, and final synchronization. Local materials in this skill should add only process-route-specific emphasis.

## Trigger phrases

- Full workflow:
  - 制备方法案
  - 工艺方法案
  - 材料制备方法
  - 制造方法
  - 处理方法
  - 配方工艺方法
  - 全流程撰写
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
  - invention-content drafting
  - process-detail drafting
  - examples design
  - testing design
  - results analysis
  - 第1阶段 / 第8阶段 / 第11阶段
  - 背景技术
  - 权利要求布局
  - 权利要求书撰写
  - 发明内容
  - 技术效果
  - 工艺细化
  - 实施例设计
  - 附图
  - 流程图
  - 测试设计
  - 结果分析

## Operating modes

Use one of these three modes:

1. Full workflow mode
   - The user wants the process-route workflow from stage 1 onward.
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

1. This workflow is for process-route and preparation-heavy method patent cases.
2. Each later stage must use the earlier user-confirmed stage as its baseline.
3. Default to one stage at a time, with a stop for user confirmation after each stage.
4. If the user names a later stage directly, do not force the full workflow, but do state any missing prerequisite baseline and risk.
5. Do not draft claims before the final disclosure and feature analysis are fixed.
6. Do not draft examples before the process-detail section is fixed.
7. Do not draft results analysis before the retained result tables are fixed.
8. Keep the entire application on one consistent technical main line.
9. Prefer this skill when process windows, raw materials, equipment coordination, examples, testing, and retained result tables are central to the case.
10. If the case is instead dominated by complex formulas, variable systems, models, or simulation outputs, prefer the formula-heavy method skill rather than this one.

## Evidence-backed materials and testing

For preparation-heavy or material-preparation cases:

- Before `实施例` and `对比例`, add a raw-materials paragraph or compact raw-materials section unless the user explicitly forbids it.
- The raw-materials text must identify each key raw material by raw-material name, commercial grade or model, and supplier when that information is available.
- Prefer commercially available domestic Chinese products when they technically fit the disclosure and claim scope.
- When completing grade/model or supplier information, use real web evidence such as a supplier page, TDS, SDS, catalog page, product manual, or credible marketplace/manufacturer listing. Do not invent commercial sources.
- Keep web-sourced commercial materials as embodiment examples, not claim-scope limitations. Add generic fallback wording around chemical type, key functional property, purity, moisture, solid content, particle size, or other relevant controls when needed.
- If no reliable source can be found for a specific commercial material, state the gap and use generic technical wording or ask for inventor confirmation instead of fabricating a grade or supplier.
- Testing standards must be real, usable standards whose number and scope match the tested metric. Prefer current GB or GB/T standards for Chinese drafts when available; otherwise use a suitable industry, ISO, ASTM, or disclosed internal method with its status made clear.
- Test data must be represented in tables. Distinguish measured data from drafted or to-be-confirmed data in the response and avoid presenting hypothetical values as measured facts.

## Stage handoff rule

After each completed stage, present:

1. the completed deliverable
2. key assumptions or unresolved points
3. the recommended next stage
4. a direct request for user confirmation

Do not silently continue to the next stage unless the user explicitly asks for uninterrupted execution.

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
- `references/specialization.md`
- `references/file-naming.md`
