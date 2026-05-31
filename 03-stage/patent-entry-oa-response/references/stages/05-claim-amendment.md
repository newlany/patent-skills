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
- prefer amendment features that materially contribute to the actual technical problem, not merely features that narrow the claim text
- check whether each candidate feature changes the distinguishing-feature set, the technical effect, and the teaching analysis

## Deliverable

- amendment-need conclusion
- dependent-claim scan table
- candidate feature ranking
- amendment option comparison
- proposed amended claim text if the user confirms
- contribution-risk note for each candidate feature: strong contribution, scope-only narrowing, unsupported effect, or added-matter risk

## Guardrails

- do not amend just to amend
- do not lock the final technical problem in this stage
- treat amendment decision and final amended claim 1 text as confirmation checkpoints
- do not use a feature as the main Article 22.3 anchor if the specification cannot connect it to a technical effect or to the problem being solved
