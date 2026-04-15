# Copaw 工作区模板：Wan2.7 技术叙事引擎

本目录用于承载项目专用的 `Copaw` runtime 与提示词骨架。`skills/` 与 **`common/`** **已与** `projects/wan2.7_tech_narrative_engine/` 下对应目录 **保持同名同内容**（由 `scripts/sync_wan27_copaw_skills.ps1` 镜像；`common` 为 skill 运行时 `import common.*` 所必需）。

## `skills/` 目录（六段）

与主工程一致，命名均为 `wan2.7_tech_narrative_engine_*`：

| 顺序 | 目录 |
|------|------|
| 1 | `wan2.7_tech_narrative_engine_intake_skill` |
| 2 | `wan2.7_tech_narrative_engine_strategy_skill` |
| 3 | `wan2.7_tech_narrative_engine_draft_skill` |
| 4 | `wan2.7_tech_narrative_engine_visual_blueprint_skill` |
| 5 | `wan2.7_tech_narrative_engine_visual_generation_skill` |
| 6 | `wan2.7_tech_narrative_engine_video_generation_skill` |

职责、闸门与输入输出以各目录下 **`SKILL.md`** 及主工程 `skills/README.md` 为准。

## 其他路径

- `config/`：地域与模型端点示例（如 `wan27_beijing.example.json`）
- `profiles/`：角色侧写
- `prompts/`：任务路由等提示骨架
- `lightweight_svgs/`、`excalidraw_*`：图示与导出辅助（非 skill 正文）

## 维护说明

更新六段 skill 时以 **`projects/wan2.7_tech_narrative_engine/skills/`** 为唯一源；同步到本工作区请在仓库根执行：

`.\scripts\sync_wan27_copaw_skills.ps1`
