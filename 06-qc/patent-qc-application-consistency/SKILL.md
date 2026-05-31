---
name: patent-qc-application-consistency
description: "Internal QC specialist under patent-cn-review and patent-cn-draft for Chinese patent application consistency and drafting-style review. Direct use is allowed for standalone 附图标记、权利要求引用关系、权利要求/说明书一致性、附图说明、术语统一、专利撰写风格检查 and safe-edit tasks."
---
# Patent Application Checker

## New Architecture Role

`patent-cn-review` is the preferred public review orchestrator, and `patent-cn-draft` may call this skill during final drafting QC. This skill is the internal `07_qc` application-consistency specialist. Direct use is appropriate only for standalone consistency-check/safe-edit requests or older prompts that explicitly name this skill.

## Skill Position

- 类型：最终质检 / application consistency QC。
- 中文入口：附图标记检查、权利要求引用关系、说明书一致性、术语统一、撰写风格检查。
- 输入：已有权利要求、说明书、摘要、附图说明或 DOCX 文件。
- 输出：问题清单、安全修改建议、必要时生成修订稿。
- 支撑能力：可调用 `patent-support-docx-math`、`patent-qc-cn-formality`、`doc`、`minimax-docx`。
- 边界：优先检查和局部修复；不要未经要求重写整套申请文件。

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
- **Commercial raw materials**: when examples name suppliers and grades, check that the named grade supports the claimed functional feature. Flag cases where `active hydrogen` is used as if it were `hydroxyl`, `nonvolatile content` is used as if it were `low water`, or a source-backed fact is written too absolutely, such as `水分为无`.
- **Example/comparative basis**: when pigments, color pastes, fillers, additives, or other active components are compared, check whether the document states the normalization basis, such as effective pigment content, active ingredient content, or total addition amount. Flag ambiguous `等量` wording if the conclusion depends on active-component equivalence.
- **Testing tables and analysis**: after a table column or metric is deleted, scan the test methods and results analysis for stale references. Tables should primarily contain measured metrics; process-label columns should be retained only when needed or user-requested.
- **Standards and units**: for Chinese test items, prefer current GB or GB/T standards where available, and check that units and symbols remain consistent, such as `kg/m³` for apparent density.

## Bundled Script

Use the drafting-entry micro-QC script before specialist review when you need quick mechanical checks for headings, abstract length, placeholders, claim citations, figure descriptions, and reference-sign list usage:

```bash
python3 /Users/chrynos/.codex/skills/patent-entry-drafting/scripts/patent_qc_micro.py check input.docx --json
```

Use this skill's script for reference-numeral and consistency-specific operations:

```bash
python scripts/patent_doc_tools.py extract input.docx --json
python scripts/patent_doc_tools.py check input.docx --mapping "皮肤基体=100,出汗孔=101"
python scripts/patent_doc_tools.py add-refs input.docx --output output.docx --scope both --mapping "皮肤基体=100,出汗孔=101"
python scripts/patent_doc_tools.py remove-refs input.docx --output output.docx --scope claims --mapping "皮肤基体=100,出汗孔=101"
```

Prefer explicit `--mapping` for edits. Use `--mapping-json` for larger mappings.

When the check belongs to a drafting case folder, write the JSON result under `07_qc/` and register it:

```bash
python3 /Users/chrynos/.codex/skills/patent-entry-drafting/scripts/patent_qc_micro.py check input.docx \
  --json \
  --output <case-dir>/07_qc/micro-qc.json
python scripts/patent_doc_tools.py check input.docx --mapping-json refs.json > <case-dir>/07_qc/application-consistency.json
python3 /Users/chrynos/.codex/skills/patent-entry-drafting/scripts/patent_workflow.py add-artifact \
  --case-dir <case-dir> \
  --stage 07_qc \
  --path 07_qc/application-consistency.json \
  --kind application-consistency-check \
  --stage-status completed \
  --json
```

## Reporting Format

For checks, return:

- `文件`: path checked.
- `结论`: pass/fail/needs review.
- `确认问题`: each item with section/claim/paragraph and suggested fix.
- `疑似问题`: possible typos or drafting improvements that require human confirmation.
- `已执行修改`: for edit tasks, list the changed file and backup file.

Do not overstate typo detection: mark uncertain wording as `疑似问题`, not as confirmed error.
