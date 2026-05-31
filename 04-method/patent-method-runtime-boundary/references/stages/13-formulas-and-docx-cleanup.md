# Stage 13: Formulas And DOCX Cleanup

## Enter this stage when

- the user asks for stage 13
- the user asks for 公式修复, step numbering cleanup, 图例一致性修复, or DOCX cleanup
- the substantive text baseline is fixed

## Required baseline

- confirmed claim set
- confirmed section drafts
- current `.docx` file if the work is document-based

## Task focus

- preserve native Word math objects where needed
- define variables consistently near the formula or in the same local context
- normalize figure references, figure labels, and step numbering
- remove stale internal labels or stale old-step traces
- validate document package integrity after writeback

## Deliverable

- cleaned formulas or numbering
- cleaned DOCX copy when applicable
- short issue note on any residual limitations

## Guardrails

- do not flatten important formulas to plain text in `.docx` deliverables
- do not overwrite the only working copy unless the user explicitly asks

## Stop rule

Stop after cleanup and wait for confirmation before testing, results, or final synchronization.
