---
stage_id: 07
stage_key: draft_amended
requires:
  - final amended claim set
  - confirmed distinguishing features
  - confirmed technical problem
produces:
  - amended response draft
  - replacement-page output when needed
confirmation_checkpoints:
  - CP-06
---

# Stage 7: Draft Amended Response

## Enter this stage when

- the user asks for 修改后答复
- the amended claim set is already fixed
- a replacement page or formal `.docx` may be required

## Required baseline

- final amended claim set
- confirmed distinguishing features for amended claim 1
- confirmed technical problem wording
- confirmed main response path
- any response template and claims replacement-page template

## Task focus

- draft the amendment section first
- explain why amended claim 1 meets Article 22.3
- keep the body, amended claims, and replacement page fully consistent
- fill the correct template when `.docx` output is required
- use the Stage 6 argument ranking so the strongest chain-break point appears first
- state amendment contribution through supported technical effects, not through bare narrowing

## Deliverable

- full amended response draft
- amendment explanation
- amended inventive-step section
- generated `.docx` and replacement-page `.docx` when required
- Article 22.3 section ordered as: amended claim baseline, distinguishing features, effects, actual problem, no teaching or no motivation, and conclusion

## Guardrails

- keep the distinguishing features matched to amended claim 1 exactly
- use the actual amendment action, not sample template text
- re-check downstream claim numbering after amendment
- do not reuse pre-amendment technical problem wording without re-checking it against the amended claim
- do not describe the amendment as creative unless the added feature contributes to solving the actual technical problem
