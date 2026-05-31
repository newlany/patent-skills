# Intent Routing

Use this file after reading `routing-architecture.md`. The routing model is layered: normalize old names, choose the public workflow, then select specialists and delivery.

## Step 0: Normalize Explicit Skill Names

If the user names a compatibility or retired skill, translate it through the registry before routing.

Examples:

- `patent-workflow-router` -> `patent-cn`
- `patent-oa-response` -> `patent-cn-response`
- `patent-disclosure-agent` -> `patent-cn-draft`, or `patent-stage-disclosure-analysis` for a narrow standalone disclosure task
- `cn-patent-formal-check` -> `patent-cn-review`, with `patent-qc-cn-formality` as the specialist
- `download-google-patents-pdfs` -> `patent-support-google-patents-pdfs`

## Step 1: Public Intent

### Drafting

Route to `patent-cn-draft` when the user provides or refers to:

- 技术交底书或发明人说明
- 研发材料或技术方案草稿
- “撰写专利”“写权利要求”“先查新再重构”
- “一口气出初稿”“自动跑完整撰写流程”

Internal specialists are selected later by the drafting orchestrator.

### Review Or QC

Route to `patent-cn-review` when the user has an existing draft and asks for:

- 形式检查或最终检查
- 成稿审查
- 权利要求引用关系
- 标号一致性
- 附图说明或摘要字数检查
- DOCX 公式、修订、批注或版式复核
- 是否可以进入提交包

### Response Work

Route to `patent-cn-response` when the user mentions:

- 审查意见
- D1/D2/D3
- 创造性答复
- 修改权利要求
- 补正通知书或替换页
- 无效或无效答辩
- 口审准备
- 请求人观点或合议组问题

### Doctor

Route to `patent-cn-doctor` when the user asks:

- “检查系统能不能跑”
- “doctor / health / status”
- “BigQuery、LibreOffice 和 DOCX 是否正常”
- “流程图工具是否正常”

### Research

Use `patent-cn` with a research specialist when the user only wants:

- prior-art, novelty, closest-reference, or 智慧芽/PatSnap browser search: `patent-stage-prior-art-search`
- patent legal-status, family, file-history, invalidity record, litigation record, or official source verification: `patent-research-records`
- patent topic research, legal-issue memo, training material, or doctrine research: `patent-research-topic`
- fixed patent or fixed comparison-set analysis: `patent-analysis-fixed-patent`

### Support Or Delivery

Use `patent-cn` with a support or delivery specialist when no full public workflow is needed:

- inventor supplement question-list content: `patent-inventor-questions`
- inventor, applicant, client, or other external communication DOCX: `patent-external-brief-docx`
- DOCX math, comments, tracked changes, tables, numbering, or layout-sensitive extraction: `patent-support-docx-math`
- Google Patents PDF bundle: `patent-support-google-patents-pdfs`
- ChatGPT Pro handoff bundle: `patent-chatgpt-pro-handoff`

## Step 2: Delivery After Legal Work

Do not let the requested output format override the legal route.

For question-list work, route directly to `patent-inventor-questions` only when the current materials are enough to judge the key missing facts. If the question list first requires disclosure analysis, OA analysis, review, or claim-strategy judgment, run the relevant public workflow and then use `patent-inventor-questions` for the final content. Use `patent-external-brief-docx` only when DOCX delivery is requested or already implied.

For correction replacement pages, route to `patent-cn-response` first. `patent-support-correction-docx` is the delivery specialist after the correction route is confirmed.

For filing-package application DOCX output, use the `patent-cn` application template rule. Do not use `patent-external-brief-docx`.

## Low-Confidence Cases

Ask before routing only when:

- a document could be either a raw disclosure or an already filed application
- the work could be OA response or invalidity and the file type is unclear
- the user asks for “检查” but it is unclear whether they want drafting QC, legal analysis, or DOCX repair
- choosing the wrong route would change claim scope, amendment strategy, evidence strategy, or filing-package contents
