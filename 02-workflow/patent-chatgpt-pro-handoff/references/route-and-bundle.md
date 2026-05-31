# Route And Bundle Rules

## Route Selection

Use the public patent route first.

- Drafting from disclosure, inventor notes, R&D material, or a technical scheme goes to `patent-cn-draft`.
- Existing application review, final QC, numbering consistency, abstract length, figure labels, and DOCX validation go to `patent-cn-review`.
- Office action, D1/D2/D3 comparison, claim amendment, correction, invalidity, and oral-hearing work go to `patent-cn-response`.
- Standalone prior-art search, record research, topic research, or document support may be handled as research or support.

If the route is unclear and the choice would change claim scope or response strategy, ask one question before preparing the handoff.

## When To Use ChatGPT Pro

Use the web Pro model for work that benefits from stronger reasoning or prose quality:

- reconstructing the technical problem and contradiction chain;
- deciding independent-claim boundaries and fallback layers;
- drafting or revising claims, invention content, background, and embodiments;
- building OA or invalidity argument logic;
- polishing a difficult technical narrative after Codex has organized the evidence.

Keep these tasks local in Codex:

- file inventory and extraction;
- patent search and PDF download;
- comparison tables and source citation tracking;
- reference numeral checks;
- claim dependency checks;
- DOCX generation, formula conversion, rendering, and final validation.

## Handoff Folder

Create a folder under the case directory. The folder must be organized so that the documents intended for ChatGPT web do not exceed 20 files:

```text
输出/过程/ChatGPT交接/<timestamp>_<task-title>/
  00_交接包说明.md
  01_发送给ChatGPT-Pro的提示词.md
  02_案件材料汇编.md
  03_材料清单.md
  04_发送前确认.md
  05_回收与整合说明.md
  06_网页端启动提示词_可直接粘贴.md
  发送全集_可直接粘贴.md
  规则_合并版.md
  交接包_manifest.json
  材料/                  # only budgeted binary attachments
  回收/
```

Use Chinese file names for human-readable files. The manifest may use English JSON keys.

## Document Limit

ChatGPT web accepts only 20 documents in one upload. Enforce this limit before presenting the handoff as ready.

- Merge all rule files into `规则_合并版.md`; do not upload separate rule files.
- Merge readable text sources into `02_案件材料汇编.md`.
- Preserve DOCX, PDF, image, spreadsheet, and other binary files as separate attachments only while the total document count remains at or below 20.
- If the source set would exceed 20 documents and cannot be merged safely, stop and extract or consolidate the excess sources before asking the user to send the package.
- Record merged, copied, and deferred sources in `03_材料清单.md` and `交接包_manifest.json`.

## Material Digest Requirements

The material digest should include:

- task purpose and expected output;
- route result and assumptions;
- source list with file names and dates if available;
- confirmed technical facts;
- closest prior-art or comparison-document facts when relevant;
- claim set, amendment basis, or target sections when relevant;
- uncertainties and questions that ChatGPT should not invent around.

Do not ask ChatGPT to infer facts from missing attachments. If a fact is not in the digest or source files, tell ChatGPT to mark it as unknown.

## Pre-Send Check

Before asking for confirmation, check:

- `发送全集_可直接粘贴.md` includes the material digest and selected rule files.
- `06_网页端启动提示词_可直接粘贴.md` can be pasted directly into ChatGPT web as the first message.
- `规则_合并版.md` includes task-specific rules, not only generic instructions.
- `03_材料清单.md` reports a document count at or below 20.
- No source in the material list is deferred unless Codex has separately extracted or merged it into the digest.
- Formula handling is explicit when formulas exist.
- The prompt asks for a structured output that Codex can integrate.
- The text avoids long strings of ideographic commas unless legally necessary.
- The material list matches the files that will be sent.

## Reply Requirement

When reporting a finished handoff bundle to the user, include:

- the bundle path;
- the full-send file path;
- the document count;
- the return folder path;
- a fenced `text` block headed `网页端启动提示词`.

The web prompt should be a concise launcher, not a replacement for the complete handoff file. It should tell ChatGPT web to use `发送全集_可直接粘贴.md` as the main instruction source, follow the copied rule files, and generate one DOCX document as the final output.
