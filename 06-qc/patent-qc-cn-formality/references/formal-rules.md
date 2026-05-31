# CN Patent Formal Rules

Use this reference to decide which issues are formal defects, which are merely drafting-quality issues, and which fixes are safe enough to apply automatically.

## Core Sources

- [中华人民共和国专利法（国家知识产权局旧站官方 PDF）](https://www.cnipa.gov.cn/transfer/pub/old/ztzl/ywzt/zwfmtlzl/gnwlfzczd/201403/P020140331546022456541.pdf)
- [中华人民共和国专利法实施细则（国家市场监督管理总局）](https://www.samr.gov.cn/zfjcj/tzgg/art/2023/art_9fcfe561729f4014bb9537458b2bcf02.html)
- [专利审查指南 2023（国家知识产权局）](https://www.cnipa.gov.cn/attach/0/%E4%B8%93%E5%88%A9%E5%AE%A1%E6%9F%A5%E6%8C%87%E5%8D%97.pdf)

## How To Use This Reference

1. Treat the Patent Law, the Implementing Rules, and the CNIPA Examination Guidelines as the controlling hierarchy.
2. Prefer rule items that can be checked mechanically from a Word file.
3. Auto-fix only issues that are text-mechanical and do not alter the technical solution.
4. Escalate when the fix requires choosing between alternative technical meanings.

## Rule Catalog

| Rule ID | What to check | Primary basis | Safe auto-fix |
| --- | --- | --- | --- |
| `title-prefix` | The title line should contain only the invention title, not a label such as `发明名称：` or `名称：`. | Guidelines 2023, Part I, Ch.1, 4.2 | Yes |
| `section-missing` | The specification should normally contain `技术领域` / `背景技术` / `发明内容` / `附图说明` / `具体实施方式`. `附图说明` may be absent when there are no drawings. | Guidelines 2023, Part I, Ch.1, 4.2 | No |
| `section-order` | Standard specification sections should appear in the usual order unless the invention nature clearly justifies otherwise. | Guidelines 2023, Part I, Ch.1, 4.2 | No |
| `claim-number-sequence` | Claims should be numbered sequentially in Arabic numerals. | Implementing Rules art. 22; Guidelines 2023, Part I, Ch.1, 4.4 | No by default |
| `claim-terminal-period` | Each claim should end with one sentence-final period only; line breaks inside a claim should use commas or semicolons, not another full stop. | Guidelines 2023, Part I, Ch.2, 7.4 / Part II, Ch.2, 3.3 | Yes |
| `claim-reference-missing` | A dependent claim may cite only claims that actually exist in the current claim set. | Implementing Rules art. 25; Guidelines 2023, Part II, Ch.2, 3.3.2 | No |
| `claim-forward-reference` | A dependent claim may cite only previous claims. | Implementing Rules art. 25; Guidelines 2023, Part II, Ch.2, 3.3.2 | No |
| `multi-dependent-conjunction` | A multi-dependent claim must use an alternative citation style such as `或` / `任一`, not a cumulative `和` / `及`. | Implementing Rules art. 25; Guidelines 2023, Part II, Ch.2, 3.3.2 | No |
| `multi-dependent-base` | A multi-dependent claim cannot depend on another multi-dependent claim. | Implementing Rules art. 25; Guidelines 2023, Part II, Ch.2, 3.3.2 | No |
| `claim-unclear-terms` | Claims should avoid unclear expressions such as `优选` / `最好是` / `尤其是` / `必要时` / `例如` / `约` / `接近` / `等`, because they can make the protection scope unclear. | Guidelines 2023, Part II, Ch.2, 3.2.2 and 3.3 | No |
| `claim-english-abbrev` | Application documents should use Chinese and standard Chinese technical terms. When a standard Chinese technical name exists, avoid writing the claim term only as an untranslated English abbreviation. | Implementing Rules art. 3 | No |
| `dependent-claim-subject` | The reference clause of a dependent claim should restate the cited claim's subject name. | Guidelines 2023, Part II, Ch.2, 3.3.2 | No |
| `dependent-claim-block-order` | All claims directly or indirectly dependent on one independent claim should stay before the next independent claim. | Guidelines 2023, Part II, Ch.2, 3.3.2 | No |
| `claim-drawing` | Claims may contain formulas, but should not contain drawings or embedded objects. | Implementing Rules art. 22; Guidelines 2023, Part I, Ch.2, 7.4 / Part II, Ch.2, 3.3 | No |
| `claim-bare-reference-sign` | When a claim uses a drawing reference sign, the sign should be in parentheses after the technical feature, and should match the specification drawings. | Implementing Rules art. 22; Guidelines 2023, Part I, Ch.2, 7.4 / Part II, Ch.2, 3.3 | Yes when the term-sign mapping is unambiguous |
| `reference-sign-conflict` | The same sign should not map to multiple terms, and the same term should not drift across multiple signs without a justified reason. | Implementing Rules art. 21 and 22; Guidelines 2023, Part I, Ch.2, 7.4 | No |
| `abstract-overlength` | The abstract text, including punctuation, should not exceed 300 characters. | Implementing Rules art. 24 / 26; Guidelines 2023, Part I, Ch.2, 7.5 | No |
| `commercial-language` | Avoid promotional or commercial wording in the title, claims, and abstract. | Guidelines 2023, Part II, Ch.2, 2.2.1 and 3.2 / Part I, Ch.2, 7.4-7.5 | No |
| `tracked-changes` | Final application files should not retain tracked changes or comments. | Practical filing requirement; high risk for filing-quality cleanup | No by default |

## Safe-Fix Boundary

Auto-fix only when all of the following are true:

1. The change is purely textual and localized.
2. The technical meaning is unchanged.
3. The replacement target is unique and deterministic.
4. The change can be applied by patching existing DOCX XML text nodes instead of rebuilding the document.

Typical safe fixes:

- Remove a title label prefix such as `发明名称：`.
- Replace a claim's terminal semicolon or half-width period with a single final `。`.
- Normalize a bare reference sign such as `壳体1` to the already-established canonical form `壳体（1）`.

Typical non-safe fixes:

- Renumber the entire claim set.
- Rewrite a dependent claim citation clause.
- Replace unclear claim-drafting words such as `优选` or `约` when multiple technical meanings are possible.
- Replace an English material abbreviation with a Chinese full name when the intended Chinese technical term is not uniquely recoverable from the file context.
- Choose between inconsistent technical terms that could affect claim scope.
- Shorten an overlength abstract by deleting or rewriting content.

## Word-Focused Interpretation

The user will often provide a `.docx` file rather than structured XML or plain text. For this skill:

1. Read the DOCX as an OOXML package, not as plain text.
2. Preserve paragraph styles, tables, headers, footers, relationships, and media files.
3. Apply text-only repairs by modifying `word/document.xml` nodes in place.
4. Rebuild the `.docx` by copying all parts and replacing only the modified XML part.
5. If the input is `.doc`, normalize it to `.docx` first with LibreOffice.

## Practical Notes

- The rules above are aimed at Chinese patent application drafting and preliminary-examination style formal defects, not at inventive-step or support analysis.
- When drafting a fresh claim set, if a parameter must be written to delimit the scope, prefer a disclosure-supported range rather than a single-point value so the claim keeps an appropriate protection scope; use a fixed-point value only when the disclosure and strategy clearly require it.
- When drafting a fresh claim set rather than only checking a finished draft, prefer single-reference dependent claims by default. Use a multi-dependent claim only when it serves a clear fallback strategy and ensure no later multi-dependent claim cites it.
- A document may be formally clean but still substantively weak. Do not blur those two review types.
- When the source contains formulas, embedded OLE objects, or layout-sensitive patent content, combine this skill with [$patent-support-docx-math](C:/Users/will3/.codex/skills/patent-support-docx-math/SKILL.md).
