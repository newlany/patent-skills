---
name: patent-support-correction-docx
description: "Internal response-support specialist under patent-cn-response for Chinese patent correction notices and replacement-page DOCX generation. Direct use is allowed for standalone 补正通知书、替换页、权利要求书替换页、说明书替换页、摘要替换页 and layout-preserving DOCX edit tasks."
---
# Patent Application Correction DOCX

## New Architecture Role

`patent-cn-response` is the preferred public response orchestrator. This skill is the internal correction-DOCX and replacement-page support specialist. Direct use is appropriate only for standalone correction/replacement-page tasks or older prompts that explicitly name this skill.

## Skill Position

- 类型：补正文档支撑 / correction DOCX support workflow。
- 中文入口：补正通知书、替换页、权利要求书/说明书/摘要替换页、保留格式修改。
- 输入：补正通知书和原申请文件 Word。
- 输出：修正文档、替换页、修改说明。
- 支撑能力：优先配合 `patent-support-docx-math`、`doc`、`minimax-docx`。
- 边界：不处理普通 OA 创造性答复；若涉及审查意见实体答复，转 `patent-entry-oa-response`。

Use this skill to turn a 补正通知书 plus the original application files into corrected patent-application deliverables and replacement pages.

## Companion Skills

- Use `minimax-docx` for direct DOCX editing and structural OOXML operations.
- Use `patent-support-docx-math` before editing when the file may contain formulas, tracked changes, numbering chains, tables, comments, drawings, or other patent-sensitive structure.
- Use `doc` when you need rendered page images or visual QA after the edits.

Do not flatten the working DOCX into plain text first unless you are only creating a temporary reading aid. The working source of truth stays in `.docx`.

## Inputs

Expect one or more of the following:

- A 补正通知书 in `.docx`, `.doc`, or `.pdf`
- The original application files in `.docx` or `.doc`
- A single combined application DOCX, or separate DOCX files for 权利要求书, 说明书, 摘要, or 附图说明

Normalize `.doc` to `.docx` before analysis. If the notice is not already in Word format, extract its required corrections first, then perform all document edits against `.docx`.

## Workflow

### 1. Normalize and Inventory

Create a working folder and keep the originals untouched.

- Normalize legacy `.doc` files to `.docx`.
- Run `patent-support-docx-math/scripts/inspect_docx.py` on the notice and each editable application DOCX when structure risk is non-trivial.
- Determine whether the application is:
  - one combined DOCX, or
  - separate DOCX files for claims/specification/abstract.

### 2. Extract Correction Items From the Notice

Convert the notice into a short structured fix list before touching the application.

Use this schema:

| Field | Meaning |
| --- | --- |
| `item_id` | Stable identifier such as `BZ-01` |
| `notice_quote` | Short quote or paraphrase of the补正要求 |
| `target_part` | `claims`, `specification`, `abstract`, `drawings`, or `multiple` |
| `target_span` | Claim number, paragraph range, heading, or unknown |
| `defect_type` | Such as `dependency-error`, `antecedent-basis`, `support-basis`, `numbering`, `terminology`, `formal-layout` |
| `required_action` | What must change to eliminate the defect |
| `allowed_scope` | Smallest safe edit scope |
| `blocker` | `none`, `ambiguous`, or a short risk note |

If issue classification or edit scope is unclear, read `references/correction-playbook.md`.

### 3. Edit the Original Application Minimally

Apply the smallest set of changes that cures the noticed defect.

Mandatory rules:

- Preserve original wording unless the noticed defect requires a change.
- Preserve original formatting, numbering, line breaks, tables, figure references, and equation placement.
- Do not add new matter that lacks support in the original application.
- Do not silently repair unrelated drafting defects while doing a补正 task.
- If the notice is ambiguous and multiple legally different fixes are possible, stop and surface the ambiguity instead of guessing.

Preferred editing order:

1. Fix the directly noticed defect.
2. Sync dependent text that must change because of that fix.
3. Re-check the affected part for secondary breakage caused by the edit.

Examples:

