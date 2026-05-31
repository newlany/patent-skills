# PatSnap/智慧芽 Browser Search

Use this reference when a prior-art search needs PatSnap/智慧芽 through an authorized logged-in browser session.

## When To Use

Use the browser path when:

- the user explicitly asks for 智慧芽, PatSnap, or a commercial patent database search
- Chinese-current-art coverage, legal-status filtering, semantic search, assignee clustering, family/citation views, or PatSnap ranking may materially improve recall
- BigQuery/Google Patents retrieval is unavailable, too thin, or needs cross-checking against a paid database

Do not make this the only evidence path unless the user specifically asks. Keep public-source expansion and local comparison bundles when possible.

## Access And Privacy

- Use the user's already-running browser profile through `browser-harness`.
- Default entry URL: `https://analytics.zhihuiya.com/` unless the user provides a company, school, SSO/CARSI, or regional entry URL.
- If the page redirects to login, CAPTCHA, SSO, or account selection, stop and ask the user to complete it in the browser.
- Never request, store, type, screenshot deliberately, or copy passwords, cookies, session tokens, QR codes, or one-time codes.
- Save only search evidence and exported result files needed for the patent task, under the active case folder or workspace.

## Browser-Harness Start

Before browser control, read the `browser-harness` skill. Start in a new tab so the user's current tab is not overwritten:

```bash
browser-harness -c '
new_tab("https://analytics.zhihuiya.com/")
wait_for_load()
print(page_info())
print(capture_screenshot("/tmp/patsnap-entry.png"))
'
```

Use screenshots to understand the visible page, then coordinate clicks or text input as directed by the browser-harness skill. After each meaningful click, search, filter change, export, or navigation, capture a screenshot or print `page_info()` to verify state.

Known tested signals:

- logged-in simple search URL: `https://analytics.zhihuiya.com/search/input/simple#/simple`
- result URL pattern: `/search/result/tablelist/1?...&q=<query>&_type=query&search_mode=publication`
- pressing `Enter` in the simple-search text area can submit the query
- result count appears near the query and as text like `共 <n> 条专利`
- result publication numbers and titles can be read from `.pn-cell-popover` and `.title-cell-popover`

## Search Procedure

1. Convert the disclosure compression into 3-5 concise query expressions:
   - broad Chinese scene query
   - Chinese scene + effect query
   - high-specificity technical-anchor query
   - English synonym query when the field has international terminology
   - applicant/inventor/CPC/IPC expansion query when relevant
2. Run searches in 智慧芽 using the available basic, advanced, semantic, or fielded search mode that best fits the query.
3. Apply only defensible filters:
   - jurisdiction, usually CN plus worldwide expansion where needed
   - publication/application date when the search has a known priority cutoff
   - IPC/CPC only after a real cluster appears
   - patent type/status only when the user asked for that scope
4. For each pass, record exact query text, filters, result count, sort order, and the top relevant records.
5. Open likely close records and capture the fields needed for comparison:
   - publication number, application number, title, abstract, claims, applicant, dates, family, CPC/IPC, citation/family signals, and direct URL
6. Export or download results only if the platform permits it and the export is needed. Save exported files under the active case folder, preferably `02_search/patsnap/`.
7. Normalize selected publication numbers and pass them back into the public-source packaging path:
   - `scripts/google_patents_fetch.py fetch`
   - `scripts/download_reference_bundle.py`
   - `patent-support-google-patents-pdfs` if official PDFs are needed

## Evidence Handling

Treat PatSnap findings as `智慧芽网页核对事实` or `检索命中事实` in the memo. For each selected reference, state whether the PDF/Markdown bundle came from public sources, PatSnap export, or browser screenshot/field capture.

If PatSnap gives a result that cannot be independently retrieved from public sources, keep the uncertainty explicit and cite the saved screenshot/export path rather than overstating verification.

## Stop Conditions

Stop the browser pass and report the blocker when:

- login, SSO, CAPTCHA, or permission checks require user action
- export/download is disabled by the account
- repeated searches return unstable or unreadable results
- the platform imposes a rate or access limit

In those cases, continue with public-source search if useful, and list the missing PatSnap step as `待补检`.
