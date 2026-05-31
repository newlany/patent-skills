---
name: patent-support-google-patents-pdfs
description: "Standalone Google Patents PDF acquisition support for extracting comparison documents from patent case files and downloading PDFs for 对比文件1/2、D1/D2/D3、本申请公开文本, and known publication numbers."
---
# Download Google Patents PDFs

## Standalone Role

Use this skill directly to acquire cited-reference PDFs, known-publication PDFs, or the original published application PDF before doing patent search or comparison analysis.

## Skill Position

- 类型：来源获取支撑 / Google Patents PDF acquisition support。
- 中文入口：下载对比文件 PDF、D1/D2/D3、对比文件1/2、本申请公开文本。
- 输入：OA、无效、检索或案件材料中的公开号/申请号/对比文件信息。
- 输出：命名后的 PDF 文件、下载记录、缺失/失败提示。
- 可服务任务：检索、OA/无效材料中的对比文件收集、固定专利文本下载。
- 边界：不独立分析创造性；下载完成后交给检索或分析步骤。

Use this skill to download:

1. The cited comparison documents only.
2. The original application's published patent PDF.

Do not download `相关专利文献`, `证据文件`, or other auxiliary references unless the user explicitly changes the requirement.

## Default Behavior

The bundled collector now does all of the following by default:

1. Read the case files.
2. Extract only explicit comparison documents such as `对比文件1` or `D1`.
3. Extract the original application's `申请号 / 公开号 / 发明名称` from the office action header when available.
4. Download those PDFs from Google Patents.
5. Save them directly in the selected output folder.

For OA response cases that use the `oa-office-action-response` shallow layout, set the output folder to `04-对比文件/` and put any manifest under `记录/答复过程/`.

Default filenames are Chinese:

- `对比文件1-CN105188447A.pdf`
- `对比文件2-US20080256830A1.pdf`
- `原申请文件-CNxxxxxxxxxA.pdf`

## Quick Start

```powershell
python "$env:CODEX_HOME\skills\patent-support-google-patents-pdfs\scripts\collect_google_patent_pdfs.py" `
  "C:\path\to\第一次审查意见通知书.pdf"
```

This writes the PDFs directly into the corresponding case folder root by default.

## Scripts

### `scripts/collect_google_patent_pdfs.py`

Use this for the end-to-end workflow.

Important defaults:

- Only downloads comparison documents.
- Also downloads the original application's published patent PDF.
- Saves files directly in the output root, which defaults to the case folder root. For OA response cases, pass `--output-root <case-folder>/04-对比文件`.
- Does not write a manifest file unless `--manifest` is provided.

Optional flags:

- `--skip-original-application`
- `--overwrite`
- `--manifest <path>`

### `scripts/extract_patent_references.py`

Use this to inspect what the skill will download before downloading anything.

By default it returns:

- explicit comparison documents
- the original application reference

### `scripts/download_google_patent_pdf.py`

Use this for a single known patent when you already have a publication number or application number.

If `--label 原申请文件` is provided, it uses `原申请文件-公开号.pdf`.

If `--category comparison` is provided, it uses `对比文件X-公开号.pdf`.

## Resolution Strategy

Follow this order:

1. Try the publication number directly against `https://patents.google.com/patent/<publication>/en`.
2. If only an application number is available, search Google Patents and verify the target page before downloading.
3. If needed, use the title as a fallback query.

For the original application, prefer the publication number from the office action. If it is not present, resolve by the application number.

## Validation

After editing the skill:

```powershell
$env:PYTHONUTF8 = "1"
python "$env:CODEX_HOME\skills\.system\skill-creator\scripts\quick_validate.py" `
  "$env:CODEX_HOME\skills\patent-support-google-patents-pdfs"
```
