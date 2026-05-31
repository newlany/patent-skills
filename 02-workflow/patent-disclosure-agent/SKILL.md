---
name: patent-disclosure-agent
description: Run the Chinese patent technical-disclosure workflow when the user wants the full disclosure-analysis process or any single stage such as the technical disclosure analysis report, defect review, logic reconstruction, or inventor follow-up questions. Trigger this one skill even when the user asks only for `01_技术交底分析报告`, `02_技术交底逻辑重构与缺陷审查报告`, `03_需要发明人补充说明的问题清单`, or a disclosure-analysis `.docx` export.
---

# Patent Disclosure Agent

## Overview

Use this skill to turn a technical disclosure into a repeatable analysis workflow with persistent output documents. This is now the only public entry for the disclosure-analysis bundle. The stage outputs for analysis report, defect review, and inventor follow-up questions are internalized in this skill rather than exposed as separate public skills.

## Public entry rule

If the user asks for any one disclosure-analysis stage, stay inside this skill and route internally. Do not split the disclosure bundle back into separate public stage skills.

## Trigger phrases

- 技术交底分析
- 交底书分析
- disclosure analysis report
- defect review
- disclosure defect review
- inventor follow-up questions
- 需要发明人补充说明的问题
- 01_技术交底分析报告
- 02_技术交底逻辑重构与缺陷审查报告
- 03_需要发明人补充说明的问题清单

## Operating modes

1. Full workflow mode
   - create or refresh the output bundle
   - produce `01` to `03` in order
   - export `.docx` copies when the disclosure is formula-heavy or layout-sensitive
2. Single-stage mode
   - route to the requested internal stage only
   - keep earlier and later stages unchanged unless the user asks for a refresh
3. Export or refresh mode
   - the Markdown bundle already exists
   - export `.docx` files or revise one specific stage without rerunning the whole workflow

## Stage loading rule

Always read:

- `references/workflow.md`
- `references/routing-map.md`
- `references/output-contracts.md`

Then read only the stage file needed for the current request from `references/stages/`.

## Workflow

1. Confirm the source disclosure material. If it is a `.doc` or `.docx` patent-style Word file, especially with formulas or layout-sensitive content, use `$patent-docx-math` before extracting text.
2. Create the output bundle with `python3 scripts/init_output_bundle.py --source <path-or-label> [--output-dir <dir>]`.
3. If the user provides earlier case analyses, issue memos, inventor question lists, or style reference documents from the same project, read them before finalizing `03_需要发明人补充说明的问题清单.md`. Use them to avoid repeated questions and to match the requested writing style.
4. Fill the generated documents in this order:
   - `01_技术交底分析报告.md` by following `references/stages/01-analysis-report.md`
   - `02_技术交底逻辑重构与缺陷审查报告.md` by following `references/stages/02-defect-review.md`
   - `03_需要发明人补充说明的问题清单.md` by following `references/stages/03-supplement-questions.md` and applying `$patent-inventor-questions` for the substantive question content.
5. For formula-heavy or layout-sensitive disclosures, export the Markdown bundle to `.docx` with `python3 scripts/export_markdown_bundle.py --output-dir <dir>`.
6. After exporting formula-heavy deliverables, run `$patent-docx-math` inspection on the generated `.docx` files to confirm native Word equation objects were produced.
7. Update `00_交底分析任务索引.md` after each step so the folder reflects what has been completed and what is still pending.

## Workflow discipline

- Keep one disclosure project per output folder.
- Treat the three stage outputs as one coordinated bundle.
- Preserve original terminology, formulas, figure numbers, and step numbering when they affect meaning.
- Mark unsupported content as `信息缺失` or `需发明人确认`.
- Mark non-explicit reasoning as `推断`.
- Do not expose the former stage skills as public routes again.

## Output Convention

- Keep one disclosure project per output folder.
- Use the generated Markdown files as the editable working drafts for each step.
- For disclosures containing formulas, tables, or detailed figure references, treat the `.docx` copies as the formal deliverables to share.
- Unless the user explicitly asks otherwise, the formal deliverables are the three report files `01` to `03`; the index file stays as Markdown.
- When a report needs to reproduce formulas, write them in TeX math syntax inside the Markdown draft so Pandoc can emit native Word equations during export.
- Do not overwrite an existing document unless the user asks for regeneration or you pass `--force` to the helper script.
- Mark unsupported content as `信息缺失` or `需发明人确认`. Mark non-explicit reasoning as `推断`.
- If the user provides a precedent issue document or asks to follow an existing file's style, mirror that file's numbering, section structure, and tone rather than forcing the default template layout.

## Resources

- `scripts/init_output_bundle.py`: create the output folder and document skeletons.
- `scripts/export_markdown_bundle.py`: convert the working Markdown bundle into `.docx` deliverables.
- `references/workflow.md`: detailed execution rules for the end-to-end workflow.
- `references/routing-map.md`: single-stage routing for `01` to `03`.
- `references/output-contracts.md`: bundle-level writing and handoff rules.
- `references/stages/01-analysis-report.md`: stage guidance for `01`.
- `references/stages/02-defect-review.md`: stage guidance for `02`.
- `references/stages/03-supplement-questions.md`: stage guidance for `03`.
- `references/invocation-template.md`: reusable prompt template for calling this agent workflow.
- `assets/templates/`: markdown templates for the generated documents.
