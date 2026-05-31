---
name: patent-entry-invalidity
description: "Internal invalidity workflow engine under patent-cn-response for Chinese patent invalidity work. Direct use is allowed for compatibility or explicit invalidity-specific prompts involving 专利无效、无效答辩、无效宣告请求、攻击防御图、口审准备、请求人观点回应、合议组问题准备."
---
# Patent Invalidity Response Agent

## New Architecture Role

`patent-cn-response` is the preferred public response orchestrator. This skill is the internal invalidity workflow engine. Direct use is appropriate only for older prompts that explicitly name this skill or for narrowly scoped invalidity work where no higher-level routing is needed.

## Skill Position

- 类型：无效案件内部工作流 / invalidity workflow engine。
- 中文入口：无效宣告、无效答辩、口审准备、攻击防御、请求人观点、合议组追问。
- 主链条：案卷梳理 -> 程序时间线 -> 攻防框架 -> 焦点问题 -> 证据/对比分析 -> 口审或答辩文件。
- 下游/支撑：`patent-stage-invalidity-hearing-prep`、`patent-analysis-fixed-patent`、`patent-research-records`、`patent-support-google-patents-pdfs`、`patent-support-docx-math`、`doc`、`pdf`、`spreadsheet`、`transcribe`。
- 边界：不作为初始申请撰写入口；不把无效论证规则混入普通交底撰写，除非用户明确要求以无效视角反审。

## Overview

This is the invalidity workflow engine behind the public `patent-cn-response` orchestrator.

Use it for:

- 无效分析
- 无效答复
- 案卷梳理
- 攻击与防守点提炼
- 口头审理准备
- 请求人观点回应
- 审查员追问备答

## Internal Routing Rule

When `patent-cn-response` selects the invalidity path, route the invalidity matter here before selecting lower-level companions such as:

- `patent-stage-invalidity-hearing-prep`
- `patent-analysis-fixed-patent`
- `patent-research-records`

Those may still be used as internal companions, but `patent-cn-response` remains the public front door.

## Core Workflow Rule

Use [$patent-stage-invalidity-hearing-prep](/Users/chrynos/.codex/skills/patent-stage-invalidity-hearing-prep/SKILL.md) as the core workflow engine.

Add companions only when needed:

- [$patent-analysis-fixed-patent](/Users/chrynos/.codex/skills/patent-analysis-fixed-patent/SKILL.md) for fixed-patent claim-focused comparison or argument stress testing
- [$patent-research-records](/Users/chrynos/.codex/skills/patent-research-records/SKILL.md) for file history, family, or status verification
- [$patent-support-google-patents-pdfs](/Users/chrynos/.codex/skills/patent-support-google-patents-pdfs/SKILL.md) for cited-document collection
- `doc`, `pdf`, and `spreadsheet` for working materials

## Operating Modes

1. sorting mode
   - only梳理案卷、时间线、焦点和证据组合
2. response mode
   - only起草无效答复、口审准备或短答
3. end-to-end mode
   - 先梳理，再进入答复和口审材料

## Output Protocol

When this skill is used, state:

```text
INVALIDITY ROUTE
- mode: <sorting|response|end-to-end>
- core workflow: patent-stage-invalidity-hearing-prep
- companions: <skill-1>, <skill-2>
- first output: <artifact>
```

Then continue with the invalidity workflow instead of stopping at routing.

## Boundaries

- This is not the drafting entry.
- This is not the OA response entry.
