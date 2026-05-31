import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


RUNTIME_ROOT = Path(__file__).resolve().parents[1]
RUNNER = RUNTIME_ROOT / "scripts" / "patent_tool_runner.py"
SPECIALIST_REGISTRY = RUNTIME_ROOT / "scripts" / "specialist_registry.json"
SKILLS_ROOT = Path("/Users/chrynos/.codex/skills")
WORKFLOW = Path("/Users/chrynos/.codex/skills/patent-entry-drafting/scripts/patent_workflow.py")


def run_python(script: Path, *args: str) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [sys.executable, str(script), *args],
        check=True,
        capture_output=True,
        text=True,
    )


class ToolRunnerTest(unittest.TestCase):
    def test_specialist_registry_points_to_existing_skills(self) -> None:
        registry = json.loads(SPECIALIST_REGISTRY.read_text(encoding="utf-8"))
        self.assertEqual(registry["schema_version"], "patent-specialist-registry/v1")
        self.assertEqual(registry["public_entries"]["top"], "patent-cn")

        public_entries = set(registry["public_entries"].values())
        self.assertEqual(
            public_entries,
            {"patent-cn", "patent-cn-draft", "patent-cn-review", "patent-cn-response", "patent-cn-doctor"},
        )

        specialist_skills = {item["skill"] for item in registry["specialists"].values()}
        self.assertIn("patent-stage-prior-art-search", specialist_skills)
        self.assertIn("patent-qc-application-consistency", specialist_skills)
        self.assertIn("patent-support-docx-math", specialist_skills)

        compatibility_entries = registry["compatibility_entries"]
        self.assertEqual(compatibility_entries["patent-entry-drafting"], "patent-cn-draft")
        self.assertEqual(compatibility_entries["patent-entry-oa-response"], "patent-cn-response")
        self.assertEqual(compatibility_entries["patent-entry-invalidity"], "patent-cn-response")

        for skill_name in public_entries | specialist_skills:
            with self.subTest(skill=skill_name):
                self.assertTrue((SKILLS_ROOT / skill_name / "SKILL.md").exists())
                agent_yaml = SKILLS_ROOT / skill_name / "agents" / "openai.yaml"
                if skill_name in specialist_skills and agent_yaml.exists():
                    self.assertIn("allow_implicit_invocation: false", agent_yaml.read_text(encoding="utf-8"))

        for old_entry, new_entry in compatibility_entries.items():
            with self.subTest(compatibility_entry=old_entry):
                self.assertTrue((SKILLS_ROOT / old_entry / "SKILL.md").exists())
                self.assertIn(new_entry, public_entries)
                agent_yaml = SKILLS_ROOT / old_entry / "agents" / "openai.yaml"
                if agent_yaml.exists():
                    self.assertIn("allow_implicit_invocation: false", agent_yaml.read_text(encoding="utf-8"))

        for alias_name, target_name in registry["retired_aliases"].items():
            with self.subTest(retired_alias=alias_name):
                self.assertFalse((SKILLS_ROOT / alias_name).exists())
                self.assertTrue((SKILLS_ROOT / target_name / "SKILL.md").exists())

    def test_list_and_describe_registry(self) -> None:
        listed = json.loads(run_python(RUNNER, "list").stdout)
        tool_ids = {item["id"] for item in listed["tools"]}
        self.assertIn("qc.micro", tool_ids)
        self.assertIn("docx.inspect", tool_ids)
        self.assertIn("docx.style_invariance", tool_ids)
        self.assertIn("workflow.doctor", tool_ids)

        described = json.loads(run_python(RUNNER, "describe", "qc.micro").stdout)
        self.assertEqual(described["tool_id"], "qc.micro")
        self.assertIn("input", described["required"])

    def test_run_qc_micro_writes_result_and_logs_event(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            tmp_path = Path(tmp)
            case_dir = tmp_path / "case"
            run_python(WORKFLOW, "init", "--case-dir", str(case_dir), "--title", "工具运行测试", "--json")
            draft = tmp_path / "draft.md"
            draft.write_text(
                "摘要\n" + "技" * 301 + "\n权利要求书\n1. 一种装置。\n说明书\n技术领域\n测试。\n",
                encoding="utf-8",
            )
            result_output = case_dir / "记录" / "07_质检" / "工具运行" / "micro-qc-tool-run.json"
            result = run_python(
                RUNNER,
                "run",
                "qc.micro",
                "--case-dir",
                str(case_dir),
                "--input",
                str(draft),
                "--result-output",
                str(result_output),
            )
            payload = json.loads(result.stdout)
            self.assertTrue(payload["ok"])
            self.assertEqual(payload["tool_id"], "qc.micro")
            self.assertTrue(result_output.exists())
            self.assertEqual(json.loads(result_output.read_text(encoding="utf-8"))["tool_id"], "qc.micro")

            events = (case_dir / "00_case_events.jsonl").read_text(encoding="utf-8")
            self.assertIn('"script": "qc.micro"', events)


if __name__ == "__main__":
    unittest.main()
