---
stage_id: 02
stage_key: review_breakdown
requires:
  - office action text
produces:
  - issue matrix
  - evidence map
  - reasoning chain
confirmation_checkpoints: []
---

# Stage 2: Review Breakdown

## Enter this stage when

- the user asks for 审查意见拆解
- the office action must be restored into a reasoning map before rebuttal

## Required baseline

- full office action text
- claim set under examination if available
- cited-reference list if available

## Task focus

- split the office action into issue units
- separate conclusions, evidence, and actual reasoning
- restore D1, Dx, distinguishing-feature, technical-problem, and combination logic chains
- for Article 22.3 issues, write the examiner's chain in order: closest prior art, D1 disclosure, alleged differences, actual technical problem, secondary source, and motivation conclusion

## Deliverable

- issue matrix
- ground-object-evidence table
- inventive-step reasoning chain
- weak-spot list
- Article 22.3 chain-break candidates, labeled as fact error, feature error, problem error, teaching error, common-knowledge gap, combination obstacle, or hindsight risk

## Guardrails

- do not jump straight to rebuttal drafting
- flag missing pages, unsupported assertions, and conclusion-only statements
