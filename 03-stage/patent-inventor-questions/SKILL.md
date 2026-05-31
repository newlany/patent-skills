---
name: patent-inventor-questions
description: "Draft concise Chinese inventor supplement question lists for patent application drafting. Use when Codex must turn a technical disclosure, disclosure-analysis gap, draftability blocker, or 发明人/申请人补充材料需求 into a numbered question list that asks only the key missing facts needed before Chinese patent drafting can proceed; use before patent-external-brief-docx when a DOCX version is requested."
---

# Patent Inventor Questions

## Purpose

Use this skill to write the substantive content of a Chinese patent inventor supplement question list. The goal is not to exhaust every possible curiosity. The goal is to identify the few missing answers without which the case cannot safely enter drafting.

Use `patent-external-brief-docx` only after the Markdown content is ready and the user wants a DOCX communication file.

## Core Principle

Ask a question only when both conditions are met:

1. The answer is needed to draft the application, define the invention boundary, support an effect, or avoid an enablement, support, clarity, or claim-scope risk.
2. The answer cannot be determined from the disclosure, prior case materials, common general knowledge in the field, or a reasonable patent-drafting inference.

If a point can be handled by conventional drafting language, by neutral generic wording, or by an assumption that does not change the technical contribution, do not put it in the inventor-facing list. Record the assumption internally if needed.

## Workflow

1. Reconstruct the draftable invention before asking questions:
   - identify the likely technical problem;
   - identify the core technical solution and the candidate independent-claim features;
   - identify the technical effect chain that the application should support;
   - identify embodiments, parameters, drawings, or experimental facts that appear necessary to support the core route.
2. Build an internal gap list from the disclosure analysis, defect review, search memo, or draft attempt.
3. Filter each gap with the ask-or-not test:
   - ask if the missing fact changes the independent-claim boundary, the necessary feature relationship, or a fallback route;
   - ask if the effect is central but the causal mechanism, data, comparison basis, or test condition is missing;
   - ask if a term, step, component, formula, parameter, or drawing relationship is ambiguous enough that drafting would guess the invention;
   - ask if an embodiment is essential to enable the solution and the implementation cannot be supplied from ordinary technical knowledge;
   - do not ask about background facts, routine implementation details, administrative information, stylistic preferences, or optional variants unless they affect claim drafting.
4. Merge duplicates and remove questions that the agent can answer from the materials.
5. Keep the final list short. Default to 3 to 8 questions. Exceed 10 only when separate draftability blockers truly remain.
6. If no inventor question is necessary, state that no key supplement question is needed and list the drafting assumptions separately for the agent, not as inventor questions.

## Question Style

Write in direct numbered order. Do not divide the final question list into multiple chapters or category headings.

For each item, start with a short quoted source excerpt or a compact context sentence when it helps the inventor locate the issue. Then ask the concrete question.

Preferred pattern:

```markdown
# 需要发明人补充说明的问题清单

以下仅列出需要补充后才能进入撰写阶段的问题。

1. 原文片段：“……”
   问题：这里的“……”具体是指哪一种结构或步骤关系？请补充其与……之间的连接方式，以及该设置带来的直接技术效果。

2. 上下文：交底书说明……，但未说明比较基准。
   问题：请确认该效果是相对于哪一种现有方案得到的；如有测试数据，请补充测试条件和主要结果。
```

Use these rules:

- Ask one issue per numbered item.
- Make each question answerable by the inventor without requiring them to understand patent-law labels.
- Use “请确认”“请补充”“这里是否可以理解为” for a professional and cooperative tone.
- When the source wording is unclear, quote only the unclear phrase or sentence fragment, then explain what must be confirmed.
- When alternatives are likely, offer a small set of choices and ask the inventor to confirm the correct one.
- Avoid broad prompts such as “请详细说明技术方案”“请补充实施例”“请说明技术效果”. Replace them with the exact missing fact.
- Avoid long strings of parallel nouns joined by ideographic commas. If several facts are needed, split the sentence or use semicolons.

## Final Check

Before finalizing, delete any question that fails one of these checks:

- Would a competent patent drafter reasonably infer or draft around this without changing the invention?
- Is this only useful for making the document richer, rather than necessary for starting drafting?
- Does the question ask for every detail of an embodiment instead of the missing claim-support fact?
- Is the answer already present elsewhere in the disclosure, figures, earlier analysis, or user-provided notes?
- Is the wording so general that the inventor will not know what to answer?

The finished list should feel like a short, high-leverage email to the inventor: each question should point to a real obstacle and make clear what answer is needed.
