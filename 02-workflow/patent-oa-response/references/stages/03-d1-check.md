---
stage_id: 03
stage_key: d1_check
requires:
  - office-action passages citing D1
  - original D1 text or a reliable copy
produces:
  - D1 disclosure findings
  - Rule-2 pre-check
confirmation_checkpoints: []
---

# Stage 3: D1 Check

## Enter this stage when

- the user asks for D1 核查
- D1 must be checked against the examiner's attribution

## Required baseline

- office-action passages citing D1
- original D1 text or a reliable copy
- current claim baseline or key feature list

## Task focus

- check each feature the examiner attributes to D1
- extract D1's real technical problem, route, and context
- state which premise for the technical problem D1 lacks

## Deliverable

- D1 disclosure check table
- D1 core concept summary
- D1 vs application difference table
- Rule-2 pre-check

## Guardrails

- "D1 does not mention it" is not enough by itself
- do not write the final inventive-step conclusion yet
