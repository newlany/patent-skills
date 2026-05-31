---
name: patentwang-decision-downloader
description: Download Chinese patent invalidity decision PDFs and reexamination decision PDFs through the local OpenCLI `patentwang` adapter. Use when the user asks to fetch, download, locate, or verify 无效决定书 or 复审决定书 by invalidity case number, reexamination case number, patent/application number, decision number, title keyword, requester, owner/applicant, agency, IPC, or decision conclusion.
---

# PatentWang Decision Downloader

## Overview

Use the local OpenCLI `patentwang` adapter before browser automation. It queries `https://www.patent.wang` and downloads exactly one PDF for either an invalidity decision or a reexamination decision.

Local adapter source:

```bash
/Users/chrynos/.opencli/clis/patentwang
```

## Setup Check

Confirm the commands exist before the first use in a session:

```bash
opencli patentwang --help -f yaml
```

The expected commands are:

```bash
opencli patentwang invalidity-search
opencli patentwang invalidity-download
opencli patentwang reexam-search
opencli patentwang reexam-download
```

If they are missing, inspect local overrides:

```bash
opencli adapter status
find /Users/chrynos/.opencli/clis/patentwang -maxdepth 2 -type f -print
```

## Choose the Decision Type

Infer the decision type from the user's wording when possible:

- Use `invalidity-*` for 无效, 无效宣告, invalidity, or case numbers like `6W135227`.
- Use `reexam-*` for 复审, reexamination, or case numbers like `1F867603`.
- If the user only gives a patent number or decision number and the type is unclear, search both types with a small limit and report the matches.

Downloads should use exactly one precise query option. Prefer `--case` when available, then `--decision`, then `--patent`.

## Search Before Downloading

Search first if the request is ambiguous, if multiple matches are possible, or if the user asks to find a decision rather than download it.

Invalidity search:

```bash
opencli patentwang invalidity-search --case 6W135227 --limit 10 -f yaml
opencli patentwang invalidity-search --patent 201910000000.0 --limit 10 -f yaml
opencli patentwang invalidity-search --decision 12345 --limit 10 -f yaml
```

Additional invalidity filters include `--title`, `--requester`, `--owner`, and `--conclusion`.

Reexamination search:

```bash
opencli patentwang reexam-search --case 1F867603 --limit 10 -f yaml
opencli patentwang reexam-search --patent 201910000000.0 --limit 10 -f yaml
opencli patentwang reexam-search --decision 12345 --limit 10 -f yaml
```

Additional reexamination filters include `--title`, `--requester`, `--agency`, `--ipc`, and `--conclusion`.

When search returns more than one plausible row, use `--index` on the download command only after the user has identified the intended row, unless the user's request clearly points to the first result.

## Download PDFs

Use an explicit output directory. For project work, prefer a task-specific folder under the current workspace, such as `./patentwang-downloads`.

Download an invalidity decision:

```bash
opencli patentwang invalidity-download --case 6W135227 --output ./patentwang-downloads -f yaml
opencli patentwang invalidity-download --decision 12345 --output ./patentwang-downloads -f yaml
opencli patentwang invalidity-download --patent 201910000000.0 --index 1 --output ./patentwang-downloads -f yaml
```

Download a reexamination decision:

```bash
opencli patentwang reexam-download --case 1F867603 --output ./patentwang-downloads -f yaml
opencli patentwang reexam-download --decision 12345 --output ./patentwang-downloads -f yaml
opencli patentwang reexam-download --patent 201910000000.0 --index 1 --output ./patentwang-downloads -f yaml
```

For invalidity downloads, the adapter may need a patent.wang key. Prefer the environment variable:

```bash
PATENT_WANG_KEY="$PATENT_WANG_KEY" opencli patentwang invalidity-download --case 6W135227 --output ./patentwang-downloads -f yaml
```

If the user gives a one-off key, pass it with `--key` for that command only. Do not write the key into skill files, shell profiles, logs, or generated documentation.

## Verify and Report

After a download, verify that the saved file exists and is a PDF:

```bash
ls -lh ./patentwang-downloads
file ./patentwang-downloads/*.pdf
```

In the final answer, report the decision type, case number, patent/application number, decision number, title if present, saved absolute path, and file size. Mention whether the PDF signature check passed if you inspected it with `file` or another tool.

## Troubleshooting

- If no results are found, rerun search with a different single query field. For example, try `--patent` if `--decision` failed.
- If a download by patent number finds several rows, search first and use the matching `index`.
- If the invalidity download says the key is missing, set `PATENT_WANG_KEY` or pass `--key` once.
- If a command disappears after local edits, rerun `opencli patentwang --help -f yaml` and inspect `/Users/chrynos/.opencli/clis/patentwang`.
- If the site returns a non-PDF response, report the command output and stop rather than saving the response as a PDF.
