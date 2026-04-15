---
name: wan2.7_tech_narrative_engine_draft_skill
description: 当 strategy 已完成、且逐页核对条件满足，需要把页面契约翻译成草稿层产物时使用。
---

# wan2.7_tech_narrative_engine_draft_skill

将本 skill 作为草稿层入口。

## 本 Skill 的职责

它主要做 6 件事：

1. 检查 `strategy_gate` 是否已批准
2. 检查 `page_review_status` 是否全部关闭
3. 收集本轮草稿偏好
4. 生成 `copy_pack`
5. 生成 `page_visual_specs`、`diagram_blueprints`、`storyboard_draft`
6. 初始化 `draft_gate`

## 开始前先读

- 当前任务目录下的 `input/strategy_brief.md`
- 当前任务目录下的 `output/review/page_contracts.md`
- 当前任务目录下的 `review/page_review_status.json`

## 输入预期

通过自然语言向用户逐项确认：

- 本轮更重视哪类草稿
- 需要强化的关键语
- 必须避免的文风或表达
- 是否有必须保留的句子或结尾

## 硬性进入门

- 如果 `strategy_gate` 未批准，停止并回到 strategy
- 如果任一页面未完成用户核对，停止并继续逐页核对

## 输出期望

使用本 skill 后，下一步应是以下之一：

- draft 被阻塞，因为 `strategy_gate` 未批准
- draft 被阻塞，因为仍有页面未确认
- 已形成草稿层正式候选产物
- 已准备进入 `visual_blueprint`
