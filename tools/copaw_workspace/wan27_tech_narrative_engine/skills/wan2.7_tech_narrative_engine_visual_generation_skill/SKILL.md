---
name: wan2.7_tech_narrative_engine_visual_generation_skill
description: 基于 Wan2.7 官方 API，将已确认蓝图强化为正式视觉效果图。
---

# wan2.7_tech_narrative_engine_visual_generation_skill

将本 skill 作为**正式视觉效果图生成入口**。

## 核心原则

- 本 skill 以**已确认蓝图**为输入，不改写上游页面语义。
- 本 skill 先做**提示词定义**，再做 API 生成。
- 本 skill 只使用 Wan2.7 官方接口能力，不使用本地“伪生成”脚本。
- 本 skill 对每页保留可追溯记录：请求参数、request_id、输出路径、失败原因。

## 本 Skill 的职责

它负责 6 件事：

1. 检查 `visual_blueprint_gate` 是否已批准。
2. 拒绝消费未确认页面或未导出蓝图页面。
3. 建立全局风格提示词与页面级提示词模板。
4. 调用 Wan2.7 官方 API 生成 10 张正式视觉图。
5. 生成 `asset_manifest.json`（含 request_id 与参数快照）。
6. 初始化 `visual_generation_gate`。

## 开始前必读输入

- `output/blueprints/visual_blueprint_bundle.json`
- `review/visual_blueprint_gate.json`
- `output/blueprints/images/*.svg`（当前 10 页）

## Wan2.7 官方调用基线

### 推荐同步端点（默认）

- 北京：`POST https://dashscope.aliyuncs.com/api/v1/services/aigc/multimodal-generation/generation`
- 新加坡：`POST https://dashscope-intl.aliyuncs.com/api/v1/services/aigc/multimodal-generation/generation`

### 必需请求头

- `Authorization: Bearer $DASHSCOPE_API_KEY`
- `Content-Type: application/json`

### 模型选择

- 默认：`wan2.7-image-pro`（质量优先，适合最终视觉稿）
- 若需要快速试稿：`wan2.7-image`（速度优先）

### 参数建议

- `size`: 默认 `2K`
- `n`: 默认 `1`（控制成本）
- `thinking_mode`: `true`
- `watermark`: 按项目要求设置（通常 `false`）

## 提示词先行（必须执行）

在第一张图生成前，先写出两层 prompt 资产：

1. 全局风格提示词（global_prompt）
2. 页面级提示词（page_prompt）

### 全局风格提示词模板

- 视觉定位：技术叙事演示稿，结构清晰优先，避免花哨噪点。
- 画面语言：中文可读性强，信息层级明确，主标题冲击力明确。
- 风格要求：现代科技感、专业演示风、统一色系、统一光照逻辑。
- 结构约束：保留页面核心对象与关系，不得删改关键节点。
- 负向约束：禁止乱码、错别字、英文替代中文、关系箭头语义错误、无关装饰。

### 页面级提示词模板

每页提示词必须包含四段：

- `must_keep`: 必须保留对象与关系（来自蓝图文本）
- `enhance_focus`: 本页主要强化点（例如主证据、执行链、收束）
- `style_overlay`: 对全局风格的本页微调
- `negative_prompt`: 本页禁止偏移项

## 10 页执行建议（当前蓝图）

- `page_1_opening`: 强化开场标题冲击力与对题感。
- `page_2_wan27_lead`: 强化 Wan2.7 能力主位与“能力到场景”映射。
- `page_3_copaw_orchestrator`: 强化 Copaw 与 AgentScope 的分层关系。
- `page_4_business_pain`: 强化业务痛点到响应链路的因果结构。
- `page_5_capability_response`: 强化能力卡片的层次与可读性。
- `page_6_layering`: 强化三层能力映射关系。
- `page_7_main_proof`: 强化总证据图的闭环与六 skill 真实命名。
- `page_8_execution_flow`: 强化“功能说明 + Wan2.7 API”双层表达。
- `page_9_agentscope_ecosystem_reuse`: 强化 MsgHub/MCP-A2A/memory 的可复用主张。
- `page_10_closing`: 强化诗意收束，保持克制与留白，不加流程箭头。

## 请求体模板（同步）

```json
{
  "model": "wan2.7-image-pro",
  "input": {
    "messages": [
      {
        "role": "user",
        "content": [
          {
            "text": "<global_prompt>\n\n<page_prompt>"
          }
        ]
      }
    ]
  },
  "parameters": {
    "size": "2K",
    "n": 1,
    "watermark": false,
    "thinking_mode": true
  }
}
```

## 响应解析与落盘规则

- 从 `output.choices[].message.content[]` 读取生成图片地址或数据。
- 记录 `request_id` 到产物清单，便于追溯。
- 生成图统一落盘到：`output/visuals/images/<page_id>.png`
- 请求快照与响应快照落盘到：`output/visuals/wan_requests/<page_id>.json`

## asset_manifest 规范

`output/visuals/asset_manifest.json` 每页至少包含：

- `page_id`
- `title`
- `source_svg_path`
- `image_path`
- `model`
- `size`
- `n`
- `global_prompt_digest`
- `page_prompt_digest`
- `request_id`
- `status`（success/failed）
- `error_code`
- `error_message`
- `confirmation_status`

## 失败处理策略

- 429/5xx：指数退避重试（建议 3 次）。
- 结构化错误（4xx 参数问题）：立即阻塞并修正 prompt/参数后重试。
- 任一页面失败：`visual_generation_gate` 不得置为 approved。

## 硬性约束

- 不消费未确认页面。
- 不消费未导出蓝图 SVG。
- 不改写上游语义与页面事实。
- 不把“图已生成”当作“业务已确认”。
- 不使用本地绘图脚本冒充 Wan2.7 生成结果。

## 输出期望

使用本 skill 后，下一步应是以下之一：

- visual generation 被阻塞（蓝图闸门未通过或页面未确认）
- 已形成 10 张正式静态图与完整 `asset_manifest`
- 已准备进入 `video_generation`
