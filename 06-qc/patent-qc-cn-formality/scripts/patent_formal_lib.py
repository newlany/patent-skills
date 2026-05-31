#!/usr/bin/env python3
"""Core helpers for the patent-qc-cn-formality skill."""

from __future__ import annotations

import json
import re
import shutil
import subprocess
import tempfile
from collections import Counter, defaultdict
from dataclasses import dataclass
from pathlib import Path
from zipfile import ZIP_DEFLATED, ZipFile

from lxml import etree

NS = {
    "w": "http://schemas.openxmlformats.org/wordprocessingml/2006/main",
}

HEADING_PATTERNS = [
    ("abstract", re.compile(r"^(摘要|说明书摘要|abstract)$", re.IGNORECASE)),
    ("field", re.compile(r"^(技术领域|technical field)$", re.IGNORECASE)),
    ("background", re.compile(r"^(背景技术|background)$", re.IGNORECASE)),
    (
        "summary",
        re.compile(
            r"^(发明内容|实用新型内容|summary|summary of the invention)$",
            re.IGNORECASE,
        ),
    ),
    (
        "drawings",
        re.compile(
            r"^(附图说明|brief description of the drawings)$",
            re.IGNORECASE,
        ),
    ),
    (
        "embodiment",
        re.compile(
            r"^(具体实施方式|具体实施例|实施例|detailed description)$",
            re.IGNORECASE,
        ),
    ),
    ("claims", re.compile(r"^(权利要求书|权利要求|claims)$", re.IGNORECASE)),
    ("specification", re.compile(r"^(说明书|specification)$", re.IGNORECASE)),
]

CLAIM_START_RE = re.compile(r"^\s*(\d+)\s*[.．、]?\s*(.+?)\s*$")
TITLE_PREFIX_RE = re.compile(r"^(发明名称|名称)\s*[:：]\s*")
CLAIM_REFERENCE_CLAUSE_RE = re.compile(r"(?:根据|如)\s*权利要求(.{0,120}?)所述")
DEPENDENT_CLAIM_RE = re.compile(r"^\s*(?:根据|如)\s*权利要求")
DEPENDENT_SUBJECT_RE = re.compile(r"(?:根据|如)\s*权利要求.{0,120}?所述的(.+?)(?:，|,|；|;)")
RANGE_RE = re.compile(r"(\d+)\s*(?:至|-|—|~|～)\s*(\d+)")
REFERENCE_SIGN_RE = re.compile(
    r"(?P<term>[A-Za-z\u4e00-\u9fff][A-Za-z0-9_\-\u4e00-\u9fff]{0,30})"
    r"\s*[（(]\s*(?P<sign>[0-9]{1,4}[A-Za-z]?)\s*[）)]"
)
FIGURE_RE = re.compile(r"图\s*([0-9]+)")
COMMERCIAL_TERMS = (
    "最佳",
    "最优",
    "优选地",
    "高效",
    "高性能",
    "顶级",
    "理想",
    "完美",
    "独家",
    "专用",
    "唯一",
    "首创",
)

REFERENCE_TERM_SPLITS = (
    "现有技术中",
    "实施例中",
    "包括",
    "包含",
    "以及",
    "连接到",
    "连接于",
    "连接在",
    "设置在",
    "设于",
    "位于",
    "安装在",
    "安装于",
    "固定在",
    "固定于",
    "所述",
    "和",
    "与",
    "及",
    "在",
    "于",
)


@dataclass
class ParagraphRecord:
    index: int
    node: etree._Element
    text: str
    style: str | None
    drawings: int


@dataclass
class ClaimRecord:
    number: int
    text: str
    paragraphs: list[ParagraphRecord]
    cited_numbers: list[int]
    is_dependent: bool
    is_multi_dependent: bool
    dependent_subject: str | None


