# Wan2.7 技术叙事引擎 · 比赛发布包

本目录为作品与复现材料的**自包含快照**（由主仓库 `scripts/sync_wan27_competition_bundle.ps1` 生成）。以下为各路径用途说明。

---

## `submission_docs/`

（使用此目录名而非 `docs/`，以免与本机全局 Git 忽略规则 `docs/` 冲突。）

- **`submission_docs/02_项目/`**
  - **`Wan2.7技术叙事引擎_比赛提交说明_2026-04-15.md`**：赛方要求的作品说明（Wan 能力、工作流、§8「`wan2.7-i2v` 与 ffmpeg 兜底」、成片路径等）。
  - **`AI短剧工厂/`**：**`AI短剧工厂_项目预研_2026-04-09.md`**，业务侧三条链路（创作中枢 / 自动化生产工厂 / 知识资产沉淀）预研结论。

---

## `projects/wan2.7_tech_narrative_engine/`

比赛向**可运行工程**：六段 skill、`common` 页面契约、`templates/`（含任务目录协议）、`knowledge/` 领域基线等。子目录与约定见该路径下的 **`README.md`** 与各 **`skills/**/SKILL.md`**。

---

## `tools/copaw_workspace/wan27_tech_narrative_engine/`

**Copaw 工作区模板**：`skills/` 与 `projects/wan2.7_tech_narrative_engine/skills/` **同名同内容**（六段 `wan2.7_tech_narrative_engine_*`）；另含 `config/`、`profiles/`、`prompts/`、图示导出脚本等。维护时请先改 `projects/.../skills`，再运行 `.\scripts\sync_wan27_copaw_skills.ps1`。

---

## `artifacts/wan2.7_current_run/`

一次任务跑通的**节选产物**（便于对照视频与页面）：

| 路径 | 内容 |
|------|------|
| `scripts/i2v_ten_pages_concat.py` | 调用 `wan2.7-i2v`（`data:` 首帧）、失败时 ffmpeg 静帧兜底、再拼接成片。 |
| `output/videos/i2v_ten_concat/wan27_i2v_10pages_concat.mp4` | 十页串联成片（约每页 2 秒）。 |
| `output/videos/i2v_ten_concat/clips_meta.public.json` | 分镜元数据（已脱敏临时下载 URL）。 |
| `output/visuals/images/*.png` | 与成片对应的十张静帧。 |
| `output/blueprints/` | 蓝图导出：SVG、Excalidraw、`pages/*.md`、`visual_blueprint_bundle.json` 等。 |

调用 DashScope 接口需自行配置环境变量 **`DASHSCOPE_API_KEY`**，**勿**将密钥写入本仓库。
