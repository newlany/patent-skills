# Office-Action DOCX Templates

Read this file only when the task requires a deliverable `.docx` response or a claims replacement page.

## Template files

Use these template assets when the task requires a deliverable `.docx` response:

- Amended response template:
  - `assets/templates/amended-template.docx`
  - `assets/templates/意见陈述-有修改.docx`
- Unamended response template:
  - `assets/templates/unamended-template.docx`
  - `assets/templates/意见陈述-无修改.docx`

When producing a final `.docx`, use [$doc](../../../doc/SKILL.md) to edit the template instead of rebuilding formatting from scratch.

If the user has provided a claims replacement-page template such as `权利要求书替换页.dotx`, treat it as part of the amended deliverable set. After the amended claim set is fixed, automatically generate a claims replacement-page `.docx`; do not wait for a separate request.

## How to choose the template

- Use the amended template if the user has confirmed claim amendments or if the final response must include an amendment section and an amended claim 1 text.
- Use the unamended template if the user has decided not to amend the claims and the response is based only on argument.
- Use the user-provided claims replacement-page template when the case proceeds with amended claims and such a template is available.

## Shared structure

Both templates are plain-paragraph templates with no tables. The formatting is simple and should be preserved. Do not restructure headings unless the user explicitly asks for a different format.

Each template already contains:

- the salutation
- the main heading hierarchy
- the inventive-step response skeleton
- the closing paragraph

Your job is to fill the blank sections and update fixed text where claim numbers, claim ranges, or amendment facts differ from the template.

## Unamended template mapping

File:

- `assets/templates/意见陈述-无修改.docx`

Main fill points:

1. Opening paragraph
   - Update claim numbers and claim range if the template range does not match the case.
   - Confirm whether the response is really based on "权利要求1-10" or another range.

2. "对比文件1公开的内容"
   - Insert the verified D1 summary from the D1-check stage.
   - Use only the original-text-checked D1 facts.

3. "权利要求1至少具备以下区别技术特征"
   - Insert the user-confirmed distinguishing features.

4. "权利要求1的技术效果"
   - Insert only specification-supported effects, examples, comparative examples, and data.

5. "实际解决的技术问题"
   - Insert the user-confirmed technical problem wording for the current unamended claims.

6. "审查意见通知书中指出"
   - Briefly restate the examiner's combination logic.

7. "申请人对此无法认同，理由如下"
   - Expand into numbered points.
   - Usually point (1) is the main attack line.
   - Add point (2) and point (3) only if needed.

8. Dependent-claim and closing paragraphs
   - Update claim ranges such as "权利要求2-5" and "权利要求1-5" to match the actual case.

## Amended template mapping

File:

- `assets/templates/意见陈述-有修改.docx`

Main fill points:

1. Opening paragraph
   - Keep the amendment framing.
   - Update only if the office action number, amendment scope, or legal basis wording needs to match the case.

2. "一、对权利要求书的修改"
   - Replace "将权利要求2的全文合并至权利要求1" with the actual amendment description.
   - If multiple claims were merged, say so precisely.

3. "修改后的权利要求1如下"
   - Paste the full, final, user-confirmed amended claim 1 text after "1.".
   - Preserve line breaks and indentation cleanly.

4. Article 33 paragraph
   - Keep it unless the case needs a more specific added-matter explanation.

5. "对比文件1公开的内容"
   - Insert the verified D1 summary from the D1-check stage.

6. "修改后的权利要求1至少具备以下区别技术特征"
   - Insert the user-confirmed distinguishing features for the amended claim 1.

7. "修改后的权利要求1的技术效果"
   - Insert only supported effects tied to the amended claim.

8. "实际解决的技术问题"
   - Insert the user-confirmed technical problem wording for the amended claim.

9. "审查意见通知书中指出"
   - Briefly restate the examiner's combination logic.

10. "申请人对此无法认同，理由如下"
   - Expand into numbered reasons.
   - Keep the main argument first.

11. Dependent-claim and closing paragraphs
   - Update claim numbers and claim ranges after amendment.
   - If claim numbering changed, fix all downstream references.

12. Claims replacement page
   - If the user has provided a template such as `权利要求书替换页.dotx`, generate a separate `.docx` replacement page after the amended claim set is fixed.
   - Use the final amended numbering, dependency relations, and wording exactly as adopted.
   - Save it as a case-specific working file instead of overwriting the template.

## Minimum preparation before filling either template

Do not fill the final `.docx` until these are fixed:

1. the current effective claim set
2. the verified D1 and Dx findings
3. the user-confirmed amendment decision
4. the user-confirmed distinguishing features for the current effective claim set
5. the user-confirmed technical problem for the current effective claim set
6. the user-confirmed key response wording if the case is sensitive

If a claims replacement-page template is available, also wait until the full amended claim set and final numbering are fixed.

## Practical filling workflow

1. Build the response text in plain text first.
2. Confirm the key judgment nodes with the user.
3. Open the correct template with [$doc](../../../doc/SKILL.md).
4. Fill the template without changing the heading hierarchy.
5. If amendments are adopted and a user-provided claims replacement-page template exists, generate the replacement-page `.docx` from that template.
6. Re-check claim numbers, amendment statements, replacement-page content, and closing paragraphs.
7. Save as a new working file, not over the original template, unless the user explicitly asks to overwrite it.
