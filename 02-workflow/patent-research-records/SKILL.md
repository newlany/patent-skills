---
name: patent-research-records
description: "Research specialist callable by patent-cn and response workflows for source-first patent record research. Direct use is allowed for standalone 专利法律状态、同族、审查历史、无效/诉讼记录、官方来源核查、特定专利事实核验、带引文备忘录. Prefer patent-analysis-fixed-patent for technical comparison after targets are fixed."
---
# Patent Deep Research

## New Architecture Role

`patent-cn` is the preferred public entry for mixed patent work, and response workflows may call this skill for record verification. This skill is a source-first record-research specialist, not a drafting or OA-response orchestrator.

## Skill Position

- 类型：记录核查研究 / patent record research。
- 中文入口：法律状态、同族、审查历史、无效记录、诉讼记录、官方来源核查、事实/推断分离。
- 输入：特定专利号、公开号、申请号、同族线索、案件材料或研究问题。
- 输出：带来源和日期的事实备忘录、时间线、状态说明、证据链。
- 支撑能力：可调用 `web-access`、`defuddle`、`pdf`、`spreadsheet`、`doc`。
- 边界：不作为普通撰写入口；技术特征对比固定后可交给 `patent-analysis-fixed-patent`。

Produce patent research that is source-first, jurisdiction-aware, date-aware, and explicit about what is proven versus inferred.

## Positioning

Do not use this as the default public entry for routine one-patent OA-stage or invalidation-stage technical analysis when a dedicated `patent-analysis-fixed-patent` workflow is available.

Prefer this skill when:

- the work is primarily source-intensive and record-first
- official status, family, prosecution, or procedural history verification is central
- the output needs a heavily cited research memo rather than a workflow-stage analysis note

## Core Rules

- Start by fixing the research target: patent number, application number, publication number, case number, party, technology, or legal issue.
- State the jurisdiction and procedural posture before analyzing substance.
- Distinguish the patent object precisely: application, published application, granted patent, amended claim set, family member, office action, invalidation decision, court judgment, or commentary.
- Treat claim text, legal status, procedural stage, and cited references as versioned facts that must be verified.
- Prefer official records and primary materials over summaries.
- Cite every nontrivial factual or legal assertion.
- Separate source-stated facts, procedural history, technical interpretation, and legal inference.
- Surface missing records, translation uncertainty, and source conflicts instead of filling gaps with assumptions.

## Patent Research Frame

Before gathering sources, fix these items:

- Research question: what exactly must be answered.
- Task type: patentability, validity, infringement, claim interpretation, office action rebuttal support, invalidation support, case-law research, legal-status check, family mapping, portfolio scan, or technical background research.
- Jurisdiction: CN, US, EP, WO, JP, KR, or another forum.
- Time scope: current status, historical status on a date, or procedural development over time.
- Decision target: quick answer, comparison table, issue memo, argument map, chronology, or full research report.

If any of these are unclear, state the assumption explicitly and proceed cautiously.

## Source Priority

Use this order unless the user instructs otherwise:

1. Official patent and court records: CNIPA, USPTO, EPO, WIPO, national patent registers, official gazettes, official case databases, court judgments, tribunal decisions, agency notices.
2. File-wrapper and procedural records: office actions, search opinions, examiner citations, applicant amendments, observations, invalidation petitions, responses, hearing notices, written decisions.
3. The patent record itself: claims, specification, abstract, drawings, sequence listings, priority data, assignment or transfer data, legal-status entries.
4. Primary technical references: cited patents, cited non-patent literature, standards, product manuals, original papers, datasets.
5. High-quality secondary sources: official guidance, examination guidelines, manuals, respected treatises, institutional reports.
6. Commentary and convenience databases: law-firm notes, analyst writeups, Google Patents, blogs, news, commercial summaries. Use for discovery or context and verify independently before relying on them.

## Patent-Specific Verification Rules

- Verify the exact document identifier and country code before drawing conclusions.
- Distinguish application publication from granted patent text.
- Identify which claim version is operative for the question being asked.
- Record amendment dates and procedural stage when claims changed.
- Check whether a legal-status statement is current or only accurate as of a past date.
- For family research, distinguish priority family, simple family, corresponding filings, and continuation or divisional relationships when relevant.
- For case-law research, distinguish court level, decision date, issue actually decided, and whether a statement is holding, reasoning, or background.
- For office-action or invalidation research, distinguish:
  - what a reference actually discloses,
  - what the examiner or requester alleges it discloses,
  - what the applicant or patentee disputes,
  - what the decision-maker ultimately accepts.

## Research Workflow

### 1. Fix the Research Object

- Normalize the patent, application, publication, or case number.
- Identify assignee, inventor, applicant, patentee, or litigating parties when relevant.
- Identify the technology field and the specific issue under review.

### 2. Build the Record Map

