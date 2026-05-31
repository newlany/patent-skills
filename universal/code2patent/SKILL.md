---
name: code2patent
version: 2.0.0
description: |
  Extract technical implementation evidence from code repositories, generate technical disclosure documents,
  and produce near-filing-ready Chinese invention patent materials. Bridges the gap between "code is done"
  and "ready for patent attorney". Trigger phrases: "代码转专利", "code to patent", "代码专利化",
  "从代码生成专利", "代码交底".
user-invocable: true
allowed-tools:
  - Read
  - Write
  - Edit
  - Bash
  - Grep
  - Glob
  - Agent
  - AskUserQuestion
---
# Code to Patent Pipeline

## Role

Extract technical implementation evidence from code repositories and produce Chinese invention patent materials.

## Inputs

Required (at least two):
- Code files/project directory
- Technical descriptions
- Innovation point descriptions
- Candidate patent schemes

Optional:
- Technical field, application scenarios, figure preferences
- Target jurisdiction, applicant info, inventor candidates

## Output Levels

| Level | Output |
|-------|--------|
| L1 | Scheme-code evidence mapping table |
| L2 | Technical disclosure document |
| L2.5 | Claim layout card + claim-code evidence matrix |
| L3 | Invention patent draft (specification + claims + abstract + self-check) |
| L4 | Candidate patentable scheme list |

## Workflow

```
Step 1: Code Analysis
  INPUT:  code files + technical description
  OUTPUT: L1 evidence mapping table

Step 2: Disclosure Generation
  INPUT:  L1 + innovation points
  OUTPUT: L2 technical disclosure document

Step 3: Claim Layout
  INPUT:  L2 + patent scheme
  OUTPUT: L2.5 claim layout card + evidence matrix

Step 4: Patent Draft
  INPUT:  L2.5
  OUTPUT: L3 full patent draft + self-check table
```

## Templates

- `templates/invention-patent-disclosure-template.md`
- `templates/invention-patent-claim-layout-template.md`
- `templates/invention-patent-claim-evidence-matrix-template.md`
- `templates/invention-patent-draft-template.md`
- `templates/invention-patent-draft-self-check-template.md`

## Boundaries

- Self-contained; does NOT require other patent skills
- Produces draft materials, not filing-ready documents
- After L3, route to `patent-cn-draft` for full drafting workflow
