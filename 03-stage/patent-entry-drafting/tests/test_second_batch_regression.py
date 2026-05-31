import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path
from zipfile import ZipFile


SKILL_ROOT = Path(__file__).resolve().parents[1]
SKILLS_ROOT = SKILL_ROOT.parent
WORKFLOW = SKILL_ROOT / "scripts" / "patent_workflow.py"
MICRO_QC = SKILL_ROOT / "scripts" / "patent_qc_micro.py"
DOCX_INSPECT = SKILLS_ROOT / "patent-support-docx-math" / "scripts" / "inspect_docx.py"
FLOWCHART = SKILLS_ROOT / "patent-drawing-generator" / "scripts" / "patent_flowchart.py"


def run_python(script: Path, *args: str) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [sys.executable, str(script), *args],
        check=True,
        capture_output=True,
        text=True,
    )


def make_minimal_docx(path: Path, paragraphs: list[str]) -> None:
    content_types = """<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types">
  <Default Extension="rels" ContentType="application/vnd.openxmlformats-package.relationships+xml"/>
  <Default Extension="xml" ContentType="application/xml"/>
  <Override PartName="/word/document.xml" ContentType="application/vnd.openxmlformats-officedocument.wordprocessingml.document.main+xml"/>
</Types>
"""
    rels = """<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">
  <Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/officeDocument" Target="word/document.xml"/>
</Relationships>
"""
    body = "".join(
        f"<w:p><w:r><w:t>{escape_xml(text)}</w:t></w:r></w:p>" for text in paragraphs
    )
    document = f"""<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<w:document xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main">
  <w:body>{body}<w:sectPr/></w:body>
</w:document>
"""
    with ZipFile(path, "w") as zf:
        zf.writestr("[Content_Types].xml", content_types)
        zf.writestr("_rels/.rels", rels)
        zf.writestr("word/document.xml", document)


def escape_xml(text: str) -> str:
    return (
        text.replace("&", "&amp;")
        .replace("<", "&lt;")
        .replace(">", "&gt;")
        .replace('"', "&quot;")
    )


