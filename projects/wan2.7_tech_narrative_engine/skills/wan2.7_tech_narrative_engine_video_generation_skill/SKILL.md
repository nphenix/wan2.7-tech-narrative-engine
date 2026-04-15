---
name: wan2.7_tech_narrative_engine_video_generation_skill
description: 基于 Wan2.7 官方视频 API，完成 10 页视觉资产到视频镜头的可追溯生成与交付编排。
---

# wan2.7_tech_narrative_engine_video_generation_skill

将本 skill 作为视频生成唯一入口。  
本 skill 的执行核心是：**先调研、先提示词、再调用官方 API**。

## 核心原则（强制）

1. 视频生成必须调用 Wan2.7 官方 API，不允许本地伪生成替代。
2. 调用方式以 skill.md 编排为主，非必要不新增 Python runner。
3. 在创建任何视频任务前，必须先完成提示词资产定义。
4. 未通过前置闸门时，必须阻塞，不得强行推进。
5. 所有镜头都要可追溯：记录 request_id、参数快照、状态和错误。

## 本 Skill 的职责

它负责 9 件事：

1. 执行“官方文档调研闸门”并记录核验结论
2. 检查 `visual_generation_gate` 与页面确认状态
3. 生成 `scene_plan`（10 页到镜头映射）
4. 先定义提示词资产：`global_video_prompt` + `shot_prompts`
5. 按镜头路由调用 `wan2.7-t2v / wan2.7-i2v / wan2.7-r2v / wan2.7-videoedit`
6. 执行异步任务轮询、重试与失败收敛
7. 产出 `video_manifest.json` 与 `wan_requests/*.json`
8. 评估音频与字幕策略并写入产物说明
9. 初始化 `final_gate`

## 开始前必读输入

- `output/visuals/asset_manifest.json`
- `review/visual_generation_gate.json`
- `output/visuals/images/*.png`

## 调研闸门（必须先完成）

在第一条视频任务创建前，必须联网核验并记录：

- 区域 endpoint（Beijing/Singapore）
- 必需 headers（含 `X-DashScope-Async: enable`）
- 异步流程（创建任务 -> 轮询 `tasks/{task_id}`）
- 支持模型与参数边界（分辨率、时长、音频设置）
- 任务状态机（`PENDING -> RUNNING -> SUCCEEDED/FAILED`）

建议引用的官方文档（执行时需核验最新内容）：

- [Wan 图生视频 API 参考](https://www.alibabacloud.com/help/en/model-studio/image-to-video-api-reference/)
- [Wan 视频编辑 API 参考（中文）](https://help.aliyun.com/zh/model-studio/wan-video-editing-api-reference)
- [视频模型对比与选型](https://www.alibabacloud.com/help/en/model-studio/use-video-generation)

## 官方调用基线（HTTP 异步）

### 创建任务

- Beijing: `POST https://dashscope.aliyuncs.com/api/v1/services/aigc/video-generation/video-synthesis`
- Singapore: `POST https://dashscope-intl.aliyuncs.com/api/v1/services/aigc/video-generation/video-synthesis`

### 查询任务

- Beijing: `GET https://dashscope.aliyuncs.com/api/v1/tasks/{task_id}`
- Singapore: `GET https://dashscope-intl.aliyuncs.com/api/v1/tasks/{task_id}`

### 必需请求头

- `Authorization: Bearer $DASHSCOPE_API_KEY`
- `Content-Type: application/json`
- `X-DashScope-Async: enable`

## 提示词先行闸门（必须执行）

必须先产出两层提示词资产，未完成则禁止调用 API：

1. `global_video_prompt`
2. `shot_prompts`（逐镜头）

### `global_video_prompt` 最低要求

- 统一叙事风格（技术叙事演示片）
- 统一视觉基调（与 visual 阶段一致）
- 运镜约束（克制、信息优先）
- 禁止项（错字、乱跳切、风格漂移）

### `shot_prompts` 每镜头字段

- `shot_id`
- `source_page_id`
- `must_keep`
- `motion_goal`
- `style_overlay`
- `negative_prompt`
- `api_type`（t2v/i2v/r2v/videoedit）

## 模型路由建议

- `i2v`：已有视觉页面做轻运动化（优先）
- `t2v`：纯文本生成补充镜头
- `r2v`：需要参考动作/角色一致性
- `videoedit`：对现有视频做局部或整体编辑

## 字幕与音频策略（基于官方能力）

- 音频：优先使用 Wan2.7 视频模型原生能力（如 `audio_setting`）。
- 字幕：Wan2.7 主视频 API 不作为字幕直生/直嵌主通道；字幕走后处理链路（SRT/渲染）或 IMS 能力。
- 默认建议：先保视频画面与音频一致性，再做字幕后处理。

## 请求体模板（示意）

```json
{
  "model": "wan2.7-i2v",
  "input": {
    "prompt": "<global_video_prompt>\n\n<shot_prompt>"
  },
  "parameters": {
    "resolution": "1080P",
    "duration": 5,
    "ratio": "16:9",
    "watermark": false
  }
}
```

## 执行与失败处理

- 轮询间隔建议：15 秒
- `429/5xx`：指数退避重试（建议 3 次）
- 参数类 `4xx`：立即阻塞并修正
- 任一关键镜头失败：不得将 `final_gate` 置为 approved

## video_manifest 规范

`output/videos/video_manifest.json` 每镜头至少包含：

- `shot_id`
- `source_page_id`
- `api_type`
- `model`
- `duration`
- `resolution`
- `fps`
- `request_id`
- `status`（PENDING/RUNNING/SUCCEEDED/FAILED）
- `error_code`
- `error_message`
- `input_assets`
- `output_path`
- `confirmation_status`

## 硬性约束

- 不消费未确认页面
- 不跳过提示词先行闸门
- 不绕过官方 API
- 不把“视频已生成”等同于“流程已闭环”

## 输出期望

使用本 skill 后，下一步应是以下之一：

- video generation 被阻塞（闸门未通过或参数不合规）
- 已形成分镜视频产物与完整 `video_manifest`
- 已进入最终人工收尾（`final_gate` 待审）
