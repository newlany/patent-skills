# Anta Output Contracts

Every Anta stage output should be self-contained enough for the next stage to use without re-reading the entire source package.

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
- If a revised baseline makes later work stale, say so directly.

## Writing rules

- Keep the technical main line consistent across stages.
- Keep legal and technical reasoning aligned.
- Prefer authorization-oriented narrowing over decorative breadth.
- Separate facts, reasonable technical completion, and points still needing user confirmation.
