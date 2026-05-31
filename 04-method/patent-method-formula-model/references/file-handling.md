# File Handling

## DOCX handling rules

For formula-heavy and model-driven method cases, DOCX integrity matters because formulas, inline math, and section order are part of the deliverable quality.

Hard rules:

- preserve Word math objects whenever possible
- do not flatten formulas into Markdown or plain Unicode text unless the user explicitly wants a text extraction
- when the embodiment is rebuilt, verify both formula content and formula display form
- prefer outputting a new DOCX instead of overwriting the only baseline file

## When to use bundled scripts

Use scripts when the task is structurally repetitive or fragile in OOXML.

### `scripts/file_inventory.py`

Use for initial case inventory.

Example:

```text
python file_inventory.py <case-root> <output-md>
```

### `scripts/docx_paragraph_patch.py`

Use for targeted paragraph-text rewrites such as:

- claim renumbering
- one-claim clarity fix
- summary sentence replacement

Inputs:

- input docx
- output docx
- JSON config containing paragraph index and replacement text

### `scripts/docx_section_copy.py`

Use when copying a section from one DOCX into another while preserving formulas and embedded objects.

Typical use:

- copy detailed embodiment from the clean technical baseline into the application draft

### `scripts/docx_inline_math_patch.py`

Use when inline variables or formulas should be Word math objects rather than plain text.

Typical use:

- repair `x_e`, `P`, `η`, `σPN≤σy`, `f_m(X)=M_f` style inline expressions

### `scripts/docx_step_labeler.py`

Use after the embodiment structure is already correct and you only need to add `S1`, `S2.1` style labels.

### `scripts/docx_formula_audit.py`

Use to compare the baseline draft with the current draft and check for missing formulas.

Typical use:

- after rewriting the embodiment
- after formula display repair

## Practical QC sequence

For formula-heavy method drafts, this order is safer:

1. complete the substantive rewrite
2. run formula completeness audit
3. repair inline math display issues
4. add step labels
5. do one final manual visual pass

## Quality checklist

Before finishing a DOCX task, check:

- are all baseline formulas still present?
- are formulas in the correct logical position?
- are inline variables displayed as math objects where they should be?
- are figure and table references synchronized with the current structure?
- if a clean draft was requested, are comments and tracked changes removed?
