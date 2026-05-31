---
name: patent-cn-response
description: "Public orchestrator for Chinese patent response work. Use for 审查意见答复、D1/D2/D3、创造性答复、补正通知书、替换页、无效答辩、无效宣告、口审准备. Routes internally to OA, correction, invalidity, fixed-patent analysis, PDF bundle, and DOCX specialists."
---
# CN Patent Response Orchestrator

## Role

This is the public response-work entry. It handles procedural matters after or outside initial drafting.

Use it for:

- OA response
- D1/D2/D3 analysis
- claim amendment strategy
- correction notices and replacement pages
- invalidity requests or responses
- oral hearing preparation

## Startup

Always read:

- [references/response-routing.md](references/response-routing.md)
- [$patent-cn/references/internal-specialists.md](/Users/chrynos/.codex/skills/patent-cn/references/internal-specialists.md)

Then dispatch to the correct internal workflow:

- [$patent-entry-oa-response](/Users/chrynos/.codex/skills/patent-entry-oa-response/SKILL.md)
- [$patent-support-correction-docx](/Users/chrynos/.codex/skills/patent-support-correction-docx/SKILL.md)
- [$patent-entry-invalidity](/Users/chrynos/.codex/skills/patent-entry-invalidity/SKILL.md)

Use support specialists as needed:

- [$patent-analysis-fixed-patent](/Users/chrynos/.codex/skills/patent-analysis-fixed-patent/SKILL.md)
- [$patent-support-google-patents-pdfs](/Users/chrynos/.codex/skills/patent-support-google-patents-pdfs/SKILL.md)
- [$patent-support-docx-math](/Users/chrynos/.codex/skills/patent-support-docx-math/SKILL.md)

## OA Response DOCX Templates

When the OA route produces a formal 意见陈述 DOCX, using an 意见陈述 template is mandatory.

If the user, case folder, or local workspace provides an 意见陈述 template, that template has priority over bundled skill assets. Known local office templates are:

```text
/Users/chrynos/Library/CloudStorage/OneDrive-个人/工作/工作文档/审查意见/意见陈述-有修改.docx
/Users/chrynos/Library/CloudStorage/OneDrive-个人/工作/工作文档/审查意见/意见陈述-无修改.docx
```

Use `意见陈述-有修改.docx` when the final answer adopts claim amendments or must include an amendment statement. Use `意见陈述-无修改.docx` when the answer is argument-only and the claims remain unchanged.

Only if no user-provided, case-provided, or local workspace template is available may the workflow fall back to the templates bundled in the internal OA workflow:

```text
/Users/chrynos/.codex/skills/patent-entry-oa-response/assets/templates/意见陈述-有修改.docx
/Users/chrynos/.codex/skills/patent-entry-oa-response/assets/templates/意见陈述-无修改.docx
```

Do not rebuild these documents from scratch and do not merely imitate the template formatting. Copy the correct template as the working DOCX, then fill or replace its existing title, salutation, amendment section, Article 33 section, inventive-step section, dependent-claim section, and closing paragraphs. Preserve the template's section settings, styles, numbering definitions, and paragraph skeleton unless a case-specific change is required.

## OA Case Folder Layout

For OA matters downloaded through `oa-office-action-response`, use the same shallow case layout. Do not create new legacy `source/`, `work/`, `filing/`, `checks/`, or `oa/` folders.

```text
<case-folder>/
  01-审查意见/
  02-申请文件/
  03-既往答复/
  04-对比文件/
  05-处理结果/
  06-提交文件/
  记录/
```

Read the current notice PDF from `01-审查意见`. Read original application files from `02-申请文件`. If the case has prior OA responses, use `03-既往答复` as the source of the current effective text. Download cited comparison PDFs into `04-对比文件`.

Put readable analysis notes, extracted text, and stage summaries in `05-处理结果`. Put the final 意见陈述 DOCX and any replacement-page DOCX files in `06-提交文件`. Put JSON reports, tool logs, render checks, and machine traces under `记录/`.

## Output Protocol

```text
CN RESPONSE ROUTE
- response type: <oa|correction|invalidity|unknown>
- confidence: <high|medium|low>
- internal workflow: <skill>
- first required material: <file or fact>
- first output: <artifact>
```

Continue into the internal workflow when confidence is high or medium.

Ask one focused question when confidence is low.
