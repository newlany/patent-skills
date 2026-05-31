---
name: patent-proposal-list
description: Generate fixed-format Chinese patent project proposal lists from patent-mining materials, disclosure folders, project reconstruction reports, extracted drawings, stage reports, or existing proposal-list DOCX/Markdown. Use when Codex needs to produce a customer-facing 专利提案清单, IPR版提案清单, 可写案件清单, 项目专利布局评估稿, or project-level list of patent proposals with overview table, original-disclosure mapping, technical problem, key technical means, technical effect, and figures; use when the user asks to standardize the layout, format, or content of such proposal lists.
---

# Patent Proposal List

## Purpose

Use this skill to turn a Chinese patent project mining folder into a customer-facing patent proposal list. The output is the project proposal package itself, not an inventor supplement list and not an IPR question list.

The reference format is the "专利提案清单_IPR版" style: a concise title page heading, a proposal overview table, and per-proposal technical content.

## Source Sweep

Build the proposal baseline before writing.

Prefer these sources when present:

- Final or near-final proposal artifacts under `输出/定稿/`, especially filenames containing `IPR版`, `提案清单`, `可写案件清单`, or `申请方案`.
- Proposal-generation scripts under `记录/*/工具运行/`, especially scripts that define proposal data and DOCX style.
- Reconstruction outputs under `输出/过程/`, especially `项目全部技术方案重整.md`, `系列分析与专利挖掘报告.md`, report images, and supplemental schematics.
- Stage reports under `记录/*/报告/` for split, merge, mapping, and validation decisions.
- Original disclosures only when the refined proposal package leaves a material gap.

When a DOCX and a script differ, treat the user-named DOCX as the format baseline, and treat the script as an implementation reference.

## Workflow

1. Identify proposal candidates.
   - Do not mechanically follow original disclosure numbers.
   - Split a disclosure when it contains multiple independent inventive concepts.
   - Merge supplement points into a proposal when they solve the same technical problem and strengthen the same claim route.
   - Split derivative routes when their airflow path, module structure, or claim boundary is materially different.
2. Order proposals by technical system layer, from larger system architecture to local details.
3. For each proposal, prepare the required case fields:
   - serial number;
   - original disclosure number;
   - original disclosure name;
   - scheme layer;
   - current proposal name;
   - application type, left blank unless the user asks to fill it;
   - table-level key technical means;
   - one-paragraph summary;
   - technical problem;
   - 3 to 5 key technical means;
   - main technical effect;
   - optional figures with captions.
4. Write the proposal list using `references/fixed-output-spec.md`.
5. For Markdown, start from `assets/proposal-list-template.md`.
6. For DOCX, create a proposal JSON file and run `scripts/build_proposal_list_docx.py`.

## Fixed Output Rules

Load `references/fixed-output-spec.md` before drafting the final list or generating DOCX. Follow it for:

- exact section order;
- overview table columns;
- per-proposal section headings;
- customer-facing cleanup rules;
- DOCX page setup, fonts, table widths, and image-caption style.

The customer-facing proposal list must not include generation dates, work directories, processing notes, AI references, script names, or internal stage labels. Keep `申请类型` blank unless the user explicitly asks for application-type suggestions.

## DOCX Builder

Use the bundled script for repeatable DOCX generation:

```bash
python3 /Users/chrynos/.codex/skills/patent-proposal-list/scripts/build_proposal_list_docx.py data.json output.docx
```

The JSON schema and a sample are described in `references/fixed-output-spec.md` and `assets/proposal-list-data.example.json`.

After generating a DOCX, render or inspect it when possible. At minimum, extract the paragraph and table structure to confirm:

- one title and subtitle;
- `一、提案总览`;
- one 7-column overview table;
- `二、提案技术内容`;
- each proposal contains `技术问题`, `关键技术手段`, and `主要技术效果`;
- figures render where image paths are provided.

## Chinese Style

- Avoid long strings of terms joined by `、`. Use short sentences or semicolons when more than three items are listed.
- Keep the wording like a professional patent-layout evaluation document: direct, technical, and not chatty.
- Do not over-explain common patent drafting concepts. The value is in proposal selection, boundaries, and traceable technical content.
