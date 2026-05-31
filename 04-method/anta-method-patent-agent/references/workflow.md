# Anta Method Workflow

This workflow is only for Anta method patent cases.

## Public routing rule

Use `anta-method-patent-agent` as the only public entry. Route internally to the selected stage. Do not treat the former stage-specific Anta skills as separate public entry points.

## Stage order

1. disclosure analysis
2. disclosure reconstruction
3. core feature analysis
4. inventive-step analysis
5. final disclosure
6. claim layout
7. claims drafting
8. background drafting
9. effects drafting
10. process-detail drafting
11. examples design
12. testing design
13. results analysis

## Dependency rules

- Do not skip from disclosure analysis directly to claims drafting.
- Do not draft formal claims before the final disclosure and core feature logic are fixed.
- Do not draft examples before the process-detail section is fixed.
- Do not draft results analysis before the retained result tables are fixed.
- If the user asks to skip a stage, explain the downstream risk before proceeding.

## Baseline discipline

Each later stage must use the user-confirmed output of the earlier stage as its baseline. If the baseline changes later, downstream work should not be treated as final until the user confirms whether to update it.
