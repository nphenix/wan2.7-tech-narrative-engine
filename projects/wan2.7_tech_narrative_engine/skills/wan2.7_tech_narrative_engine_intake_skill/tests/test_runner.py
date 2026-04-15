import json
import shutil
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REPO_ROOT = Path.cwd()
ARTIFACT_ROOT = REPO_ROOT / "artifacts" / "test_wan27_intake_skill"
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from runtime.runner import IntakeSkillConfig, IntakeSkillRunner


class IntakeSkillRunnerTest(unittest.TestCase):
    def tearDown(self) -> None:
        if ARTIFACT_ROOT.exists():
            shutil.rmtree(ARTIFACT_ROOT)

    def test_init_task_dir_creates_research_snapshot_and_page_review_status(self) -> None:
        task_dir = ARTIFACT_ROOT / self._testMethodName
        runner = IntakeSkillRunner(IntakeSkillConfig())

        result = runner.init_task_dir(task_dir)

        self.assertEqual("initialized", result["status"])
        self.assertTrue((task_dir / "input" / "research_context.md").exists())
        self.assertTrue((task_dir / "meta" / "domain_terms.snapshot.json").exists())
        self.assertTrue((task_dir / "review" / "page_review_status.json").exists())

        domain_terms = json.loads((task_dir / "meta" / "domain_terms.snapshot.json").read_text(encoding="utf-8"))
        self.assertEqual(["repo", "web", "user"], domain_terms["research_order"])
        self.assertGreaterEqual(len(domain_terms["terms"]), 3)

        page_review_status = json.loads((task_dir / "review" / "page_review_status.json").read_text(encoding="utf-8"))
        self.assertEqual(11, len(page_review_status))
        self.assertTrue(all(item["status"] == "awaiting_user_confirmation" for item in page_review_status))
        self.assertTrue(all(item["requires_user_confirmation"] for item in page_review_status))

    def test_run_keeps_page_review_status_in_strategy_gate_artifacts(self) -> None:
        task_dir = ARTIFACT_ROOT / self._testMethodName
        runner = IntakeSkillRunner(IntakeSkillConfig())
        runner.init_task_dir(task_dir)

        result = runner.run(
            task_dir,
            answers={
                "比赛任务目标": "生成 11 页比赛讲解图并衔接最终介绍视频",
                "目标评委或观众": "比赛评委与技术观众",
                "必须出现的对象": "Wan2.7、CoPaw、AgentScope",
                "必须避免的风险": "空泛口号、概念误读、结构失真",
                "结尾收束要求": "收束到成为 AI 时代的参与者",
            },
        )

        self.assertEqual("completed", result["status"])
        strategy_gate = json.loads((task_dir / "review" / "strategy_gate.json").read_text(encoding="utf-8"))
        self.assertIn("review/page_review_status.json", strategy_gate["artifacts"])
        self.assertIn("input/research_context.md", strategy_gate["artifacts"])


if __name__ == "__main__":
    unittest.main()
