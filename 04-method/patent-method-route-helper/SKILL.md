---
name: patent-method-route-helper
description: "Internal/helper router for Chinese method-patent drafting families. Use after the matter is already identified as a method patent case, or when the user explicitly asks 用方法类skill判断路线. Routes among 工艺/制备路线、公式/模型驱动、运行步骤链/方法边界 workflows. Prefer patent-entry-drafting or patent-entry-router when the overall task type is unclear."
---
# CN Method Patent Router Agent

## New Architecture Role

This is an internal route helper behind `patent-cn-draft`. It should not be presented as a normal public entry. Use it only after the case has already been identified as method-patent drafting and the bottleneck route is still unresolved.

## Skill Position

- 类型：方法类案件内部路由 / internal method-route helper。
- 中文入口：仅在已经确认是方法类撰写时使用，例如“这个方法案该走哪个路线”。
- 路由对象：`patent-method-process-route`、`patent-method-formula-model`、`patent-method-runtime-boundary`、必要时配合 `patent-method-boundary-alignment`。
- 判断基准：按撰写瓶颈分类，而不是按申请人、项目名称或文件标题分类。
- 边界：不要和 `patent-cn`、`patent-cn-draft` 抢公共入口；不处理 OA、无效或文档-only 任务。

## Scope

Use this skill as an internal/helper router for Chinese method patent drafting work.

Its job is to decide which workflow family best fits the case, then hand the work to exactly one specialized method skill:

1. preparation and process-route-heavy method cases
2. formula and model-driven method cases
3. general runtime-chain and method-boundary method cases

If the user provides disclosure files and says things like `用方法的skill处理这个案件`, `用方法类skill处理`, or `你自己判断该用哪一个方法skill`, this router can be used after confirming that the work is indeed method-patent drafting rather than OA, invalidity, correction, or document-only processing.

## Architecture Rule

Keep one shared full workflow base in [$patent-method-runtime-boundary](/Users/chrynos/.codex/skills/patent-method-runtime-boundary/SKILL.md). That shared base owns the reusable stages and common writing standards, especially for:

- disclosure analysis
- technical-problem definition
- key-technical-means definition
- inventive-step analysis
- claims
- background
- invention content
- embodiments
- figures and flowcharts
- final synchronization

Let the specialized skills keep only scene-specific overlays:

- [$patent-method-process-route](/Users/chrynos/.codex/skills/patent-method-process-route/SKILL.md): process-route, examples, testing, and results-table emphasis
- [$patent-method-formula-model](/Users/chrynos/.codex/skills/patent-method-formula-model/SKILL.md): formula, model, figure-label, and DOCX-formula emphasis

If a rule is reusable across method cases, update the shared workflow base first rather than maintaining parallel local versions.

## Helper Entry Rule

If the user is unsure which method-patent skill to use after the matter is already classified as method drafting, use this router first.

If the user is unsure about the overall patent task type, prefer `patent-entry-router`. If the user clearly wants disclosure-to-application drafting but not specifically method-family routing, prefer `patent-entry-drafting`.

After routing, do not mix multiple specialized method skills unless the case truly has two equally dominant difficulty centers and the user explicitly wants a hybrid treatment.

When disclosure files are available, do not classify only from the title, applicant, or a short user summary. Read the operative disclosure content first, extract route signals from the file, then decide the skill.

## File-First Intake Rule

Always read the disclosure file content before routing when the user has provided files.

At intake, do these in order:

1. identify the main disclosure file and any companion files
2. if the files are `.doc`, `.docx`, or other document formats, use the appropriate document-reading path and extract the operative content before classifying
3. read enough of the file content to understand the technical route, implementation burden, and likely claim focus
4. extract route signals from the actual disclosure rather than from the file name or topic label
5. choose the route by the dominant drafting bottleneck

If the disclosure is mixed or noisy, still make a provisional route decision from the file itself. Only ask the user to choose manually when the file evidence cannot support even a provisional classification.

## Routing Rule

Read `references/scene-routing.md` first.

Then route as follows:

- If the case is dominated by raw materials, process windows, equipment cooperation, examples, testing, and retained result tables, use [$patent-method-process-route](/Users/chrynos/.codex/skills/patent-method-process-route/SKILL.md).
- If the case is dominated by formulas, variables, models, simulation outputs, result curves, or equation-sensitive DOCX handling, use [$patent-method-formula-model](/Users/chrynos/.codex/skills/patent-method-formula-model/SKILL.md).
- If the case is dominated by runtime step-chain design, method-boundary clarification, precondition versus runtime-step distinction, or full-draft synchronization, use [$patent-method-runtime-boundary](/Users/chrynos/.codex/skills/patent-method-runtime-boundary/SKILL.md).

State the routing result with:

1. the chosen skill
2. the file-based route signals that support it
3. any competing signals that were present but not dominant
4. whether the route is high-confidence or provisional

## Mixed-Case Rule

When a case shows features of more than one family, choose the skill that matches the dominant drafting bottleneck:

- formulas or models are the bottleneck -> formula/model-driven skill
- experiments, examples, and process windows are the bottleneck -> process-route skill
- step-chain boundary and cross-section consistency are the bottleneck -> general workflow skill

If the bottleneck is still unclear after reading the file:

1. use [$patent-method-runtime-boundary](/Users/chrynos/.codex/skills/patent-method-runtime-boundary/SKILL.md) as the provisional intake route
2. run the shared baseline stages through technical-problem and key-technical-means clarification
3. re-evaluate the dominant bottleneck before claim drafting or major section drafting

Only ask the user to choose manually when two routes remain equally plausible and the next requested deliverable would materially differ depending on the route.

## Classification Quality Rule

Judge the route by drafting burden, not by topic label alone.

In particular:

- do not choose the formula/model route merely because the disclosure contains a few formulas if the real burden is process examples, testing, and result tables
- do not choose the process-route route merely because equipment or processing steps appear if the real burden is variable logic, objective functions, or simulation outputs
- do not choose the general route merely because every method has steps; use it when method-boundary alignment, preconditions versus runtime steps, or whole-draft synchronization are the main problem

When in doubt, ask: if claim 1 and the main embodiments were drafted today, what part would be hardest to draft correctly from this disclosure?

## Shared Completeness Check

Regardless of which specialized skill is chosen, confirm that the workflow covers:

- disclosure analysis
- prior-art checkpoint A after disclosure analysis
- technical-problem definition
- key-technical-means definition
- prior-art checkpoint B before inventive-step judgment and claims
- inventive-step judgment
- claim construction
- background drafting
- invention-content drafting
- embodiments and examples
- figure or flowchart planning and drawing
- final synchronization when needed

If any of these are missing from the chosen route, the draft workflow is incomplete and should be expanded before proceeding.