def normalize_input(path: str | Path) -> tuple[Path, list[str]]:
    """Return a docx path. Convert .doc via LibreOffice when available."""
    input_path = Path(path).expanduser().resolve()
    notes: list[str] = []
    suffix = input_path.suffix.lower()
    if suffix == ".docx":
        return input_path, notes
    if suffix != ".doc":
        raise SystemExit(f"unsupported file type: {input_path.suffix}")

    office = find_executable(
        ["soffice", "libreoffice", "/Applications/LibreOffice.app/Contents/MacOS/soffice"]
    )
    if not office:
        raise SystemExit("input is .doc and LibreOffice/soffice is unavailable for normalization")

    temp_dir = Path(tempfile.mkdtemp(prefix="patent-formal-docx-"))
    cmd = [
        office,
        "--headless",
        "--convert-to",
        "docx",
        "--outdir",
        str(temp_dir),
        str(input_path),
    ]
    completed = subprocess.run(cmd, capture_output=True, text=True)
    if completed.returncode != 0:
        raise SystemExit(
            completed.stderr.strip() or completed.stdout.strip() or "failed to convert .doc to .docx"
        )
    output = temp_dir / f"{input_path.stem}.docx"
    if not output.exists():
        raise SystemExit("conversion reported success but produced no .docx file")
    notes.append(f"normalized .doc to {output}")
    return output, notes


def find_executable(candidates: list[str]) -> str | None:
    for candidate in candidates:
        resolved = shutil.which(candidate)
        if resolved:
            return resolved
        path = Path(candidate)
        if path.exists():
            return str(path)
    return None


def scan_docx(path: str | Path) -> dict:
    docx_path, notes = normalize_input(path)
    with ZipFile(docx_path) as zf:
        names = set(zf.namelist())
        if "word/document.xml" not in names:
            raise SystemExit("DOCX does not contain word/document.xml")
        document_root = etree.fromstring(zf.read("word/document.xml"))
        paragraphs = build_paragraph_records(document_root)
        sections = detect_sections(paragraphs)
        claims = extract_claims(paragraphs, sections)
        title_record = find_title_record(paragraphs)
        abstract_info = extract_abstract(paragraphs, sections)
        ref_sign_catalog = build_reference_sign_catalog(paragraphs)
        issues = []
        issues.extend(check_title(title_record))
        issues.extend(check_section_order(sections))
        issues.extend(check_abstract(abstract_info))
        issues.extend(check_claims(claims))
        issues.extend(check_reference_signs(paragraphs, claims, ref_sign_catalog))
        issues.extend(check_commercial_terms(title_record, abstract_info, claims))
        issues.extend(check_tracked_objects(document_root, names, zf))

        summary = {
            "paragraph_count": len(paragraphs),
            "claim_count": len(claims),
            "auto_fixable_count": sum(1 for issue in issues if issue["auto_fixable"]),
            "issue_count": len(issues),
            "abstract_char_count": abstract_info["char_count"],
            "tracked_insertions": len(document_root.xpath(".//w:ins", namespaces=NS)),
            "tracked_deletions": len(document_root.xpath(".//w:del", namespaces=NS)),
            "comment_reference_count": len(
                document_root.xpath(".//w:commentReference", namespaces=NS)
            ),
        }

    return {
        "input": str(Path(path).expanduser().resolve()),
        "normalized_input": str(docx_path),
        "notes": notes,
        "summary": summary,
        "sections": sections,
        "title": serialize_paragraph(title_record),
        "abstract": abstract_info,
        "claims": [serialize_claim(claim) for claim in claims],
        "reference_sign_catalog": ref_sign_catalog,
        "issues": sorted(issues, key=issue_sort_key),
    }


