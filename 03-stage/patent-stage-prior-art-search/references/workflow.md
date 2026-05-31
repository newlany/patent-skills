# Workflow

## 1. Intake

Work file-first when a disclosure document is present.

Use:

```bash
python3 scripts/extract_disclosure_text.py <path-to-disclosure>
```

If the file is old `.doc`, let the bundled script handle `textutil` first and `soffice` fallback when needed.

Do not classify the technology only from the file name. Read the operative content first.

## 2. Feature Compression

Reduce the disclosure into five search buckets:

1. application scene
2. performance goals
3. core composition or module structure
4. process route or manufacturing window
5. unusual sub-components, reagents, or numerical windows

Use these buckets to build search strings instead of pasting the full disclosure into a query.

## 2A. Drafting-Gate Checkpoints

When the downstream goal is patent drafting, technical-solution reconstruction, or inventive-step assessment, use this skill twice instead of only once:

### Checkpoint A. Current-art baseline scan

Run this after disclosure analysis and before reconstruction.

Inputs:

- disclosure analysis output
- operative disclosure text
- any explicit narrowing direction from the user

Goals:

- identify the closest current technical routes
- surface novelty and inventive-step pressure early
- decide which branches are worth reconstructing and which should be narrowed or abandoned

### Checkpoint B. Reconstructed-scheme recheck

Run this after the reconstructed disclosure, method boundary, or candidate claim-1 feature chain stabilizes.

Inputs:

- reconstructed disclosure
- fixed method-boundary decision if relevant
- candidate claim-1 feature chain or core-feature report

Goals:

- search around the reconstructed scheme rather than the raw disclosure
- identify the closest route to the reconstructed scheme
- test combination risk, common-knowledge risk, and additive-improvement pressure before inventive-step judgment

## 3. Layered Search Plan

Run search in layers, not all at once:

### Layer A. Scene discovery

Use generic scene words first:

- `鞋材`
- `鞋底`
- `鞋垫`
- `中底`
- `跑鞋`

### Layer B. Scene + effect

Add target functions:

- `高回弹`
- `高弹性`
- `透湿`
- `透气`
- `抗菌`
- `防臭`

### Layer C. High-specificity anchors

Add only the most differentiating technical anchors:

- base polymer pair or trio
- named antibacterial route
- special prepolymer route
- special nano-filler or modified cellulose route
- narrow process-window features if they look distinctive

### Layer D. Classification expansion

If discovery references stabilize around one cluster, expand by CPC or IPC to catch semantic neighbors.

## 4. Retrieval Sequence

Prefer this order:

1. `scripts/bigquery_search.py search` for broad worldwide retrieval
2. `scripts/bigquery_search.py cpc` if classification expansion is needed
3. `scripts/bigquery_search.py get` for full record pull
4. PatSnap/智慧芽 browser-assisted retrieval when the user asks for it, logged-in commercial coverage is available, or the public-data route leaves obvious gaps; see `references/patsnap-browser-search.md`
5. `scripts/google_patents_fetch.py fetch` for low-cost claims/description retrieval
6. `scripts/patent_search.py` when US-only structured metadata or assignee/inventor narrowing helps
7. `scripts/download_reference_bundle.py` after the closest references are selected and need `pdf + md` packaging

## 4A. PatSnap/智慧芽 Browser Pass

Use this pass as a complement to the script-first public-data route, not as an opaque replacement. Before opening the browser, compress the disclosure into 3-5 concise Chinese/English query expressions. During the browser run, record:

- the actual entry URL used
- whether the user was already logged in or completed login interactively
- each query expression and filter
- result count, sort order, and date/jurisdiction limits
- selected publication numbers or application numbers
- exported file paths, screenshots, or copied record fields saved under the active case folder

If login, CAPTCHA, SSO, or account permissions block progress, stop and ask the user to complete that step in the browser. Do not request or handle passwords, cookies, session tokens, or other secrets.

## 5. Search Loop

Use an iterative narrowing loop:

1. broad discovery
2. review top 5-15 references
3. identify repeated terms and routes
4. tighten the next queries around the real differentiators
5. stop when new results become repetitive and the closest-reference set stabilizes

Do not treat a single search hit as enough. A novelty search should converge through multiple passes.

## 6. Comparison Rule

Compare references by technical features, not titles alone.

For each likely close reference, note:

- which layer it overlaps
- which features it clearly teaches
- which features are missing
- whether the missing features are central or easily combinable

## 6A. Drafting-Quality Evaluation Rule

After selecting technically relevant comparison documents, evaluate whether any of them are also useful drafting references.

Applicant/assignee/patentee or inventor strength is only one external provenance signal. It may raise confidence when the text also looks strong, but it must not make a reference high quality by itself.

Assess these dimensions:

- technical fit: comparable technical field, claim type, drafting route, and problem setting
- claim architecture: clear independent-claim boundary, necessary feature relationships, coherent preamble/body split, sensible dependent-claim fallback layers, and no excessive reliance on pure effects or broad functional labels
- problem-solution logic: identifiable technical problem, technical contradiction, technical means, and direct technical effects; background does not over-admit the invention
- specification support: claims are mirrored and supported by summary and embodiments; examples, variants, parameters, drawings, and effects are concrete enough for later drafting reference
- terminology and consistency: stable terms, clear antecedents, consistent reference numerals, and no unexplained synonym drift across claims and specification
- drafting expression: polished Chinese patent phrasing, concise section organization, legally conventional wording, and absence of marketing-style adjectives or vague superlatives
- prosecution robustness: fallback positions, range support, alternative embodiments, avoidance of avoidable clarity/support defects, and enough detail to resist simple combination pressure
- external provenance: strong applicant, assignee, patentee, inventor, patent family, grant history, or globally known filer such as Huawei, Xiaomi, Nike, Apple, or a comparable company

Mark a reference as:

- high quality: strong in most text-intrinsic dimensions and no serious negative signal
- medium quality: useful in one or two drafting aspects but uneven, narrow, translated awkwardly, or weakly supported
- low quality: mainly useful as technical prior art, with poor drafting structure or support

Negative signals include inconsistent terminology, claim/specification mismatch, unsupported effects, overbroad functional claiming, boilerplate embodiments, missing fallback layers, unclear drawings, poor machine translation, or background admissions that would be risky to imitate.

For each high-quality reference, record what can be reused as writing technique: terminology discipline, claim hierarchy, section sequence, background framing, effect linkage, or embodiment organization. Keep this separate from technical comparison. Later drafting may learn from expression and structure, but must not copy unsupported technical content, claim scope, examples, results, or long verbatim passages.

## 7. Memo Rule

Separate:

- verified record facts
- supported technical overlap
- inference about likely inventive-step pressure
- unresolved uncertainty

Prefer a short, cited, high-signal memo over a long undifferentiated list of search hits.

When the search is a drafting checkpoint, also state:

- which route still looks worth reconstructing
- which branches should be narrowed or abandoned
- which questions must be sent back to the inventor before claims are drafted
- which high-quality comparison documents, if any, should be consulted as drafting-style references in reconstruction, claims, or specification drafting

## 8. Download Rule

The search workflow is not complete when it stops at a list of hits.

After screening the closest references:

1. pick the references that are really relevant enough to keep
2. package each selected reference into `pdf + md`
3. record the saved paths in the memo or manifest
4. if direct PDF download fails, surface the browser-automation fallback rather than silently omitting the PDF
