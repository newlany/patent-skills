---
name: patent-research-topic
description: "Research specialist callable by patent-cn for patent special-topic studies. Direct use is allowed for standalone 专利专题研究、创造性、公知常识、第26条、功能性特征、侵权判定、证据规则、趋势研究、培训底稿, with source hierarchy, date verification, and reusable report modules."
---
# Patent Topic Deep Research

## New Architecture Role

`patent-cn` is the preferred public entry for mixed patent work. This skill is a standalone/topic-research specialist for reusable patent research reports and methodology modules, not a drafting, review, or response orchestrator.

## Skill Position

- 类型：专题研究 / patent topic research。
- 中文入口：创造性、公知常识、法26、功能性特征、侵权判定、证据规则、趋势分析、培训材料。
- 输入：研究主题、辖区、时间范围、知识库或参考材料。
- 输出：专题报告、争点图、来源层级、可复用附录和提示词。
- 支撑能力：可调用 `patent-research-records`、`web-access`、`defuddle`、`obsidian-cli`、Notion 技能、`doc`。
- 边界：不用于单件申请撰写的普通检索；具体案件查新用 `patent-stage-prior-art-search`。

Produce patent专题/课题 research that is source-first, date-aware, reusable, and explicit about what is rule, case practice, inference, and practical guidance.

## Quick Start

1. Fix the research frame before searching: topic, jurisdiction, procedural posture, exact verified-through date, output form, and inclusion/exclusion scope.
2. Start from the local patent knowledge vault when available. Use it to build the issue tree and find canonical materials, not to replace official verification.
3. Use `references/methodology.md` for the full workflow, source hierarchy, issue-tree patterns, and anti-patterns.
4. Use `references/master-prompt.md` when the user wants a reusable full prompt or when you need to launch the research from scratch in a fresh thread.
5. Use `references/report-template.md` when drafting the final long report, appendices, quick-check tables, or reusable response modules.
6. Keep every nontrivial conclusion traceable to a source category and a verified date.

## Workflow

1. Lock the topic.
   - State the exact legal issue, not a broad area.
   - State the jurisdiction and procedural posture.
   - State the cut-off date with an absolute date.
   - State what is inside and outside scope.

2. Build the question tree.
   - Split the topic into normative baseline, concept boundaries, issue map, evidence or proof structure, procedural differences, case clusters, recent trend, and practice takeaways.
   - If the topic is highly specific, adapt the branches instead of forcing a generic outline.

3. Gather in layers.
   - Read the local vault first.
   - Verify time-sensitive or high-stakes points against current official sources.
   - Treat commentaries as discovery aids unless independently verified.

4. Research iteratively.
   - Run a first pass to map authorities and dispute points.
   - Run a second pass to fill gaps, latest updates, and boundary cases.
   - Run a third pass only where sources conflict, dates matter, or the conclusion still feels under-supported.

5. Write with labels.
   - Separate `规范事实`, `裁判规则`, `研究判断`, `实务建议`, and `趋势观察`.
   - Mark unresolved points as `不确定` or `待核验`.
   - Never let a draft or commentary masquerade as current law.

6. Leave reusable artifacts.
   - Include checklists, quick tables, issue maps, or reusable response modules when they materially help later work.
   - Prefer outputs that can support future OA replies, invalidation work, litigation prep, training, or knowledge-vault updates.

## Boundaries

- Prefer this skill for 专题/课题型 patent research that must become a structured long report or reusable methodology package.
- Prefer `$patent-research-records` for record-first research on a specific patent, family, prosecution history, invalidation, legal status, or single case file.
- Prefer more specialized patent workflow skills when the user is already inside OA response, invalidity hearing prep, disclosure drafting, or formal CN patent drafting.

## Quality Bar

- Do not start from conclusions and backfill authorities.
- Do not mix source levels.
- Do not omit the verified date for time-sensitive points.
- Do not merge facts and inference.
- Do not stop at a prose summary when the user asked for a reusable research method or skill.

## Resources

- `references/methodology.md`: unified methodology, source hierarchy, issue-tree patterns, search loop, and anti-patterns.
- `references/master-prompt.md`: the complete reusable prompt set for full-report, update, and rapid-brief modes.
- `references/report-template.md`: report outline, appendix patterns, quick-check tables, and final self-audit.
