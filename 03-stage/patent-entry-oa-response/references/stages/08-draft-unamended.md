---
stage_id: 08
stage_key: draft_unamended
requires:
  - current effective unamended claim set
  - confirmed distinguishing features
  - confirmed technical problem
produces:
  - unamended response draft
confirmation_checkpoints:
  - CP-06
---

# Stage 8: Draft Unamended Response

## Enter this stage when

- the user asks for 不修改答复
- the user has decided to defend the existing claims
- a formal unamended draft is required

## Required baseline

- current effective unamended claim set
- confirmed distinguishing features for current claim 1
- confirmed technical problem wording
- confirmed main argument path
- any unamended response template

## Task focus

- state clearly that no amendment is made
- keep the entire analysis tied to the current claims
- draft a focused main argument with no amendment fallback
- fill the correct template when `.docx` output is required
- identify the examiner's strongest chain-break point and lead with it
- defend only features already present in the current claims, using the specification only for interpretation and effects

## Deliverable

- full unamended response draft
- explanation for not amending
- inventive-step section for current claim 1
- generated `.docx` when required
- Article 22.3 section ordered as: current claim baseline, distinguishing features, effects, actual problem, no teaching or no motivation, and conclusion

## Guardrails

- do not smuggle new features or parameters into the argument
- do not drift into amendment-based fallback language
- keep the technical problem aligned with the current claims
- do not rely on a technical effect that the current claim does not support
- do not use broad praise of the invention as a substitute for breaking the obviousness chain
