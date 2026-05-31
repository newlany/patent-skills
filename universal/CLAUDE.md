# Chinese Patent Workflow - Global Rules

## Entry Point

ALL patent work MUST enter through the `patent-cn` skill. Never call internal skills (`patent-entry-*`, `patent-stage-*`, `patent-method-*`, `patent-support-*`, `patent-qc-*`) directly.

## Workflow Invariants

1. **Stage ordering is mandatory**: Disclosure Analysis -> Prior-Art Search -> Solution Reconstruction -> Claims -> Specification -> QC. No stage may be skipped.
2. **Manifest is truth**: Every artifact must be registered in `manifest.json`. The manifest IS the case state.
3. **Validation before completion**: Never declare `drafting-complete` or `filing-ready` without running `patent_workflow.py validate`.
4. **Template compliance**: All 意见陈述 DOCX must use the mandated template. All application DOCX must use `专利撰写模板文件.docx`.
5. **Chinese naming**: All human-readable files use Chinese names. English only for tool contracts, JSON keys, and script-expected names.
6. **Lazy directory creation**: Only create the immediate parent directory of the file being written.
7. **Stop at uncertainty**: When route confidence is low, ask one focused question. Do not guess.

## Completion Terms (Exact Only)

| Term | Meaning |
|------|---------|
| `drafting-complete` | All draft-stage artifacts exist, no hard-fail |
| `filing-ready` | Final DOCX/package present, no hard or soft fail |
| `blocked` | Cannot proceed, needs user input |
| `needs-fix` | QC found issues that must be resolved |

NEVER use: "ready", "done", "complete", "finished" without the exact prefix.

## Directory Layout

```
<case-folder>/
  00_case_status.md
  00_case_events.jsonl
  manifest.json
  输出/
    过程/<中文阶段名>/
    定稿/
  记录/
    <中文阶段名>/
      报告/
      工具运行/
```

## Chinese Drafting Style

- Avoid dense strings of ideographic commas (概念一、概念二、概念三、概念四)
- Prefer splitting sentences, using semicolons, or natural connectors (和、以及、并且)
- Keep dense ideographic-comma wording only for quoted source text, formal names, or table entries

## Search-To-Drafting Carryover

For selected comparison documents, evaluate drafting quality across:
- Technical fit, claim architecture, problem-solution logic, specification support
- Drafting expression, prosecution robustness, external provenance

High-quality references may be used as style/expression aids. Never copy unsupported technical content.
