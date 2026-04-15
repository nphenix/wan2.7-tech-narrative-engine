---
name: wan2.7_tech_narrative_engine_strategy_skill
description: 当 intake 已完成，需要把任务目标翻译成正式策略层产物、候选页面契约与知识阻塞项时使用。
---

# wan2.7_tech_narrative_engine_strategy_skill

将本 skill 作为六段链路中的策略入口。

## 本 Skill 的职责

它主要做 6 件事：

1. 检查 intake 产物是否存在
2. 收集本轮策略偏好
3. 生成 `strategy_brief`
4. 生成 `technical_brief`
5. 生成候选 `page_contracts`
6. 把未完成逐页核对写入 `knowledge_gaps`

## 开始前先读

- 当前任务目录下的 `input/user_request.md`
- 当前任务目录下的 `input/research_context.md`
- 当前任务目录下的 `review/page_review_status.json`
- `projects/wan2.7_tech_narrative_engine/knowledge/domain_terms.md`

## 输入预期

通过自然语言向用户逐项确认：

- 本轮最重要的评审重点
- 本轮主证据页想强调什么
- 本轮必须避免的表达偏差
- 是否有额外页面或扩展要求

## 核心流程

1. 先检查 intake 产物是否存在
2. 再确认本轮策略偏好
3. 生成三类 brief
4. 生成候选页面职责与页面契约
5. 将未确认页面显式写入 `knowledge_gaps`
6. 推进 `strategy_gate`

## 硬性约束

- 不要把候选页面契约当成已确认事实
- 只要页面未逐页确认，就必须写入阻塞项
- 不要在 strategy 阶段直接推进视觉生成

## 输出期望

使用本 skill 后，下一步应是以下之一：

- 已形成 strategy / technical / narrative brief
- 已形成候选 `page_contracts`
- 已形成正式 `knowledge_gaps`
- 已准备进入 `draft`
- 因逐页未确认而明确阻塞