- List the core records needed to answer the question.
- Identify missing primary documents early.
- Map the expected chronology: filing, priority, publication, grant, office actions, amendments, transfers, litigation, invalidation, appeal, expiration.

### 3. Gather Sources

- Collect the official record first.
- Pull the underlying cited references instead of relying only on citations to them.
- Capture title, institution or author, exact date, direct link, and why the source matters.
- For time-sensitive requests such as current legal status, latest office action, or most recent decision, verify against current official sources and state the exact verified date.

### 4. Check Source Quality

- Authority: who issued or authored the record.
- Directness: whether the source itself proves the point.
- Currency: whether the record still governs the present question.
- Scope: whether the source addresses the same claim set, same family member, same jurisdiction, and same issue.
- Conflict: whether a later document supersedes or contradicts an earlier one.

### 5. Analyze by Task Type

Use the narrowest analysis that fits the assignment:

- Patentability or validity research: isolate claim features, disclosure gaps, closest references, combination logic, and what is actually taught versus inferred.
- Infringement or claim-interpretation research: isolate disputed terms, specification support, prosecution statements, and case-law treatment of similar language.
- Office-action or invalidation support: separate examiner or requester logic from the record and from your own analysis.
- Family or legal-status research: prioritize dates, jurisdiction, procedural events, assignments, term adjustments, and maintenance or renewal events.
- Case-law research: isolate issue, rule, reasoning, factual posture, and practical takeaway; do not overread dicta.

### 6. Synthesize Carefully

- Label direct record facts as facts.
- Label technical or legal conclusions drawn from multiple sources as inference.
- Label unresolved points as disputed or unknown.
- Prefer the narrowest supportable conclusion.
- If translation may affect interpretation, say so.

## Evidence Labels

Use these labels when they improve clarity:

- Verified record fact: directly supported by the patent, court, or agency record.
- Supported technical point: directly supported by cited technical material.
- Inference: reasoned conclusion drawn from the record, not explicitly stated by it.
- Disputed: credible materials or parties conflict.
- Unknown: the required record was not found or does not resolve the issue.

## Citation Contract

- Use numbered citations such as `[1]`, `[2]` immediately after the supported sentence or bullet.
- Cite every claim construction point, legal-status statement, procedural event, date, priority claim, amendment statement, cited-reference comparison, and legal proposition.
- For patent materials, identify the document precisely in the source list.
- When possible, cite the exact claim number, paragraph, page, section, or decision portion that supports the statement.
- Use multiple citations for important or high-risk propositions when available.
- Do not present docket summaries, database snippets, or commentary as if they were the underlying record.

## Uncertainty and Conflict Handling

- If the authoritative record is unavailable, say so explicitly.
- If different databases show inconsistent status or dates, identify the conflict and prefer the official source.
- If only a family counterpart is available, state that you are inferring from a related filing rather than the exact target document.
- If a later amendment, decision, or status entry changes the analysis, treat the later document as controlling and note the earlier one as superseded background.
- If you cannot verify a current position, state the last verified date and avoid implying that the result is current.

## Recommended Output

Use this structure unless the user asks for another format:

```markdown
## Executive Summary
[2-4 sentences answering the research question, with the key qualifier and citations]

## Research Frame
- Question: ...
- Task type: ...
- Jurisdiction: ...
- Time scope: ...
- Target patent or case: ...

## Record Baseline
- Patent or case identity: ...
- Operative document or claim set: ...
- Procedural posture: ...
- Key dates: ...

## Key Findings
- **[Finding 1]**: [Short explanation] [1][2]
- **[Finding 2]**: [Short explanation] [3]
- **[Finding 3]**: [Short explanation] [4][5]

## Detailed Analysis

### [Sub-issue 1]
[Analysis with citations]

### [Sub-issue 2]
[Analysis with citations]

## Chronology or Procedural Timeline
[Only include when timing matters]

## Disagreement and Uncertainty
[Conflicts, missing records, translation limits, unresolved issues]

## Practical Bottom Line
[What the evidence safely supports for the user's purpose]

## Sources
[1] [Full citation + credibility note]
[2] [Full citation + credibility note]
```

## High-Risk Boundaries

Apply extra caution when the user is relying on the research for litigation, invalidation, infringement, freedom-to-operate, filing strategy, or deadline-sensitive decisions:

- Prefer official records over commentary.
- Verify dates, jurisdiction, and claim version.
- Separate record facts from legal advice.
- Say when attorney review is still required.

## Failure Modes to Avoid

- Do not mix up application text, grant text, and amended claim text.
- Do not call a convenience database the authoritative source when the official record is available.
- Do not treat an examiner's allegation as a proven disclosure.
- Do not treat a court's factual summary as a holding on law.
- Do not say "current" or "latest" without verifying the record date.
- Do not overstate certainty where the file history, translation, or status data is incomplete.