def fix_docx(path: str | Path, output_path: str | Path) -> dict:
    report = scan_docx(path)
    source = Path(report["normalized_input"])
    output = Path(output_path).expanduser().resolve()
    output.parent.mkdir(parents=True, exist_ok=True)

    with ZipFile(source) as zf:
        document_root = etree.fromstring(zf.read("word/document.xml"))
        paragraphs = build_paragraph_records(document_root)
        paragraph_map = {paragraph.index: paragraph for paragraph in paragraphs}
        paragraph_updates = {paragraph.index: paragraph.text for paragraph in paragraphs}

        for issue in report["issues"]:
            if not issue["auto_fixable"]:
                continue
            rule_id = issue["rule_id"]
            if rule_id == "title-prefix":
                index = issue["paragraph_index"]
                paragraph_updates[index] = TITLE_PREFIX_RE.sub("", paragraph_updates[index]).strip()
            elif rule_id == "claim-terminal-period":
                index = issue["paragraph_index"]
                paragraph_updates[index] = normalize_terminal_period(paragraph_updates[index])
            elif rule_id == "claim-bare-reference-sign":
                index = issue["paragraph_index"]
                old = issue["before"]
                new = issue["after"]
                paragraph_updates[index] = paragraph_updates[index].replace(old, new)

        applied_updates = []
        for index, new_text in paragraph_updates.items():
            paragraph = paragraph_map[index]
            if paragraph.text == new_text:
                continue
            replace_paragraph_text(paragraph.node, new_text)
            applied_updates.append(
                {
                    "paragraph_index": index,
                    "before": paragraph.text,
                    "after": new_text,
                }
            )

        xml_bytes = etree.tostring(
            document_root,
            encoding="UTF-8",
            xml_declaration=True,
            standalone="yes",
        )

        with ZipFile(output, "w", compression=ZIP_DEFLATED) as out_zip:
            for name in zf.namelist():
                if name == "word/document.xml":
                    out_zip.writestr(name, xml_bytes)
                else:
                    out_zip.writestr(name, zf.read(name))

    after_report = scan_docx(output)
    return {
        "input": report["input"],
        "normalized_input": report["normalized_input"],
        "output": str(output),
        "applied_update_count": len(applied_updates),
        "applied_updates": applied_updates,
        "issues_before": report["summary"]["issue_count"],
        "issues_after": after_report["summary"]["issue_count"],
        "auto_fixable_before": report["summary"]["auto_fixable_count"],
        "auto_fixable_after": after_report["summary"]["auto_fixable_count"],
        "verification": {
            "paragraph_count_unchanged": report["summary"]["paragraph_count"]
            == after_report["summary"]["paragraph_count"],
            "claim_count_unchanged": report["summary"]["claim_count"]
            == after_report["summary"]["claim_count"],
        },
        "remaining_issues": after_report["issues"],
    }


def build_paragraph_records(document_root) -> list[ParagraphRecord]:
    records = []
    for index, node in enumerate(document_root.xpath("./w:body//w:p", namespaces=NS), start=1):
        records.append(
            ParagraphRecord(
                index=index,
                node=node,
                text=paragraph_text(node).strip(),
                style=paragraph_style(node),
                drawings=len(node.xpath(".//w:drawing | .//w:object", namespaces=NS)),
            )
        )
    return records


def paragraph_text(node) -> str:
    texts = node.xpath(".//w:t[not(ancestor::w:del)]", namespaces=NS)
    return "".join(text.text or "" for text in texts)


def paragraph_style(node) -> str | None:
    values = node.xpath("./w:pPr/w:pStyle/@w:val", namespaces=NS)
    return values[0] if values else None


def detect_sections(paragraphs: list[ParagraphRecord]) -> list[dict]:
    sections = []
    for paragraph in paragraphs:
        heading = normalize_heading(paragraph.text)
        if not heading:
            continue
        for label, pattern in HEADING_PATTERNS:
            if pattern.match(heading):
                sections.append(
                    {
                        "label": label,
                        "paragraph_index": paragraph.index,
                        "text": paragraph.text,
                        "style": paragraph.style,
                    }
                )
                break
    return sections


def normalize_heading(text: str) -> str:
    return re.sub(r"\s+", "", text).strip("：: ")


def find_title_record(paragraphs: list[ParagraphRecord]) -> ParagraphRecord | None:
    for paragraph in paragraphs:
        if TITLE_PREFIX_RE.match(paragraph.text):
            return paragraph
    for paragraph in paragraphs:
        heading = normalize_heading(paragraph.text)
        if not paragraph.text:
            continue
        if any(pattern.match(heading) for _, pattern in HEADING_PATTERNS):
            continue
        return paragraph
    return None


def serialize_paragraph(record: ParagraphRecord | None) -> dict | None:
    if record is None:
        return None
    return {
        "paragraph_index": record.index,
        "text": record.text,
        "style": record.style,
        "drawings": record.drawings,
    }


def section_boundaries(
    paragraphs: list[ParagraphRecord], sections: list[dict]
) -> dict[str, tuple[int, int, int]]:
    boundaries: dict[str, tuple[int, int, int]] = {}
    ordered = sorted(sections, key=lambda item: item["paragraph_index"])
    index_lookup = {paragraph.index: position for position, paragraph in enumerate(paragraphs)}
    for position, section in enumerate(ordered):
        start_index = index_lookup[section["paragraph_index"]]
        end_index = len(paragraphs) - 1
        if position + 1 < len(ordered):
            next_index = index_lookup[ordered[position + 1]["paragraph_index"]]
            end_index = next_index - 1
        boundaries.setdefault(section["label"], (start_index, end_index, section["paragraph_index"]))
    return boundaries


