# Workflow

## Scope

This workflow is for XMU method-type patent cases with explicit steps, formulas, variables, and Word-based drafting outputs.

## Baseline Rule

Before drafting, identify:

- the technical baseline
  - usually the cleanest disclosure or final technical supplement
- the wording baseline
  - usually the question-answer file or a unified issue memo

If those two baselines conflict, resolve the conflict first and carry one unified wording line into all downstream documents.

## Recommended Stage Order

### 1. Baseline cleanup

Output:

- a unified wording memo or issue-resolution memo

Check:

- variable names
- formula direction
- constraint form
- exit condition
- figure numbering
- material parameter wording

### 2. Claim layout

Output:

- compressed or reorganized claim system

Check:

- no missing core technical chain in claim 1
- merged dependent claims still preserve key formula logic
- numbering and dependencies are valid

### 3. Creativity-oriented claim optimization

Output:

- revised claim 1 and supporting dependent claims

Check:

- claim 1 contains only technical means, not technical effects
- inventive route is moved forward into claim 1
- ambiguous “respectively calculated as” language is closed properly

### 4. Background, summary, effects

Output:

- background
- summary / invention content
- technical effects

Check:

- background explains the traditional route and its gap
- summary mirrors the claims system
- effects explain difference, non-obviousness logic, and stronger effect path

### 5. Detailed embodiment rewrite

Output:

- detailed embodiment rewritten in claim order

Hard rule:

- do not simply keep the disclosure's original `S1-S11` order if it no longer matches the claims

Check:

- claim 1 step chain is the embodiment backbone
- dependent-claim formulas and parameters are inserted at the correct step
- tables, models, sensitivity derivations, and result analysis are restored

### 6. Formula repair

Output:

- formula-corrected DOCX

Check:

- all baseline formulas still exist
- line formulas remain Word math objects
- inline variables that should be math objects are restored
- no accidental flattening into plain text

### 7. Step numbering and flowchart

Output:

- step-labeled embodiment
- optional Mermaid or SVG flowchart

Check:

- numbering follows the current claim logic
- substeps are subordinate to the correct major step

### 8. Final QC

Output:

- final checked draft or issue list

Check:

- formula completeness
- variable consistency
- step numbers
- figure/table references
- no tracked changes or comments if a clean draft is required

## Single-Stage Mode

If the user asks for only one stage:

1. use the latest confirmed document as the working baseline
2. complete the requested stage
3. note briefly which later stages may need to be refreshed

## Frequent Failure Modes

- claim 1 is too abstract and leaves the inventive route in dependent claims
- the embodiment follows disclosure order instead of claim order
- formulas are present in content but displayed as plain text instead of math objects
- effects only state results and do not explain the technical distinction from traditional methods
- figure references are not synchronized with the result-analysis section

