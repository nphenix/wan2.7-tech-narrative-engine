# 视频产物规范与 2-shot 试跑方案

## 1. video_manifest 建议结构

目标：确保每个镜头可追溯、可审计、可回放问题。

```json
{
  "run_id": "wan27_video_20260414_xxx",
  "engine": "wan2.7-video-api",
  "region": "beijing",
  "generated_at": "2026-04-14T20:00:00+08:00",
  "shots": [
    {
      "shot_id": "shot_01",
      "source_page_id": "page_1_opening",
      "api_type": "i2v",
      "model": "wan2.7-i2v",
      "duration": 5,
      "resolution": "1080P",
      "fps": 30,
      "request_id": "xxx",
      "status": "SUCCEEDED",
      "error_code": null,
      "error_message": null,
      "input_assets": [
        "output/visuals/images/page_1_opening.png"
      ],
      "output_path": "output/videos/shots/shot_01.mp4",
      "confirmation_status": "pending_review"
    }
  ]
}
```

## 2. 状态机定义

- `PENDING`: 任务已创建，等待调度
- `RUNNING`: 任务处理中
- `SUCCEEDED`: 任务成功，已拿到可下载视频
- `FAILED`: 任务失败，需记录错误并决定重试/阻塞

## 3. 2-shot 试跑方案（先验真，再全量）

### 试跑目标

1. 验证 endpoint + header + async 轮询链路可用
2. 验证 `video_manifest` 字段完整
3. 验证音频与字幕策略的工程可行性

### 试跑镜头建议

- `shot_01`（来源 `page_1_opening`）：`i2v`
  - 目标：验证静态页轻运动化与文字稳定性
- `shot_02`（来源 `page_10_closing`）：`t2v` 或 `videoedit`
  - 目标：验证诗意收束镜头的风格控制

### 验收标准

- 两个镜头都获得有效 `request_id`
- 轮询最终状态均为 `SUCCEEDED`
- 输出视频可下载、可播放、参数符合预期（时长/分辨率）
- `video_manifest` 与 `wan_requests` 完整落盘

## 4. 字幕 vs 音频能力评估结论

- 音频：优先使用 Wan2.7 原生能力（含 `audio_setting`，按镜头选择 `auto/origin`）。
- 字幕：不依赖 Wan2.7 主视频 API 直接产出 SRT/烧录字幕。
- 推荐链路：
  1. 先完成视频画面与音频生成
  2. 再进行字幕后处理（SRT 生成/校对/烧录），必要时可对接 IMS 能力

## 5. 风险与回退

- 若任一镜头 `FAILED`，不进入全量 10-shot 阶段
- 429/5xx 允许重试，4xx 参数错误直接阻塞并修正
- 未记录 request_id 的任务视为无效执行