def extract_claims(paragraphs: list[ParagraphRecord], sections: list[dict]) -> list[ClaimRecord]:
    boundaries = section_boundaries(paragraphs, sections)
    if "claims" in boundaries:
        start_index, end_index, heading_index = boundaries["claims"]
        claim_paragraphs = paragraphs[start_index : end_index + 1]
        if claim_paragraphs and claim_paragraphs[0].index == heading_index:
            claim_paragraphs = claim_paragraphs[1:]
    else:
        claim_paragraphs = paragraphs

    claims: list[ClaimRecord] = []
    current: list[ParagraphRecord] = []
    current_number: int | None = None
    for paragraph in claim_paragraphs:
        if not paragraph.text:
            continue
        match = CLAIM_START_RE.match(paragraph.text)
        if match:
            if current and current_number is not None:
                claims.append(build_claim(current_number, current))
            current_number = int(match.group(1))
            current = [paragraph]
        elif current:
            current.append(paragraph)
    if current and current_number is not None:
        claims.append(build_claim(current_number, current))
    return claims


def build_claim(number: int, paragraphs: list[ParagraphRecord]) -> ClaimRecord:
    text_parts = []
    for offset, paragraph in enumerate(paragraphs):
        if not paragraph.text:
            continue
        if offset == 0:
            match = CLAIM_START_RE.match(paragraph.text)
            text_parts.append(match.group(2).strip() if match else paragraph.text)
        else:
            text_parts.append(paragraph.text)
    text = "\n".join(text_parts)
    cited_numbers = extract_cited_numbers(text)
    dependent_subject = None
    subject_match = DEPENDENT_SUBJECT_RE.search(text)
    if subject_match:
        dependent_subject = subject_match.group(1).strip()
    return ClaimRecord(
        number=number,
        text=text,
        paragraphs=paragraphs,
        cited_numbers=cited_numbers,
        is_dependent=bool(DEPENDENT_CLAIM_RE.match(text)),
        is_multi_dependent=len(cited_numbers) > 1,
        dependent_subject=dependent_subject,
    )


def extract_cited_numbers(text: str) -> list[int]:
    match = CLAIM_REFERENCE_CLAUSE_RE.search(text)
    if not match:
        return []
    clause = match.group(1)
    numbers: list[int] = []
    for start, end in RANGE_RE.findall(clause):
        first = int(start)
        last = int(end)
        step = 1 if last >= first else -1
        for value in range(first, last + step, step):
            numbers.append(value)
    clause_without_ranges = RANGE_RE.sub(" ", clause)
    numbers.extend(int(value) for value in re.findall(r"\d+", clause_without_ranges))
    deduped = []
    seen = set()
    for value in numbers:
        if value not in seen:
            deduped.append(value)
            seen.add(value)
    return deduped


def serialize_claim(claim: ClaimRecord) -> dict:
    return {
        "number": claim.number,
        "text": claim.text,
        "paragraph_indexes": [paragraph.index for paragraph in claim.paragraphs],
        "is_dependent": claim.is_dependent,
        "is_multi_dependent": claim.is_multi_dependent,
        "cited_numbers": claim.cited_numbers,
        "dependent_subject": claim.dependent_subject,
    }


def extract_abstract(paragraphs: list[ParagraphRecord], sections: list[dict]) -> dict:
    boundaries = section_boundaries(paragraphs, sections)
    if "abstract" not in boundaries:
        return {"paragraph_indexes": [], "text": "", "char_count": 0}
    start_index, end_index, heading_index = boundaries["abstract"]
    abstract_paragraphs = paragraphs[start_index : end_index + 1]
    if abstract_paragraphs and abstract_paragraphs[0].index == heading_index:
        abstract_paragraphs = abstract_paragraphs[1:]
    text = "\n".join(paragraph.text for paragraph in abstract_paragraphs if paragraph.text)
    char_count = len(re.sub(r"\s+", "", text))
    return {
        "paragraph_indexes": [paragraph.index for paragraph in abstract_paragraphs],
        "text": text,
        "char_count": char_count,
    }


