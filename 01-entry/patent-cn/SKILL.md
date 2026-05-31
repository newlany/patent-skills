---
name: patent-cn
description: "Canonical top-level entry for Chinese patent work. Use when the user asks to handle a patent matter and the task may be drafting, review/QC, OA response, correction, invalidity, prior-art search, research, filing package, inventor/applicant question-list content or DOCX, external communication brief DOCX, DOCX/PDF support, or system doctor. Routes to patent-cn-draft, patent-cn-review, patent-cn-response, patent-cn-doctor, or existing internal specialists."
---
# CN Patent Command Center

## Role

This is the new public front door for local Chinese patent work.

Use it when the user says things like:

- “用专利系统处理这个案子”
- “这个交底帮我走流程”
- “检查这套申请文件”
- “处理这个审查意见”
- “看这个专利任务该怎么做”

Do not ask the user to choose among low-level skills unless the task is genuinely ambiguous and the route choice changes the legal or drafting outcome.

## Architecture Rule

External users should see a small product surface:

- `patent-cn`: top-level intent router
- `patent-cn-draft`: new Chinese application drafting
- `patent-cn-review`: filing-draft review and QC
- `patent-cn-response`: OA, correction, and invalidity response routing
- `patent-cn-doctor`: system health and dependency checks

Existing `patent-entry-*`, `patent-stage-*`, `patent-method-*`, `patent-support-*`, and `patent-qc-*` skills remain available as internal specialists or compatibility entries.

Other support skills may be used when they fit a patent workflow output. In particular, route substantive inventor supplement question content to `patent-inventor-questions`, then route external communication DOCX delivery to `patent-external-brief-docx`.

The specialist map is maintained in:

```text
/Users/chrynos/.codex/skills/patent-cn-runtime/scripts/specialist_registry.json
```

## Startup

Always read:

- [references/routing-architecture.md](references/routing-architecture.md)
- [references/intent-routing.md](references/intent-routing.md)
- [references/internal-specialists.md](references/internal-specialists.md)

Read when the user asks what commands to use:

- [references/public-commands.md](references/public-commands.md)

## Chinese Drafting Style Rule

When `patent-cn` routes work that may generate or revise Chinese patent prose, carry this style rule into the downstream workflow and any internal specialist prompt.

- Avoid dense strings of ideographic commas in generated Chinese files. Do not write long sequences like “概念一、概念二、概念三、概念四” unless the structure is legally or technically necessary.
- This rule is especially important in 背景技术、发明内容和具体实施方式, where prose should read like careful patent drafting instead of a mechanical list of adjacent concepts.
- When three or more parallel concepts appear in one sentence, prefer splitting the sentence, using semicolons, using a numbered list, or rewriting with natural connectors such as “和”“以及”“并且”.
- Before finalizing a Chinese drafting artifact, actively scan for dense ideographic-comma chains and revise them when doing so does not change claim scope, technical boundaries, or support relationships.
- Keep dense ideographic-comma wording only for quoted source text, formal names, necessary claim enumeration, table entries, or explicit user instructions.

## Application DOCX Template

The default Chinese invention application template for filing-package DOCX output is stored in this skill:

```text
templates/专利撰写模板文件.docx
```

Use this template when generating or replacing a Chinese invention application DOCX unless the user provides a different case-specific template. Treat `templates/专利撰写模板文件.docx` as the canonical reference document for Markdown-to-DOCX and OpenXML formatting flows.

Legacy template assets remain available only for compatibility:

```text
templates/发明专利撰写模板xml.dotx
templates/发明专利撰写模板xml.docx
```

When routed work produces a filing package or final application document:

- apply `templates/专利撰写模板文件.docx` as the default reference/template document;
- keep generated application DOCX files under `输出/定稿/`;
- register the generated DOCX and any validation report in `manifest.json`;
- run DOCX validation and rendering checks before describing the package as ready.

## External Communication Brief Route

When the user asks for a 发明人问题清单 or 补充材料问题清单 and the content is not already drafted, route the content step to:

```text
/Users/chrynos/.codex/skills/patent-inventor-questions/SKILL.md
```

Use this route to draft a concise numbered list that asks only the key missing facts needed before the case can enter drafting. Do not use this route to produce a long defect inventory for internal analysis.

When the user asks for an inventor, applicant, client, or other external-facing patent communication DOCX, route the delivery step to:

```text
/Users/chrynos/.codex/skills/patent-external-brief-docx/SKILL.md
```

Use these routes for concise communication outputs. Typical examples include:

- 发明人问题清单或补充材料问题清单
- 申请人沟通说明
- 驳回决定简要分析
- 复审分析及建议
- 审查意见沟通简报
- 查新或检索结果简报
- 补正或形式缺陷沟通说明
- 无效风险或稳定性初步说明

For these tasks:

- use intent `support` in the route block;
- set public workflow to `patent-cn` unless the content first needs full drafting, review, or response analysis;
- list `patent-inventor-questions` as the content specialist when a question list must be drafted;
- list `patent-external-brief-docx` as the delivery specialist when DOCX output is requested;
- draft the communication content in Markdown first, then call the `patent-external-brief-docx` workflow only if a DOCX is needed;
- keep process Markdown under `输出/过程/` and final user-facing DOCX under `输出/定稿/` when working inside a case folder;
- run the structural and render checks required by `patent-external-brief-docx` before saying the DOCX is ready.

If the requested external brief depends on unresolved legal or technical analysis, run the relevant public workflow first, then use `patent-external-brief-docx` only for the final communication package. For inventor question lists, use `patent-inventor-questions` for the final question content before DOCX delivery.

