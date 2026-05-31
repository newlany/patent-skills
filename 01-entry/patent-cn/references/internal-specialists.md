# Internal Specialists

The patent skill library is organized as a small public surface plus internal specialists. Use this file to pick specialists after the public route is already clear.

## Public Surface

Users should normally call only:

- `patent-cn`
- `patent-cn-draft`
- `patent-cn-review`
- `patent-cn-response`
- `patent-cn-doctor`

## Registry

The machine-readable registry is:

```text
/Users/chrynos/.codex/skills/patent-cn-runtime/scripts/specialist_registry.json
```

Use the registry for three things:

- normalize old skill names
- find the correct internal specialist
- distinguish stage specialists from delivery specialists

## Compatibility Entries

These old entry skills remain available for compatibility, but the public route should be used first:

- `patent-entry-drafting` -> `patent-cn-draft`
- `patent-entry-oa-response` -> `patent-cn-response`
- `patent-entry-invalidity` -> `patent-cn-response`

## Retired Names

The directories for these old names should not exist. If an older prompt names one of them, translate the name and continue through the public route:

| retired name | canonical route |
| --- | --- |
| `patent-workflow-router` | `patent-cn` |
| `patent-disclosure-agent` | `patent-cn-draft`, or `patent-stage-disclosure-analysis` for a narrow standalone stage |
| `patent-oa-response` | `patent-cn-response` |
| `patent-invalidity-hearing-prep` | `patent-cn-response`, then invalidity-hearing specialist if needed |
| `patent-application-checker` | `patent-cn-review` |
| `patent-application-correction-docx` | `patent-cn-response`, then `patent-support-correction-docx` |
| `patent-docx-math` | `patent-support-docx-math` |
| `cn-patent-formal-check` | `patent-cn-review`, then `patent-qc-cn-formality` |
| `cn-patent-invention-content` | `patent-cn-draft`, then `patent-stage-invention-content` |
| `download-google-patents-pdfs` | `patent-support-google-patents-pdfs` |
| `deep-research` | `patent-research-records` or `patent-research-topic` |
| `patent-topic-deep-research` | `patent-research-topic` |
| `anta-method-patent-agent` | `patent-cn-draft`, then `patent-method-process-route` when the method-route facts fit |
| `xmu-method-patent-agent` | `patent-cn-draft`, then `patent-method-formula-model` when the formula-route facts fit |

## Specialist Groups

Drafting and disclosure:

- `patent-entry-drafting`
- `patent-stage-disclosure-analysis`
- `patent-stage-prior-art-search`

Method-route specialists:

- `patent-method-route-helper`
- `patent-method-process-route`
- `patent-method-formula-model`
- `patent-method-runtime-boundary`
- `patent-method-boundary-alignment`

Specification-section specialists:

- `patent-stage-invention-content`
- `patent-stage-embodiments`
- `patent-cn-software-embodiment-layout`

Document, communication, drawing, and QC specialists:

- `patent-inventor-questions`
- `patent-external-brief-docx`
- `patent-support-docx-math`
- `patent-drawing-generator`
- `patent-qc-cn-formality`
- `patent-qc-application-consistency`

Response and evidence specialists:

- `patent-entry-oa-response`
- `patent-entry-invalidity`
- `patent-stage-invalidity-hearing-prep`
- `patent-support-correction-docx`
- `patent-support-google-patents-pdfs`
- `patent-analysis-fixed-patent`

Research and handoff specialists:

- `patent-research-records`
- `patent-research-topic`
- `patent-chatgpt-pro-handoff`

Adjacent non-patent tool skills:

- `read-chinese-files`
- `doc`
- `pdf`
- `minimax-docx`
- `yuandian-legal-api`
- `ipeasy-case-fetcher`

Use adjacent tools only after the patent route is known. They do not decide claim scope, amendment strategy, or evidence strategy by themselves.

## Dispatch Rule

Do not ask the user to choose an internal specialist unless:

- route confidence is low
- two specialists would produce materially different claim scope, evidence strategy, or filing output
- the user explicitly asks to use a specific specialist

When a specialist is called inside a case folder, it should obey the runtime discipline:

- log stage events or tool runs
- write `stage-report` JSON for substantial stage work
- register artifacts in `manifest.json`
- leave final status decisions to validation
