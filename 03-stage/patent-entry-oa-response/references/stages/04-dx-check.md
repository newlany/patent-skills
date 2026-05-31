---
stage_id: 04
stage_key: dx_check
requires:
  - office-action passages citing each Dx
  - original text of each Dx
produces:
  - Dx disclosure findings
  - combination-fit findings
confirmation_checkpoints: []
---

# Stage 4: Dx Check

## Enter this stage when

- the user asks for D2/D3 or Dx 核查
- secondary references must be checked before accepting the combination logic

## Required baseline

- office-action passages citing each Dx
- original text of each Dx
- current feature comparison baseline against D1 if available

## Task focus

- analyze each Dx separately
- check disclosure, same-function use, and combination fit
- mark negative teaching, incompatibility, and hindsight-only combinations
- compare the corresponding Dx feature in its own technical problem, technical route, and effect before using it as a teaching source

## Deliverable

- Dx-by-Dx disclosure table
- function identity table
- D1 + Dx combination difficulty table
- rebuttal point list
- teaching-source conclusion for each Dx: concrete teaching, abstract direction only, different-function disclosure, or no usable teaching

## Guardrails

- shared terminology does not equal shared teaching
- do not stop at disclosure; also test function and combination fit
- if common knowledge is cited instead of a Dx document, require either evidence or a concrete technical explanation tied to the actual technical problem
