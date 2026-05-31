#!/usr/bin/env python3
"""Utilities for Chinese patent application DOCX/TXT review.

Stdlib-only by design. This is a first-pass helper, not a substitute for
attorney review or a full OpenXML document editor.
"""

from __future__ import annotations

import argparse
import json
import re
import shutil
import sys
import tempfile
import zipfile
import xml.etree.ElementTree as ET
from pathlib import Path

W_NS = "http://schemas.openxmlformats.org/wordprocessingml/2006/main"
W = f"{{{W_NS}}}"

NAMESPACES = {
    "wpc": "http://schemas.microsoft.com/office/word/2010/wordprocessingCanvas",
    "cx": "http://schemas.microsoft.com/office/drawing/2014/chartex",
    "cx1": "http://schemas.microsoft.com/office/drawing/2015/9/8/chartex",
    "cx2": "http://schemas.microsoft.com/office/drawing/2015/10/21/chartex",
    "cx3": "http://schemas.microsoft.com/office/drawing/2016/5/9/chartex",
    "cx4": "http://schemas.microsoft.com/office/drawing/2016/5/10/chartex",
    "cx5": "http://schemas.microsoft.com/office/drawing/2016/5/11/chartex",
    "cx6": "http://schemas.microsoft.com/office/drawing/2016/5/12/chartex",
    "cx7": "http://schemas.microsoft.com/office/drawing/2016/5/13/chartex",
    "cx8": "http://schemas.microsoft.com/office/drawing/2016/5/14/chartex",
    "mc": "http://schemas.openxmlformats.org/markup-compatibility/2006",
    "o": "urn:schemas-microsoft-com:office:office",
    "r": "http://schemas.openxmlformats.org/officeDocument/2006/relationships",
    "m": "http://schemas.openxmlformats.org/officeDocument/2006/math",
    "v": "urn:schemas-microsoft-com:vml",
    "wp14": "http://schemas.microsoft.com/office/word/2010/wordprocessingDrawing",
    "wp": "http://schemas.openxmlformats.org/drawingml/2006/wordprocessingDrawing",
    "w10": "urn:schemas-microsoft-com:office:word",
    "w": W_NS,
    "w14": "http://schemas.microsoft.com/office/word/2010/wordml",
    "w15": "http://schemas.microsoft.com/office/word/2012/wordml",
    "w16cex": "http://schemas.microsoft.com/office/word/2018/wordml/cex",
    "w16cid": "http://schemas.microsoft.com/office/word/2016/wordml/cid",
    "w16": "http://schemas.microsoft.com/office/word/2018/wordml",
    "wpg": "http://schemas.microsoft.com/office/word/2010/wordprocessingGroup",
    "wpi": "http://schemas.microsoft.com/office/word/2010/wordprocessingInk",
    "wne": "http://schemas.microsoft.com/office/word/2006/wordml",
    "wps": "http://schemas.microsoft.com/office/word/2010/wordprocessingShape",
}

for prefix, uri in NAMESPACES.items():
    ET.register_namespace(prefix, uri)


def load_docx(path: Path) -> tuple[ET.Element, dict[str, bytes], list[zipfile.ZipInfo]]:
    with zipfile.ZipFile(path, "r") as zin:
        files = {info.filename: zin.read(info.filename) for info in zin.infolist()}
        infos = zin.infolist()
    root = ET.fromstring(files["word/document.xml"])
    return root, files, infos


def save_docx(path: Path, root: ET.Element, files: dict[str, bytes], infos: list[zipfile.ZipInfo], output: Path) -> None:
    files["word/document.xml"] = ET.tostring(root, encoding="utf-8", xml_declaration=True)
    tmp = output.with_suffix(output.suffix + ".tmp")
    with zipfile.ZipFile(tmp, "w", compression=zipfile.ZIP_DEFLATED) as zout:
        for info in infos:
            zi = zipfile.ZipInfo(info.filename, date_time=info.date_time)
            zi.compress_type = zipfile.ZIP_DEFLATED
            zi.external_attr = info.external_attr
            zi.comment = info.comment
            zout.writestr(zi, files[info.filename])
    shutil.move(tmp, output)


def paragraphs_from_root(root: ET.Element) -> list[tuple[ET.Element, str]]:
    out = []
    for p in root.findall(".//" + W + "p"):
        text = "".join(t.text or "" for t in p.findall(".//" + W + "t"))
        out.append((p, text))
    return out


def read_text(path: Path) -> list[str]:
    if path.suffix.lower() == ".docx" or zipfile.is_zipfile(path):
        root, _, _ = load_docx(path)
        return [text for _, text in paragraphs_from_root(root)]
    return path.read_text(encoding="utf-8").splitlines()


def section_bounds(paras: list[str], start_heading: str, end_headings: list[str]) -> tuple[int, int] | None:
    start = None
    for i, text in enumerate(paras):
        if text.strip() == start_heading:
            start = i
            break
    if start is None:
        return None
    end = len(paras)
    for j in range(start + 1, len(paras)):
        if paras[j].strip() in end_headings:
            end = j
            break
    return start, end


