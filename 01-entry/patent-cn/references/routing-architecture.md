# Layered Routing Architecture

Use this file as the first routing model for Chinese patent work. It exists to keep the public surface small while still allowing many internal specialists.

## Routing Passes

### Pass 0: Normalize Skill Names

If the user explicitly names an old or compatibility skill, translate it before deciding the workflow.

Check these maps in order:

- `compatibility_entries`
- `retired_aliases`

The maps live in:

```text
/Users/chrynos/.codex/skills/patent-cn-runtime/scripts/specialist_registry.json
```

Do not expose old names as the normal user-facing choice. Use retired aliases only to translate older prompts, then continue through the public route or selected internal specialist.

### Pass 1: Decide The Main Intent

Choose exactly one primary intent:

| intent | public workflow | Use when |
| --- | --- | --- |
| `drafting` | `patent-cn-draft` | New application drafting from a disclosure, invention notes, R&D materials, or a draft technical solution |
| `review` | `patent-cn-review` | Existing application draft or filing package needs QC, consistency check, formal check, or DOCX-sensitive review |
| `response` | `patent-cn-response` | OA, correction notice, replacement pages, invalidity, oral-hearing prep, or fixed cited-reference analysis |
| `research` | `patent-cn` plus research specialist | Standalone record research, topic research, legal-status check, family check, or source-backed patent memo |
| `support` | `patent-cn` plus support or delivery specialist | Standalone document conversion, PDF bundle, client brief DOCX, tool support, or handoff bundle |
| `doctor` | `patent-cn-doctor` | System health, dependency checks, registry checks, tool readiness |

### Pass 2: Select Stage Or Specialist

Only select a specialist after the public workflow is known.

| group | specialists |
| --- | --- |
| Drafting engine | `patent-entry-drafting` |
| Disclosure and search | `patent-stage-disclosure-analysis`; `patent-stage-prior-art-search` |
| Method-route family | `patent-method-route-helper`; `patent-method-process-route`; `patent-method-formula-model`; `patent-method-runtime-boundary`; `patent-method-boundary-alignment` |
| Specification sections | `patent-stage-invention-content`; `patent-stage-embodiments`; `patent-cn-software-embodiment-layout` |
| Review and QC | `patent-qc-cn-formality`; `patent-qc-application-consistency` |
| Response engines | `patent-entry-oa-response`; `patent-entry-invalidity`; `patent-stage-invalidity-hearing-prep`; `patent-support-correction-docx` |
| Evidence and analysis | `patent-analysis-fixed-patent`; `patent-support-google-patents-pdfs` |
| Research | `patent-research-records`; `patent-research-topic` |
| Document and communication support | `patent-inventor-questions`; `patent-support-docx-math`; `patent-drawing-generator` |

### Pass 3: Select The Delivery

Delivery is the artifact format, not the legal workflow.

| delivery need | delivery specialist or route |
| --- | --- |
| Filing application DOCX | `patent-cn` application template rules |
| Inventor or applicant question-list content | `patent-inventor-questions` |
| Inventor or applicant question-list DOCX | `patent-inventor-questions`, then `patent-external-brief-docx` |
| External OA, rejection, or reexamination brief DOCX | `patent-external-brief-docx` after the legal analysis is stable |
| Search-result, correction, invalidity-risk, or filing-strategy brief DOCX | `patent-external-brief-docx` after the relevant workflow is stable |
| Formal OA response statement DOCX | `patent-entry-oa-response` templates under `patent-cn-response` |
| Correction or replacement pages | `patent-support-correction-docx` under `patent-cn-response` |
| Comparison-document PDF bundle | `patent-support-google-patents-pdfs` |
| Figure assets or drawing package | `patent-drawing-generator` |
| ChatGPT Pro handoff bundle | `patent-chatgpt-pro-handoff` |

## Conflict Rules

When a prompt contains both a legal task and a delivery request, the legal task wins first.

Examples:

- “根据审查意见生成给客户的沟通简报 DOCX”：route to `patent-cn-response`, then deliver with `patent-external-brief-docx`.
- “根据交底生成发明人补充问题清单 DOCX”：route to `patent-cn-draft` if disclosure analysis is still needed, draft the content with `patent-inventor-questions`, then deliver with `patent-external-brief-docx`.
- “把这份 Markdown 沟通稿转成 DOCX”：route directly to `patent-external-brief-docx`.
- “检查申请文件并修复格式”：route to `patent-cn-review`; use DOCX specialists only after review intent is clear.

Ask one focused question only when the wrong route would change claim scope, amendment strategy, evidence strategy, or filing-package contents.

## Skill Inventory

Public entries:

- `patent-cn`
- `patent-cn-draft`
- `patent-cn-review`
- `patent-cn-response`
- `patent-cn-doctor`

Internal runtime:

- `patent-cn-runtime`

Internal specialists:

- `patent-entry-drafting`
- `patent-stage-disclosure-analysis`
- `patent-stage-prior-art-search`
- `patent-stage-invention-content`
- `patent-stage-embodiments`
- `patent-method-route-helper`
- `patent-method-process-route`
- `patent-method-formula-model`
- `patent-method-runtime-boundary`
- `patent-method-boundary-alignment`
- `patent-cn-software-embodiment-layout`
- `patent-qc-cn-formality`
- `patent-qc-application-consistency`
- `patent-drawing-generator`
- `patent-support-docx-math`
- `patent-support-correction-docx`
- `patent-entry-oa-response`
- `patent-entry-invalidity`
- `patent-stage-invalidity-hearing-prep`
- `patent-analysis-fixed-patent`
- `patent-support-google-patents-pdfs`
- `patent-research-records`
- `patent-research-topic`
- `patent-chatgpt-pro-handoff`
- `patent-inventor-questions`
- `patent-external-brief-docx`

Retired names handled by `retired_aliases`:

- `patent-workflow-router`
- `patent-disclosure-agent`
- `patent-oa-response`
- `patent-invalidity-hearing-prep`
- `patent-application-checker`
- `patent-application-correction-docx`
- `patent-docx-math`
- `cn-patent-formal-check`
- `cn-patent-invention-content`
- `download-google-patents-pdfs`
- `deep-research`
- `patent-topic-deep-research`
- `anta-method-patent-agent`
- `xmu-method-patent-agent`

Adjacent tool skills may be used after the patent route is chosen:

- `read-chinese-files`
- `doc`
- `pdf`
- `minimax-docx`
- `yuandian-legal-api`
- `ipeasy-case-fetcher`
