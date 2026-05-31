---
name: patent-qc-cn-formality
description: "Internal QC specialist under patent-cn-review and patent-cn-draft for Chinese patent formal defects under CNIPA preliminary-examination style rules. Direct use is allowed for standalone 形式检查、权利要求编号/引用、句号、摘要字数、章节标题、术语一致、法26形式缺陷、DOCX低风险修复 tasks."
---
# CN Patent Formal Check

## New Architecture Role

`patent-cn-review` is the preferred public review orchestrator, and `patent-cn-draft` may call this skill during final drafting QC. This skill is the internal `07_qc` CN-formality specialist. Direct use is appropriate only for standalone formal-check/fix requests or older prompts that explicitly name this skill.

## Skill Position

- 类型：最终质检 / CN formality QC。
- 中文入口：形式问题、初审式检查、权利要求编号/引用、摘要字数、章节标题、句号、法26形式缺陷。
- 输入：准备提交或已成稿的 Word 申请文件。
- 输出：形式缺陷清单、低风险修复稿、需要人工确认的问题。
- 支撑能力：公式或复杂 Word 文件先用 `patent-support-docx-math`；输出可用 `doc`、`minimax-docx`。
- 边界：不负责创造性主线或实质性保护范围重写。

## Overview

Use this skill to review a Chinese patent application Word file as a filing draft, not as plain prose. Start from the legal/formal requirements, detect which problems are mechanical enough to repair safely, then deliver a corrected `.docx` copy without rebuilding the entire document layout.

## Workflow

1. Normalize the source file.
   - Inspect `.docx` directly.
   - Convert `.doc` to `.docx` first if LibreOffice is available.
2. Inspect the file as an OOXML package.
   - Read section headings, claims, abstract, drawings, tracked changes, and reference-sign patterns.
   - Do not begin with copy-paste text extraction.
3. Classify issues using [formal-rules.md](./references/formal-rules.md).
   - Separate `safe-auto-fix` issues from higher-risk issues.
4. Apply safe fixes with the bundled script.
   - Patch existing XML text nodes in place.
   - Preserve styles, runs, tables, headers, footers, media, and relationships.
5. Re-scan the corrected output.
   - Confirm which issues disappeared.
   - Confirm paragraph count and claim count stayed stable.
6. Escalate when needed.
   - Stop and confirm before any change that could affect claim scope or technical meaning.

## Commands

For fast mechanical preflight on headings, abstract length, placeholders, claim citations, figure descriptions, and reference-sign list usage:

```bash
python3 /Users/chrynos/.codex/skills/patent-entry-drafting/scripts/patent_qc_micro.py check /path/to/file.docx --json
```

Inspect a file:

```bash
python3 scripts/check_patent_formal.py scan /path/to/file.docx
```

Inspect with JSON output:

```bash
python3 scripts/check_patent_formal.py scan /path/to/file.docx --json
```

Apply safe fixes and write a corrected copy:

```bash
python3 scripts/check_patent_formal.py fix /path/to/file.docx --output /path/to/file-formal-fixed.docx
```

For drafting workflow orchestration, use JSON and register the result in the case manifest:

```bash
python3 /Users/chrynos/.codex/skills/patent-entry-drafting/scripts/patent_qc_micro.py check /path/to/file.docx \
  --json \
  --output <case-dir>/07_qc/micro-qc.json
python3 scripts/check_patent_formal.py scan /path/to/file.docx --json > <case-dir>/07_qc/cn-formality-scan.json
python3 /Users/chrynos/.codex/skills/patent-entry-drafting/scripts/patent_workflow.py add-artifact \
  --case-dir <case-dir> \
  --stage 07_qc \
  --path 07_qc/cn-formality-scan.json \
  --kind cn-formality-scan \
  --stage-status completed \
  --json
```

## What The Bundled Script Checks

- title-line label prefixes such as `发明名称：`
- missing or out-of-order standard specification headings
- abstract length over 300 characters
- claim numbering sequence
- dependent claims citing non-existent or later claims
- multi-dependent claims using non-alternative wording
- multi-dependent claims citing other multi-dependent claims
- dependent claims that likely omit the repeated subject name
- dependent claims that fall outside their independent-claim block
- claims containing drawings or embedded objects
- bare reference signs such as `壳体1` when a canonical bracketed form already exists
- reference-sign conflicts across the draft
- promotional or commercial wording in title / claims / abstract
- tracked changes or comments left in the package

## Safe-Fix Policy

Apply safe fixes automatically only when the change is localized, deterministic, and scope-neutral. The bundled script currently auto-fixes these items:

- remove a title label prefix such as `发明名称：`
- normalize a claim's terminal punctuation to a single final `。`
- normalize a bare reference sign to an already-established canonical form such as `壳体（1）`

Do not auto-fix these items without deliberate review:

- claim renumbering
- dependent-claim citation rewrites
- abstract shortening
- terminology substitutions that could alter claim scope
- tracked-change cleanup when the intended final text is unclear

## DOCX Handling Rules

- Prefer OOXML text-node patching over whole-document regeneration.
- Do not use `python-docx` paragraph `.text = ...` on a live filing draft when layout fidelity matters.
- Rebuild the final `.docx` by copying all ZIP parts and replacing only the modified XML.
- If the source contains formulas, OLE objects, or layout-sensitive patent math, switch first to [$patent-support-docx-math](C:/Users/will3/.codex/skills/patent-support-docx-math/SKILL.md).
- If visual verification is possible, use [$doc](C:/Users/will3/.codex/skills/doc/SKILL.md) after the fix pass.

## Output Contract

Produce:

1. a corrected `.docx` file, usually `*-formal-fixed.docx`
2. a concise review summary that says:
   - what was auto-fixed
   - what remains
   - which remaining items were not auto-fixed because they are legally risky

## References

- Read [formal-rules.md](./references/formal-rules.md) before deciding whether a defect is safe to auto-fix.
- Read [workflow.md](./references/workflow.md) when the user wants a corrected Word deliverable rather than only a defect list.
