# Patent DOCX Workflow

## Typical uses

- Read Chinese or bilingual patent drafts stored as `.docx`.
- Inspect claims, specification text, amendment drafts, or disclosure files that contain formulas.
- Verify whether formulas are native Word equations, images, or legacy embedded objects.
- Check whether revisions, comments, footnotes, or headers carry legally relevant text.

## OOXML parts to inspect

- `word/document.xml`: main body text, most equations, tables, and figure anchors.
- `word/footnotes.xml` and `word/endnotes.xml`: symbols, citations, or formula notes can hide here.
- `word/comments.xml`: reviewer instructions or unresolved legal edits.
- `word/header*.xml` and `word/footer*.xml`: filing metadata, titles, or draft labels.
- `word/embeddings/*`: legacy Microsoft Equation Editor objects or embedded Office files.
- `word/media/*`: images; formulas stored only as images require visual review.

## Patent section cues

Common Chinese section titles:

- `发明名称`
- `摘要`
- `技术领域`
- `背景技术`
- `发明内容`
- `附图说明`
- `具体实施方式`
- `具体实施例`
- `权利要求书`
- `说明书`
- `说明书摘要`

Common English section titles:

- `Title`
- `Abstract`
- `Technical Field`
- `Background`
- `Summary`
- `Brief Description of the Drawings`
- `Detailed Description`
- `Claims`

## Formula handling

- Treat OMML nodes (`m:oMath`, `m:oMathPara`) as the source of truth for native Word equations.
- Treat `word/embeddings/oleObject*.bin` as a warning that part of the math may be a legacy object rather than inspectable XML.
- If formulas appear as images, report that limitation explicitly and export a PDF for review.
- When comparing formulas across revisions, compare both numbering references such as `式(1)` and local paragraph context.

## Review checklist

- Confirm which patent sections are present.
- Count equations, tables, drawings, comments, insertions, and deletions before summarizing.
- Check whether equation numbering matches references in the surrounding text.
- Check whether symbols stay consistent between abstract, claims, and embodiment sections.
- Check figure and table references after any edit.
- Check whether tracked deletions remove legally meaningful limitations.
- Check headers and footers for draft labels or stale metadata.

## Common failure modes

- Equation content disappears when converted to plain text.
- Subscripts, superscripts, and Greek letters collapse into ambiguous inline text.
- Figures and formula references drift after paragraph edits.
- Old Equation Editor content survives as OLE data that ordinary XML extraction misses.
- Review comments or tracked deletions are omitted from the analysis.

## Recommended order

1. Run `scripts/inspect_docx.py`.
2. Dump equations if the request is formula-sensitive.
3. Read only the OOXML parts implicated by the summary.
4. Export to PDF if layout or image-only formulas matter.
5. State any residual uncertainty before giving a final legal or technical summary.