## Search-To-Drafting Carryover Rule

When `patent-cn` routes into `patent-cn-draft`, or routes directly to a prior-art search that may later feed drafting, the search result must preserve more than patentability risk.

For selected comparison documents, require the search specialist to evaluate drafting quality and record it in the search memo or a separate `输出/过程/02_现有技术检索/参考文献撰写质量.md` artifact. Applicant/assignee/patentee or inventor credibility is only one external signal; it must not decide quality by itself.

Evaluate drafting quality across multiple dimensions:

- technical fit: whether the reference belongs to a comparable technical field, claim type, and drafting route
- claim architecture: clear independent-claim boundary, necessary technical relationships, sensible dependent-claim fallback layers, and limited reliance on pure functional effects
- problem-solution logic: explicit technical problem, contradiction, technical means, and technical effect linkage
- specification support: stable terminology, sufficient embodiments, alternative implementations, parameter support, and consistency between claims, summary, embodiments, and drawings
- drafting expression: polished Chinese patent phrasing, concise section organization, careful background framing, and absence of marketing-style or vague language
- prosecution robustness: fallback positions, avoidable overbreadth, support for effects, and low risk of common clarity/support defects
- external provenance: strong applicants, assignees, patentees, inventors, large patent families, or globally known companies such as Huawei, Xiaomi, Nike, Apple, and similarly strong filers

If a comparison document is both technically relevant and high quality, later drafting may use it as a style and expression reference for terminology, claim-dependency layout, background framing, invention-content phrasing, and embodiment organization. Do not copy unsupported technical content, claim scope, experimental results, or long verbatim passages from the comparison document.

## Routing Output

Before continuing, emit a concise route block:

```text
CN PATENT ROUTE
- normalized request: <original skill name translated or none>
- intent: <drafting|review|response|doctor|research|support>
- confidence: <high|medium|low>
- public workflow: <patent-cn-*>
- stage specialists: <skill list or none yet>
- delivery specialists: <skill list or none yet>
- first action: <what will be done next>
```

If confidence is high or medium, continue into the chosen public workflow instead of stopping at the route block.

If confidence is low, ask one focused question and explain why the answer matters.

## Case Directory Layout

For any case folder, use the fewest directories possible, and use Chinese names for directories. Do not create placeholder stage, admin, archive, report, or tool-run folders at case initialization.

Minimum case folder after initialization:

```text
<case-folder>/
  00_case_status.md
  00_case_events.jsonl
  manifest.json
```

Create only the immediate parent directories needed by the file being written:

```text
<case-folder>/
  输出/
    过程/
      <中文阶段名>/        # only if useful to group multiple process files
    定稿/
  记录/
    <中文阶段名>/
      报告/              # only when a machine stage-report JSON is written
      工具运行/          # only when a normalized tool-run JSON is written
```

Use `输出/过程/` for process outputs that the user may want to read, such as disclosure analysis memos, search memos, claim-strategy notes, intermediate draft text, review checklists, OA argument outlines, and correction notes. Keep it flat when there is only one or two files; create a stage subfolder only when it prevents clutter.

Process files should be expressed in Chinese by default: use Chinese file names, headings, and main prose for human-readable process artifacts. Keep English only for stable tool contracts, JSON keys, command IDs, source titles, citations, or file names that a script explicitly expects.

Use `输出/定稿/` for final outputs that the user may want to submit, archive, or send onward, such as final claims/specification text, DOCX/PDF deliverables, replacement pages, final OA responses, invalidity/hearing materials, filing-readiness reports, and final validation reports.

Use numbered Chinese stage folder names only when a stage folder is actually needed, for example `01_交底分析`, `02_现有技术检索`, `03_方案重构`, `04_权利要求`, `05_说明书`, `06_附图`, `07_质检`, `08_提交包`.

Do not scatter human-readable process or final files under legacy `<stage>/outputs/`. Preserve `记录/` for machine-oriented records, diagnostics, and script traces. If an existing case already uses legacy English folders, keep reading and registering those artifacts, but create new folders in the Chinese lazy layout unless the user asks for migration.

## State Discipline

For any multi-stage matter:

- use `patent_workflow.py init` or locate an existing `manifest.json`
- if no case folder exists, create it under `<project-root>/专利工作区/<中文案件名>` instead of writing process files into the project root
- after `init`, do not pre-create `输出/过程/`, `输出/定稿/`, `记录/`, stage folders, or archive folders
- create a directory only at the moment a file is written, and only create that file's immediate parent chain
- keep `00_case_status.md`, `00_case_events.jsonl`, and `manifest.json` current
- keep human-readable stage memos and process artifacts under `输出/过程/` or `输出/过程/<中文阶段名>/`
- keep final deliverables and final validation artifacts under `输出/定稿/`
- keep machine JSON reports under `记录/<中文阶段名>/报告/` and tool-run JSON under `记录/<中文阶段名>/工具运行/`; if a JSON report is meant for user review, also mirror or summarize it under `输出/过程/` or `输出/定稿/`
- register all user-facing artifacts from `输出/过程/` and `输出/定稿/` in `manifest.json`
- log stage starts, stage ends, script calls, dependency calls, and manual interruptions
- run validation before saying a case is `drafting-complete` or `filing-ready`

## Boundaries

- Do not do detailed drafting inside this router.
- Do not do detailed legal argument inside this router.
- Do not directly patch DOCX files inside this router.
- The router chooses the workflow and then hands control to the workflow orchestrator.
