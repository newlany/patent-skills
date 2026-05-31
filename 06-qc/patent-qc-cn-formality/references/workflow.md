# Workflow

Use this workflow when the user wants a corrected Word deliverable, not only a defect list.

## Default Path

1. Normalize the source.
   - If the input is `.docx`, inspect it directly.
   - If the input is `.doc`, convert it to `.docx` first.
2. Inspect the DOCX package.
   - Inventory sections, claims, abstract, drawings, tracked changes, and reference-sign pairs.
   - Build a defect list with rule IDs from `formal-rules.md`.
3. Split issues into three buckets.
   - `safe-auto-fix`: deterministic text fixes with no scope impact.
   - `manual-but-deterministic`: the agent can repair after reviewing context, but the bundled script does not auto-apply it safely by default.
   - `needs-user-confirmation`: any fix that could change claim scope, terminology, or technical meaning.
4. Apply safe fixes by patching existing DOCX XML text nodes.
   - Do not rebuild the entire file with `python-docx` when the user wants formatting preserved.
5. Re-scan the corrected copy.
   - Verify that the auto-fixable issues dropped.
   - Confirm that paragraph count and claim count stayed unchanged.
6. If rendering tools are available, perform visual review.
   - Convert to PDF or page images and verify that no layout damage was introduced.

## Recommended Commands

Scan:

```bash
python3 scripts/check_patent_formal.py scan /path/to/file.docx
```

Machine-readable scan:

```bash
python3 scripts/check_patent_formal.py scan /path/to/file.docx --json
```

Apply safe fixes:

```bash
python3 scripts/check_patent_formal.py fix /path/to/file.docx --output /path/to/file-formal-fixed.docx
```

## DOCX Editing Strategy

Prefer this order of operations:

1. Patch `word/document.xml` text nodes in place.
2. Preserve all non-targeted parts exactly as they are.
3. Re-zip the DOCX with the modified `word/document.xml`.
4. Avoid resetting paragraph runs unless it is unavoidable.

Use `python-docx` only for generating synthetic test files or for very small helper tasks. Do not use paragraph `.text = ...` on a live user document when format fidelity matters.

## When To Pull In Other Skills

- Use [$patent-support-docx-math](C:/Users/will3/.codex/skills/patent-support-docx-math/SKILL.md) when the source contains formulas, OLE objects, or layout-sensitive patent math.
- Use [$doc](C:/Users/will3/.codex/skills/doc/SKILL.md) when a visual render is required and the environment can convert DOCX to PDF/images.

## Output Contract

Deliver these artifacts unless the user asks for less:

1. A corrected `.docx` copy, typically named `*-formal-fixed.docx`.
2. A concise issue report summarizing:
   - what was auto-fixed
   - what remains
   - which remaining items were not auto-fixed because they could affect legal scope

## Escalation Triggers

Stop and confirm with the user before finalizing if any of the following remain:

- claim renumbering is needed
- dependent-claim citation clauses need rewriting
- abstract shortening requires deletion or paraphrase
- terminology conflicts could change technical meaning
- tracked changes leave uncertainty about which text version is intended
