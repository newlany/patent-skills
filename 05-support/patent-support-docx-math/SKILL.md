---
name: patent-support-docx-math
description: "Internal document-support specialist for patent-oriented DOCX reading, inspection, extraction, and formula-safe handling under patent-cn-draft/review/response. Direct use is allowed for standalone 带公式交底书、OMML/旧公式对象、表格、附图、批注、修订、编号链、版式敏感 Word 文件 tasks. This is not a drafting workflow entry."
---
# Patent DOCX Math

## New Architecture Role

`patent-cn-draft`, `patent-cn-review`, and `patent-cn-response` may call this skill for DOCX/formula fidelity support. Direct use is appropriate only for standalone Word/formula handling tasks or older prompts that explicitly name this skill.

## Skill Position

- 类型：文档支撑 / DOCX and formula fidelity support。
- 中文入口：带公式交底、Word 公式、旧公式对象、修订/批注、表格、编号、版式不能丢。
- 输入：专利交底、权利要求、说明书、OA 文件、补正文档等 `.docx` 或规范化后的 `.doc`。
- 输出：结构检查、公式保真提取、中间稿、风险提示。
- 可服务阶段：交底分析、公式模型案撰写、OA/无效材料读取、DOCX 输出前 QC。
- 边界：不独立决定专利撰写策略；只保证文件结构和公式信息可靠。

## Overview

Use this skill to read or process patent Word documents without losing formula structure. Prefer direct OOXML inspection first, then use visual PDF review only when layout or equation rendering must be checked.

## Workflow

1. Normalize the source format.
   - If the input is `.doc`, convert it to `.docx` before analysis.
   - Do not begin with `txt`, `markdown`, or clipboard-style extraction.
2. Inventory the package and formula burden.
   - Run `scripts/inspect_docx.py <file.docx>` to count equations, tables, drawings, comments, revisions, headers, footers, footnotes, and embedded objects.
   - Use `--json` when you need structured downstream processing.
   - Use `--dump-equations <dir>` when the user cares about exact formula content or numbering.
3. Read only the relevant OOXML parts.
   - Start with `word/document.xml`.
   - Load `word/footnotes.xml`, `word/endnotes.xml`, `word/comments.xml`, and `word/header*.xml` or `word/footer*.xml` only if the summary shows relevant content there.
   - Treat `word/embeddings/oleObject*.bin` as a warning that legacy equation objects or embedded Office content may exist.
4. Extract the requested information while preserving structure.
   - Keep section boundaries, numbering, tables, and formula context.
   - When summarizing, mention whether formulas were present as OMML, embedded objects, or likely images.
   - If revising text, preserve equation locations and references such as `式(1)`, figure numbers, table numbers, and claim dependencies.
   - If you need a readable text intermediate that still preserves formulas, run `scripts/extract_math_markdown.py <file.docx> --output <file.md>` and read the generated Markdown. Pandoc will keep native Word equations as TeX math instead of flattening them into plain text.
5. When a formula-heavy patent deliverable is generated or re-exported as `.docx`, inspect the generated file again with `scripts/inspect_docx.py` to confirm equations were emitted as native Word math objects and that no unexpected embedded objects appeared.
6. Verify the visual result when layout matters.
   - Use `scripts/convert_with_libreoffice.py <file.docx> --to pdf --output-dir <dir>` to export a review PDF.
   - Add `--render-preview` when `pdftoppm` is available and page images are needed.
   - If the task turns into a PDF rendering review, use the `pdf` skill after the PDF is created.

If the document is part of a drafting case folder, keep the machine-readable inspection output as an artifact and register it in `manifest.json`:

```bash
python3 scripts/inspect_docx.py <file.docx> --json > <case-dir>/07_qc/docx-inspection.json
python3 /Users/chrynos/.codex/skills/patent-entry-drafting/scripts/patent_workflow.py add-artifact \
  --case-dir <case-dir> \
  --stage 07_qc \
  --path 07_qc/docx-inspection.json \
  --kind docx-inspection \
  --json
```

## Patent Checks

- Confirm the document type before acting: disclosure draft, claims set, specification, amendment response, or internal note.
- Preserve section headings such as `发明名称`, `摘要`, `技术领域`, `背景技术`, `发明内容`, `附图说明`, `具体实施方式`, and `权利要求书`.
- Check formula numbering and nearby references. Do not rewrite formulas without checking every `式(...)` reference that points to them.
- Check figure and table numbering, especially when formulas refer to variables defined in figure callouts or tables.
- Inspect tracked changes and comments before declaring the text final. Patent review files often hide deletions that plain extraction misses.
- Watch for symbol drift. Greek letters, subscripts, superscripts, and unit strings are easy to damage when copying between formats.
- Treat equations stored as images or legacy OLE objects as high-risk; escalate to visual review and state the limitation explicitly.
- When validating generated `.docx` deliverables, report whether the generated file still contains equations as OMML and whether embedded objects remain at zero or at least did not increase unexpectedly.

## Quick Commands

Inspect a patent DOCX package:
```bash
python3 scripts/inspect_docx.py /path/to/file.docx
```

Write a machine-readable summary:
```bash
python3 scripts/inspect_docx.py /path/to/file.docx --json
```

Extract Markdown while preserving equations as TeX math:
```bash
python3 scripts/extract_math_markdown.py /path/to/file.docx --output tmp/source.formula.md
```

Dump each formula as standalone XML for review:
```bash
python3 scripts/inspect_docx.py /path/to/file.docx --dump-equations tmp/equations
```

Convert a Word file for visual review:
```bash
python3 scripts/convert_with_libreoffice.py /path/to/file.docx --to pdf --output-dir tmp/review --render-preview
```

Normalize an old `.doc` before inspection:
```bash
python3 scripts/convert_with_libreoffice.py /path/to/file.doc --to docx --output-dir tmp/normalized
```

## Editing / Replacing Text

- Do not replace a DOCX paragraph by deleting all original `w:r` children and rebuilding one plain run. That flattens character properties (`w:rPr`) and can change fonts, emphasis, spacing behavior, and reviewer-visible layout.
- Prefer in-place replacement inside existing runs when the changed text is small and run boundaries still make sense.
- For paragraph-level replacement, reuse the source paragraph template: preserve `w:pPr`, keep the original run count and run-level `w:rPr`, preserve inline layout tokens such as page breaks (`w:br w:type="page"`), tabs, line breaks, and `w:lastRenderedPageBreak`, then distribute the new text across existing text runs. Only rebuild a single run when the paragraph is known to have no character-level formatting or inline layout-token needs.
- Refuse or escalate complex paragraphs containing hyperlinks, fields, drawings, equations, comments, or tracked-change markup unless a targeted OOXML edit is designed for those structures. Do not treat page breaks or tabs as discardable text noise.
- Use the bundled helper for repeatable paragraph replacements:

```bash
python3 scripts/replace_docx_text_preserve_runs.py source.docx \
  --output revised.docx \
  --replacements-json replacements.json \
  --strip-match \
  --strict \
  --json
```

`replacements.json` may be either a list of `{ "old": "...", "new": "..." }` objects or an object with `paragraph_replacements`.

## References

- Read `references/patent-workflow.md` for the patent-specific checklist, section patterns, and common failure modes.

## Quality Bar

- Do not claim formula fidelity if the source contains only images or opaque OLE objects.
- Do not paraphrase equations into prose unless the user explicitly asks for interpretation.
- When reporting extracted content, separate confirmed structure from inferred meaning.
- When a document includes formulas and the user requests edits, preserve equation placement and cross-references unless the user approves a structural rewrite.
