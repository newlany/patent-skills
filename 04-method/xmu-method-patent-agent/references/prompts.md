# Prompt Templates

Use these as reusable prompt skeletons. Replace placeholders with the current case data.

## Baseline unification

```text
Please read the following files and output a unified wording memo for this XMU method patent case:
1. <technical baseline docx>
2. <wording baseline docx>
3. <optional analysis outputs>

Requirements:
1. Identify conflicts in variables, formulas, constraints, figure numbering, and exit conditions.
2. Give one final wording line for each conflict.
3. Distinguish substantive issues from formatting issues.
4. End with a short list of wording rules that should govern all later drafting.
```

## Claim layout compression

```text
Please compress and reorganize the claims for this XMU method case.

Requirements:
1. Keep only <target count> claims.
2. Preserve the full technical route in claim 1.
3. Merge dependent claims only where the logic is adjacent and the formula chain remains intact.
4. Explain which original claims were merged into which revised claim.
```

## Claim 1 inventive-route optimization

```text
Please optimize the current claim set and strengthen claim 1 for inventive-step support.

Requirements:
1. Claims may recite only technical solution features, not technical effects.
2. Move the real inventive technical route into claim 1.
3. Close any open loop in claim 1 around objective function, constraint, sensitivity analysis, and variable update if those are essential.
4. Fix any clarity issues such as circular definitions or mismatched “respectively calculated as” wording.
```

## Background drafting

```text
Please draft the background section for this XMU method patent case in CN patent style.

Inputs:
- case topic: <topic>
- references: <reference patents or folder>

Requirements:
1. Introduce the engineering context.
2. Explain the conventional method route.
3. State what the conventional route can control.
4. State what it still cannot balance or quantify.
5. End by introducing the problem addressed by this case.
```

## Effects drafting

```text
Please redraft the technical effects section.

Requirements:
1. Explain how the present route differs from traditional methods.
2. Explain why that difference is not a routine extension of the traditional route.
3. Explain why the difference produces stronger technical effects.
4. Keep the style as patent-specification effects drafting, not OA argumentation.
```

## Detailed embodiment rewrite

```text
Using <technical baseline> and <wording baseline> as the final disclosure baseline, rewrite the detailed embodiment in the application draft.

Requirements:
1. The embodiment must follow the current claim 1 step sequence, not the original disclosure order.
2. Restore all key formulas, tables, models, derivations, and result analysis from the baseline draft.
3. Do not omit any formula.
4. Place each formula under the correct step and logical position.
5. If needed, output a new DOCX draft directly.
```

## Formula display repair

```text
Please check the current DOCX for formula-display defects.

Requirements:
1. Check both line formulas and inline symbols.
2. If baseline content was wrongly left as plain text where it should be a math object, convert it to the correct format.
3. Do not blindly copy baseline formatting mistakes.
4. Output a corrected draft and summarize the repaired ranges.
```

## Final completeness check

```text
Please compare the current final draft against the baseline draft and confirm:
1. whether all formulas are preserved
2. whether the embodiment order now matches the claims
3. whether any inline variables still need to be restored as math objects
4. whether the effects section now explains difference, non-obvious path, and significant effect
5. whether figures, tables, steps, and variables are consistent throughout
```

