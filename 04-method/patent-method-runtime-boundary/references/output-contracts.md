# General Method Patent Output Contracts

Every stage output should be self-contained enough for the next stage to use without re-reading the full source package.

## Standard stage handoff

When returning a completed stage, use this structure:

1. stage deliverable
2. baseline used
3. key assumptions or unresolved points
4. recommended next stage
5. direct confirmation request

## Baseline rules

- Always state which confirmed earlier-stage output was used.
- If the user skipped a prerequisite stage, state that the baseline is provisional.
- If the work is patentability-oriented, stage 2 should identify whether Search Checkpoint A was used, and stage 5 should identify whether Search Checkpoint B was used.
- If a revised baseline makes later work stale, say so directly.

## Writing rules

- Keep the technical main line consistent across stages.
- Keep the closest prior-art baseline and the technical main line consistent across stages.
- Keep the method boundary consistent across claims, specification, abstract, and figures.
- Distinguish disclosed facts, reasonable technical completion, and points still needing user confirmation.
- Prefer authorization-oriented narrowing over decorative breadth, especially when a search checkpoint shows a branch is already crowded.

## DOCX rules

When the deliverable is a Word file:

- create a new copy unless the user explicitly asks to overwrite
- if a bundled or user-provided template is part of the workflow, create the new copy from that template
- preserve the template's existing font, size, spacing, headers, footers, and other non-body formatting
- when filling a template, replace only the requested body sections unless the user explicitly asks for broader edits
- report the output path
- report the checks performed
- mention any warnings or residual limitations