def build_reference_sign_catalog(paragraphs: list[ParagraphRecord]) -> dict:
    rendered_pairs = {}
    sign_to_terms: dict[str, list[str]] = defaultdict(list)
    term_to_signs: dict[str, list[str]] = defaultdict(list)
    paragraph_pairs: dict[int, list[dict]] = defaultdict(list)
    for paragraph in paragraphs:
        for match in REFERENCE_SIGN_RE.finditer(paragraph.text):
            raw_term = match.group("term")
            term = normalize_reference_term(raw_term)
            sign = match.group("sign")
            left = "（" if "（" in match.group(0) else "("
            right = "）" if "）" in match.group(0) else ")"
            rendered = f"{term}{left}{sign}{right}"
            rendered_pairs.setdefault((term, sign), rendered)
            sign_to_terms[sign].append(term)
            term_to_signs[term].append(sign)
            paragraph_pairs[paragraph.index].append(
                {"term": term, "sign": sign, "rendered": rendered}
            )

    canonical_pairs = {}
    for term, signs in term_to_signs.items():
        unique_signs = set(signs)
        if len(unique_signs) != 1:
            continue
        sign = next(iter(unique_signs))
        if len(set(sign_to_terms[sign])) != 1:
            continue
        canonical_pairs[(term, sign)] = rendered_pairs[(term, sign)]

    conflicts = []
    for sign, terms in sign_to_terms.items():
        if len(set(terms)) > 1:
            conflicts.append(
                {
                    "type": "same-sign-multiple-terms",
                    "sign": sign,
                    "terms": sorted(set(terms)),
                }
            )
    for term, signs in term_to_signs.items():
        if len(set(signs)) > 1:
            conflicts.append(
                {
                    "type": "same-term-multiple-signs",
                    "term": term,
                    "signs": sorted(set(signs)),
                }
            )

    return {
        "canonical_pairs": [
            {"term": term, "sign": sign, "rendered": rendered}
            for (term, sign), rendered in sorted(canonical_pairs.items())
        ],
        "conflicts": conflicts,
        "paragraph_pairs": paragraph_pairs,
    }


def normalize_reference_term(raw_term: str) -> str:
    term = re.split(r"[，,；;、\s]", raw_term)[-1]
    for splitter in REFERENCE_TERM_SPLITS:
        if splitter in term:
            term = term.split(splitter)[-1]
    term = re.sub(r"\d+$", "", term)
    term = term.strip("，,；;：:（）() ")
    return term or raw_term.strip()


def check_title(title_record: ParagraphRecord | None) -> list[dict]:
    if title_record is None:
        return []
    issues = []
    if TITLE_PREFIX_RE.match(title_record.text):
        issues.append(
            issue(
                rule_id="title-prefix",
                level="error",
                summary="Title paragraph uses a disallowed label prefix",
                detail="The title line starts with '发明名称' or '名称'. Remove the label and keep only the invention title.",
                paragraph_index=title_record.index,
                auto_fixable=True,
            )
        )
    return issues


def check_section_order(sections: list[dict]) -> list[dict]:
    issues = []
    expected = ["field", "background", "summary", "embodiment"]
    found = {section["label"]: section for section in sections}
    for label in expected:
        if label not in found:
            issues.append(
                issue(
                    rule_id="section-missing",
                    level="warning",
                    summary=f"Missing expected specification section: {label}",
                    detail="The specification usually needs the standard CN section headings in order.",
                    paragraph_index=None,
                    auto_fixable=False,
                )
            )

    ordered = [section["label"] for section in sections if section["label"] in expected + ["drawings"]]
    order_map = {"field": 1, "background": 2, "summary": 3, "drawings": 4, "embodiment": 5}
    scores = [order_map[label] for label in ordered]
    if scores != sorted(scores):
        issues.append(
            issue(
                rule_id="section-order",
                level="warning",
                summary="Specification section headings appear out of order",
                detail="Standard sections should appear in the usual CN order unless the nature of the invention justifies a different structure.",
                paragraph_index=None,
                auto_fixable=False,
            )
        )
    return issues


