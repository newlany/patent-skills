---
name: patent-stage-prior-art-search
description: "Standalone patent prior-art and novelty-search specialist for disclosure-driven search, topic search, known-patent expansion, closest-reference screening, PatSnap/智慧芽 browser-assisted retrieval, and comparison-document PDF packaging."
---
# Patent Prior-Art Search Agent

## Standalone Role

Use this skill directly when the task is 专利查新、现有技术检索、新颖性检索、最接近现有技术筛选、已知专利扩展检索、智慧芽/PatSnap 检索，或对比文件 PDF 下载。

## Skill Position

- 类型：专利检索 / prior-art search。
- 中文入口：查新、检索、最接近现有技术、D1/D2 候选、交底驱动检索。
- 输入：交底分析报告、关键词、技术方案草稿或已重构方案。
- 输出：检索式、最接近现有技术、区别特征压力点、下载的对比文件、对比文件撰写质量评估、检索备忘录。
- 支撑能力：可调用 `patent-support-google-patents-pdfs`、`web-access`、`defuddle`、`pdf`、`spreadsheet`、浏览器自动化能力。
- 边界：不负责最终权利要求撰写；检索结论应以特征对比和风险提示为主。

## Overview

Use this skill as a standalone specialist when the user asks for patent 检索、查新、现有技术筛选 or closest-reference comparison.

It internalizes the workflow that would otherwise be split across document-reading, search, and research-summary skills:

- disclosure file intake and text extraction
- layered search-plan design
- BigQuery patent retrieval
- Google Patents full-text expansion
- PatSnap/智慧芽 browser-assisted retrieval when authorized access is needed
- PatentsView structured US search
- comparison-document packaging as PDF and Markdown
- cited novelty-search memo drafting

## Routing Rule

If the user asks for patent novelty search, prior-art search, closest-reference screening, disclosure-driven retrieval, or whether a disclosure looks novel, use this skill directly.

Do not ask the user to separately invoke document-reading or patent-search utility skills. This skill already owns those steps.

This skill is the preferred specialist for prior-art retrieval. Treat `patent-search` as a lower-level backend, not as the normal user-facing starting point.

## Operating Modes

### 1. Disclosure-driven novelty search

Use when the user provides a `.doc`, `.docx`, `.txt`, `.md`, or similar disclosure file and wants:

- a search plan
- prior-art screening
- closest-reference comparison
- a novelty or inventive-step risk memo

### 2. Topic or keyword prior-art search

Use when the user gives only a technology topic, product concept, feature list, or draft claim direction and wants likely prior art.

### 3. Known-patent expansion search

Use when the user already has one or more patent numbers and wants:

- nearby references
- family expansion
- CPC expansion
- closest-document comparison

### 4. Draft-support search

Use when the search will later support patent drafting rather than ending at a standalone novelty memo.

- First pass: broad current-art baseline scan.
- Second pass: focused recheck after the core technical feature chain stabilizes.

## Startup Rule

Always read:

- [references/workflow.md](references/workflow.md)
- [references/report-template.md](references/report-template.md)
- [references/downloads.md](references/downloads.md)

Also read [references/patsnap-browser-search.md](references/patsnap-browser-search.md) when the user asks for 智慧芽/PatSnap retrieval, when a commercial logged-in search platform is needed, or when the script-first public-data route leaves important Chinese/current-art gaps.

Then use only the specific bundled script needed for the current task.

## Tooling Rule

This skill is self-contained. Prefer the bundled scripts in `scripts/`:

- `extract_disclosure_text.py` for intake and text extraction
- `bigquery_search.py` for worldwide search and CPC discovery
- `google_patents_fetch.py` for low-cost full-text retrieval by publication number
- `patent_search.py` for structured US PatentsView searches
- `download_reference_bundle.py` for packaging selected references into `pdf + md`

Use companion skills only as backends when needed:

- `patent-search` as the low-level search backend
- `patent-support-google-patents-pdfs` as the preferred PDF-download backend
- `browser-harness` for logged-in PatSnap/智慧芽 search through the user's existing browser session
- `playwright` as browser-automation fallback when direct PDF download fails

For Google Patents pages that expose a real `Download PDF` link or `citation_pdf_url`, prefer that direct PDF link before any browser-rendered fallback.

Use the PatSnap/智慧芽 browser path only when the user has access or can complete login interactively. Never ask for, store, or type the user's credentials; if the platform redirects to login, open the login page and pause for the user to sign in.

Use web research only when:

- you need a direct citation URL
- you need to verify current status on a public page
- you need to inspect a patent page or related public source not already covered by the bundled scripts

If the older `patent-search` skill is also installed, treat this skill as the preferred specialist and treat `patent-search` as a lower-level search backend.

## Draft-Support Rule

When the user is not just searching, but preparing to draft a patent application, use this skill as the retrieval checkpoint around the technical-solution refinement work:

1. after disclosure analysis, run a first pass to map the current-art baseline and closest routes
2. use that result to guide which technical branch should be repaired, narrowed, or abandoned in reconstruction
3. after the reconstructed route or candidate claim-1 chain is fixed, run a second pass around that reconstructed scheme
4. only then treat inventive-step judgment and claim drafting as stable enough to continue

