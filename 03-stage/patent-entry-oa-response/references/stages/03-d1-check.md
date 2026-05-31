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
- distinguish direct and unambiguous disclosure from examiner inference or after-the-fact reconstruction

## Deliverable

- D1 disclosure check table
- D1 core concept summary
- D1 vs application difference table
- Rule-2 pre-check
- D1 improvement-start assessment: whether D1 objectively faces the same actual technical problem

## Guardrails

- "D1 does not mention it" is not enough by itself
- do not write the final inventive-step conclusion yet
- do not treat a possible modification of D1 as D1's existing disclosure