def check_abstract(abstract_info: dict) -> list[dict]:
    if not abstract_info["paragraph_indexes"]:
        return []
    issues = []
    if abstract_info["char_count"] > 300:
        issues.append(
            issue(
                rule_id="abstract-overlength",
                level="error",
                summary="Abstract exceeds 300 characters",
                detail="The CN patent abstract text, including punctuation, should not exceed 300 characters.",
                paragraph_index=abstract_info["paragraph_indexes"][0],
                auto_fixable=False,
            )
        )
    return issues


def check_claims(claims: list[ClaimRecord]) -> list[dict]:
    issues = []
    numbers = [claim.number for claim in claims]
    expected = list(range(1, len(claims) + 1))
    if numbers != expected:
        issues.append(
            issue(
                rule_id="claim-number-sequence",
                level="error",
                summary="Claims are not numbered sequentially in Arabic numerals",
                detail=f"Observed claim numbers: {numbers}; expected: {expected}.",
                paragraph_index=claims[0].paragraphs[0].index if claims else None,
                auto_fixable=False,
            )
        )

    claim_map = {claim.number: claim for claim in claims}
    root_cache: dict[int, set[int]] = {}

    def roots(number: int, visiting: set[int] | None = None) -> set[int]:
        if number in root_cache:
            return root_cache[number]
        if visiting is None:
            visiting = set()
        if number in visiting:
            return set()
        visiting = set(visiting)
        visiting.add(number)
        claim = claim_map.get(number)
        if claim is None:
            return set()
        if not claim.is_dependent:
            root_cache[number] = {number}
            return root_cache[number]
        result: set[int] = set()
        for cited in claim.cited_numbers:
            result.update(roots(cited, visiting))
        root_cache[number] = result
        return result

    latest_independent: int | None = None
    multi_dependent_numbers = {claim.number for claim in claims if claim.is_multi_dependent}

    for claim in claims:
        if not claim.is_dependent:
            latest_independent = claim.number
        if claim.paragraphs and claim.paragraphs[-1].text:
            terminal = claim.paragraphs[-1].text[-1]
            if terminal != "。":
                issues.append(
                    issue(
                        rule_id="claim-terminal-period",
                        level="error",
                        summary=f"Claim {claim.number} does not end with a full stop",
                        detail="Each claim should end with a single sentence-final full stop.",
                        paragraph_index=claim.paragraphs[-1].index,
                        auto_fixable=True,
                    )
                )
        if any(paragraph.drawings for paragraph in claim.paragraphs):
            issues.append(
                issue(
                    rule_id="claim-drawing",
                    level="error",
                    summary=f"Claim {claim.number} contains a drawing or embedded object",
                    detail="Claims may contain formulas but should not contain drawings.",
                    paragraph_index=claim.paragraphs[0].index,
                    auto_fixable=False,
                )
            )
        if not claim.is_dependent:
            continue

        if not claim.dependent_subject:
            issues.append(
                issue(
                    rule_id="dependent-claim-subject",
                    level="warning",
                    summary=f"Dependent claim {claim.number} may be missing the repeated subject name",
                    detail="The reference clause of a dependent claim should restate the cited claim's subject name.",
                    paragraph_index=claim.paragraphs[0].index,
                    auto_fixable=False,
                )
            )

        for cited in claim.cited_numbers:
            if cited not in claim_map:
                issues.append(
                    issue(
                        rule_id="claim-reference-missing",
                        level="error",
                        summary=f"Claim {claim.number} cites a missing claim {cited}",
                        detail="All cited claim numbers must exist in the current claim set.",
                        paragraph_index=claim.paragraphs[0].index,
                        auto_fixable=False,
                    )
                )
            if cited >= claim.number:
                issues.append(
                    issue(
                        rule_id="claim-forward-reference",
                        level="error",
                        summary=f"Claim {claim.number} cites a non-previous claim {cited}",
                        detail="A dependent claim may cite only claims that appear before it.",
                        paragraph_index=claim.paragraphs[0].index,
                        auto_fixable=False,
                    )
                )

        if claim.is_multi_dependent:
            clause_match = CLAIM_REFERENCE_CLAUSE_RE.search(claim.text)
            clause_text = clause_match.group(0) if clause_match else claim.text[:80]
            if "或" not in clause_text and "任一" not in clause_text and "任意" not in clause_text:
                issues.append(
                    issue(
                        rule_id="multi-dependent-conjunction",
                        level="error",
                        summary=f"Multi-dependent claim {claim.number} is not written in alternative form",
                        detail="A multi-dependent claim should cite claims in an 'or/任一' style rather than a cumulative 'and/及/和' style.",
                        paragraph_index=claim.paragraphs[0].index,
                        auto_fixable=False,
                    )
                )
            if any(cited in multi_dependent_numbers for cited in claim.cited_numbers):
                issues.append(
                    issue(
                        rule_id="multi-dependent-base",
                        level="error",
                        summary=f"Multi-dependent claim {claim.number} cites another multi-dependent claim",
                        detail="A multi-dependent claim must not use another multi-dependent claim as its basis.",
                        paragraph_index=claim.paragraphs[0].index,
                        auto_fixable=False,
                    )
                )

        if latest_independent is not None:
            root_numbers = roots(claim.number)
            if root_numbers and any(root != latest_independent for root in root_numbers):
                issues.append(
                    issue(
                        rule_id="dependent-claim-block-order",
                        level="warning",
                        summary=f"Dependent claim {claim.number} appears after a later independent-claim block",
                        detail="All claims directly or indirectly dependent on one independent claim should stay before the next independent claim.",
                        paragraph_index=claim.paragraphs[0].index,
                        auto_fixable=False,
                    )
                )

    return issues


