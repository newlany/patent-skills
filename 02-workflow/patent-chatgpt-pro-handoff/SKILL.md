---
name: patent-chatgpt-pro-handoff
description: "Prepare human-approved handoff bundles from local Codex Chinese patent workflows to the ChatGPT web Pro model. Use when the user wants Codex to route a patent drafting, review, OA response, invalidity, research, or document-support task; collect and merge the materials ChatGPT should see; keep the web-send bundle within ChatGPT's 20-document upload limit; add task-specific patent drafting rules; write a prompt that requires ChatGPT Pro to generate a DOCX document; assist browser submission after explicit confirmation; and later integrate returned DOCX output, including formula-safe handling."
---

# Patent ChatGPT Pro Handoff

## Overview

Use this skill to build a controlled local handoff package for using the ChatGPT web Pro model as a high-quality patent drafting and reasoning assistant. Keep Codex responsible for routing, evidence collection, source control, file conversion, validation, and final DOCX work.

This skill does not replace `patent-cn`, `patent-cn-draft`, `patent-cn-review`, or `patent-cn-response`. It adds a handoff layer when the user wants the web ChatGPT Pro model to handle a selected high-judgment writing task.

## Required References

Always read:

- `references/route-and-bundle.md`

Read when generating or revising a drafting handoff:

- `references/drafting-handoff.md`

Read when preparing a response, invalidity, or correction handoff:

- `references/response-handoff.md`

Read before using browser automation for ChatGPT web:

- `references/browser-handoff.md`

The files under `references/chatgpt-rules/` are copied into the generated handoff folder. Load them only if you need to inspect or patch the exact rule text.

## Workflow

1. Route the patent task first.
   Use the public `patent-cn` routing surface. If the matter is drafting, route to `patent-cn-draft`; if it is review, route to `patent-cn-review`; if it is OA, correction, invalidity, or oral-hearing work, route to `patent-cn-response`.

2. Decide whether ChatGPT Pro is needed.
   Use handoff for high-judgment text generation or strategy work, such as claim architecture, invention-content drafting, background framing, embodiment expansion, OA argument structure, invalidity attack and defense framing, or polishing a difficult technical narrative. Keep deterministic extraction, comparison tables, numbering checks, and DOCX validation in Codex.

3. Build a local material digest.
   Extract or summarize the source files that ChatGPT should actually read. Include source names, version dates when available, confirmed facts, uncertain facts, and open questions. Merge materials whenever possible because ChatGPT web accepts only 20 documents in one upload. For confidential matter, include only what is needed for the selected task.

4. Create the handoff folder.
   Use `scripts/create_handoff_bundle.py` rather than manually inventing the folder layout.

```bash
python3 /Users/chrynos/.codex/skills/patent-chatgpt-pro-handoff/scripts/create_handoff_bundle.py \
  --case-dir <case-folder> \
  --task-title "<short Chinese task title>" \
  --route <drafting|review|response|research|support> \
  --task-kind <claims|background|invention-content|embodiments|specification|oa-response|invalidity|review|prior-art|generic> \
  --material-md <compiled-material.md> \
  --source <source-file> \
  --max-documents 20 \
  --has-formulas
```

Use `--has-formulas` when the task includes mathematical formulas, chemical formulas, algorithmic expressions, or table-heavy calculation material.
Use `--max-documents 20` unless the web product limit changes. The script merges readable text sources into `02_案件材料汇编.md`, merges all rules into `规则_合并版.md`, and keeps only budgeted binary attachments under `材料/`. If a source cannot be merged within the limit, treat the bundle as not ready for web upload until Codex extracts or consolidates that source.

5. Inspect the generated folder before sending.
   Confirm that `发送全集_可直接粘贴.md` contains the task, material digest, selected rules, formula instructions when needed, and required output format. Confirm that `03_材料清单.md` reports no more than 20 documents and that any deferred source has been extracted or merged before upload.

6. Output a direct web prompt.
   Whenever a handoff folder is created, include a `网页端启动提示词` block in the Codex reply. The block should be short enough to paste directly into ChatGPT web and should tell ChatGPT Pro to read the generated handoff files, obey the task-specific rules, preserve unsupported facts as questions, and generate one DOCX document as the final output. Also write the same prompt to `06_网页端启动提示词_可直接粘贴.md`.

7. Ask for explicit human confirmation before transmitting.
   State the exact destination, the model target, and the material names. Do not transmit patent materials to ChatGPT web until the user confirms this specific package.

8. Use browser assistance only after confirmation.
   If the user confirms, use the Browser skill to open ChatGPT, select the Pro model when visible, place the prompt into the web composer, and leave the user in control of any account, login, or unexpected safety prompt. Do not build an unattended loop that treats the web UI as an API.

9. Integrate returned DOCX locally.
   When the user provides the ChatGPT DOCX result or saves it into the handoff folder, place it under `回收/`, then use the appropriate patent workflow to integrate it. For formula-bearing output, verify that formulas are editable DOCX equations or convert them during local validation.

## Route Block

Before creating a handoff folder, emit:

```text
CHATGPT PRO HANDOFF ROUTE
- patent route: <patent-cn-draft|patent-cn-review|patent-cn-response|research|support>
- confidence: <high|medium|low>
- ChatGPT task kind: <claims|background|invention-content|embodiments|specification|oa-response|invalidity|review|prior-art|generic>
- formula handling: <none|docx-with-editable-equations>
- handoff folder: <path to be created>
- first local action: <material extraction or bundle creation>
```

Ask one focused question only when the route changes claim scope, amendment strategy, or the set of materials to be sent.
