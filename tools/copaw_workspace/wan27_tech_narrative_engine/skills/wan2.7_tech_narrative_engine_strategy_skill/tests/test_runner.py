import importlib.util
import json
import shutil
import sys
import unittest
from pathlib import Path

REPO_ROOT = Path.cwd()
ROOT = Path(__file__).resolve().parents[1]
INTAKE_ROOT = ROOT.parent / "wan2.7_tech_narrative_engine_intake_skill"
ARTIFACT_ROOT = REPO_ROOT / "artifacts" / "test_wan27_strategy_skill"
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from runtime.runner import StrategySkillConfig, StrategySkillRunner

intake_spec = importlib.util.spec_from_file_location("wan27_intake_runner", INTAKE_ROOT / "runtime" / "runner.py")
assert intake_spec and intake_spec.loader
intake_module = importlib.util.module_from_spec(intake_spec)
sys.modules[intake_spec.name] = intake_module
intake_spec.loader.exec_module(intake_module)
IntakeSkillConfig = intake_module.IntakeSkillConfig
IntakeSkillRunner = intake_module.IntakeSkillRunner


class StrategySkillRunnerTest(unittest.TestCase):
    def tearDown(self) -> None:
        if ARTIFACT_ROOT.exists():
            shutil.rmtree(ARTIFACT_ROOT)

    def test_run_outputs_page_contracts_with_confirmation_status_and_open_gaps(self) -> None:
        task_dir = ARTIFACT_ROOT / self._testMethodName
        intake = IntakeSkillRunner(IntakeSkillConfig())
        intake.init_task_dir(task_dir)
        intake.run(
            task_dir,
            answers={
                "比赛任务目标": "生成比赛视频和 11 页讲解图",
                "目标评委或观众": "比赛评委",
                "必须出现的对象": "Wan2.7、CoPaw、AgentScope",
                "必须避免的风险": "空泛口号",
                "结尾收束要求": "成为 AI 时代的参与者",
            },
        )

        runner = StrategySkillRunner(StrategySkillConfig())
        result = runner.run(
            task_dir,
            answers={
                "本轮最重要的评审重点": "先确认每页图是否说对",
                "本轮主证据页想强调什么": "CoPaw、Wan2.7、AgentScope 的关系必须可核对",
                "本轮必须避免的表达偏差": "把未确认概念直接画死",
                "是否有额外页面或扩展要求": "否",
            },
        )

        self.assertEqual("completed", result["status"])
        page_contracts = (task_dir / "output" / "review" / "page_contracts.md").read_text(encoding="utf-8")
        self.assertIn("confirmation_status: awaiting_user_confirmation", page_contracts)
        self.assertIn("open_knowledge_gaps: 用户尚未完成本页核对", page_contracts)

        knowledge_gaps = (task_dir / "output" / "review" / "knowledge_gaps.md").read_text(encoding="utf-8")
        self.assertIn("当前仍有逐页核对缺口", knowledge_gaps)
        self.assertIn("page_3_copaw_agentscope_architecture", knowledge_gaps)

        page_review_status = json.loads((task_dir / "review" / "page_review_status.json").read_text(encoding="utf-8"))
        self.assertEqual("awaiting_user_confirmation", page_review_status[0]["status"])
        self.assertFalse(page_review_status[0]["approved"])


if __name__ == "__main__":
    unittest.main()