def check_reference_signs(
    paragraphs: list[ParagraphRecord], claims: list[ClaimRecord], catalog: dict
) -> list[dict]:
    issues = []
    for conflict in catalog["conflicts"]:
        issues.append(
            issue(
                rule_id="reference-sign-conflict",
                level="warning",
                summary="Reference sign terminology is inconsistent",
                detail=json.dumps(conflict, ensure_ascii=False),
                paragraph_index=None,
                auto_fixable=False,
            )
        )

    canonical_pairs = {
        (entry["term"], entry["sign"]): entry["rendered"] for entry in catalog["canonical_pairs"]
    }
    claim_paragraph_indexes = {
        paragraph.index for claim in claims for paragraph in claim.paragraphs
    }
    for paragraph in paragraphs:
        if paragraph.index not in claim_paragraph_indexes:
            continue
        for (term, sign), rendered in canonical_pairs.items():
            pattern = re.compile(rf"{re.escape(term)}\s*{re.escape(sign)}(?!\d)")
            for match in pattern.finditer(paragraph.text):
                candidate = match.group(0)
                if "（" in candidate or "(" in candidate:
                    continue
                issues.append(
                    issue(
                        rule_id="claim-bare-reference-sign",
                        level="warning",
                        summary="Reference sign is not enclosed in parentheses",
                        detail=f"Normalize '{candidate}' to '{rendered}' after the same technical feature.",
                        paragraph_index=paragraph.index,
                        auto_fixable=True,
                        before=candidate,
                        after=rendered,
                    )
                )
    return issues


def check_commercial_terms(
    title_record: ParagraphRecord | None, abstract_info: dict, claims: list[ClaimRecord]
) -> list[dict]:
    issues = []
    locations = []
    if title_record is not None:
        locations.append((title_record.index, title_record.text, "title"))
    if abstract_info["paragraph_indexes"]:
        locations.append((abstract_info["paragraph_indexes"][0], abstract_info["text"], "abstract"))
    for claim in claims:
        locations.append((claim.paragraphs[0].index, claim.text, f"claim {claim.number}"))

    for paragraph_index, text, label in locations:
        for term in COMMERCIAL_TERMS:
            if term in text:
                issues.append(
                    issue(
                        rule_id="commercial-language",
                        level="warning",
                        summary=f"Commercial or promotional wording appears in {label}",
                        detail=f"Found '{term}'. CN practice disfavors commercial or promotional wording in titles, claims, and abstracts.",
                        paragraph_index=paragraph_index,
                        auto_fixable=False,
                    )
                )
    return issues