- A claim dependency error: fix the parent-claim reference, then verify the dependency chain and claim numbering still work.
- A missing antecedent basis: repair the earliest valid basis using already disclosed terminology; if no disclosed basis exists, stop and report the support gap.
- A specification-reference mismatch caused by a claim edit: update only the mirrored passages that must stay consistent with the corrected claim wording.

### 4. Decide Which Replacement Pages Are Required

Generate replacement pages only for the parts that actually changed.

- If only the claims changed, output `权利要求书替换页.docx`.
- If the specification changed, output `说明书替换页.docx`.
- If the abstract changed, output `摘要替换页.docx`.
- If both claims and specification changed, output both replacement-page files.

If the user provides a replacement-page template, always use the template as the output base and fill only the corrected target part into the template body.

If the working files are already separated by part, the replacement page is still generated from the template, not by blindly renaming the corrected source file.

If the working file is a combined application DOCX, extract only the changed target part and render that content into the template body.

### 5. Fill Replacement-Page Templates

Use `scripts/extract_replacement_pages.py` with `--template` for replacement-page generation.

Template rules:

- `权利要求书替换页模板.dotx` receives only the corrected claims content.
- `说明书替换页模板.dotx` receives only the corrected specification text content.
- Do not carry over abstract pages, claims pages, or standalone figure pages into the specification template output.
- Keep the template header, footer, page setup, and fixed formatting unchanged.
- Use the corrected application DOCX as the content source and the template DOTX as the package base.

Common commands:

```bash
python scripts/extract_replacement_pages.py combined.docx --list-sections
python scripts/extract_replacement_pages.py corrected.docx --start-index 6 --end-index 23 --template 权利要求书替换页模板.dotx --output 权利要求书替换页.docx
python scripts/extract_replacement_pages.py corrected.docx --section specification --start-index 23 --template 说明书替换页模板.dotx --output 说明书替换页.docx
```

If the section headings are non-standard, override the range manually:

```bash
python scripts/extract_replacement_pages.py corrected.docx --start-index 18 --end-index 67 --template 权利要求书替换页模板.dotx --output 权利要求书替换页.docx
python scripts/extract_replacement_pages.py corrected.docx --start-text "权利要求书" --end-text "说明书" --template 权利要求书替换页模板.dotx --output 权利要求书替换页.docx
```

Template-fill rules:

- Copy the edited content from the corrected DOCX, not from the pre-edit original.
- Preserve the selected body content at the OOXML block level instead of retyping it.
- Preserve the template package structure by cloning the template and replacing only its `word/document.xml` body content plus the DOTX main content type needed for DOCX output.
- Keep only the target claims or specification body in the output; do not let unrelated sections appear.
- In specification mode, trim trailing standalone figure-label pages unless the user explicitly asks to keep them.

### 6. Validate Before Delivery

Before handing over the final files:

- Confirm every noticed defect has a corresponding fix item and status.
- Re-check claim dependencies, antecedent basis, and terminology consistency in the edited range.
- Confirm there are no unintended tracked changes or comments in the deliverables unless the user explicitly asked to keep them.
- Use `doc` or LibreOffice rendering if layout fidelity matters or if the notice concerns formatting.
- Confirm each replacement-page DOCX contains only the changed target part and still opens correctly in Word.
- Confirm template-derived outputs still preserve the template header and footer titles.

## Output Contract

Deliver three kinds of artifacts when the task is completed:

- Corrected working DOCX file or files
- Replacement-page DOCX file or files for the changed parts
- A short change log that maps each notice item to the document change

Prefer concise file naming:

- `权利要求书替换页.docx`
- `说明书替换页.docx`
- `摘要替换页.docx`
- `补正处理说明.md`

## Escalate Instead of Guessing

Stop and ask the user when any of the following appears:

- The notice requires content that is not clearly supported by the original application.
- Multiple claim-reference repairs are possible and they lead to different technical scope.
- The original file structure is corrupted, heavily redlined, or section boundaries cannot be identified reliably.
- The notice and the original application use inconsistent terminology and you cannot map the target passage with high confidence.

## References

- Read `references/correction-playbook.md` when you need the defect-to-fix decision rules.