def parse_mapping(args: argparse.Namespace, paras: list[str]) -> dict[str, str]:
    mapping: dict[str, str] = {}
    if getattr(args, "mapping_json", None):
        mapping.update(json.loads(Path(args.mapping_json).read_text(encoding="utf-8")))
    if getattr(args, "mapping", None):
        for pair in args.mapping.split(","):
            if not pair.strip():
                continue
            if "=" not in pair:
                raise SystemExit(f"Bad mapping pair: {pair!r}; expected term=number")
            term, num = pair.split("=", 1)
            mapping[term.strip()] = num.strip()
    if mapping:
        return mapping

    joined = "\n".join(paras)
    marker = re.search(r"主要附图标记说明[:：]?(.*?)(?:具体实施方式|实施例|说明书附图|$)", joined, re.S)
    if marker:
        block = marker.group(1)
        for term, num in re.findall(r"([\u4e00-\u9fffA-Za-z][\u4e00-\u9fffA-Za-z0-9]{0,20})[（(]?(\d{2,4})[）)]?", block):
            if len(term) >= 2:
                mapping[term] = num
    return mapping


def target_indices(paras: list[str], scope: str) -> set[int]:
    indices: set[int] = set()
    if scope in ("claims", "both"):
        bounds = section_bounds(paras, "权利要求书", ["说明书"])
        if bounds:
            indices.update(range(bounds[0] + 1, bounds[1]))
    if scope in ("embodiments", "both"):
        start = None
        for heading in ("具体实施方式", "实施例"):
            b = section_bounds(paras, heading, ["说明书附图", "权利要求书"])
            if b:
                start = b
                break
        if start:
            indices.update(range(start[0] + 1, start[1]))
    return indices


def add_refs_to_text(text: str, mapping: dict[str, str], claim_style: bool) -> str:
    items = sorted(mapping.items(), key=lambda kv: len(kv[0]), reverse=True)
    for term, num in items:
        # Protect already-numbered forms.
        token = f"§§{term}{num}§§"
        text = text.replace(f"{term}（{num}）", token)
        text = text.replace(f"{term}({num})", token)
        text = re.sub(rf"{re.escape(term)}{re.escape(num)}(?!\d)", token, text)
        repl = f"{term}（{num}）" if claim_style else f"{term}{num}"
        text = text.replace(term, repl)
        text = text.replace(token, repl)
    return text


def remove_refs_from_text(text: str, mapping: dict[str, str]) -> str:
    items = sorted(mapping.items(), key=lambda kv: len(kv[0]), reverse=True)
    for term, num in items:
        text = text.replace(f"{term}（{num}）", term)
        text = text.replace(f"{term}({num})", term)
        text = re.sub(rf"{re.escape(term)}{re.escape(num)}(?!\d)", term, text)
    return text


def rewrite_docx_text(path: Path, output: Path, scope: str, mapping: dict[str, str], mode: str) -> int:
    root, files, infos = load_docx(path)
    paras = paragraphs_from_root(root)
    texts = [text for _, text in paras]
    targets = target_indices(texts, scope)
    changed = 0
    for i, (p, text) in enumerate(paras):
        if i not in targets or not text.strip():
            continue
        if mode == "add":
            claim_style = section_bounds(texts, "权利要求书", ["说明书"]) and i in target_indices(texts, "claims")
            new_text = add_refs_to_text(text, mapping, bool(claim_style))
        else:
            new_text = remove_refs_from_text(text, mapping)
        if new_text != text:
            nodes = p.findall(".//" + W + "t")
            if nodes:
                nodes[0].text = new_text
                if new_text.startswith(" ") or new_text.endswith(" "):
                    nodes[0].set("{http://www.w3.org/XML/1998/namespace}space", "preserve")
                for node in nodes[1:]:
                    node.text = ""
            changed += 1
    save_docx(path, root, files, infos, output)
    return changed


def extract_claims(paras: list[str]) -> dict[int, str]:
    bounds = section_bounds(paras, "权利要求书", ["说明书"])
    if not bounds:
        return {}
    claims: dict[int, str] = {}
    current = None
    parts: list[str] = []
    for text in paras[bounds[0] + 1 : bounds[1]]:
        m = re.match(r"\s*(\d+)\.\s*(.*)", text)
        if m:
            if current is not None:
                claims[current] = "".join(parts)
            current = int(m.group(1))
            parts = [m.group(2)]
        elif current is not None:
            parts.append(text)
    if current is not None:
        claims[current] = "".join(parts)
    return claims


def parse_refs(ref_text: str) -> list[int]:
    nums: list[int] = []
    for part in re.split(r"[、,，和及]", ref_text):
        part = part.strip()
        m = re.match(r"(\d+)\s*[-至]\s*(\d+)", part)
        if m:
            a, b = int(m.group(1)), int(m.group(2))
            nums.extend(range(min(a, b), max(a, b) + 1))
        elif part.isdigit():
            nums.append(int(part))
    return nums


