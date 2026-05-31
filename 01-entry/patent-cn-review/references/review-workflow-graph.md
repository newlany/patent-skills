# Review Workflow Graph

Use this graph for Chinese patent application draft review.

## Standard Review Graph

```text
case/runtime intake
-> DOCX/package inspection
-> micro-QC
-> CN formality scan
-> application consistency scan
-> support/coverage review when needed
-> safe fixes only if requested or clearly authorized
-> validation-report
```

## Internal Specialists

| Review Area | Internal Specialist | JSON Artifact |
|---|---|---|
| DOCX formulas, OLE, tracked changes, comments, layout risk | `patent-support-docx-math` | `记录/07_质检/报告/docx-inspection.json` |
| deterministic headings/abstract/claim citation/figure checks | `patent_qc_micro.py` | `记录/07_质检/报告/micro-qc.json` |
| CNIPA-style formal defects and safe fixes | `patent-qc-cn-formality` | `记录/07_质检/报告/cn-formality-scan.json` |
| reference numerals, figure signs, terminology, claim/spec consistency | `patent-qc-application-consistency` | `记录/07_质检/报告/application-consistency.json` |
| package state and hard/soft fails | `patent_workflow.py validate` | `输出/定稿/验证报告.md` |

## Safe-Fix Policy

Only auto-fix:

- deterministic punctuation/format defects
- title label prefixes
- established reference-sign normalization
- local DOCX XML text-node changes that preserve layout

Do not auto-fix without confirmation:

- claim scope
- claim dependencies that change legal dependency structure
- abstract shortening that may remove technical substance
- terminology substitutions
- tracked changes where final accepted text is unclear

## Filing-Ready Gate

Filing-ready requires:

- final DOCX/package artifacts
- DOCX inspection complete
- CN formality and consistency checks complete
- validation has no hard fail and no soft fail
- official filing-channel assumptions have been verified when relevant
