import importlib.util
import json
import shutil
import sys
import unittest
from pathlib import Path

REPO_ROOT = Path.cwd()
ROOT = Path(__file__).resolve().parents[1]
INTAKE_ROOT = ROOT.parent / "wan2.7_tech_narrative_engine_intake_skill"
STRATEGY_ROOT = ROOT.parent / "wan2.7_tech_narrative_engine_strategy_skill"
ARTIFACT_ROOT = REPO_ROOT / "artifacts" / "test_wan27_draft_skill"
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from runtime.runner import DraftSkillConfig, DraftSkillRunner


def _load_module(name: str, file_path: Path):
    spec = importlib.util.spec_from_file_location(name, file_path)
    assert spec and spec.loader
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


intake_module = _load_module("wan27_intake_runner", INTAKE_ROOT / "runtime" / "runner.py")
strategy_module = _load_module("wan27_strategy_runner", STRATEGY_ROOT / "runtime" / "runner.py")
IntakeSkillConfig = intake_module.IntakeSkillConfig
IntakeSkillRunner = intake_module.IntakeSkillRunner
StrategySkillConfig = strategy_module.StrategySkillConfig
StrategySkillRunner = strategy_module.StrategySkillRunner


class DraftSkillRunnerTest(unittest.TestCase):
    def tearDown(self) -> None:
        if ARTIFACT_ROOT.exists():
            shutil.rmtree(ARTIFACT_ROOT)

    def test_run_blocks_when_any_page_is_not_user_confirmed(self) -> None:
        task_dir = self._prepare_task_dir(self._testMethodName)
        runner = DraftSkillRunner(DraftSkillConfig())

        with self.assertRaisesRegex(ValueError, "未完成用户核对"):
            runner.run(
                task_dir,
                answers={
                    "本轮更重视哪类草稿": "结构与页面契约",
                    "需要强化的关键语": "闭环、编排、闸门",
                    "必须避免的文风或表达": "空泛激情文案",
                    "是否有必须保留的句子或结尾": "成为 AI 时代的参与者",
                },
            )

    def test_run_outputs_visual_specs_after_all_pages_are_confirmed(self) -> None:
        task_dir = self._prepare_task_dir(self._testMethodName)
        status_path = task_dir / "review" / "page_review_status.json"
        statuses = json.loads(status_path.read_text(encoding="utf-8"))
        for item in statuses:
            item["status"] = "approved"
            item["approved"] = True
            item["approved_by"] = "user"
            item["approved_at"] = "2026-04-12T10:00:00+08:00"
            item["notes"] = "已核对"
        status_path.write_text(json.dumps(statuses, ensure_ascii=False, indent=2), encoding="utf-8")

        runner = DraftSkillRunner(DraftSkillConfig())
        result = runner.run(
            task_dir,
            answers={
                "本轮更重视哪类草稿": "结构与页面契约",
                "需要强化的关键语": "闭环、编排、闸门",
                "必须避免的文风或表达": "空泛激情文案",
                "是否有必须保留的句子或结尾": "成为 AI 时代的参与者",
            },
        )

        self.assertEqual("completed", result["status"])
        visual_specs = (task_dir / "output" / "drafts" / "page_visual_specs.md").read_text(encoding="utf-8")
        self.assertIn("confirmation_status: approved", visual_specs)
        self.assertIn("confirmed_by: user", visual_specs)
        draft_gate = json.loads((task_dir / "review" / "draft_gate.json").read_text(encoding="utf-8"))
        self.assertEqual("ready_for_review", draft_gate["status"])

    def _prepare_task_dir(self, test_name: str) -> Path:
        task_dir = ARTIFACT_ROOT / test_name
        intake = IntakeSkillRunner(IntakeSkillConfig())
        intake.init_task_dir(task_dir)
        intake.run(
            task_dir,
            answers={
                "比赛任务目标": "生成比赛介绍视频",
                "目标评委或观众": "比赛评委",
                "必须出现的对象": "Wan2.7、CoPaw、AgentScope",
                "必须避免的风险": "空泛口号",
                "结尾收束要求": "成为 AI 时代的参与者",
            },
        )
        strategy = StrategySkillRunner(StrategySkillConfig())
        strategy.run(
            task_dir,
            answers={
                "本轮最重要的评审重点": "链路可执行且逐页可核对",
                "本轮主证据页想强调什么": "CoPaw 是编排中枢",
                "本轮必须避免的表达偏差": "把未确认概念画成既定事实",
                "是否有额外页面或扩展要求": "否",
            },
        )
        strategy_gate = json.loads((task_dir / "review" / "strategy_gate.json").read_text(encoding="utf-8"))
        strategy_gate["approved"] = True
        strategy_gate["status"] = "approved"
        (task_dir / "review" / "strategy_gate.json").write_text(
            json.dumps(strategy_gate, ensure_ascii=False, indent=2),
            encoding="utf-8",
        )
        return task_dir


if __name__ == "__main__":
    unittest.main()
