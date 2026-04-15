---
name: wan2.7_tech_narrative_engine_intake_skill
description: 当需要为 wan2.7 比赛版工作创建新任务、收口正式输入、初始化研究上下文与页级核对状态时使用。
---

# wan2.7_tech_narrative_engine_intake_skill

将本 skill 作为 `wan2.7_tech_narrative_engine` 六段链路的正式入口。

## 本 Skill 的职责

本 skill 不替代后续 strategy、draft、blueprint、visual、video skill。

它主要做 6 件事：

1. 初始化标准任务目录
2. 建立本轮研究上下文
3. 收集正式 `user_request`
4. 写入术语快照与页级核对状态
5. 初始化 `strategy_gate`
6. 为后续逐页核对建立起点

## 开始前先读

在做 intake 前，先读：

- `projects/wan2.7_tech_narrative_engine/README.md`
- `projects/wan2.7_tech_narrative_engine/templates/任务目录协议.md`
- `projects/wan2.7_tech_narrative_engine/knowledge/research_protocol.md`
- `projects/wan2.7_tech_narrative_engine/knowledge/domain_terms.md`

如果涉及本轮历史判断，再读：

- `spec_coding/plans/2026-04-12_wan2.7六技能重构交接文档.md`

## 输入预期

通过自然语言向用户逐项确认以下正式输入：

- 比赛任务目标
- 目标评委或观众
- 必须出现的对象
- 必须避免的风险
- 结尾收束要求

## 核心流程

按以下顺序执行：

1. 先创建或重置本轮任务目录
2. 写入 `research_context.md`
3. 写入 `domain_terms.snapshot.json`
4. 初始化 `page_review_status.json`
5. 逐项收集 `user_request`
6. 写入 `strategy_gate`

## 硬性约束

- 不要跳过研究上下文初始化
- 不要假设用户已经完成澄清
- 不要在 intake 阶段进入 strategy 之后的任何生成阶段
- 不要把术语来源写成已确认事实，除非用户明确确认

## 输出期望

使用本 skill 后，下一步应是以下之一：

- 已完成任务目录初始化
- 已形成正式 `user_request`
- 已形成研究快照与页级核对状态
- 已准备进入 `wan2.7_tech_narrative_engine_strategy_skill`
- 因用户信息缺失而继续澄清
