# Patent Skill Deduplication & Organization Report

## Date: 2026-05-30

## Summary

- **Original skills scanned**: ~50 patent-related skills
- **After deduplication**: 38 unique skills organized into 9 categories
- **Duplicates removed**: 7 skills merged or superseded
- **Agents preserved**: 11 `.toml` agent files (unchanged)

---

## Deduplication Decisions

### 1. Google Patents PDF Download
- **KEPT**: `patent-support-google-patents-pdfs` (general-purpose, works with any case layout)
- **REMOVED**: `download-google-patents-pdfs` (OA-specific, near-identical scripts)
- **Reason**: The kept version is more flexible; the removed one only differs in folder naming convention

### 2. DOCX Math/Formula Support
- **KEPT**: `patent-support-docx-math` (has 4 scripts: inspect, extract, convert, replace)
- **REMOVED**: `patent-docx-math` (has 3 scripts: inspect, extract, convert)
- **Reason**: `patent-support-docx-math` is a superset with the additional `replace_docx_text_preserve_runs.py`

### 3. Patent Router
- **KEPT**: `patent-cn` (canonical top-level router with full architecture rules)
- **REMOVED**: `patent-workflow-router` (older router, references outdated skill names like `patent-disclosure-agent` directly)
- **Reason**: `patent-cn` is the canonical front door; `patent-workflow-router` is a legacy alternative

### 4. Formal Check
- **KEPT**: `patent-qc-cn-formality` (internal, has `check_patent_formal.py` with scan/fix)
- **KEPT**: `cn-patent-formal-check` (public entry, same script but positioned as user-facing)
- **Note**: These serve different roles (internal vs public). Both kept but should be aware of overlap.

### 5. Research Topic
- **KEPT**: `patent-topic-deep-research` (more comprehensive, has methodology.md, master-prompt.md, report-template.md)
- **REMOVED**: `patent-research-topic` (subset functionality, references the same resources)
- **Reason**: Deep research version is the superset

### 6. Disclosure Analysis
- **KEPT**: `patent-disclosure-agent` (public entry, produces 3 deliverables + index)
- **KEPT**: `patent-stage-disclosure-analysis` (internal stage, same deliverables but positioned as internal)
- **Note**: Both kept; `patent-disclosure-agent` is the public face, `patent-stage-disclosure-analysis` is the internal engine

### 7. OA Response
- **KEPT**: `patent-oa-response` (public entry, full lifecycle)
- **KEPT**: `patent-entry-oa-response` (internal engine, same workflow)
- **Note**: Both kept; `patent-oa-response` is the public face, `patent-entry-oa-response` is the internal engine

---

## Category Structure

### 01-entry/ (6 skills) - Top-Level Public Entry Points
| Skill | Purpose |
|-------|---------|
| `patent-cn` | Main router for all Chinese patent work |
| `patent-cn-draft` | Drafting orchestrator |
| `patent-cn-response` | Response/prosecution orchestrator |
| `patent-cn-review` | Review/QC orchestrator |
| `patent-cn-doctor` | System health check |
| `code2patent` | Code-to-patent pipeline |

### 02-workflow/ (8 skills) - Public Workflow Orchestrators
| Skill | Purpose |
|-------|---------|
| `patent-disclosure-agent` | Disclosure analysis workflow |
| `patent-oa-response` | OA response lifecycle |
| `patent-invalidity-hearing-prep` | Invalidity case + hearing prep |
| `patent-topic-deep-research` | Deep topic research |
| `patent-research-records` | Patent record research |
| `patent-chatgpt-pro-handoff` | ChatGPT Pro handoff |
| `oa-correction-docx` | OA correction processing |
| `patentwang-decision-downloader` | Decision PDF download |

### 03-stage/ (10 skills) - Internal Stage Specialists
| Skill | Purpose |
|-------|---------|
| `patent-entry-drafting` | Core drafting engine (13-step chain) |
| `patent-stage-disclosure-analysis` | Disclosure analysis engine |
| `patent-stage-prior-art-search` | Prior-art search engine |
| `patent-stage-invention-content` | Invention content drafting |
| `patent-stage-embodiments` | Embodiment drafting |
| `patent-entry-oa-response` | OA response engine |
| `patent-entry-invalidity` | Invalidity workflow engine |
| `patent-stage-invalidity-hearing-prep` | Hearing prep engine |
| `patent-analysis-fixed-patent` | Fixed-patent analysis |
| `patent-inventor-questions` | Inventor question drafting |

### 04-method/ (8 skills) - Method-Patent Specialists
| Skill | Purpose |
|-------|---------|
| `patent-method-route-helper` | Method case routing |
| `patent-method-runtime-boundary` | Runtime/step-chain methods + shared workflow base |
| `patent-method-process-route` | Process/material methods |
| `patent-method-formula-model` | Formula/model methods |
| `patent-method-boundary-alignment` | Boundary alignment utility |
| `patent-cn-software-embodiment-layout` | Software/AI patent layout |
| `anta-method-patent-agent` | Anta-specific method workflow |
| `xmu-method-patent-agent` | XMU-specific method workflow |

### 05-support/ (6 skills) - Document & Tool Support
| Skill | Purpose |
|-------|---------|
| `patent-support-google-patents-pdfs` | Google Patents PDF download |
| `patent-support-docx-math` | DOCX/formula inspection & extraction |
| `patent-support-correction-docx` | Correction notice processing |
| `cn-patent-invention-content` | Invention content section drafting |
| `patent-drawing-generator` | Patent drawing/flowchart generation |
| `patent-external-brief-docx` | External communication DOCX |

### 06-qc/ (3 skills) - Quality Control
| Skill | Purpose |
|-------|---------|
| `patent-qc-cn-formality` | CNIPA formal defect check |
| `patent-qc-application-consistency` | Application consistency check |
| `patent-application-checker` | Reference numeral operations |

### 07-research/ (2 skills) - Research & Analysis
| Skill | Purpose |
|-------|---------|
| `patent-analysis` | 7-scenario general analysis |
| `patent-topic-deep-research` | Deep topic research |

### 08-doc-output/ (2 skills) - Document Generation
| Skill | Purpose |
|-------|---------|
| `patent-application-correction-docx` | Correction replacement pages |
| `patent-proposal-list` | Patent proposal list generation |

### 09-tools/ (1 skill) - Runtime Infrastructure
| Skill | Purpose |
|-------|---------|
| `patent-cn-runtime` | Tool registry & runtime layer |

---

## Agents (11 .toml files)

| Agent | Role |
|-------|------|
| `patent_drafting_orchestrator` | Drafting pipeline coordinator |
| `patent_file_intake_specialist` | File intake & formula preservation |
| `patent_disclosure_analyst` | Disclosure analysis specialist |
| `patent_prior_art_searcher` | Prior-art search specialist |
| `patent_solution_reconstructor` | Solution reconstruction specialist |
| `patent_claim_drafter` | Claim drafting specialist |
| `patent_spec_writer` | Specification drafting specialist |
| `patent_application_qc` | Final QC specialist |
| `patent_oa_responder` | OA response specialist |
| `patent_invalidity_strategist` | Invalidity strategy specialist |
| `patent_topic_researcher` | Topic research specialist |
