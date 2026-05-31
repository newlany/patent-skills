---
name: patent-stage-invalidity-hearing-prep
description: "Internal/stage workflow for Chinese patent invalidity docket sorting and oral-hearing preparation. Use for 无效案卷梳理、时间线、攻防框架、口审焦点、开庭陈述、请求人观点短答、合议组追问备答, usually under patent-entry-invalidity."
---
# Patent Invalidity Hearing Prep

## Skill Position

- 类型：无效案件阶段引擎 / invalidity hearing-prep stage。
- 中文入口：案卷梳理、程序时间线、攻防框架、口审焦点、开庭陈述、追问备答。
- 上游：通常由 `patent-entry-invalidity` 调用。
- 输出：案卷清单、时间线、焦点问题、口审准备文件、Word 导出。
- 支撑能力：可调用 `patent-analysis-fixed-patent`、`patent-research-records`、`patent-support-docx-math`、`doc`、`pdf`、`transcribe`。
- 边界：不是无效公共入口；用户不明确时优先转 `patent-entry-invalidity`。

## Overview

围绕“先梳理、再分步起草、最后导出”的方式准备专利无效口审材料。这个 skill 现在同时覆盖两类需求：

- 无效过程梳理 / 案卷梳理
- 口头审理准备 / 口审稿起草 / 备答 / Word 导出

优先把 [$patent-entry-invalidity](/Users/chrynos/.codex/skills/patent-entry-invalidity/SKILL.md) 作为用户侧公开入口；本 skill 更适合作为其核心 workflow 引擎或兼容调用入口。

## Public entry rule

这是无效案件梳理和口审准备的核心 workflow skill。若用户明确点名本 skill，则继续在本 skill 内部完成；否则优先使用公开别名 [$patent-entry-invalidity](/Users/chrynos/.codex/skills/patent-entry-invalidity/SKILL.md)。

如果用户只要“无效过程梳理”或“案卷梳理”，也仍然使用本 skill 并进入内部梳理模式。

## Operating modes

1. Case-sorting mode
   - 用户只要无效过程梳理、程序时间线、攻击/答辩变化、口审前焦点
   - 先读 `references/routing-map.md` 和 `references/case-sorting.md`
2. Hearing-prep mode
   - 用户要口审准备文件、开庭陈述、正式抗辩、备答、总结陈述
   - 先读 `references/routing-map.md` 和 `references/prompt-templates.md`
3. End-to-end mode
   - 先做案卷梳理，再进入口审稿与备答起草
   - 同时读取 `references/case-sorting.md`、`references/case-sorting-prompts.md`、`references/prompt-templates.md`

## Quick Start

1. 盘点案件目录，找出关键材料并输出“案卷材料清单”和“时间线与争点概览”。
2. 确认审查基础是原权利要求还是修改后的权利要求，并提炼真正的核心争点。
3. 按五步起草：开庭陈述、正式抗辩、请求人可能观点及短答、审查员可能追问及短答、总结陈述。
4. 检查口头化表达和附图指引，再按要求导出 Word。

## Build Context First

在动笔前先找齐这些材料：

- 口头审理通知书
- 无效宣告请求受理通知书
- 请求人的无效请求书、补充意见
- 我方意见陈述书、修改后的权利要求书
- 本专利授权文本
- 授权委托书
- 既有口审稿或参考稿（如有）

先回答这些问题，再开始起草：

- 请求人攻击的是原权利要求还是修改后权利要求
- 我方是否修改权利要求，具体修改了什么
- 请求人的核心证据组合是什么
- 我方真正能守住的创造性支点是什么
- 哪些点最可能在口审中被反复追问

优先产出：

- 一份“案卷材料清单”
- 一份“时间线和争点概览”
- 一页式案件分析
- 一份“核心争点列表”

如果用户只要求梳理案卷，到这里可以停下，不要强行继续生成口审稿。

## Draft in Five Passes

### 1. 梳理案卷

先梳理程序过程、关键证据组合、权利要求修改和真正争点。不要一上来就写整份口审稿。

### 2. 起草开庭陈述

只交代出庭身份、代理关系、我方主张和请求事项。保持简短，不展开证据分析。

### 3. 起草正式抗辩

先说明审查基础，再结合附图讲清专利方案，最后围绕 2 到 4 个核心争点做短句式答复。不要按请求书逐页反驳，也不要复述书面答辩全文。

### 4. 准备临场备答

分别准备两类短答：

- 请求人可能继续坚持的观点
- 审查员高概率追问的问题

每条答复控制在 2 到 4 句话，先给结论，再给理由。

### 5. 完成总结与交付

总结陈述只做收束，不补新观点。最后检查口头化程度、附图指引和文件命名，再导出 Word。

## Keep The Output Oral

遵守这些写法：

- 先讲结构，再讲法律评价
- 先讲我方方案，再讲对方证据为什么拼不出来
- 压缩重写书面意见，不要直接照抄
- 优先短句、短段、口头化表达
- 每个关键结论尽量落到具体结构、连接关系或附图
- 不要平均用力，重点守修改后的独立权利要求和真正的核心争点

## Use Figure-Guided Explanations

把附图讲解组织成“图号 + 关注点 + 结论”：

- 先用总体图讲清部件和关系
- 再用局部图讲清关键连接、配合或装配逻辑
- 最后用细节图支撑核心争点

表达时直接说：

- “这部分请结合图 X、图 Y 来看”
- “这里重点看部件 A 与部件 B 的连接关系”
- “这张图主要对应权利要求中的哪一组结构特征”

如果现有案件没有完全对应的图号分层，就按“总体结构 / 关键连接 / 细节特征”重新分组，不要机械套用示例图号。

## Standard Output Structure

默认输出以下结构：

```text
一、开庭陈述
1. 出庭人员介绍
2. 我方主张
3. 请求事项

二、案件分析/正式抗辩
1. 审查基础
2. 本专利方案释明（结合附图）
3. 核心争点一
4. 核心争点二
5. 核心争点三（如有）
6. 核心争点四（如有）
7. 从属权利要求处理
8. 请求人可能观点及备答
9. 审查员可能追问及备答

三、总结陈述
1. 重申审查基础
2. 重申独立权利要求创造性
3. 重申从属权利要求成立
4. 请求维持有效
```

## References

- `references/routing-map.md`
- `references/case-sorting.md`
- `references/case-sorting-prompts.md`
- `references/prompt-templates.md`

当用户需要做“无效过程梳理”，优先读取 `references/case-sorting.md` 和 `references/case-sorting-prompts.md`。
当用户需要可直接复用的口审准备提示词、分步提示词、材料清单或交付检查项时，读取 `references/prompt-templates.md`。
