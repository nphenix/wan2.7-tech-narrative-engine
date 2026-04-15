from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Any

import sys

PROJECT_ROOT = Path(__file__).resolve().parents[3]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from common.pipeline import (  # noqa: E402
    PAGE_DEFINITIONS,
    build_knowledge_gaps_markdown,
    build_page_contracts_markdown,
    build_page_roles_markdown,
    format_request_markdown,
    normalize_page_review_status,
    now_iso,
    parse_request_markdown,
    read_json,
    update_manifest,
    write_json,
    write_markdown,
)

STRATEGY_FIELDS = [
    "本轮最重要的评审重点",
    "本轮主证据页想强调什么",
    "本轮必须避免的表达偏差",
    "是否有额外页面或扩展要求",
]

USER_REQUEST_FIELDS = [
    "比赛任务目标",
    "目标评委或观众",
    "必须出现的对象",
    "必须避免的风险",
    "结尾收束要求",
]


@dataclass
class StrategySkillConfig:
    dry_run: bool = False


class StrategySkillRunner:
    def __init__(self, config: StrategySkillConfig) -> None:
        self.config = config

    def run(self, task_dir: Path, answers: dict[str, str] | None = None) -> dict[str, Any]:
        task_dir = Path(task_dir)
        self._validate_inputs(task_dir)

        strategy_request = self._prepare_strategy_request(task_dir, answers)
        request_data = parse_request_markdown(
            (task_dir / "input" / "user_request.md").read_text(encoding="utf-8"),
            USER_REQUEST_FIELDS,
        )
        page_review_status = normalize_page_review_status(read_json(task_dir / "review" / "page_review_status.json"))
        write_json(task_dir / "review" / "page_review_status.json", page_review_status)

        write_markdown(task_dir / "input" / "strategy_brief.md", self._build_strategy_brief(request_data, strategy_request))
        write_markdown(task_dir / "input" / "technical_brief.md", self._build_technical_brief(request_data, strategy_request))
        write_markdown(task_dir / "input" / "narrative_brief.md", self._build_narrative_brief(request_data, strategy_request))
        write_markdown(task_dir / "output" / "review" / "page_roles.md", build_page_roles_markdown())
        write_markdown(task_dir / "output" / "review" / "page_contracts.md", build_page_contracts_markdown(page_review_status))
        write_markdown(task_dir / "output" / "review" / "knowledge_gaps.md", build_knowledge_gaps_markdown(page_review_status))
        write_json(task_dir / "meta" / "page_contracts.json", self._page_contracts_json(page_review_status))
        write_json(task_dir / "meta" / "knowledge_gaps.json", self._knowledge_gaps_json(page_review_status))

        gate = read_json(task_dir / "review" / "strategy_gate.json")
        gate["status"] = "ready_for_review"
        gate["approved"] = False
        gate["artifacts"] = [
            "input/strategy_request.md",
            "input/strategy_brief.md",
            "input/technical_brief.md",
            "input/narrative_brief.md",
            "output/review/page_roles.md",
            "output/review/page_contracts.md",
            "output/review/knowledge_gaps.md",
            "review/page_review_status.json",
        ]
        write_json(task_dir / "review" / "strategy_gate.json", gate)

        outputs = {
            "strategy_request": "input/strategy_request.md",
            "strategy_brief": "input/strategy_brief.md",
            "technical_brief": "input/technical_brief.md",
            "narrative_brief": "input/narrative_brief.md",
            "page_roles": "output/review/page_roles.md",
            "page_contracts": "output/review/page_contracts.md",
            "knowledge_gaps": "output/review/knowledge_gaps.md",
            "page_review_status": "review/page_review_status.json",
        }
        update_manifest(task_dir, "strategy_ready", outputs=outputs)

        result = {"status": "completed", "generated_at": now_iso("STRATEGY_SKILL_NOW"), "outputs": outputs}
        write_json(task_dir / "meta" / "strategy_result.json", result)
        return result

    def _validate_inputs(self, task_dir: Path) -> None:
        for relative in (
            "input/user_request.md",
            "input/knowledge_sources.md",
            "input/research_context.md",
            "meta/domain_terms.snapshot.json",
            "review/page_review_status.json",
            "meta/task_manifest.json",
            "review/strategy_gate.json",
        ):
            if not (task_dir / relative).exists():
                raise FileNotFoundError(f"Missing input file: {relative}")

    def _prepare_strategy_request(self, task_dir: Path, answers: dict[str, str] | None) -> dict[str, str]:
        request_path = task_dir / "input" / "strategy_request.md"
        if answers is not None:
            normalized = self._validate_answers(answers, STRATEGY_FIELDS)
            write_markdown(request_path, format_request_markdown("strategy_request", normalized))
            return normalized
        if request_path.exists():
            return parse_request_markdown(request_path.read_text(encoding="utf-8"), STRATEGY_FIELDS)
        raise FileNotFoundError("Missing input file: input/strategy_request.md")

    def _validate_answers(self, answers: dict[str, str], fields: list[str]) -> dict[str, str]:
        normalized: dict[str, str] = {}
        for field in fields:
            value = answers.get(field, "").strip()
            if not value:
                raise ValueError(f"Missing answer for field: {field}")
            normalized[field] = value
        return normalized

    def _build_strategy_brief(self, request: dict[str, str], strategy_request: dict[str, str]) -> str:
        return "\n".join(
            [
                "# strategy_brief",
                "",
                f"- 比赛任务目标：{request['比赛任务目标']}",
                f"- 目标评委或观众：{request['目标评委或观众']}",
                f"- 本轮最重要的评审重点：{strategy_request['本轮最重要的评审重点']}",
                f"- 本轮主证据页想强调什么：{strategy_request['本轮主证据页想强调什么']}",
                f"- 本轮必须避免的表达偏差：{strategy_request['本轮必须避免的表达偏差']}",
                f"- 是否有额外页面或扩展要求：{strategy_request['是否有额外页面或扩展要求']}",
                "",
                "## 当前判断",
                "- 当前固定采用 11 页页面体系。",
                "- 先形成候选页面契约，再逐页与用户核对。",
                "- 未完成逐页核对前，不能把任何页面当作正式出图依据。",
                "",
            ]
        )

    def _build_technical_brief(self, request: dict[str, str], strategy_request: dict[str, str]) -> str:
        return "\n".join(
            [
                "# technical_brief",
                "",
                f"- 必须出现的对象：{request['必须出现的对象']}",
                "- 研究协议：先查仓库，再补外部，最后向用户澄清。",
                "- 图形规则：每一页图都必须在用户确认后才能进入 blueprint / visual / video。",
                "- 第 3 页 CoPaw + AgentScope 架构页和第 7 页总体可实现性架构页必须先完成官方资料核验。",
                f"- 主证据页强化点：{strategy_request['本轮主证据页想强调什么']}",
                "",
            ]
        )

    def _build_narrative_brief(self, request: dict[str, str], strategy_request: dict[str, str]) -> str:
        return "\n".join(
            [
                "# narrative_brief",
                "",
                "- 固定主线：Wan2.7 -> CoPaw -> AgentScope -> 成为 AI 时代的参与者。",
                "- 叙事原则：先说对，再说美；先核对，再出图。",
                f"- 本轮最重要的评审重点：{strategy_request['本轮最重要的评审重点']}",
                f"- 需要避免的表达偏差：{strategy_request['本轮必须避免的表达偏差']}",
                f"- 结尾收束要求：{request['结尾收束要求']}",
                "",
            ]
        )

    def _page_contracts_json(self, page_review_status: list[dict[str, Any]]) -> list[dict[str, Any]]:
        status_lookup = {item["page_id"]: item for item in page_review_status}
        payload: list[dict[str, Any]] = []
        for page in PAGE_DEFINITIONS:
            status = status_lookup[page["page_id"]]
            payload.append(
                {
                    "page_id": page["page_id"],
                    "page_number": page["page_number"],
                    "page_title": page["title"],
                    "must_prove": page["must_prove"],
                    "required_objects": page["required_objects"],
                    "required_relations": page["required_relations"],
                    "forbidden_distortions": page["forbidden_distortions"],
                    "knowledge_sources": page["knowledge_source_ids"],
                    "confirmation_status": status["status"],
                    "approved": status["approved"],
                    "approved_by": status["approved_by"],
                }
            )
        return payload

    def _knowledge_gaps_json(self, page_review_status: list[dict[str, Any]]) -> list[dict[str, Any]]:
        payload: list[dict[str, Any]] = []
        for item in page_review_status:
            payload.append(
                {
                    "page_id": item["page_id"],
                    "status": "closed" if item["approved"] else "open",
                    "reason": "已完成用户核对" if item["approved"] else "用户尚未完成本页核对",
                }
            )
        return payload
