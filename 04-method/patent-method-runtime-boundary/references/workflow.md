# General Method Patent Workflow

This workflow is for general Chinese method patent drafting whose main challenge is the runtime step chain, method-boundary clarity, and cross-section synchronization.

## Public routing rule

Use `patent-method-runtime-boundary` as the only public entry. Route internally to the selected stage.

## Stage order

1. disclosure analysis
   mandatory checkpoint A: disclosure-driven prior-art baseline scan
2. disclosure reconstruction
3. method-boundary alignment
4. core-feature analysis
   mandatory checkpoint B: reconstructed-scheme recheck
5. inventive-step analysis
6. final disclosure
7. claim layout
8. claims drafting
9. background drafting
10. invention-content drafting
11. embodiments and examples
12. figures, flowcharts, and legends
13. formulas and DOCX cleanup
14. testing design
15. results analysis
16. abstract and final synchronization

Stages 1 to 5 plus the two mandatory search checkpoints establish the technical baseline, the closest prior-art baseline, the key technical means, and the inventive-step main line. Stages 7 to 12 build the claim set, background, invention content, embodiments, and figure or flowchart output on that baseline.

## Search checkpoint rule

When the workflow is being used for patentability judgment, technical-solution reconstruction, or claim drafting, use [$patent-stage-prior-art-search](/Users/chrynos/.codex/skills/patent-stage-prior-art-search/SKILL.md) as the default search workflow at two points:

- Checkpoint A: after stage 1 and before stage 2, to map the current-art baseline and decide which route still deserves reconstruction
- Checkpoint B: after stages 2 to 4 stabilize the reconstructed route, to test the reconstructed scheme against the closest art before stage 5

Checkpoint A is about choosing a technically and commercially sensible reconstruction direction. Checkpoint B is about deciding whether that reconstructed direction still has a defensible inventive-step main line.

## Dependency rules

- Do not skip from an unstable disclosure baseline directly to formal claims.
- When the task is patentability-oriented, do not start stage 2 until checkpoint A is complete.
- If the disclosure mixes current runtime steps with preconditions or later updates, do not perform claim layout before stage 3.
- Use checkpoint A to decide which branch should be repaired, narrowed, or abandoned before reconstruction is treated as stable.
- Do not start stage 5 until checkpoint B is complete.
- Do not draft claim layout before checkpoint B and stage 5 are both complete.
- Do not draft invention content before the claim baseline is fixed.
- Do not draft embodiments before the claim chain and invention-content main line are fixed.
- Do not finalize figures or abstract before the claim chain is fixed.
- Do not finalize results analysis before the retained test items and retained tables are fixed.
- If checkpoint B changes the closest prior-art route or the distinguishing-feature chain, reopen stages 2 to 5 as needed instead of drafting forward on a stale inventive-step theory.
- If the user asks to skip a stage, explain the downstream risk before proceeding.

## Baseline discipline

Each later stage must use the user-confirmed output of the earlier stage as its baseline. For patentability-oriented work, the confirmed search checkpoints are part of that baseline too. If the baseline changes later, downstream work should not be treated as final until the user confirms whether to update it.

## Typical use patterns

- For a new case with messy disclosure: start at stage 1.
- For a mature case with claim-boundary confusion: start at stage 3.
- For a section rewrite against existing claims: start at stage 8, 9, 10, or 11 as appropriate, but state any missing prerequisite baseline.
- For a document-wide refresh: start at stage 16 after confirming the operative claim chain.
- If formulas, variables, or simulation outputs dominate the case, use the formula-heavy method skill instead.
- If the case is primarily a preparation or manufacturing route with strong example, testing, and results-table dependence, use the process-route method skill instead.
