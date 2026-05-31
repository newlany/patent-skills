---
stage_id: 01
stage_key: case_baseline
requires:
  - current claims
  - specification
  - abstract
produces:
  - application-side fact baseline
  - claim breakdown
  - support tables
confirmation_checkpoints: []
---

# Stage 1: Case Baseline

## Enter this stage when

- the user asks for the application fact baseline
- the OA response has not yet established the application-side facts

## Required baseline

- current claims
- specification
- abstract
- examples, comparative examples, and figures if available

## Task focus

- extract the original technical problem, core solution, effects, and parameter relationships
- break down claims and key support points
- separate directly supported facts from later legal debate points

## Deliverable

- technical case summary
- claim breakdown table
- effect evidence table
- example/comparative example table
- parameter table

## Guardrails

- do not reconstruct the final inventive-step problem yet
- do not invent effects, mechanisms, or parameter functions
