from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Any

import sys

PROJECT_ROOT = Path(__file__).resolve().parents[3]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from common.pipeline import (  # noqa: E402
    GATE_NAMES,
    build_default_page_review_status,
    build_gate,
    build_knowledge_sources_json,
    build_knowledge_sources_markdown,
    build_manifest,
    build_research_context_markdown,
    ensure_project_knowledge_files,
    ensure_task_structure,
    now_iso,
    project_root_from,
    read_json,
    update_manifest,
    write_json,
    write_markdown,
)
REQUIRED_FIELDS = [
    "比赛任务目标",
    "目标评委或观众",
    "必须出现的对象",
    "必须避免的风险",
    "结尾收束要求",
]


@dataclass
class IntakeSkillConfig:
    dry_run: bool = False


class IntakeSkillRunner:
    def __init__(self, config: IntakeSkillConfig) -> None:
        self.config = config

    def init_task_dir(self, task_dir: Path) -> dict[str, Any]:
        task_dir = Path(task_dir)
        ensure_task_structure(task_dir)
        repo_root = project_root_from(Path.cwd())
        knowledge_files = ensure_project_knowledge_files(repo_root)

        write_markdown(task_dir / "input" / "user_request.md", self._build_template())
        write_markdown(task_dir / "input" / "knowledge_sources.md", build_knowledge_sources_markdown(repo_root))
        write_markdown(task_dir / "input" / "research_context.md", build_research_context_markdown(repo_root))
        write_json(task_dir / "meta" / "knowledge_sources.json", build_knowledge_sources_json(repo_root))
        write_json(task_dir / "meta" / "domain_terms.snapshot.json", read_json(knowledge_files["domain_terms_json"]))
        write_json(task_dir / "review" / "page_review_status.json", build_default_page_review_status())
        write_json(task_dir / "meta" / "task_manifest.json", build_manifest())

        checks_by_gate = {
            "strategy_gate": [
                "仓库内研究上下文是否已写入任务目录",
                "页级核对状态是否已初始化",
                "目标评委与必须出现对象是否明确",
                "是否具备继续进入 strategy 的最低信息量",
            ],
            "draft_gate": [
                "page_contracts 是否完整",
                "knowledge_gaps 是否如实记录未确认页面",
                "逐页核对状态是否已全部关闭",
            ],
            "visual_blueprint_gate": [
                "page_visual_specs 是否完整",
                "蓝图是否保留关键对象和连线",
                "是否所有页面都已有用户确认记录",
            ],
            "visual_generation_gate": [
                "静态图是否保留关键标签",
                "asset_manifest 是否完整",
                "视频阶段所需页面图是否齐备",
            ],
            "final_gate": [
                "视频是否完整输出",
                "字幕和旁白是否与页面语义一致",
                "submission 和展示摘要是否完整",
            ],
        }
        for gate_name in GATE_NAMES:
            write_json(task_dir / "review" / f"{gate_name}.json", build_gate(checks_by_gate[gate_name]))

        return {
            "status": "initialized",
            "generated_at": now_iso("INTAKE_SKILL_NOW"),
            "outputs": {
                "user_request": "input/user_request.md",
                "knowledge_sources": "input/knowledge_sources.md",
                "research_context": "input/research_context.md",
                "task_manifest": "meta/task_manifest.json",
                "page_review_status": "review/page_review_status.json",
            },
        }

    def run(self, task_dir: Path, answers: dict[str, str] | None = None) -> dict[str, Any]:
        task_dir = Path(task_dir)
        self._validate_inputs(task_dir)

        if answers is not None:
            normalized = self._validate_answers(answers)
            write_markdown(task_dir / "input" / "user_request.md", self._build_request_markdown(normalized))

        request_text = (task_dir / "input" / "user_request.md").read_text(encoding="utf-8")
        request_summary = self._extract_request_summary(request_text)
        outputs = {
            "user_request": "input/user_request.md",
            "knowledge_sources": "input/knowledge_sources.md",
            "research_context": "input/research_context.md",
            "page_review_status": "review/page_review_status.json",
        }
        update_manifest(task_dir, "intake_ready", outputs=outputs, summary=request_summary)

        strategy_gate = read_json(task_dir / "review" / "strategy_gate.json")
        strategy_gate["status"] = "pending"
        strategy_gate["approved"] = False
        strategy_gate["artifacts"] = [
            "input/user_request.md",
            "input/knowledge_sources.md",
            "input/research_context.md",
            "meta/domain_terms.snapshot.json",
            "review/page_review_status.json",
            "meta/task_manifest.json",
        ]
        write_json(task_dir / "review" / "strategy_gate.json", strategy_gate)

        result = {
            "status": "completed",
            "generated_at": now_iso("INTAKE_SKILL_NOW"),
            "outputs": {
                **outputs,
                "task_manifest": "meta/task_manifest.json",
                "strategy_gate": "review/strategy_gate.json",
                "domain_terms_snapshot": "meta/domain_terms.snapshot.json",
            },
        }
        write_json(task_dir / "meta" / "intake_result.json", result)
        return result

    def _validate_inputs(self, task_dir: Path) -> None:
        for relative in (
            "input/user_request.md",
            "input/knowledge_sources.md",
            "input/research_context.md",
            "meta/domain_terms.snapshot.json",
            "review/page_review_status.json",
            "meta/task_manifest.json",
        ):
            if not (task_dir / relative).exists():
                raise FileNotFoundError(f"Missing input file: {relative}")

    def _validate_answers(self, answers: dict[str, str]) -> dict[str, str]:
        normalized: dict[str, str] = {}
        for field in REQUIRED_FIELDS:
            value = answers.get(field, "").strip()
            if not value:
                raise ValueError(f"Missing required answer: {field}")
            normalized[field] = value
        return normalized

    def _build_template(self) -> str:
        return "\n".join(
            [
                "# user_request",
                "",
                "- 比赛任务目标：",
                "- 目标评委或观众：",
                "- 必须出现的对象：",
                "- 必须避免的风险：",
                "- 结尾收束要求：",
                "",
            ]
        )

    def _build_request_markdown(self, answers: dict[str, str]) -> str:
        return "\n".join(
            [
                "# user_request",
                "",
                f"- 比赛任务目标：{answers['比赛任务目标']}",
                f"- 目标评委或观众：{answers['目标评委或观众']}",
                f"- 必须出现的对象：{answers['必须出现的对象']}",
                f"- 必须避免的风险：{answers['必须避免的风险']}",
                f"- 结尾收束要求：{answers['结尾收束要求']}",
                "",
            ]
        )

    def _extract_request_summary(self, request_text: str) -> str:
        for line in request_text.splitlines():
            cleaned = line.strip()
            if cleaned.startswith("- 比赛任务目标："):
                return cleaned.removeprefix("- ").strip()
        return "比赛任务目标待补充"
