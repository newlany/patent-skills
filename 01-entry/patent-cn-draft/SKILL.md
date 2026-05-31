---
name: patent-cn-draft
description: "Public orchestrator for Chinese patent application drafting from technical disclosure to draft package. Use for 交底分析、查新、方案重构、创造性判断、权利要求书、说明书、附图、QC, with guided/autonomous execution and case manifest management. Keeps stage specialists internal."
---
# CN Patent Drafting Orchestrator

## Role

This is the user-facing drafting orchestrator. It reduces the old multi-skill calling burden by owning the drafting workflow graph and dispatching internal specialists.

Use it for new Chinese application drafting from:

- 技术交底书
- 发明人说明
- 研发材料
- 技术方案草稿
- inventor interview notes

Do not use it for OA response, invalidity, correction-only work, or standalone DOCX repair.

## Startup

Always read:

- [references/drafting-workflow-graph.md](references/drafting-workflow-graph.md)
- [references/case-workspace-layout.md](references/case-workspace-layout.md)
- [references/stage-contracts.md](references/stage-contracts.md)
- [references/stop-conditions.md](references/stop-conditions.md)
- [$patent-cn/references/internal-specialists.md](/Users/chrynos/.codex/skills/patent-cn/references/internal-specialists.md)

When the task involves inventive-step strategy, claim-scope choices, or claim drafting/revision, read:

- [$patent-entry-drafting/references/problem-based-inventive-claim-drafting.md](/Users/chrynos/.codex/skills/patent-entry-drafting/references/problem-based-inventive-claim-drafting.md)

When drafting or revising `具体实施方式` / `实施例` for a structural, device, assembly, product, component-relation, or layered-structure case, read:

- [references/structural-embodiment-drafting.md](references/structural-embodiment-drafting.md)

Then call the existing internal drafting engine:

- [$patent-entry-drafting](/Users/chrynos/.codex/skills/patent-entry-drafting/SKILL.md)
- [$patent-cn-runtime](/Users/chrynos/.codex/skills/patent-cn-runtime/SKILL.md) for registry-based tool calls

Treat `patent-entry-drafting`, `patent-stage-*`, `patent-method-*`, `patent-support-*`, and `patent-qc-*` as internal specialists unless the user explicitly asks for one of them.

## Runtime Rule

For every multi-stage drafting case:

- if the current project root has no `manifest.json`, create the case under `<project-root>/专利工作区/<中文案件名>` and pass that as `--case-dir`
- do not write process documents directly into the project root
- create directories lazily: only create the immediate parent directory of an artifact when writing that artifact
- keep human process deliverables under `输出/过程/` or `输出/过程/<中文阶段名>/`
- name and write human-readable process deliverables in Chinese by default, except for stable tool contracts, citations, source titles, or script-required file names
- keep final deliverables and validation reports under `输出/定稿/`
- keep machine JSON reports under `记录/<中文阶段名>/报告/`, and deterministic tool results under `记录/<中文阶段名>/工具运行/`

```bash
python3 /Users/chrynos/.codex/skills/patent-entry-drafting/scripts/patent_workflow.py init \
  --case-dir <case-dir> \
  --title "<case-title>" \
  --source <source-file-or-label> \
  --mode guided
```

Use `--mode autonomous` only when the user clearly requests continuous first-pass drafting.

For each stage:

```bash
python3 /Users/chrynos/.codex/skills/patent-entry-drafting/scripts/patent_workflow.py stage-start --case-dir <case-dir> --stage <stage> --json
python3 /Users/chrynos/.codex/skills/patent-entry-drafting/scripts/patent_workflow.py stage-report --case-dir <case-dir> --stage <stage> --name <logical-stage-name> --status completed --json
python3 /Users/chrynos/.codex/skills/patent-entry-drafting/scripts/patent_workflow.py add-artifact --case-dir <case-dir> --stage <stage> --path <artifact> --kind <kind> --stage-status completed --json
python3 /Users/chrynos/.codex/skills/patent-entry-drafting/scripts/patent_workflow.py stage-end --case-dir <case-dir> --stage <stage> --status completed --json
```

Before claiming completion:

```bash
python3 /Users/chrynos/.codex/skills/patent-entry-drafting/scripts/patent_workflow.py validate --case-dir <case-dir> --json
```

For deterministic scripts, prefer the Phase-3 tool runner:

```bash
python3 /Users/chrynos/.codex/skills/patent-cn-runtime/scripts/patent_tool_runner.py run workflow.validate \
  --case-dir <case-dir> \
  --result-output <case-dir>/记录/07_质检/工具运行/workflow-validate-tool-run.json
```

## Reference Drafting Quality Carryover

At prior-art Checkpoint A and Checkpoint B, require `patent-stage-prior-art-search` to assess the drafting quality of selected comparison documents, not only their technical proximity.

Before reconstruction, inventive-step strategy, claims, or specification drafting, read the search memo's `Reference Drafting Quality` section or the artifact `输出/过程/02_现有技术检索/参考文献撰写质量.md` if present. When a reference is marked high quality, use it only as a drafting-style aid:

- borrow phrasing patterns, term-definition discipline, claim hierarchy logic, problem-solution framing, and embodiment organization where they fit the present disclosure
- keep all technical facts, claim scope, effects, and examples grounded in the user's disclosure and confirmed search analysis
- avoid long verbatim copying and avoid importing limitations that were not selected for the current invention strategy

## Output Protocol

At the beginning of a drafting run, state:

```text
CN DRAFTING PLAN
- execution mode: <guided|autonomous>
- case folder: <path or to be created>
- route confidence: <high|medium|low>
- stage graph: intake -> disclosure -> search A -> reconstruction -> route cleanup -> search B -> inventive-step -> claims -> specification -> figures -> QC -> package
- first deliverable: <artifact>
```

At each stage boundary, summarize:

- artifact created
- confirmed findings
- suspected issues
- assumptions
- blockers
- next stage

Also write the same boundary data into the `stage-report` JSON contract defined in [references/stage-contracts.md](references/stage-contracts.md).

## Completion Language

Use only these completion terms:

- `drafting-complete`: all required draft-stage artifacts exist and validation has no hard fail.
- `filing-ready`: final DOCX/package artifacts are present and validation has no hard or soft fail.

Do not call a text draft `filing-ready`.
