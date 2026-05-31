# Patent External Brief DOCX Layout

This reference freezes the shared style for outward-facing Chinese patent communication DOCX files.

## Preset

Base archetype: compact formal business brief.

Page:

- Size: US Letter portrait
- Margins: 1 inch on all sides
- Header/footer: none
- Footer page numbers: do not add by default

Typography:

- Font: `Microsoft YaHei`
- Title: 20 pt, bold, centered, dark blue `#0B2545`, bottom rule `#2E74B5`
- Metadata: 10.5 pt, gray `#555555`, label bold, compact spacing
- Heading 1: 15 pt, bold, blue `#2E74B5`, 16 pt before, 8 pt after
- Heading 2: 13 pt, bold, blue `#2E74B5`, 12 pt before, 6 pt after
- Body: 11 pt, black, left aligned, 1.10 line spacing, 6 pt after

Document character:

- Formal, direct, readable
- No decorative cover page
- No tables unless content is truly tabular
- No footers or page-number fields unless specifically requested
- Preserve a concise external-facing tone
- Prefer clear conclusions and practical next steps over internal process detail

## Conversion Rules

- Treat `#` as the centered document title.
- Treat metadata lines before the first `##` as compact gray matter.
- Treat each non-empty Markdown paragraph as a Word paragraph.
- Avoid full justification; use left alignment to reduce awkward Chinese spacing.
- Keep headings blue for scanability.
- Render after generation and inspect for clipping, missing glyphs, overlap, stray footer fields, or poor page breaks.
