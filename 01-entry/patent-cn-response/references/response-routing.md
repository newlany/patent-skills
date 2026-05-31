# Response Routing

## OA Response

Route to `patent-entry-oa-response` when the user mentions:

- 审查意见通知书
- D1/D2/D3
- 新颖性/创造性驳回
- 是否修改权利要求
- 答复审查意见
- 修改后答复 or 不修改答复

First materials:

- office action
- current claims/application
- cited references if available

If cited PDFs are missing, use `patent-support-google-patents-pdfs` first.

## Correction

Route to `patent-support-correction-docx` when the user mentions:

- 补正通知书
- 替换页
- 形式缺陷补正
- 只做页码/编号/格式性替换

First materials:

- correction notice
- current DOCX
- target replacement page scope

## Invalidity

Route to `patent-entry-invalidity` when the user mentions:

- 无效宣告
- 无效答辩
- 请求人观点
- 合议组问题
- 口审准备
- 攻防图

First materials:

- target patent
- invalidity request or evidence
- current claim set
- oral-hearing or response deadline if relevant

## Low Confidence

Ask before routing if:

- the file is just “通知书” but the notice type is not visible
- the user says “答复” but it could be OA, correction, invalidity, or client reply
- the user provides only a patent number and no procedural context
