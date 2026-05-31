---
stage_id: 05
stage_key: claim_amendment
requires:
  - current effective claim set
  - preliminary current-claim-1-vs-D1 difference snapshot
  - application support baseline
produces:
  - amendment recommendation
  - amendment path candidates
  - amended claim 1 candidate
confirmation_checkpoints:
  - CP-01
  - CP-02
  - CP-03
---

# Stage 5: Claim Amendment

## Enter this stage when

- the user asks whether claims should be amended
- the OA response needs amendment options and risk analysis

## Required baseline

- current effective claim set
- preliminary current-claim-1-vs-D1 difference snapshot
- D1 and Dx check results if available
- application support baseline

## Task focus

- decide whether amendment is truly needed
- scan dependent claims and preferred features
- compare at least two amendment options
- test support, clarity, added-matter risk, and inventive-step effect

## Deliverable

- amendment-need conclusion
- dependent-claim scan table
- candidate feature ranking
- amendment option comparison
- proposed amended claim text if the user confirms

## Guardrails

- do not amend just to amend
- do not lock the final technical problem in this stage
- treat amendment decision and final amended claim 1 text as confirmation checkpoints
