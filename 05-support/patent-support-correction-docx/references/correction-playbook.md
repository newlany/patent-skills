# Correction Playbook

Use this file when the notice item is easy to read but the safe editing scope is not obvious.

## Structured Extraction Checklist

Record each notice item with:

- `item_id`
- `notice_quote`
- `target_part`
- `target_span`
- `defect_type`
- `required_action`
- `allowed_scope`
- `blocker`

Keep this list short and operational. It is the bridge between the notice and the document edits.

## Common Defect Patterns

| Defect type | Typical notice wording | Safe default action | Stop condition |
| --- | --- | --- | --- |
| `dependency-error` | 权利要求引用关系错误、引用项不存在、引用顺序错误 | Repair the parent-claim reference and then re-check the entire dependency chain of the affected claims | More than one parent claim could legally fit and each choice changes scope |
| `antecedent-basis` | 技术特征没有引用基础、缺少引用基础、前述基础缺失 | Add or restore the earliest disclosed basis term using the application's own wording | No valid basis exists in the original disclosure |
| `support-basis` | 说明书中无记载基础、摘要无依据、附图标记无依据 | Modify only with wording already supported in the specification or claims | The notice would require new matter |
| `numbering` | 序号错误、权利要求编号错误、附图标记不对应 | Correct numbering and all direct references that depend on it | Renumbering would ripple into unclear or disputed passages |
| `terminology` | 名称不一致、术语前后不统一 | Align the affected part to the original dominant terminology | Two different terms may intentionally denote different structures |
| `formal-layout` | 标题、段落、页码、格式、替换页要求不规范 | Repair the formatting defect with the smallest layout change and keep content untouched | The notice actually masks a substantive content issue |

## Scope Rules

- Fix only the noticed defect and the minimum dependent passages that must follow it.
- If a claim changes, check whether the specification or abstract must mirror that claim wording.
- Do not rephrase unaffected sections for style.
- Do not “optimize” claims during a补正 unless the notice requires it.

## Replacement Page Rules

- Replacement pages come from the corrected source, never from the original uncorrected source.
- If the user provides a `.dotx` replacement-page template, use the template as the output base package and fill only the corrected target part into the template body.
- If the application is stored as separate DOCX files, still render the corrected target part into the template instead of simply renaming the working file.
- If the application is stored as one combined DOCX, extract the affected top-level part only.
- For combined DOCX, prefer heading-based extraction first and manual boundary overrides second.
- For specification replacement pages, exclude abstract, claims, and trailing standalone figure pages unless the user explicitly asks to include them.

## Delivery Checklist

- Each notice item has a fix status.
- Each changed part has a replacement page.
- No unintended tracked changes remain.
- The extracted replacement-page DOCX still opens cleanly and keeps the original formatting.
