---
name: patent-analysis-fixed-patent
description: "Internal analysis specialist under patent-cn-response and patent-cn for one fixed patent or a fixed comparison set during OA, invalidity, or argument work. Direct use is allowed for standalone 固定专利分析、权利要求拆解、D1/D2/D3对比、区别特征、支持性、公开内容、争点备忘录 tasks. Do not use for broad prior-art discovery."
---
# Patent Analysis Agent

## New Architecture Role

`patent-cn-response` is the preferred public orchestrator for OA/invalidity work, and `patent-cn` may route standalone fixed-patent analysis here. This skill is an internal fixed-object analysis specialist. Direct use is appropriate only when the target patent or comparison set is already fixed, or when older prompts explicitly name this skill.

## Skill Position

- 类型：固定对象分析 / fixed-patent analysis。
- 中文入口：分析某一件专利、D1/D2/D3 对比、区别特征、权利要求范围、说明书支持、争点备忘录。
- 输入：已确定的目标专利、对比文件、OA/无效材料或权利要求文本。
- 输出：权利要求拆解、对比表、区别特征、论证压力点和备忘录。
- 支撑能力：可调用 `patent-research-records`、`patent-support-google-patents-pdfs`、`patent-support-docx-math`、`spreadsheet`。
- 边界：不做开放式查新；目标未固定时先用 `patent-stage-prior-art-search`。

## Overview

Use this skill for one-patent or fixed-patent analysis after the search stage is over.

This is the internal fixed-object analysis specialist for tasks like:

- OA-stage target patent analysis
- invalidation-stage patent analysis
- D1/D2/D3 comparison against a fixed target patent
- claim-scope and distinguishing-feature analysis
- support, disclosure, and terminology analysis
- argument-point extraction and issue memo drafting

## Specialist Routing Rule

If `patent-cn-response` or `patent-cn` has already fixed the target patent and the next step is analysis rather than retrieval, route the work here. Direct standalone use is also acceptable when the user's prompt already fixes the patent or comparison set.

Do not start from broad prior-art discovery here. If the user still needs to search for references, use `patent-stage-prior-art-search` first.

## Companion Skills

This skill may use these as companions when needed:

- `patent-research-records` for source-heavy record verification
- `patent-support-docx-math` for formula-sensitive patent DOCX reading
- `patent-support-google-patents-pdfs` when cited reference PDFs must be collected
- `spreadsheet` when a feature matrix or D1/D2/D3 chart is useful

## Operating Modes

### 1. OA analysis mode

Use when the user wants:

- D1 / D2 / D3 comparison support
- distinguishing-feature extraction
- whether-to-amend support
- claim-strength diagnosis before drafting a response

### 2. Invalidation analysis mode

Use when the user wants:

- attack/defense point extraction
- reference-combination analysis
- granted-claim vulnerability analysis
- issue memo support before oral-hearing preparation

### 3. Fixed-patent technical analysis mode

Use when the user wants to understand:

- what the patent really teaches
- where the claim boundary sits
- what terms are key
- where support or disclosure pressure may lie

## Workflow

1. Fix the analysis object precisely.
   - publication number
   - application number when relevant
   - claim version or procedural posture when relevant
2. Fix the analysis question.
   - claim-scope reading
   - D1/D2/D3 comparison
   - distinguishing features
   - support / disclosure
   - amendment impact
   - invalidation vulnerability
3. Gather the operative materials.
   - target patent text
   - cited references if already known
   - office action / invalidation petition / hearing materials if present
4. Separate:
   - patent record facts
   - comparison facts
   - argument options
   - unresolved uncertainty
5. Produce an issue-focused memo, not a generic summary.

## Output Contract

Unless the user asks otherwise, produce:

1. analysis frame
2. operative patent identity and claim baseline
3. key findings
4. comparison or issue analysis
5. argument-useful takeaways
6. uncertainty / evidence gaps

## Boundaries

- This skill is not the entry point for prior-art retrieval.
- This skill is not a broad patent-topic research workflow.
- If the target is not fixed yet, route to `patent-stage-prior-art-search`.
- If the work becomes heavily source- or status-verification-intensive, bring in `patent-research-records` as a companion or handoff.
