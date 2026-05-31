# OA State Model

Use this file to track the live case state explicitly instead of letting important baselines drift across stages.

## Core state objects

```yaml
current_effective_claim_set:
  status: draft | confirmed
  source: original | amended
  claim_set_scope: text or file reference
  claim_1_text: text

superseded_claim_sets:
  - claim_set_scope: text or file reference
    reason: replaced by later effective claim set

preliminary_diff_snapshot:
  status: absent | draft | superseded
  based_on_claim_set: current claim 1 before amendment decision
  purpose: amendment_decision_only

amendment_decision:
  status: pending | confirmed
  value: amend | not_amend

amendment_path:
  status: absent | candidate | confirmed
  merged_features: list

final_distinguishing_features:
  status: pending | draft | confirmed
  based_on_claim_set: current_effective_claim_set

technical_problem:
  status: pending | draft | confirmed
  based_on_claim_set: current_effective_claim_set

argument_path:
  status: absent | draft | confirmed
  main_line: text
  support_lines: list

draft_output:
  type: none | amended | unamended
  status: none | draft | final
```

## Transition rules

1. Stage 1 may establish the application-side fact baseline without fixing any strategic judgment.
2. Stage 2 may establish the examiner reasoning map without fixing the live claim state.
3. Stages 3 and 4 may establish D1 and Dx findings without fixing the final technical problem.
4. The preliminary difference snapshot may exist before the amendment decision, but it is not the final distinguishing-feature set.
5. Stage 5 may recommend amendment paths, but the amendment decision and final amended claim 1 become live only after confirmation.
6. Once amendment is confirmed, rebuild the full current effective claim set and mark the pre-amendment snapshot as superseded for final-analysis purposes.
7. Final distinguishing features may be fixed only for the current effective claim set.
8. The technical problem may be fixed only after the final distinguishing features for the current effective claim set are fixed.
9. Draft output may be treated as final only after the effective claim set, distinguishing features, technical problem, and required key wording are fixed.

## Invalid states

Treat these as workflow errors and resolve them before continuing:

- `technical_problem.status = confirmed` while `current_effective_claim_set.status != confirmed`
- `final_distinguishing_features.status = confirmed` while it is still tied to a superseded claim set
- `draft_output.type = amended` while `amendment_decision.value != amend`
- `draft_output.type = unamended` while `amendment_decision.value = amend`
- replacement-page generation before the full amended claim set and numbering are fixed

## Stage-to-state map

- Stage 1: populate application-side fact baseline and support tables
- Stage 2: populate office-action reasoning map
- Stage 3: populate D1 findings and Rule-2 pre-check
- Stage 4: populate Dx findings and combination-fit findings
- Stage 5: populate or confirm `amendment_decision`, `amendment_path`, `current_effective_claim_set`, and the amended claim 1 text when applicable
- Stage 6: populate or confirm `final_distinguishing_features`, `technical_problem`, and `argument_path`
- Stage 7 or 8: populate `draft_output`
- Stage 9: validate consistency across all live state objects
