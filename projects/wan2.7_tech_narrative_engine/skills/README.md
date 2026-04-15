# skills

本目录用于承载 `wan2.7_tech_narrative_engine` 的 6 个正式 skill。

## 当前已完成

- `wan2.7_tech_narrative_engine_intake_skill`
  负责初始化任务目录、知识源清单、manifest 和全部 gate
- `wan2.7_tech_narrative_engine_strategy_skill`
  负责生成 strategy / technical / narrative brief，以及 `page_contracts`
- `wan2.7_tech_narrative_engine_draft_skill`
  负责生成 `copy_pack`、`page_visual_specs`、`diagram_blueprints`、`storyboard_draft`
- `wan2.7_tech_narrative_engine_visual_blueprint_skill`
  `SKILL.md` 为薄护栏：设计师主导读稿与构图，Excalidraw MCP 导出 11 页 SVG 并回写 bundle
- `wan2.7_tech_narrative_engine_visual_generation_skill`
  负责生成 10 张正式静态图和 `asset_manifest`
- `wan2.7_tech_narrative_engine_video_generation_skill`
  负责生成场景规划、字幕、旁白、最终视频和提交材料

## 当前原则

- 业务内容必须先形成正式中间产物，再进入下一段 skill
- 第 3 页 CoPaw 架构图和第 8 页执行链路图是强约束页面
- 不允许跳过人工审阅闸门直接进入昂贵生成阶段
- 不允许把“仓库里找到来源”直接等同于“已经和用户核对”
- `intake_skill` 必须写入研究上下文、术语快照和页级核对状态
- `strategy_skill` 必须输出带 `confirmation_status` 的 `page_contracts`
- `draft_skill` 必须在所有页面用户确认后才能继续
- `visual_blueprint_skill` 必须在 bundle 和页面蓝图文档中继续携带确认状态
- `visual_generation_skill` 必须拒绝消费未确认页面，并在 `asset_manifest` 中保留确认状态
- `video_generation_skill` 必须拒绝消费未确认页面，并在 `scene_plan` 中保留来源确认状态
