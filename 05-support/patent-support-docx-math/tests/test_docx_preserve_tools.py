import json
import subprocess
import sys
import tempfile
import unittest
import zipfile
from pathlib import Path
from xml.etree import ElementTree as ET


SKILL_ROOT = Path(__file__).resolve().parents[1]
REPLACE_SCRIPT = SKILL_ROOT / "scripts" / "replace_docx_text_preserve_runs.py"
STYLE_SCRIPT = SKILL_ROOT / "scripts" / "docx_style_invariance.py"
W = "http://schemas.openxmlformats.org/wordprocessingml/2006/main"
NS = {"w": W}


def run_python(script: Path, *args: str) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [sys.executable, str(script), *args],
        check=True,
        capture_output=True,
        text=True,
    )


def minimal_docx(path: Path, text_a: str = "Hello", text_b: str = "World", *, page_break: bool = False) -> None:
    middle_run = '<w:r><w:br w:type="page"/></w:r>' if page_break else ""
    document = f'''<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<w:document xmlns:w="{W}">
  <w:body>
    <w:p>
      <w:pPr><w:pStyle w:val="Normal"/></w:pPr>
      <w:r><w:rPr><w:rFonts w:ascii="SimSun" w:eastAsia="宋体"/><w:sz w:val="24"/></w:rPr><w:t>{text_a}</w:t></w:r>
      {middle_run}
      <w:r><w:rPr><w:b/></w:rPr><w:t>{text_b}</w:t></w:r>
    </w:p>
    <w:sectPr/>
  </w:body>
</w:document>
'''
    with zipfile.ZipFile(path, "w", zipfile.ZIP_DEFLATED) as package:
        package.writestr("[Content_Types].xml", "<Types/>")
        package.writestr("_rels/.rels", "<Relationships/>")
        package.writestr("word/document.xml", document)
        package.writestr("word/styles.xml", f'<w:styles xmlns:w="{W}"/>')
        package.writestr("word/settings.xml", f'<w:settings xmlns:w="{W}"/>')
        package.writestr("word/fontTable.xml", f'<w:fonts xmlns:w="{W}"/>')
        package.writestr("word/numbering.xml", f'<w:numbering xmlns:w="{W}"/>')
        package.writestr(
            "word/theme/theme1.xml",
            '<a:theme xmlns:a="http://schemas.openxmlformats.org/drawingml/2006/main"/>',
        )


def paragraph_runs(path: Path) -> list[ET.Element]:
    with zipfile.ZipFile(path) as package:
        root = ET.fromstring(package.read("word/document.xml"))
    paragraph = root.find(".//w:p", NS)
    assert paragraph is not None
    return paragraph.findall("w:r", NS)


def page_break_count(path: Path) -> int:
    with zipfile.ZipFile(path) as package:
        root = ET.fromstring(package.read("word/document.xml"))
    return sum(1 for node in root.findall(".//w:br", NS) if node.attrib.get(f"{{{W}}}type") == "page")


class DocxPreserveToolsTest(unittest.TestCase):
    def test_replace_preserves_run_templates(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            tmp_path = Path(tmp)
            source = tmp_path / "source.docx"
            output = tmp_path / "output.docx"
            replacements = tmp_path / "replacements.json"
            minimal_docx(source)
            replacements.write_text(
                json.dumps({"paragraph_replacements": [{"old": "HelloWorld", "new": "GoodByeAll"}]}),
                encoding="utf-8",
            )

            result = run_python(
                REPLACE_SCRIPT,
                str(source),
                "--output",
                str(output),
                "--replacements-json",
                str(replacements),
                "--strict",
                "--json",
            )
            payload = json.loads(result.stdout)
            self.assertEqual(payload["modified"], 1)

            runs = paragraph_runs(output)
            self.assertEqual(len(runs), 2)
            self.assertTrue(all(run.find("w:rPr", NS) is not None for run in runs))
            text = "".join(node.text or "" for run in runs for node in run.findall(".//w:t", NS))
            self.assertEqual(text, "GoodByeAll")

    def test_replace_preserves_page_break_runs(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            tmp_path = Path(tmp)
            source = tmp_path / "source.docx"
            output = tmp_path / "output.docx"
            replacements = tmp_path / "replacements.json"
            minimal_docx(source, page_break=True)
            replacements.write_text(
                json.dumps({"paragraph_replacements": [{"old": "HelloWorld", "new": "GoodByeAll"}]}),
                encoding="utf-8",
            )

            run_python(
                REPLACE_SCRIPT,
                str(source),
                "--output",
                str(output),
                "--replacements-json",
                str(replacements),
                "--strict",
                "--json",
            )

            runs = paragraph_runs(output)
            self.assertEqual(len(runs), 3)
            self.assertEqual(page_break_count(output), 1)
            text = "".join(node.text or "" for run in runs for node in run.findall(".//w:t", NS))
            self.assertEqual(text, "GoodByeAll")

    def test_style_invariance_reports_key_parts_and_run_profile(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            tmp_path = Path(tmp)
            before = tmp_path / "before.docx"
            after = tmp_path / "after.docx"
            minimal_docx(before, page_break=True)
            minimal_docx(after, "Hello", "There", page_break=True)

            result = run_python(STYLE_SCRIPT, str(before), str(after), "--json")
            payload = json.loads(result.stdout)

            self.assertTrue(payload["ok"])
            self.assertTrue(payload["summary"]["key_parts_same"])
            self.assertTrue(payload["summary"]["core_structure_same"])
            self.assertTrue(payload["summary"]["page_breaks_same"])
            self.assertEqual(payload["summary"]["changed_paragraph_count"], 1)
            self.assertEqual(payload["profiles"]["before"]["page_break_count"], 1)
            self.assertEqual(payload["profiles"]["after"]["page_break_count"], 1)

    def test_style_invariance_flags_missing_page_break(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            tmp_path = Path(tmp)
            before = tmp_path / "before.docx"
            after = tmp_path / "after.docx"
            minimal_docx(before, page_break=True)
            minimal_docx(after)

            result = run_python(STYLE_SCRIPT, str(before), str(after), "--json")
            payload = json.loads(result.stdout)

            self.assertFalse(payload["ok"])
            self.assertFalse(payload["summary"]["page_breaks_same"])
            self.assertIn("page-break-count-different", {issue["code"] for issue in payload["issues"]})


if __name__ == "__main__":
    unittest.main()
