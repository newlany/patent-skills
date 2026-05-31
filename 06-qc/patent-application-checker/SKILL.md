---
name: patent-application-checker
description: Review and edit Chinese patent application documents for reference numerals, claim/specification consistency, formal defects, formatting errors, and specification drafting style. Use when the user asks to add or remove patent reference numerals, check claim citation relationships, check drawing descriptions and reference-sign usage, proofread patent application formatting, or evaluate whether the embodiments/specification are drafted in a proper patent style.
---

# Patent Application Checker

Use this skill for Chinese patent application files, especially `.docx` drafts containing `权利要求书`, `说明书`, `附图说明`, `主要附图标记说明`, and `具体实施方式`.

## First Choice Tools

- For `.docx` editing, use `minimax-docx` when available. Preserve formatting and change only the requested sections.
- If the DOCX skill environment is unavailable, use the bundled `scripts/patent_doc_tools.py` as a fallback for text extraction, reference-numeral operations, and initial checks. Always keep a backup before writing a `.docx`.
- For non-DOCX text or Markdown, operate directly on the text and cite edited files in the final response.

## Reference Numeral Rules

- Source the term-number mapping from `主要附图标记说明` when present. If absent or incomplete, infer from drawings only with user confirmation, or ask for the mapping when the edit would be risky.
- Add claim reference numerals with full-width parentheses: `皮肤基体（100）`.
- Add embodiment/specification reference numerals without parentheses: `皮肤基体100`.
- Do not add numerals to abstract, title, background, technical field, or claims/spec sections outside the user-requested scope unless explicitly requested.
- Do not number purely functional or abstract terms unless they are listed as drawing reference signs or clearly correspond to a structural element.
- Avoid double numbering. Treat `术语（100）`, `术语(100)`, and `术语100` as already numbered when operating in the relevant section.
- When removing numerals, remove both claim-style `（100）`/`(100)` and embodiment-style trailing numbers after known structure terms, without deleting numeric ranges such as `2cm至5cm`.

## Default Workflow

1. Preview or extract the document text.
2. Identify sections: `权利要求书`, `说明书`, `附图说明`, `主要附图标记说明`, `具体实施方式`.
3. Build or confirm the reference-sign mapping.
4. Perform the requested operation:
   - `标号`: add numerals in claims and/or embodiments according to the rules above.
   - `去除标号`: remove numerals from requested sections.
   - `检查格式`: run punctuation, duplicate-word, spacing, and obvious typo checks.
   - `检查形式错误`: run claim citation, figure-description, and reference-sign checks.
   - `检查说明书撰写方式`: inspect whether embodiments first summarize all components, then describe each component in order.
5. Validate the output. For DOCX, ensure the file opens or passes a zip/package check, then preview the affected section.
6. Report concise results with locations and suggested fixes. Separate confirmed errors from possible issues.

## Check Categories

Read `references/checklists.md` for detailed criteria. In short:

- **Reference numerals**: claims use parentheses; embodiments do not.
- **Formatting**: duplicate punctuation, repeated words, extra words, inconsistent punctuation, suspicious spaces, obvious OCR/typing artifacts.
- **Claim citation form**: later claims may only use `所述X` for terms introduced in the cited earlier claim or its citation chain.
- **Drawings**: every `图N` actually included or referenced should be described in `附图说明`; every drawing reference sign should appear in the application text.
- **Embodiment drafting style**: a good embodiment starts with a total structure statement such as `包括A、B和C`, then describes A, B, C in the same logical order.

## Bundled Script

Use the script for deterministic first-pass operations:

```bash
python scripts/patent_doc_tools.py extract input.docx
python scripts/patent_doc_tools.py check input.docx --mapping "皮肤基体=100,出汗孔=101"
python scripts/patent_doc_tools.py add-refs input.docx --output output.docx --scope both --mapping "皮肤基体=100,出汗孔=101"
python scripts/patent_doc_tools.py remove-refs input.docx --output output.docx --scope claims --mapping "皮肤基体=100,出汗孔=101"
```

Prefer explicit `--mapping` for edits. Use `--mapping-json` for larger mappings.

## Reporting Format

For checks, return:

- `文件`: path checked.
- `结论`: pass/fail/needs review.
- `确认问题`: each item with section/claim/paragraph and suggested fix.
- `疑似问题`: possible typos or drafting improvements that require human confirmation.
- `已执行修改`: for edit tasks, list the changed file and backup file.

Do not overstate typo detection: mark uncertain wording as `疑似问题`, not as confirmed error.
