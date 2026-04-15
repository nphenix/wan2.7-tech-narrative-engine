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
    build_diagram_blueprints_markdown,
    build_knowledge_resolution_markdown,
    build_page_visual_specs_markdown,
    build_review_checklist_markdown,
    build_storyboard_markdown,
    ensure_gate_approved,
    format_request_markdown,
    normalize_page_review_status,
    now_iso,
    parse_request_markdown,
    read_json,
    unresolved_page_review_items,
    update_manifest,
    write_json,
    write_markdown,
)

DRAFT_FIELDS = [
    "本轮更重视哪类草稿",
    "需要强化的关键语",
    "必须避免的文风或表达",
    "是否有必须保留的句子或结尾",
]

STRATEGY_FIELDS = [
    "本轮最重要的评审重点",
    "本轮主证据页想强调什么",
    "本轮必须避免的表达偏差",
    "是否有额外页面或扩展要求",
]


@dataclass
class DraftSkillConfig:
    dry_run: bool = False


class DraftSkillRunner:
    def __init__(self, config: DraftSkillConfig) -> None:
        self.config = config

    def run(self, task_dir: Path, answers: dict[str, str] | None = None) -> dict[str, Any]:
        task_dir = Path(task_dir)
        self._validate_inputs(task_dir)
        ensure_gate_approved(task_dir, "strategy_gate")

        page_review_status = normalize_page_review_status(read_json(task_dir / "review" / "page_review_status.json"))
        unresolved = unresolved_page_review_items(page_review_status)
        if unresolved:
            unresolved_pages = ", ".join(item["page_id"] for item in unresolved)
            raise ValueError(f"未完成用户核对：{unresolved_pages}")

        draft_request = self._prepare_draft_request(task_dir, answers)
        strategy_request = parse_request_markdown(
            (task_dir / "input" / "strategy_request.md").read_text(encoding="utf-8"),
            STRATEGY_FIELDS,
        )

        write_markdown(task_dir / "output" / "drafts" / "copy_pack.md", self._build_copy_pack(draft_request, strategy_request))
        write_markdown(task_dir / "output" / "drafts" / "page_visual_specs.md", build_page_visual_specs_markdown(page_review_status))
        write_markdown(task_dir / "output" / "drafts" / "diagram_blueprints.md", build_diagram_blueprints_markdown())
        write_markdown(task_dir / "output" / "drafts" / "storyboard_draft.md", build_storyboard_markdown())
        write_markdown(task_dir / "output" / "drafts" / "knowledge_resolution.md", build_knowledge_resolution_markdown())
        write_markdown(task_dir / "output" / "drafts" / "review_checklist.md", build_review_checklist_markdown())

        write_json(task_dir / "meta" / "page_visual_specs.json", self._page_visual_specs_json(page_review_status))
        write_json(task_dir / "meta" / "diagram_blueprints.json", self._diagram_blueprints_json())

        gate = read_json(task_dir / "review" / "draft_gate.json")
        gate["status"] = "ready_for_review"
        gate["approved"] = False
        gate["artifacts"] = [
            "input/draft_request.md",
            "output/drafts/copy_pack.md",
            "output/drafts/page_visual_specs.md",
            "output/drafts/diagram_blueprints.md",
            "output/drafts/storyboard_draft.md",
            "output/drafts/knowledge_resolution.md",
            "output/drafts/review_checklist.md",
            "review/page_review_status.json",
        ]
        write_json(task_dir / "review" / "draft_gate.json", gate)

        outputs = {
            "draft_request": "input/draft_request.md",
            "copy_pack": "output/drafts/copy_pack.md",
            "page_visual_specs": "output/drafts/page_visual_specs.md",
            "diagram_blueprints": "output/drafts/diagram_blueprints.md",
            "storyboard_draft": "output/drafts/storyboard_draft.md",
            "knowledge_resolution": "output/drafts/knowledge_resolution.md",
            "review_checklist": "output/drafts/review_checklist.md",
        }
        update_manifest(task_dir, "draft_ready", outputs=outputs)

        result = {"status": "completed", "generated_at": now_iso("DRAFT_SKILL_NOW"), "outputs": outputs}
        write_json(task_dir / "meta" / "draft_result.json", result)
        return result

    def _validate_inputs(self, task_dir: Path) -> None:
        for relative in (
            "input/strategy_request.md",
            "input/strategy_brief.md",
            "input/technical_brief.md",
            "input/narrative_brief.md",
            "review/strategy_gate.json",
            "review/page_review_status.json",
        ):
            if not (task_dir / relative).exists():
                raise FileNotFoundError(f"Missing input file: {relative}")

    def _prepare_draft_request(self, task_dir: Path, answers: dict[str, str] | None) -> dict[str, str]:
        request_path = task_dir / "input" / "draft_request.md"
        if answers is not None:
            normalized = self._validate_answers(answers, DRAFT_FIELDS)
            write_markdown(request_path, format_request_markdown("draft_request", normalized))
            return normalized
        if request_path.exists():
            return parse_request_markdown(request_path.read_text(encoding="utf-8"), DRAFT_FIELDS)
        raise FileNotFoundError("Missing input file: input/draft_request.md")

    def _validate_answers(self, answers: dict[str, str], fields: list[str]) -> dict[str, str]:
        normalized: dict[str, str] = {}
        for field in fields:
            value = answers.get(field, "").strip()
            if not value:
                raise ValueError(f"Missing answer for field: {field}")
            normalized[field] = value
        return normalized

    def _build_copy_pack(self, draft_request: dict[str, str], strategy_request: dict[str, str]) -> str:
        lines = [
            "# copy_pack",
            "",
            "## 总体约束",
            f"- 本轮更重视哪类草稿：{draft_request['本轮更重视哪类草稿']}",
            f"- 需要强化的关键语：{draft_request['需要强化的关键语']}",
            f"- 必须避免的文风或表达：{draft_request['必须避免的文风或表达']}",
            f"- 是否有必须保留的句子或结尾：{draft_request['是否有必须保留的句子或结尾']}",
            f"- 本轮主证据页想强调什么：{strategy_request['本轮主证据页想强调什么']}",
            "",
        ]
        for page in PAGE_DEFINITIONS:
            lines.extend(
                [
                    f"## {page['page_id']}",
                    f"- 页面名称：{page['title']}",
                    f"- 页面目标：{page['must_prove']}",
                    f"- 必须保留标签：{', '.join(page['required_labels'])}",
                    f"- 视觉目标：{page['visual_goal']}",
                    f"- 文案建议：{self._copy_for_page(page)}",
                    "",
                ]
            )
        return "\n".join(lines)

    def _copy_for_page(self, page: dict[str, Any]) -> str:
        copy_map = {
            1: "先完成对题，明确 Wan2.7 是整套作品的核心能力入口，Copaw 与 AI短剧工厂作为辅助标识出现。",
            2: "把 Wan2.7 的图像与视频能力拆成清晰能力簇，并补上与本项目各阶段的落点映射。",
            3: "把 CoPaw 画成编排层，把 AgentScope 画成底座层，并明确区分官方能力层与本项目实现映射。",
            4: "把六个 skill 串成正式工程链路，强调用户核对、状态推进和中间产物，而不是脚本拼接。",
            5: "从 AI短剧工厂的场景价值切入，突出创作价值、生产价值、资产价值三条主线。",
            6: "把三层能力承接关系画清楚，每层同时写承接价值、关键动作和最终结果，避免只剩口号。",
            7: "把业务目标、三层能力、CoPaw、AgentScope、六个 skill 和 Wan2.7 合成总体可实现性主证据图。",
            8: "明确单页从页面契约到完整演示视频的生成链路，并把三次用户核对与阻塞闸门嵌进流程。",
            9: "把状态推进、审阅检查点和阻塞原因画成可控流程，强调未确认不得继续向下游生成。",
            10: "把最终交付收束到成片、可复用 skill、说明文档与结构化产物，强调评委可见与团队可复用。",
            11: "以前面的技术论证为基础完整落诗，用 Wan2.7 的能力升华结尾，落到参与 AI 时代的主题。",
        }
        return copy_map[page["page_number"]]

    def _page_visual_specs_json(self, page_review_status: list[dict[str, Any]]) -> list[dict[str, Any]]:
        status_lookup = {item["page_id"]: item for item in page_review_status}
        return [
            {
                "page_id": page["page_id"],
                "title": page["title"],
                "layout_template": page["layout_template"],
                "diagram_mode": page["diagram_mode"],
                "zones": page["zones"],
                "module_cards": page["module_cards"],
                "required_labels": page["required_labels"],
                "visual_goal": page["visual_goal"],
                "confirmation_status": status_lookup[page["page_id"]]["status"],
                "approved_by": status_lookup[page["page_id"]]["approved_by"],
            }
            for page in PAGE_DEFINITIONS
        ]

    def _diagram_blueprints_json(self) -> list[dict[str, Any]]:
        return [
            {
                "page_id": page["page_id"],
                "title": page["title"],
                "nodes": [card["title"] for card in page["module_cards"]],
                "edges": page["required_relations"],
            }
            for page in PAGE_DEFINITIONS
        ]
