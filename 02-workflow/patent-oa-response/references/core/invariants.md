# OA Invariants

These rules are workflow invariants. Preserve them in every mode and every stage.

## Source priority

- Original source text beats examiner summaries.
- When the office action is the main input and case-folder copies produced by [$download-google-patents-pdfs](../../../download-google-patents-pdfs/SKILL.md) are available, prefer those copies before falling back to examiner excerpts.
- Cite the basis for each key point by source layer: application, office action, D1, Dx, or common knowledge.

## Claim-state discipline

- Keep a strict distinction between:
  - the preliminary current-claim-1-vs-D1 difference snapshot used to judge amendment need
  - the final distinguishing features for the current effective claim set
- Keep the current effective claim set separate from any superseded claim set.
- If the effective claim set changes, treat any final distinguishing-feature set, technical problem, or argument path tied to the old claim set as stale until re-checked.

## Technical-problem discipline

- Do not lock the actual technical problem before the effective claim set is fixed.
- Derive the actual technical problem from the effects of the final distinguishing features for the current effective claim set.
- Do not write distinguishing features into the technical problem.

## Inventive-step discipline

- Analyze inventive step against the current effective claims only.
- Apply the seven-rule check only after the current effective claim set is fixed.
- If a rule is weak, say so directly instead of padding the draft.

## Amendment discipline

- Do not amend just to amend.
- Any amendment must be checked for support, clarity, and added-matter risk.
- If amendment is adopted, fix the final amended claim 1 and rebuild the full current effective claim set before treating later outputs as final.
- If claim numbering or dependency changes, re-check all downstream references before drafting or rendering.

## Drafting and rendering discipline

- Give the conclusion first, then the basis.
- Prefer stable intermediate deliverables before full drafting.
- Keep the current effective claims, distinguishing features, technical problem, and final draft mutually consistent.
- If amendments are adopted and the user has provided a claims replacement-page template, generate the replacement-page `.docx` automatically after the amended claim set is fixed.
