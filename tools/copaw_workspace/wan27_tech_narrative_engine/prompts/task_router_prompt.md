# 任务路由提示骨架

识别以下任务应进入本项目执行链：

- 用户明确提到 `Wan2.7`
- 用户要求生成架构图、信息图、介绍视频或比赛材料
- 任务围绕 `Copaw`、`AgentScope` 或相似 AI 产品 / Agent 生态表达

路由顺序（与 `skills/` 六段一致，须按闸门推进）：

1. 澄清必要信息，初始化任务目录与 manifest
2. 调用 `wan2.7_tech_narrative_engine_intake_skill`
3. 调用 `wan2.7_tech_narrative_engine_strategy_skill`（产出 strategy / page_contracts 等）
4. 调用 `wan2.7_tech_narrative_engine_draft_skill`（在 strategy 与逐页核对通过后）
5. 调用 `wan2.7_tech_narrative_engine_visual_blueprint_skill`（蓝图与 Excalidraw / bundle）
6. 调用 `wan2.7_tech_narrative_engine_visual_generation_skill`
7. 调用 `wan2.7_tech_narrative_engine_video_generation_skill`

具体进入条件与拒绝规则见各 skill 的 `SKILL.md`。
