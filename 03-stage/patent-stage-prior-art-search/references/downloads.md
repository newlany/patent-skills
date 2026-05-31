# Downloads

For selected comparison references, prefer delivering both:

- `PDF`
- `Markdown`

## Default Packaging Rule

After the closest-reference set is stable, package the chosen references with:

```bash
.venv/bin/python scripts/download_reference_bundle.py <publication-number> --save-dir <dir>
```

This should save, per reference when possible:

- `<publication>.pdf`
- `<publication>.md`
- optional helper files such as `.json` or `.html`

## Preferred Download Path

Use this order:

1. `scripts/download_reference_bundle.py`
2. direct PDF link extraction from the Google Patents HTML, such as `citation_pdf_url` or the `Download PDF` link
3. headless browser rendering of the Google Patents page into PDF
4. direct PDF resolution through the companion `patent-support-google-patents-pdfs` backend when needed
5. Google Patents Markdown extraction through `google_patents_fetch.py`
6. Playwright browser-automation fallback if the automated PDF paths still fail

## Browser-Automation Fallback

If the Google Patents HTML exposes a `Download PDF` link or `citation_pdf_url`, use that first.

If no direct PDF link is exposed or the download still fails, prefer a headless browser page-PDF render next. If that still fails, use Playwright as a fallback path.

Typical page-PDF path on macOS:

```bash
'/Applications/Microsoft Edge.app/Contents/MacOS/Microsoft Edge' \
  --headless --disable-gpu --no-first-run \
  --print-to-pdf='<output.pdf>' \
  'https://patents.google.com/patent/<publication>/en'
```

Recommended pattern:

```bash
export CODEX_HOME="${CODEX_HOME:-$HOME/.codex}"
export PWCLI="$CODEX_HOME/skills/playwright/scripts/playwright_cli.sh"
"$PWCLI" --session patent-pdf open "https://patents.google.com/patent/<publication>/en" --headed
"$PWCLI" --session patent-pdf snapshot
```

Then either:

- click the PDF/download element after snapshotting, or
- use `"$PWCLI" --session patent-pdf pdf` to save a browser-rendered page PDF as a fallback artifact when the official PDF link is unavailable

If page-PDF fallback is used, state that clearly in the memo so it is not mistaken for the official patent PDF.

## Naming Rule

Prefer one folder per search task and stable publication-based filenames.

Good default:

- `US12424224B2.pdf`
- `US12424224B2.md`

If the user wants `D1`, `D2`, or Chinese comparison labels, add them as prefixes rather than replacing the publication number entirely.
