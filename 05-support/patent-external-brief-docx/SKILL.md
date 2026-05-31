---
name: patent-external-brief-docx
description: "Convert concise Chinese patent external communication Markdown into a polished DOCX using a fixed blue-heading business-brief layout. Use when Codex must generate or convert outward-facing patent communication documents for inventors, applicants, clients, or business/legal decision makers, including inventor question lists, supplemental-material requests, OA communication briefs, rejection-decision analyses, reexamination analyses, search-result briefs, filing-strategy notes, invalidity-risk notes, correction notices, or other client-facing patent reports; use patent-inventor-questions first when substantive inventor question content is not drafted yet."
---

# Patent External Brief DOCX

## Purpose

Use this skill to turn a concise Chinese patent communication draft in Markdown into a clean DOCX for external delivery.

This is a shared layout skill. It does not decide legal strategy, claim scope, amendment strategy, or whether a case is worth pursuing. Produce or stabilize the substantive analysis with the relevant patent workflow first, then use this skill for the outward-facing document package.

For inventor supplement question lists, draft the question content with:

```text
/Users/chrynos/.codex/skills/patent-inventor-questions/SKILL.md
```

Then use this skill to generate and verify the DOCX.

## Suitable Scenarios

Use this fixed brief layout for short to medium external patent communications, including:

- 发明人补充问题清单，补充材料请求，技术交底确认函。
- 申请人沟通说明，例如撰写路线和保护范围建议。是否补实验或补图，也可以写成决策说明。
- 审查意见沟通简报，重点写清主要驳回理由和可争辩点。答复风险与修改建议放在结论部分。
- 驳回决定分析报告，说明复审可能性和复审风险，并给出是否继续的建议。
- 复审分析报告，围绕合议组关注点和可用证据判断成功率，并说明可能的修改方向。
- 查新或检索结果简报，说明最接近现有技术和主要区别，并给出初步新创性风险判断。
- 补正或形式缺陷沟通说明，包括需要客户确认或补交的事项。
- 无效风险或稳定性初步说明，写清核心攻击点和抗辩空间，并提示证据缺口。
- 侵权比对或 FTO 初步沟通摘要，前提是分析结论已经由相应工作流形成。
- 提交前确认清单，例如申请人信息和发明人信息；优先权、附图与委托事项可另列确认。

Use a fuller document-generation skill instead when the output needs formal filing templates, complex tables, tracked changes, comments, native equations, or a long litigation-style report.

## Quick Workflow

1. Draft or receive the communication content in Markdown.
2. Confirm the content is suitable for external delivery: concise, decision-oriented, and free of internal scratch notes.
3. Use `scripts/md_to_docx.py` to generate the DOCX.
4. Run structural checks and render the DOCX to PNG pages.
5. Inspect the rendered pages for layout issues before delivery.

Prefer the bundled Codex Python runtime because it includes `python-docx`:

```bash
PY="/Users/chrynos/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/bin/python3"
SKILL="/Users/chrynos/.codex/skills/patent-external-brief-docx"
"$PY" "$SKILL/scripts/md_to_docx.py" input.md --output output.docx
```

For visual QA, use the Documents renderer when available:

```bash
env TMPDIR=/private/tmp "$PY" /Users/chrynos/.codex/plugins/cache/openai-primary-runtime/documents/26.506.11943/skills/documents/render_docx.py output.docx --output_dir render-check
```

If that exact renderer path is stale, locate the current `render_docx.py` under `/Users/chrynos/.codex/plugins/cache/openai-primary-runtime/` or use the active Documents skill instructions.

## Markdown Contract

Use this compact structure:

```markdown
# 驳回决定简要分析及复审建议

案号：56885
申请号：202210074403.5
发明名称：一种基片转运装置
申请人：厦门大学；嘉庚创新实验室
日期：2026年5月20日

## 一、结论摘要

正文段落。

## 二、主要理由

正文段落。

## 三、建议处理方式

正文段落。
```

Supported Markdown features:

- `#` title.
- `##` main section heading.
- `###` subheading.
- compact metadata lines such as `案号：...`, `申请号：...`, `发明名称：...`, `申请人：...`, `客户：...`, `主题：...`, `日期：...`, and `答复期限：...`.
- normal paragraphs.
- simple `-` / `*` bullets and `1.` numbered items.
- inline `**bold**`.

Keep the draft concise and readable. Prefer prose paragraphs and short lists over dense tables. If the communication has many comparison dimensions, put only the conclusion and key basis in this brief, and keep heavy analysis in the underlying work product.

## Writing Discipline

- Write for the external recipient, not for the internal agent.
- Keep conclusions early. If the document supports a decision, state the recommendation before the detailed basis.
- Remove internal labels such as “推断”, “信息缺失”, “stage”, “artifact”, or raw workflow notes unless the user explicitly wants them preserved.
- Do not overstate certainty. Use measured wording when the analysis depends on incomplete facts or examiner discretion.
- For inventor question lists, do not expand the list beyond the key blockers identified by `patent-inventor-questions`.
- Avoid dense strings of ideographic commas in Chinese prose. Use short sentences, semicolons, or natural connectors when several facts must appear together.

## Fixed Layout

The style tokens are documented in `references/layout.md`. Do not redesign the document unless the user explicitly asks. The default layout is a compact formal business brief: centered dark-blue title, blue rule, compact gray metadata, blue section headings, black left-aligned body text, 1 inch margins, and no footer/page-number furniture by default.

If a case needs a formal patent filing template, replacement pages, tracked changes, or equation-heavy DOCX handling, use the relevant patent or DOCX support skill instead.

## Output Discipline

- Save final DOCX files under the case folder's `输出/定稿/` when working inside a patent case folder.
- Keep Markdown/process drafts under `输出/过程/`.
- Register generated external DOCX files in `manifest.json` if the case uses a manifest.
- Always run at least structural checks: `file`, `unzip -t`, and text extraction with `textutil` when available.
- Render and inspect page PNGs before saying the DOCX is ready.