class SecondBatchRegressionTest(unittest.TestCase):
    def test_workflow_execution_mode_round_trip(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            case_dir = Path(tmp) / "case"
            result = run_python(
                WORKFLOW,
                "init",
                "--case-dir",
                str(case_dir),
                "--title",
                "测试案件",
                "--source",
                "source.docx",
                "--mode",
                "autonomous",
                "--json",
            )
            payload = json.loads(result.stdout)
            self.assertEqual(payload["execution_mode"], "autonomous")

            manifest = json.loads((case_dir / "manifest.json").read_text(encoding="utf-8"))
            self.assertEqual(manifest["execution_mode"], "autonomous")
            self.assertEqual(manifest["layout"]["project_workspace_dir"], "专利工作区")
            self.assertEqual(manifest["layout"]["directory_policy"], "lazy-create-only-parents-for-written-files")
            self.assertIn("execution_mode: `autonomous`", (case_dir / "00_case_status.md").read_text(encoding="utf-8"))
            self.assertFalse((case_dir / "00_admin").exists())
            self.assertFalse((case_dir / "01_disclosure").exists())
            self.assertFalse(any(path.is_dir() for path in case_dir.iterdir()))

            result = run_python(
                WORKFLOW,
                "set-mode",
                "--case-dir",
                str(case_dir),
                "--mode",
                "guided",
                "--json",
            )
            payload = json.loads(result.stdout)
            self.assertEqual(payload["execution_mode"], "guided")

    def test_workflow_event_log_and_metrics(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            case_dir = Path(tmp) / "case"
            run_python(
                WORKFLOW,
                "init",
                "--case-dir",
                str(case_dir),
                "--title",
                "指标测试案件",
                "--json",
            )
            run_python(
                WORKFLOW,
                "stage-start",
                "--case-dir",
                str(case_dir),
                "--stage",
                "01_disclosure",
                "--json",
            )
            run_python(
                WORKFLOW,
                "log-event",
                "--case-dir",
                str(case_dir),
                "--event",
                "script-run",
                "--stage",
                "01_disclosure",
                "--script",
                "extract_disclosure_text.py",
                "--json",
            )
            run_python(
                WORKFLOW,
                "log-event",
                "--case-dir",
                str(case_dir),
                "--event",
                "dependency-call",
                "--dependency",
                "LibreOffice",
                "--json",
            )
            run_python(
                WORKFLOW,
                "log-event",
                "--case-dir",
                str(case_dir),
                "--event",
                "manual-interruption",
                "--severity",
                "warning",
                "--message",
                "stopped for confirmation",
                "--json",
            )
            run_python(
                WORKFLOW,
                "stage-end",
                "--case-dir",
                str(case_dir),
                "--stage",
                "01_disclosure",
                "--status",
                "completed",
                "--json",
            )
            result = run_python(
                WORKFLOW,
                "metrics",
                "--case-dir",
                str(case_dir),
                "--output",
                "记录/07_质检/报告/workflow-metrics.json",
                "--json",
            )
            metrics = json.loads(result.stdout)
            self.assertEqual(metrics["script_runs_count"], 1)
            self.assertEqual(metrics["dependency_calls_count"], 1)
            self.assertEqual(metrics["manual_interruptions_count"], 1)
            self.assertTrue((case_dir / "00_case_events.jsonl").exists())
            self.assertTrue((case_dir / "记录/07_质检/报告/workflow-metrics.json").exists())

            run_python(WORKFLOW, "validate", "--case-dir", str(case_dir), "--json")
            report_text = (case_dir / "输出" / "定稿" / "验证报告.md").read_text(encoding="utf-8")
            self.assertIn("## Workflow Metrics", report_text)
            self.assertIn("script_runs_count: 1", report_text)

    def test_stage_report_contract_is_registered_and_summarized(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            case_dir = Path(tmp) / "case"
            run_python(
                WORKFLOW,
                "init",
                "--case-dir",
                str(case_dir),
                "--title",
                "阶段报告测试案件",
                "--json",
            )
            memo = case_dir / "输出" / "过程" / "01_交底分析" / "交底分析.md"
            memo.parent.mkdir(parents=True, exist_ok=True)
            memo.write_text("# Disclosure Analysis\n\n人工可读 memo 保留。\n", encoding="utf-8")

            result = run_python(
                WORKFLOW,
                "stage-report",
                "--case-dir",
                str(case_dir),
                "--stage",
                "01_disclosure",
                "--name",
                "disclosure-analysis",
                "--status",
                "completed",
                "--input",
                "source.docx",
                "--artifact",
                "输出/过程/01_交底分析/交底分析.md",
                "--confirmed",
                "确认技术问题与核心方案",
                "--suspected",
                "效果数据仍需发明人确认",
                "--assumption",
                "以当前交底文本为基线",
                "--next-stage",
                "checkpoint-a-search",
                "--memo-path",
                "输出/过程/01_交底分析/交底分析.md",
                "--json",
            )
            payload = json.loads(result.stdout)
            report_path = Path(payload["report"])
            report = json.loads(report_path.read_text(encoding="utf-8"))
            self.assertEqual(report["schema_version"], "patent-stage-report/v1")
            self.assertEqual(report["runtime_stage"], "01_disclosure")

            manifest = json.loads((case_dir / "manifest.json").read_text(encoding="utf-8"))
            artifacts = manifest["stages"]["01_disclosure"]["artifacts"]
            self.assertTrue(any(item["kind"] == "stage-report" for item in artifacts))

            run_python(WORKFLOW, "validate", "--case-dir", str(case_dir), "--json")
            validation = (case_dir / "输出" / "定稿" / "验证报告.md").read_text(encoding="utf-8")
            self.assertIn("## Stage Reports", validation)
            self.assertIn("记录/01_交底分析/报告/disclosure-analysis-stage-report.json", validation)
            self.assertIn("checkpoint-a-search", validation)

    def test_micro_qc_detects_mechanical_issues(self) -> None:
        long_abstract = "技" * 301
        draft = f"""摘要
{long_abstract}
权利要求书
1. 一种装置，包括壳体（1）。
2. 根据所述装置，其特征在于，还包括待补充模块。
3. 根据权利要求3所述的装置，其特征在于，所述壳体设有孔。
说明书
技术领域
本发明涉及测试领域。
发明内容
本发明解决测试问题。
具体实施方式
如图1所示，壳体（1）形成容纳空间。
附图说明
图2为另一结构示意图。
主要附图标记说明
1：壳体
"""
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "draft.md"
            path.write_text(draft, encoding="utf-8")
            result = run_python(MICRO_QC, "check", str(path), "--json")
            report = json.loads(result.stdout)
            codes = {item["code"] for item in report["checks"]}

        self.assertIn("abstract-too-long", codes)
        self.assertIn("claim-forward-or-self-citation", codes)
        self.assertIn("dependent-claim-without-citation", codes)
        self.assertIn("figure-reference-not-described", codes)
        self.assertIn("missing-spec-section", codes)
        self.assertIn("placeholder-text", codes)

    def test_docx_inspector_still_extracts_sections(self) -> None:
        if not DOCX_INSPECT.exists():
            self.skipTest("DOCX inspector script is not installed")
        if subprocess.run([sys.executable, "-c", "import lxml"], capture_output=True).returncode:
            self.skipTest("lxml is not installed")

        with tempfile.TemporaryDirectory() as tmp:
            docx = Path(tmp) / "draft.docx"
            make_minimal_docx(
                docx,
                ["摘要", "本摘要用于测试。", "权利要求书", "1. 一种测试方法。", "说明书", "技术领域"],
            )
            result = run_python(DOCX_INSPECT, str(docx), "--json")
            report = json.loads(result.stdout)
            labels = {item["label"] for item in report["detected_sections"]}

        self.assertIn("abstract", labels)
        self.assertIn("claims", labels)
        self.assertIn("specification", labels)

    def test_flowchart_renderer_outputs_svg(self) -> None:
        if not FLOWCHART.exists():
            self.skipTest("flowchart renderer is not installed")
        if subprocess.run([sys.executable, "-c", "import PIL"], capture_output=True).returncode:
            self.skipTest("Pillow is not installed")

        with tempfile.TemporaryDirectory() as tmp:
            steps = Path(tmp) / "steps.txt"
            out = Path(tmp) / "flow.svg"
            steps.write_text("S1、采集数据\nS2、生成控制指令\n", encoding="utf-8")
            run_python(FLOWCHART, "--steps-file", str(steps), "--out", str(out), "--quiet")

            self.assertTrue(out.exists())
            self.assertIn("<svg", out.read_text(encoding="utf-8"))


if __name__ == "__main__":
    unittest.main()