def check_document(path: Path, mapping: dict[str, str]) -> dict[str, list[dict[str, str]]]:
    paras = read_text(path)
    text = "\n".join(paras)
    issues: dict[str, list[dict[str, str]]] = {"confirmed": [], "suspected": []}

    for i, p in enumerate(paras, 1):
        if re.search(r"[，。；、：？！]{2,}", p):
            issues["confirmed"].append({"location": f"段落{i}", "issue": "存在连续重复标点", "text": p})
        if re.search(r"(的的|所述所述|该该|和和|与与|在在)", p):
            issues["suspected"].append({"location": f"段落{i}", "issue": "疑似重复字词", "text": p})

    claims = extract_claims(paras)
    for n, claim in claims.items():
        refs_match = re.search(r"权利要求([\d、,，至\\-和及]+)", claim)
        if n > 1 and not refs_match:
            issues["confirmed"].append({"location": f"权利要求{n}", "issue": "从属权利要求未发现引用基础", "text": claim[:120]})
            continue
        refs = parse_refs(refs_match.group(1)) if refs_match else []
        for r in refs:
            if r >= n:
                issues["confirmed"].append({"location": f"权利要求{n}", "issue": f"引用了非在前权利要求{r}", "text": claim[:120]})
        if mapping and refs:
            basis = "".join(claims.get(r, "") for r in refs if r < n)
            # Include one level of ancestor basis to reduce false positives.
            for r in list(refs):
                m = re.search(r"权利要求([\d、,，至\\-和及]+)", claims.get(r, ""))
                if m:
                    basis += "".join(claims.get(rr, "") for rr in parse_refs(m.group(1)) if rr < r)
            for term in mapping:
                needle = f"所述{term}"
                for hit in re.finditer(re.escape(needle), claim):
                    earlier_same_claim = claim[: hit.start()]
                    if term not in basis and term not in earlier_same_claim:
                        issues["confirmed"].append({"location": f"权利要求{n}", "issue": f"“所述{term}”在引用基础或本权项前文中未找到前序基础", "text": claim[:160]})
                        break

    drawing_bounds = section_bounds(paras, "附图说明", ["主要附图标记说明", "具体实施方式", "说明书"])
    if drawing_bounds:
        drawing_text = "\n".join(paras[drawing_bounds[0] : drawing_bounds[1]])
        full_figs = set(re.findall(r"图\s*(\d+)", text))
        described = set(re.findall(r"图\s*(\d+)", drawing_text))
        missing = sorted(full_figs - described, key=int)
        if missing:
            issues["suspected"].append({"location": "附图说明", "issue": "部分图号在全文出现但未在附图说明中描述", "text": "、".join("图" + x for x in missing)})

    if mapping:
        for term, num in mapping.items():
            if term not in text and num not in text:
                issues["suspected"].append({"location": "附图标记", "issue": "附图标记项未在文本中出现", "text": f"{term}={num}"})
    return issues


def main() -> None:
    parser = argparse.ArgumentParser()
    sub = parser.add_subparsers(dest="cmd", required=True)
    for name in ("extract", "check", "add-refs", "remove-refs"):
        sp = sub.add_parser(name)
        sp.add_argument("input")
        sp.add_argument("--mapping")
        sp.add_argument("--mapping-json")
        sp.add_argument("--json", action="store_true", help="Emit machine-readable JSON when applicable")
        if name == "extract":
            sp.add_argument("--output", help="Optional text output path for extracted paragraphs")
        if name in ("add-refs", "remove-refs"):
            sp.add_argument("--output", required=True)
            sp.add_argument("--scope", choices=["claims", "embodiments", "both"], default="both")
    args = parser.parse_args()
    path = Path(args.input)
    paras = read_text(path)
    mapping = parse_mapping(args, paras)

    if args.cmd == "extract":
        text = "\n".join(paras)
        output_path = None
        if args.output:
            output_path = Path(args.output).expanduser().resolve()
            output_path.parent.mkdir(parents=True, exist_ok=True)
            output_path.write_text(text, encoding="utf-8")
        if args.json:
            print(
                json.dumps(
                    {
                        "input": str(path.expanduser().resolve()),
                        "output": str(output_path) if output_path else None,
                        "paragraphs": len(paras),
                        "characters": len(text),
                        "preview": text[:300],
                    },
                    ensure_ascii=False,
                    indent=2,
                )
            )
        else:
            print(text)
    elif args.cmd == "check":
        print(json.dumps(check_document(path, mapping), ensure_ascii=False, indent=2))
    else:
        if not mapping:
            raise SystemExit("A mapping is required for add/remove operations.")
        output = Path(args.output)
        if output.resolve() == path.resolve():
            backup = path.with_suffix(path.suffix + ".bak")
            if not backup.exists():
                shutil.copy2(path, backup)
        changed = rewrite_docx_text(path, output, args.scope, mapping, "add" if args.cmd == "add-refs" else "remove")
        print(json.dumps({"changed_paragraphs": changed, "output": str(output)}, ensure_ascii=False))


if __name__ == "__main__":
    main()
