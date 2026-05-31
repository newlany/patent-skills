# Browser Handoff Rules

## Confirmation Requirement

Before sending any patent material to ChatGPT web, obtain explicit confirmation for the specific package. The confirmation message must identify:

- destination: ChatGPT web Pro model;
- case or task name;
- material files or digest that will be transmitted;
- whether formulas or DOCX generation are requested.

Do not rely on a broad standing instruction as confirmation for a new package.

## Browser Assistance

After confirmation, use the Browser skill if available:

1. Open `https://chatgpt.com/`.
2. Verify the user is logged in or ask the user to handle login.
3. Select the Pro model when the model selector is visible.
4. Paste `发送全集_可直接粘贴.md` into the composer, or attach only the files listed as sendable in `03_材料清单.md`.
5. Stop for any unexpected account, payment, policy, captcha, or file-access prompt.

Do not build a background loop that repeatedly submits jobs or extracts output from ChatGPT web as if it were an API.
Do not attempt to upload more than 20 documents. If the package lists deferred sources, consolidate them locally before sending.

## Return Path

Ask the user to save the ChatGPT output into:

```text
<handoff-folder>/回收/
```

Recommended names:

- `ChatGPT-Pro返回_权利要求.docx`
- `ChatGPT-Pro返回_发明内容.docx`
- `ChatGPT-Pro返回_审查意见答复.docx`
- `ChatGPT-Pro返回_公式版本.docx`

After a returned file exists, Codex may integrate it locally, check consistency, and generate DOCX deliverables.