def check_tracked_objects(document_root, names: set[str], zf: ZipFile) -> list[dict]:
    issues = []
    insertion_count = len(document_root.xpath(".//w:ins", namespaces=NS))
    deletion_count = len(document_root.xpath(".//w:del", namespaces=NS))
    comment_count = len(document_root.xpath(".//w:commentReference", namespaces=NS))
    if "word/comments.xml" in names:
        comments_root = etree.fromstring(zf.read("word/comments.xml"))
        comment_count += len(comments_root.xpath(".//w:comment", namespaces=NS))
    if insertion_count or deletion_count or comment_count:
        issues.append(
            issue(
                rule_id="tracked-changes",
                level="warning",
                summary="Tracked changes or comments remain in the document package",
                detail=(
                    f"tracked insertions={insertion_count}, tracked deletions={deletion_count}, "
                    f"comments={comment_count}"
                ),
                paragraph_index=None,
                auto_fixable=False,
            )
        )
    return issues


def normalize_terminal_period(text: str) -> str:
    stripped = text.rstrip()
    stripped = re.sub(r"[。.;；]+$", "", stripped)
    return f"{stripped}。"


def replace_paragraph_text(paragraph, new_text: str) -> None:
    text_nodes = paragraph.xpath(".//w:t[not(ancestor::w:del)]", namespaces=NS)
    if not text_nodes:
        run = paragraph.find("./w:r", namespaces=NS)
        if run is None:
            run = etree.SubElement(paragraph, f"{{{NS['w']}}}r")
        text_node = etree.SubElement(run, f"{{{NS['w']}}}t")
        text_node.text = new_text
        return

    remaining = new_text
    for node in text_nodes[:-1]:
        current = node.text or ""
        take = min(len(current), len(remaining))
        node.text = remaining[:take]
        remaining = remaining[take:]
        if not node.text:
            node.text = ""
    text_nodes[-1].text = remaining


def issue(
    *,
    rule_id: str,
    level: str,
    summary: str,
    detail: str,
    paragraph_index: int | None,
    auto_fixable: bool,
    before: str | None = None,
    after: str | None = None,
) -> dict:
    payload = {
        "rule_id": rule_id,
        "level": level,
        "summary": summary,
        "detail": detail,
        "paragraph_index": paragraph_index,
        "auto_fixable": auto_fixable,
    }
    if before is not None:
        payload["before"] = before
    if after is not None:
        payload["after"] = after
    return payload


def issue_sort_key(item: dict) -> tuple[int, int]:
    level_rank = {"error": 0, "warning": 1}
    return (
        level_rank.get(item["level"], 9),
        item["paragraph_index"] if item["paragraph_index"] is not None else 999999,
    )


def format_scan_report(report: dict) -> str:
    lines = [
        f"Input: {report['input']}",
        f"Normalized input: {report['normalized_input']}",
        f"Claims: {report['summary']['claim_count']}",
        f"Abstract chars: {report['summary']['abstract_char_count']}",
        f"Issues: {report['summary']['issue_count']} (auto-fixable: {report['summary']['auto_fixable_count']})",
    ]
    if report["notes"]:
        lines.append("Notes:")
        for note in report["notes"]:
            lines.append(f"  - {note}")
    if report["issues"]:
        lines.append("")
        lines.append("Issues:")
        for issue_item in report["issues"]:
            location = (
                f"paragraph {issue_item['paragraph_index']}"
                if issue_item["paragraph_index"] is not None
                else "document"
            )
            lines.append(
                f"  - [{issue_item['level']}] {issue_item['rule_id']} at {location}: {issue_item['summary']}"
            )
    else:
        lines.append("")
        lines.append("Issues: none")
    return "\n".join(lines)


def format_fix_report(report: dict) -> str:
    lines = [
        f"Input: {report['input']}",
        f"Output: {report['output']}",
        f"Applied updates: {report['applied_update_count']}",
        f"Issues before: {report['issues_before']}",
        f"Issues after: {report['issues_after']}",
        "Verification:",
        f"  - paragraph count unchanged: {report['verification']['paragraph_count_unchanged']}",
        f"  - claim count unchanged: {report['verification']['claim_count_unchanged']}",
    ]
    if report["remaining_issues"]:
        lines.append("Remaining issues:")
        for issue_item in report["remaining_issues"]:
            location = (
                f"paragraph {issue_item['paragraph_index']}"
                if issue_item["paragraph_index"] is not None
                else "document"
            )
            lines.append(
                f"  - [{issue_item['level']}] {issue_item['rule_id']} at {location}: {issue_item['summary']}"
            )
    else:
        lines.append("Remaining issues: none")
    return "\n".join(lines)
