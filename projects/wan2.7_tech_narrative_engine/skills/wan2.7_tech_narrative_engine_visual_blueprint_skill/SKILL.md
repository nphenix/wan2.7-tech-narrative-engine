---
name: wan2.7_tech_narrative_engine_visual_blueprint_skill
description: draft 完成后，以设计师身份用 Excalidraw MCP 为 11 页导出蓝图 SVG 并回写 bundle
---

# wan2.7_tech_narrative_engine_visual_blueprint_skill

你是**设计师**，不是填表员。先读任务目录里的草稿与契约，再决定每一页怎么画才讲得清、好看、好读；本文件只给**硬边界**，不教你版式、配色或必须几块板子。

**硬边界**

- `page_id` 与顺序：`projects/wan2.7_tech_narrative_engine/common/pipeline.py` 的 `PAGE_DEFINITIONS`（共 11 页，含 `page_1_opening` 等）。  
- 产出：每页 `output/blueprints/images/<page_id>.svg`；更新 `output/blueprints/visual_blueprint_bundle.json` 与 `review/visual_blueprint_gate.json`。  
- 只用 **`user-excalidraw`** MCP 出图，**禁止**手写假 SVG；本 skill 目录下**不要**加 `runtime/runner.py`，也不要让别的 skill 的 runner 替你构图。  
- 叙事依据：任务目录的 `output/review/page_contracts.md`、`output/drafts/diagram_blueprints.md`、`output/drafts/page_visual_specs.md`（必要时再瞟一眼 `review/page_review_status.json`）。**不要**把本 `SKILL.md` 当幻灯片正文抄进画布。  
- **可读关系（必选）**：`diagram_blueprints.md` / `page_contracts.md` 里每条有向边，画布上必须有一根**可辨认的箭头**对应；优先 `arrow` + `startBinding` / `endBinding` 绑到两侧**已有节点**（矩形/菱形等），禁止一段线漂在空白处看不出从谁到谁。多组关系要**拉开间距**，避免交叉难辨。  
- **文字不出框（必选）**：形状内短词优先用 `label`（与容器绑定）。独立 `text` 时，字号与行长、框宽要匹配；过长就**缩写、拆成第二块、或单独一块说明区**，禁止标题/正文压住箭头或其它模块。长句放进**足够大的矩形容器**（仍优先 `label` 或多行），导出前自检：无裁切、无压线。

**MCP**：每页先 `start_session`（独立 `sessionId`）且浏览器已连接，再 `add_elements` / `create_from_mermaid` / `update_element`，最后 `export_diagram`（`path` + `format: svg` + 同上 `sessionId`）；未连接时 `export_diagram` 会失败。参数以 IDE 里该 MCP 的 schema 为准。

**闸门**：`draft_gate` 未批准就停；前置某页材料不够就先补再画。
