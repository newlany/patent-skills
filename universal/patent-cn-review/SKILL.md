---
name: patent-cn-review
version: 2.0.0
description: |
  Public orchestrator for reviewing Chinese patent application drafts and filing packages.
  Dispatches internal QC and document specialists for formal checks, DOCX/formula checks,
  claim references, reference numerals, consistency, abstract word count, figure descriptions.
  Trigger phrases: "审查", "检查", "QC", "质检", "review", "申请文件检查", "形式审查".
user-invocable: true
allowed-tools:
  - Read
  - Write
  - Edit
  - Bash
  - Grep
  - Glob
  - Agent
---
# CN Patent Review Orchestrator

## Role

Public orchestrator for reviewing Chinese patent application drafts and filing packages.

Use for:
- Formal defect checking (形式缺陷)
- Reference numeral consistency (附图标记)
- Claim/specification consistency
- Abstract word count validation
- Figure description review
- DOCX formula and revision-trace checks

## Review Workflow

```
Step 1: Formal Check (patent-qc-cn-formality)
  INPUT:  application DOCX
  OUTPUT: formal defect report + auto-fixed DOCX

Step 2: Consistency Check (patent-qc-application-consistency)
  INPUT:  claims + specification + abstract
  OUTPUT: consistency issue checklist

Step 3: DOCX/Math Check (patent-support-docx-math)
  INPUT:  DOCX with formulas
  OUTPUT: formula fidelity report

Step 4: Validation (patent_workflow.py validate)
  INPUT:  case directory
  OUTPUT: validation report
```

## Output Protocol

```
CN REVIEW REPORT
- file checked: <path>
- overall status: pass|needs-fix|blocked
- drafting status: <drafting-complete|filing-ready|in-progress>
- confirmed issues: <count>
- suspected issues: <count>
- auto-fix candidates: <count>
- required next action: <action>
```

## Boundaries

- Does NOT rewrite applications
- Does NOT make broad changes without explaining risks
- Reports issues; user decides which to fix
