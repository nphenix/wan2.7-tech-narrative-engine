# wan2.7_tech_narrative_engine

这是 `wan2.7_tech_narrative_engine` 的运行时项目目录。

## 当前定位

- 面向比赛版交付的可运行项目
- 以 6 个正式 skill 串起任务理解、页面契约、视觉蓝图、静态图和视频交付
- 目标是让中断后的后续开发者可以直接按任务目录协议恢复工作

## 六段执行链

1. `wan2.7_tech_narrative_engine_intake_skill`
2. `wan2.7_tech_narrative_engine_strategy_skill`
3. `wan2.7_tech_narrative_engine_draft_skill`
4. `wan2.7_tech_narrative_engine_visual_blueprint_skill`
5. `wan2.7_tech_narrative_engine_visual_generation_skill`
6. `wan2.7_tech_narrative_engine_video_generation_skill`

## 关键目录

- `skills/`：6 个正式 skill
- `templates/`：任务目录协议和示例请求
- `common/`：共享页面契约、任务状态和文档生成逻辑
- `knowledge/`：项目级长期研究基线、术语定义和研究协议

## 关键说明

- 正式设计说明：
  `docs/02_项目/wan2.7_技术叙事引擎/wan2.7_技术叙事引擎_六技能贯通设计说明_2026-04-11.md`
- 当前任务协议：
  `templates/任务目录协议.md`
- 项目级研究协议：
  `knowledge/research_protocol.md`
- 项目级术语基线：
  `knowledge/domain_terms.md`
- 项目级任务清单：
  `spec_coding/plans/2026-04-12_wan2.7六技能重构与续开发任务清单.md`

## 新增规则

- 先查仓库资料，再补联网资料，最后向用户求证
- 每一页图都必须与用户核对
- `review/page_review_status.json` 未全部关闭前，不允许进入 `draft -> visual_blueprint -> visual_generation -> video_generation`
- `visual_blueprint_bundle.json`、`asset_manifest.json`、`scene_plan.md` 现在都会继续携带页级确认状态，保证下游不丢失确认链路