For every selected comparison document that may affect drafting, also assess drafting quality using the multi-dimensional rubric in `references/workflow.md`. Applicant/assignee/patentee or inventor strength, including globally known filers such as Huawei, Xiaomi, Nike, Apple, and comparable companies, is only an external provenance signal. Do not mark a reference high quality from provenance alone. Also review claim architecture, problem-solution logic, specification support, terminology stability, drafting expression, and prosecution robustness. If one or more references are high quality, record reusable drafting moves in the search memo or in `02_search/outputs/reference-drafting-quality.md`, then register that artifact as `search-memo` or `drafting-reference`. This is a style and expression handoff to later drafting stages, not permission to copy unsupported technical content.

## Search Workflow

1. If a disclosure file is present, extract operative text first with `scripts/extract_disclosure_text.py`.
2. If the search is feeding patent drafting, explicitly label the pass as:
   - First pass: current-art baseline scan before technical-solution refinement
   - Second pass: focused recheck before inventive-step and claims
3. Compress the disclosure into searchable dimensions:
   - application scene
   - function or performance targets
   - composition or module structure
   - process or manufacturing route
   - unusual reagents, sub-steps, or parameter windows
4. Design a layered search plan before bulk searching:
   - broad scene words
   - scene + performance words
   - high-specificity composition or process anchors
   - CPC or IPC expansion where useful
5. Run discovery through `scripts/bigquery_search.py` first when BigQuery is available.
6. When authorized PatSnap/智慧芽 coverage is requested or public-data retrieval looks thin, run the browser-assisted search path in `references/patsnap-browser-search.md` and record the exact queries, filters, result counts, and selected records.
7. Pull the most relevant publication numbers and expand them with:
   - `scripts/bigquery_search.py get`
   - `scripts/google_patents_fetch.py fetch`
   - `scripts/patent_search.py` for structured US follow-up where useful
8. Select the closest references and package them with `scripts/download_reference_bundle.py` so the output folder includes at least:
   - `*.pdf`
   - `*.md`
9. Evaluate the drafting quality of selected comparison documents and mark any high-quality references that can guide later expression or section organization.
10. Converge on the closest references, then draft the memo using the report contract in `references/report-template.md`.
11. If this is draft-support search rather than a standalone search, close with concrete reconstruction or narrowing advice, not just a hit list.

Prefer JSON mode for orchestration-facing calls:

```bash
python3 scripts/extract_disclosure_text.py <source> --output <case-dir>/01_disclosure/source.txt --json
python3 scripts/bigquery_search.py doctor
python3 scripts/patent_search.py doctor
python3 scripts/download_reference_bundle.py <publication> --save-dir <case-dir>/02_search/references
```

## Setup

From the skill directory:

```bash
cd ~/.codex/skills/patent-stage-prior-art-search
python3 -m venv .venv
.venv/bin/pip install -r scripts/requirements.txt
```

BigQuery self-check:

```bash
.venv/bin/python scripts/bigquery_search.py doctor
```

Reference-package example:

```bash
.venv/bin/python scripts/download_reference_bundle.py US-12424224-B2 --save-dir ./downloads/references
```

PatentsView self-check:

```bash
python3 scripts/patent_search.py doctor
```

## Output Contract

Unless the user asks for a different format, produce:

1. a short search frame
2. the layered search strategy
3. the closest references with links
4. packaged comparison documents for the chosen references, preferably `pdf + md`
5. a feature-focused comparison, not just title matching
6. drafting-quality assessment for selected comparison documents, including high-quality references that may guide later drafting style
7. reconstruction-direction advice for a first pass, or a reconstructed-scheme recheck verdict for a second pass
8. a preliminary novelty or inventive-step risk view
9. uncertainty and next-search suggestions

When a local deliverable is useful, save the memo under the active workspace rather than requiring the user to assemble it manually.

## Boundaries

- This skill is for retrieval and novelty-style comparison, not full application drafting.
- This skill can support patent drafting, but it should not replace claim drafting or specification drafting.
- If the user wants legal-status, litigation, invalidation, or prosecution-history research on a specific patent, this skill may start the search but should narrow into record-first research once the target patent is fixed.

## Resources

- `scripts/extract_disclosure_text.py`: disclosure text extraction for `.doc`, `.docx`, `.txt`, `.md`, and simple `.pdf` cases.
- `scripts/bigquery_search.py`: BigQuery worldwide patent search helper.
- `scripts/google_patents_fetch.py`: Google Patents full-text fetch helper.
- `scripts/patent_search.py`: PatentsView helper for structured US metadata queries.
- `scripts/download_reference_bundle.py`: package selected references into `pdf + md` outputs.
- `references/workflow.md`: end-to-end search workflow and search-loop rules.
- `references/patsnap-browser-search.md`: browser-assisted PatSnap/智慧芽 search path for authorized logged-in retrieval.
- `references/downloads.md`: download rules for PDF/Markdown comparison-document packaging.
- `references/report-template.md`: memo structure and evidence labels.
