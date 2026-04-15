from __future__ import annotations

import json
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import Any

PROJECT_NAME = "wan2.7_tech_narrative_engine"
PROJECT_RUNTIME_DIR = Path("projects") / PROJECT_NAME
PROJECT_KNOWLEDGE_DIR = PROJECT_RUNTIME_DIR / "knowledge"

TASK_STATUSES = [
    "created",
    "intake_ready",
    "strategy_ready",
    "draft_ready",
    "visual_blueprint_ready",
    "visual_generation_ready",
    "video_ready",
    "final_ready",
]

GATE_NAMES = [
    "strategy_gate",
    "draft_gate",
    "visual_blueprint_gate",
    "visual_generation_gate",
    "final_gate",
]

PARTICIPANT_MANIFESTO = (
    "湛湛长空，乱云飞度，吹尽繁红无数。"
    "正当年，紫金空铸，万里黄沙无觅处。"
    "沉江望极，狂涛乍起，惊飞一滩鸥鹭。"
    "鲜衣怒马少年郎，不负昭华行且知。"
)
DEFAULT_IMAGE_SIZE = (1440, 960)


@dataclass(frozen=True)
class KnowledgeSource:
    source_id: str
    title: str
    relative_path: str
    source_type: str
    summary: str
    objects: tuple[str, ...]


KNOWLEDGE_SOURCES: tuple[KnowledgeSource, ...] = (
    KnowledgeSource(
        "doc_project_prereseach",
        "Copaw驱动的Wan2.7技术叙事引擎_项目预研_2026-04-06.md",
        "docs/02_项目/wan2.7_技术叙事引擎/Copaw驱动的Wan2.7技术叙事引擎_项目预研_2026-04-06.md",
        "repo_doc",
        "定义项目 framing、目标受众、核心叙事链路和 Copaw 角色边界。",
        ("Wan2.7", "Copaw", "AgentScope", "技术叙事引擎"),
    ),
    KnowledgeSource(
        "doc_design_competition",
        "wan2.7_技术叙事引擎_比赛版设计方案_2026-04-11.md",
        "docs/02_项目/wan2.7_技术叙事引擎/wan2.7_技术叙事引擎_比赛版设计方案_2026-04-11.md",
        "repo_doc",
        "定义比赛版目录分层、阶段范围、交付物和比赛约束。",
        ("比赛版", "任务目录协议", "交付物"),
    ),
    KnowledgeSource(
        "doc_design_chain",
        "wan2.7_技术叙事引擎_六技能贯通设计说明_2026-04-11.md",
        "docs/02_项目/wan2.7_技术叙事引擎/wan2.7_技术叙事引擎_六技能贯通设计说明_2026-04-11.md",
        "repo_doc",
        "定义六技能正式输入输出、知识传递链、闸门和页面契约。",
        ("page_contracts", "page_visual_specs", "visual_blueprint", "video_generation"),
    ),
    KnowledgeSource(
        "doc_ai_drama_factory",
        "AI短剧工厂_项目预研_2026-04-09.md",
        "docs/02_项目/AI短剧工厂/AI短剧工厂_项目预研_2026-04-09.md",
        "repo_doc",
        "提供创作中枢、自动化生产工厂、知识资产沉淀管理三层方法论。",
        ("创作中枢", "自动化生产工厂", "知识资产沉淀管理"),
    ),
    KnowledgeSource(
        "sample_technical",
        "默认样例_技术骨架摘要.md",
        "docs/02_项目/wan2.7_技术叙事引擎/samples/默认样例_技术骨架摘要.md",
        "sample_doc",
        "提供技术架构图、执行链路图、生态关系图的关键对象和约束。",
        ("CoPaw 架构图", "执行链路图", "AgentScope 生态图"),
    ),
    KnowledgeSource(
        "sample_narrative",
        "默认样例_叙事摘要.md",
        "docs/02_项目/wan2.7_技术叙事引擎/samples/默认样例_叙事摘要.md",
        "sample_doc",
        "提供标题、副标题、叙事顺序、视觉气质和收束要求。",
        ("主叙事", "视觉节奏", "参与者宣言"),
    ),
    KnowledgeSource(
        "sample_storyboard",
        "默认样例_分镜摘要.md",
        "docs/02_项目/wan2.7_技术叙事引擎/samples/默认样例_分镜摘要.md",
        "sample_doc",
        "提供 45-70 秒视频的场景结构、字幕重点和收束方式。",
        ("Scene 1", "Scene 11", "字幕", "旁白"),
    ),
)


PAGE_DEFINITIONS: list[dict[str, Any]] = [
    {
        "page_number": 1,
        "page_id": "page_1_opening",
        "title": "对题页",
        "role": "比赛对题封面",
        "must_prove": "这是一个以 Wan2.7 为核心能力、面向 AI 短剧工厂的可运行项目 skill。",
        "required_objects": ["Wan2.7", "Copaw", "AI短剧工厂", "项目 skill"],
        "required_relations": ["Wan2.7 -> 技术叙事引擎", "技术叙事引擎 -> AI短剧工厂"],
        "forbidden_distortions": ["不要弱化 Wan2.7", "不要把封面做成空泛海报"],
        "knowledge_source_ids": ["doc_project_prereseach", "sample_narrative"],
        "layout_template": "hero_opening",
        "zones": [
            {"name": "header", "purpose": "主标题与副标题"},
            {"name": "hero", "purpose": "Wan2.7 主视觉"},
            {"name": "footer", "purpose": "比赛对题主张"}
        ],
        "module_cards": [
            {"title": "主标题", "zone": "header", "body": "Wan2.7 驱动的 Copaw 技术叙事引擎"},
            {"title": "副标题", "zone": "header", "body": "面向 AI 短剧工厂的可调用、可复用、可升级的 Skill 化多模态生成链路"},
            {"title": "主张", "zone": "footer", "body": "我们提交的不是一次性效果演示，而是一套基于 Wan2.7 API 的可运行项目 skill。"}
        ],
        "required_labels": ["Wan2.7", "Copaw", "AI短剧工厂", "项目 skill"],
        "text_density": "low",
        "allowed_freestyle": "high",
        "diagram_mode": "hero",
        "visual_goal": "用封面级主视觉快速完成对题。",
        "scene_title": "Scene 1：Wan2.7 对题开场",
        "scene_goal": "建立 Wan2.7 是整套作品主引擎的第一印象。",
        "subtitle_focus": "Wan2.7 不是背景板，而是技术叙事引擎的核心能力入口。"
    },
    {
        "page_number": 2,
        "page_id": "page_2_wan27_api",
        "title": "Wan2.7 API 展示页",
        "role": "能力展示页",
        "must_prove": "Wan2.7 API 提供真实可调用的图像与视频能力，并进入本项目生成链路。",
        "required_objects": ["Wan2.7 API", "图像能力", "视频能力", "项目落点"],
        "required_relations": ["Wan2.7 API -> 图像能力", "Wan2.7 API -> 视频能力", "图像能力/视频能力 -> 项目落点"],
        "forbidden_distortions": ["不要只写模型名", "不要把能力页画成纯文字说明"],
        "knowledge_source_ids": ["sample_technical", "official_source_findings"],
        "layout_template": "uml_capability_map",
        "zones": [
            {"name": "left", "purpose": "图像能力簇"},
            {"name": "right", "purpose": "视频能力簇"},
            {"name": "bottom", "purpose": "项目落点映射"}
        ],
        "module_cards": [
            {"title": "图像能力", "zone": "left", "body": "文生图、图生组图、图像编辑、多图参考生成、4K 高清输出"},
            {"title": "视频能力", "zone": "right", "body": "首帧生视频、首尾帧生视频、视频续写、视频编辑/视频迁移"},
            {"title": "项目落点", "zone": "bottom", "body": "上游 skill 组织结构化输入，visual_generation 与 video_generation 负责调用能力完成正式生成"}
        ],
        "required_labels": ["Wan2.7 API", "图像能力", "视频能力", "项目落点"],
        "text_density": "high",
        "allowed_freestyle": "limited",
        "diagram_mode": "capability",
        "visual_goal": "把 Wan2.7 的真实能力与项目生成环节准确对齐。",
        "scene_title": "Scene 2：Wan2.7 能力全景",
        "scene_goal": "证明项目不是空喊 Wan2.7，而是明确承接它的图像与视频能力。",
        "subtitle_focus": "Wan2.7 API 的能力展示必须能映射到项目中的真实生成步骤。"
    },
    {
        "page_number": 3,
        "page_id": "page_3_copaw_agentscope_architecture",
        "title": "Copaw + AgentScope 架构页",
        "role": "核心架构页",
        "must_prove": "Copaw 作为上层工作站化编排承载，AgentScope 作为底座框架，共同支撑六个项目 skill。",
        "required_objects": ["用户自然语言入口", "Copaw", "AgentScope", "六个项目 skill", "技术 agent", "叙事导演 agent"],
        "required_relations": ["用户自然语言入口 -> Copaw", "Copaw -> AgentScope", "Copaw -> 六个项目 skill", "AgentScope -> 六个项目 skill"],
        "forbidden_distortions": ["不要把项目角色冒充为官方组件", "不要删掉 skill 编排关系"],
        "knowledge_source_ids": ["doc_project_prereseach", "official_source_findings"],
        "layout_template": "uml_component_architecture",
        "zones": [
            {"name": "left", "purpose": "用户入口"},
            {"name": "center", "purpose": "Copaw / AgentScope 双层结构"},
            {"name": "right", "purpose": "六个项目 skill"},
            {"name": "bottom", "purpose": "能力说明与项目映射"}
        ],
        "module_cards": [
            {"title": "Copaw 上层承载", "zone": "center", "body": "多通道交互、Agent Core、Skill 调度、Memory / Heartbeat"},
            {"title": "AgentScope 底座", "zone": "center", "body": "MsgHub / Pipeline、Tool / MCP、Memory、Human-in-the-loop、Deploy / Observe"},
            {"title": "项目映射", "zone": "bottom", "body": "技术 agent 与叙事导演 agent 作为项目映射挂在 Copaw 层，六个项目 skill 在 AgentScope 承载之上执行"}
        ],
        "required_labels": ["Copaw", "AgentScope", "六个项目 skill", "技术 agent", "叙事导演 agent"],
        "text_density": "high",
        "allowed_freestyle": "none",
        "diagram_mode": "architecture",
        "visual_goal": "用专业组件/部署式结构图解释 Copaw 与 AgentScope 的分层关系。",
        "scene_title": "Scene 3：Copaw + AgentScope 架构证据",
        "scene_goal": "说明这不是脚本堆砌，而是有工作站化编排层与框架底座的正式系统。",
        "subtitle_focus": "官方能力层与项目映射层必须分开表达。"
    },
    {
        "page_number": 4,
        "page_id": "page_4_six_skill_flow",
        "title": "六个 skill 串联流程页",
        "role": "阶段流程页",
        "must_prove": "intake 到 video_generation 构成正式阶段链，而不是零散脚本串联。",
        "required_objects": ["intake", "strategy", "draft", "visual_blueprint", "visual_generation", "video_generation", "正式产物", "状态闸门"],
        "required_relations": ["intake -> strategy", "strategy -> draft", "draft -> visual_blueprint", "visual_blueprint -> visual_generation", "visual_generation -> video_generation"],
        "forbidden_distortions": ["不要隐藏用户核对", "不要把正式产物省略掉"],
        "knowledge_source_ids": ["doc_design_chain"],
        "layout_template": "uml_activity_flow",
        "zones": [
            {"name": "top", "purpose": "六个 skill 阶段"},
            {"name": "middle", "purpose": "正式产物"},
            {"name": "bottom", "purpose": "状态推进与闸门"}
        ],
        "module_cards": [
            {"title": "前置收敛", "zone": "top", "body": "intake / strategy / draft"},
            {"title": "视觉生产", "zone": "top", "body": "visual_blueprint / visual_generation"},
            {"title": "视频交付", "zone": "top", "body": "video_generation"},
            {"title": "正式产物", "zone": "middle", "body": "用户请求、页面契约、页面视觉规格、视觉蓝图包、静态资产清单、场景计划"}
        ],
        "required_labels": ["intake", "strategy", "draft", "visual_blueprint", "visual_generation", "video_generation"],
        "text_density": "high",
        "allowed_freestyle": "high",
        "diagram_mode": "workflow",
        "visual_goal": "把六个 skill 的正式工程链表达清楚。",
        "scene_title": "Scene 4：六个 skill 执行链",
        "scene_goal": "证明项目是可审阅、可推进、可交付的多阶段链路。",
        "subtitle_focus": "每个阶段都产生正式中间产物，并受状态闸门控制。"
    },
    {
        "page_number": 5,
        "page_id": "page_5_ai_drama_factory_value",
        "title": "AI短剧工厂场景价值页",
        "role": "价值定义页",
        "must_prove": "AI 短剧工厂是一个同时要求创作组织、生产执行与资产沉淀协同成立的真实业务场景。",
        "required_objects": ["创作价值", "生产价值", "资产价值", "场景总价值"],
        "required_relations": ["场景总价值 -> 创作价值", "场景总价值 -> 生产价值", "场景总价值 -> 资产价值"],
        "forbidden_distortions": ["不要把这一页画成抱怨困难", "不要缺少业务价值落点"],
        "knowledge_source_ids": ["doc_ai_drama_factory"],
        "layout_template": "value_cards",
        "zones": [
            {"name": "top", "purpose": "总价值句"},
            {"name": "bottom", "purpose": "三类价值"}
        ],
        "module_cards": [
            {"title": "总价值", "zone": "top", "body": "AI短剧工厂不是单点生成场景，而是同时要求创作组织、生产执行与资产沉淀协同成立的真实业务场景。"},
            {"title": "创作价值", "zone": "bottom", "body": "把创意组织成可推进的内容生产链"},
            {"title": "生产价值", "zone": "bottom", "body": "把内容生产变成可规模化执行流程"},
            {"title": "资产价值", "zone": "bottom", "body": "把每次项目结果沉淀成可复用资产"}
        ],
        "required_labels": ["创作价值", "生产价值", "资产价值"],
        "text_density": "medium",
        "allowed_freestyle": "limited",
        "diagram_mode": "value",
        "visual_goal": "先把场景值得做讲透，再承接到能力层。",
        "scene_title": "Scene 5：AI短剧工厂场景价值",
        "scene_goal": "让评委先认同场景价值，再进入能力和架构。",
        "subtitle_focus": "这不是概念秀，而是有真实业务价值承载的 AI Agent 项目。"
    },
    {
        "page_number": 6,
        "page_id": "page_6_capability_layers",
        "title": "三层能力承接页",
        "role": "价值到能力映射页",
        "must_prove": "创作中枢、自动化生产工厂、知识资产沉淀管理三层能力分别承接三类价值，并给出动作与结果。",
        "required_objects": ["创作中枢", "自动化生产工厂", "知识资产沉淀管理", "创作价值", "生产价值", "资产价值"],
        "required_relations": ["创作价值 -> 创作中枢", "生产价值 -> 自动化生产工厂", "资产价值 -> 知识资产沉淀管理"],
        "forbidden_distortions": ["不要只写口号", "不要缺少动作与结果"],
        "knowledge_source_ids": ["doc_ai_drama_factory", "doc_design_chain"],
        "layout_template": "layer_mapping",
        "zones": [
            {"name": "left", "purpose": "三类价值"},
            {"name": "right", "purpose": "三层能力映射"}
        ],
        "module_cards": [
            {"title": "创作中枢", "zone": "right", "body": "承接创作价值；理解任务、组织叙事、形成页面契约；产出可执行内容结构"},
            {"title": "自动化生产工厂", "zone": "right", "body": "承接生产价值；组织生成、推进状态、产出图片与视频；形成稳定交付资产"},
            {"title": "知识资产沉淀管理", "zone": "right", "body": "承接资产价值；沉淀规则、归档产物、支持复用；形成长期可复用项目资产"}
        ],
        "required_labels": ["创作中枢", "自动化生产工厂", "知识资产沉淀管理"],
        "text_density": "high",
        "allowed_freestyle": "limited",
        "diagram_mode": "layering",
        "visual_goal": "把价值承接关系落到明确能力层与结果层。",
        "scene_title": "Scene 6：三层能力承接",
        "scene_goal": "解释方法论如何映射为具体产品能力。",
        "subtitle_focus": "每一层都必须说清承接什么价值、做什么动作、产出什么结果。"
    },
    {
        "page_number": 7,
        "page_id": "page_7_main_proof",
        "title": "总体可实现性架构页",
        "role": "主证据页",
        "must_prove": "AI短剧工厂业务目标、三层能力、Copaw、AgentScope、六个项目 skill 与 Wan2.7 共同构成可运行、可扩展、可复用的生产闭环。",
        "required_objects": ["AI短剧工厂", "三层能力", "Copaw", "AgentScope", "六个项目 skill", "Wan2.7"],
        "required_relations": ["AI短剧工厂 -> 三层能力", "三层能力 -> Copaw", "Copaw -> AgentScope", "Copaw -> 六个项目 skill", "Wan2.7 -> 六个项目 skill"],
        "forbidden_distortions": ["不要把主证据页画成概念口号墙", "不要混淆官方能力与项目实现映射"],
        "knowledge_source_ids": ["doc_project_prereseach", "doc_ai_drama_factory", "official_source_findings"],
        "layout_template": "uml_system_architecture",
        "zones": [
            {"name": "top", "purpose": "业务目标层"},
            {"name": "middle", "purpose": "三层能力"},
            {"name": "bottom_left", "purpose": "Copaw / AgentScope 双层底座"},
            {"name": "bottom_right", "purpose": "六个项目 skill"},
            {"name": "right", "purpose": "Wan2.7 外部能力"}
        ],
        "module_cards": [
            {"title": "业务目标层", "zone": "top", "body": "AI短剧工厂"},
            {"title": "三层能力", "zone": "middle", "body": "创作中枢 / 自动化生产工厂 / 知识资产沉淀管理"},
            {"title": "执行底座", "zone": "bottom_left", "body": "Copaw 上层编排 + AgentScope 底座框架"},
            {"title": "实现层", "zone": "bottom_right", "body": "六个项目 skill 按阶段串联并由 Copaw 编排调用"}
        ],
        "required_labels": ["AI短剧工厂", "Copaw", "AgentScope", "Wan2.7", "六个项目 skill"],
        "text_density": "high",
        "allowed_freestyle": "none",
        "diagram_mode": "system_architecture",
        "visual_goal": "用主证据页证明整套系统能真正落起来。",
        "scene_title": "Scene 7：总体可实现性架构",
        "scene_goal": "把业务、能力、编排、底座、技能和外部能力压成一张可核对总图。",
        "subtitle_focus": "这一页不是概念图，而是整套方案能跑起来的主证据。"
    },
    {
        "page_number": 8,
        "page_id": "page_8_single_page_flow",
        "title": "单页生成链路页",
        "role": "单页执行链页",
        "must_prove": "单页内容从用户目标到最终视频，必须经历页面契约、视觉规格、视觉蓝图和三次用户核对。",
        "required_objects": ["用户目标", "页面契约", "页面视觉规格", "视觉蓝图", "页面静帧资产", "完整演示视频", "用户核对"],
        "required_relations": ["用户目标 -> 页面契约", "页面契约 -> 页面视觉规格", "页面视觉规格 -> 视觉蓝图", "视觉蓝图 -> 页面静帧资产", "页面静帧资产 -> 完整演示视频"],
        "forbidden_distortions": ["不要省略三次用户核对", "不要虚构不存在的镜头级中间资产"],
        "knowledge_source_ids": ["doc_design_chain"],
        "layout_template": "uml_gated_activity",
        "zones": [
            {"name": "center", "purpose": "单页链路主流程"},
            {"name": "bottom", "purpose": "Wan2.7 介入点说明"}
        ],
        "module_cards": [
            {"title": "单页链路", "zone": "center", "body": "用户目标 -> 页面契约 -> 用户核对 -> 页面视觉规格 -> 用户核对 -> 视觉蓝图 -> 用户核对 -> 页面静帧资产 -> 完整演示视频"},
            {"title": "Wan2.7 介入点", "zone": "bottom", "body": "Wan2.7 在页面静帧资产与完整演示视频阶段承担正式生成能力"}
        ],
        "required_labels": ["页面契约", "页面视觉规格", "视觉蓝图", "页面静帧资产", "完整演示视频", "用户核对"],
        "text_density": "high",
        "allowed_freestyle": "limited",
        "diagram_mode": "activity",
        "visual_goal": "让评委一眼看懂单页如何从需求进入最终视频。",
        "scene_title": "Scene 8：单页生成链路",
        "scene_goal": "解释单页生产链如何在控制成本的前提下逐步推进。",
        "subtitle_focus": "先蓝图手绘校验，再决定是否调用昂贵生成能力。"
    },
    {
        "page_number": 9,
        "page_id": "page_9_review_gates",
        "title": "状态推进与审阅闸门页",
        "role": "状态机页",
        "must_prove": "项目不是一把梭生成，而是带有状态推进、审阅检查点和阻塞机制的可控流程。",
        "required_objects": ["状态推进", "检查点1", "检查点2", "检查点3", "阻塞原因"],
        "required_relations": ["已进入策略阶段 -> 检查点1", "已进入蓝图阶段 -> 检查点2", "已进入视觉生成阶段 -> 检查点3"],
        "forbidden_distortions": ["不要只画单线流程", "不要漏掉阻塞原因"],
        "knowledge_source_ids": ["doc_design_chain", "official_source_findings"],
        "layout_template": "uml_state_gate",
        "zones": [
            {"name": "center", "purpose": "状态流转"},
            {"name": "right", "purpose": "阻塞原因说明"}
        ],
        "module_cards": [
            {"title": "状态流转", "zone": "center", "body": "已初始化 -> 已进入策略阶段 -> [检查点1] -> 已进入草稿阶段 -> 已进入蓝图阶段 -> [检查点2] -> 已进入视觉生成阶段 -> [检查点3] -> 已进入视频生成阶段 -> 已完成最终交付"},
            {"title": "阻塞原因", "zone": "right", "body": "术语定义未闭环 / 页面未完成用户核对 / 关键结构未完成官方资料核验"}
        ],
        "required_labels": ["检查点1", "检查点2", "检查点3", "阻塞原因"],
        "text_density": "high",
        "allowed_freestyle": "limited",
        "diagram_mode": "state_machine",
        "visual_goal": "强调项目的可控性和审阅机制。",
        "scene_title": "Scene 9：状态推进与审阅闸门",
        "scene_goal": "让评委看到项目如何控制风险与成本。",
        "subtitle_focus": "真正昂贵的生成动作只在前置检查通过后才允许发生。"
    },
    {
        "page_number": 10,
        "page_id": "page_10_deliverables",
        "title": "交付物与可复用 skill 页",
        "role": "交付矩阵页",
        "must_prove": "比赛最终证明物不是中间草稿，而是可展示成片、可复用项目 skill、说明文档与结构化产物。",
        "required_objects": ["最终视频", "可复用项目 skill", "说明文档", "结构化产物"],
        "required_relations": ["最终视频 -> 评委可见", "可复用项目 skill -> 团队可复用", "结构化产物 -> 团队可复用"],
        "forbidden_distortions": ["不要把交付物页误画成收束页", "不要只讲视频不讲工程沉淀"],
        "knowledge_source_ids": ["doc_design_competition", "doc_design_chain"],
        "layout_template": "delivery_matrix",
        "zones": [
            {"name": "top", "purpose": "交付主张"},
            {"name": "bottom", "purpose": "交付矩阵"}
        ],
        "module_cards": [
            {"title": "交付主张", "zone": "top", "body": "比赛最终证明物不是中间草稿，而是可展示成片与可复用 skill。"},
            {"title": "交付矩阵", "zone": "bottom", "body": "最终视频 / 可复用项目 skill / 说明文档 / 页面契约、页面视觉规格、视觉蓝图、任务元数据与状态记录"}
        ],
        "required_labels": ["最终视频", "可复用项目 skill", "说明文档", "结构化产物"],
        "text_density": "medium",
        "allowed_freestyle": "high",
        "diagram_mode": "matrix",
        "visual_goal": "把比赛交付与工程沉淀一起讲明白。",
        "scene_title": "Scene 10：交付矩阵",
        "scene_goal": "强调项目除了成片，还留下可复用的正式能力。",
        "subtitle_focus": "可展示成片与可复用项目 skill 同时构成比赛证明物。"
    },
    {
        "page_number": 11,
        "page_id": "page_11_closing",
        "title": "收束页",
        "role": "诗性收束页",
        "must_prove": "以前面的技术论证为基础，用整首诗完成收束，并把 Wan2.7 抬到时代参与者的生产能力位置。",
        "required_objects": ["整首诗", "Wan2.7", "参与进来", "时代主张"],
        "required_relations": ["整首诗 -> 时代主张", "Wan2.7 -> 参与进来"],
        "forbidden_distortions": ["不要提前在其他页面泄露整首诗", "不要把结尾写成说明页"],
        "knowledge_source_ids": ["sample_narrative", "sample_storyboard"],
        "layout_template": "closing_manifesto",
        "zones": [
            {"name": "hero", "purpose": "诗句与留白"},
            {"name": "footer", "purpose": "最终主张"}
        ],
        "module_cards": [
            {"title": "诗句", "zone": "hero", "body": PARTICIPANT_MANIFESTO},
            {"title": "最终主张", "zone": "footer", "body": "让 Wan2.7 真正进入创作、生产与沉淀的链路之中，我们交付的就不再只是作品，而是属于 AI 时代参与者的生产能力。"}
        ],
        "required_labels": ["Wan2.7", "参与者", "鲜衣怒马少年郎"],
        "text_density": "medium",
        "allowed_freestyle": "high",
        "diagram_mode": "closing",
        "visual_goal": "以前面的技术论证为底，用诗性表达完成收束。",
        "scene_title": "Scene 11：参与者宣言",
        "scene_goal": "把作品从技术论证落到时代参与感与参与者身份。",
        "subtitle_focus": "当 Wan2.7 真正进入链路，参与者才真正进入 AI 时代。"
    }
]

def now_iso(env_key: str | None = None) -> str:
    if env_key:
        import os

        value = os.environ.get(env_key)
        if value:
            return value
    return datetime.now().astimezone().isoformat(timespec="seconds")


def project_root_from(path: Path) -> Path:
    for candidate in [path, *path.parents]:
        if (candidate / "projects" / PROJECT_NAME).exists():
            return candidate
    raise FileNotFoundError("Unable to locate repository root")


def write_json(path: Path, payload: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")


def read_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def write_markdown(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content.rstrip() + "\n", encoding="utf-8")


def format_request_markdown(title: str, fields: dict[str, str]) -> str:
    lines = [f"# {title}", ""]
    for key, value in fields.items():
        lines.append(f"- {key}：{value}")
    lines.append("")
    return "\n".join(lines)


def parse_request_markdown(request_text: str, fields: list[str]) -> dict[str, str]:
    parsed = {field: "" for field in fields}
    for line in request_text.splitlines():
        cleaned = line.strip()
        for field in fields:
            prefix = f"- {field}："
            if cleaned.startswith(prefix):
                parsed[field] = cleaned.removeprefix(prefix).strip()
    return parsed


def task_output_paths() -> dict[str, str]:
    return {
        "knowledge_sources": "input/knowledge_sources.md",
        "research_context": "input/research_context.md",
        "strategy_request": "input/strategy_request.md",
        "strategy_brief": "input/strategy_brief.md",
        "technical_brief": "input/technical_brief.md",
        "narrative_brief": "input/narrative_brief.md",
        "page_roles": "output/review/page_roles.md",
        "page_contracts": "output/review/page_contracts.md",
        "knowledge_gaps": "output/review/knowledge_gaps.md",
        "draft_request": "input/draft_request.md",
        "copy_pack": "output/drafts/copy_pack.md",
        "page_visual_specs": "output/drafts/page_visual_specs.md",
        "diagram_blueprints": "output/drafts/diagram_blueprints.md",
        "storyboard_draft": "output/drafts/storyboard_draft.md",
        "knowledge_resolution": "output/drafts/knowledge_resolution.md",
        "review_checklist": "output/drafts/review_checklist.md",
        "visual_blueprint_request": "input/visual_blueprint_request.md",
        "visual_blueprint_bundle": "output/blueprints/visual_blueprint_bundle.json",
        "visual_generation_request": "input/visual_generation_request.md",
        "style_board": "output/visuals/style_board.md",
        "asset_manifest": "output/visuals/asset_manifest.json",
        "video_generation_request": "input/video_generation_request.md",
        "scene_plan": "output/video/scene_plan.md",
        "shot_list": "output/video/shot_list.md",
        "subtitles": "output/video/subtitles.srt",
        "voiceover_script": "output/video/voiceover_script.md",
        "final_video": "output/video/final_intro_video.mp4",
        "submission": "output/docs/submission.md",
        "showcase_summary": "output/docs/showcase_material_summary.md",
        "page_review_status": "review/page_review_status.json",
    }


def ensure_task_structure(task_dir: Path) -> None:
    for relative in (
        "input",
        "output/review",
        "output/drafts",
        "output/blueprints/pages",
        "output/blueprints/mcp_requests",
        "output/blueprints/mermaid",
        "output/blueprints/excalidraw",
        "output/blueprints/images",
        "output/visuals/pages",
        "output/visuals/images",
        "output/visuals/prompts",
        "output/video",
        "output/docs",
        "meta",
        "review",
    ):
        (task_dir / relative).mkdir(parents=True, exist_ok=True)


def build_manifest() -> dict[str, Any]:
    return {
        "project": PROJECT_NAME,
        "created_at": now_iso(),
        "updated_at": now_iso(),
        "status": "created",
        "outputs": [],
        "summary": "",
    }


def update_manifest(task_dir: Path, status: str, outputs: list[str] | None = None, summary: str | None = None) -> None:
    manifest_path = task_dir / "meta" / "task_manifest.json"
    manifest = read_json(manifest_path)
    manifest["status"] = status
    manifest["updated_at"] = now_iso()
    if outputs is not None:
        manifest["outputs"] = outputs
    if summary is not None:
        manifest["summary"] = summary
    write_json(manifest_path, manifest)


def build_gate(checks: list[str], status: str = "pending") -> dict[str, Any]:
    return {
        "status": status,
        "approved": False,
        "checks": checks,
        "artifacts": [],
        "approved_by": "",
        "approved_at": "",
    }


def ensure_gate_approved(task_dir: Path, gate_name: str) -> dict[str, Any]:
    gate_path = task_dir / "review" / f"{gate_name}.json"
    gate = read_json(gate_path)
    if not gate.get("approved"):
        raise ValueError(f"{gate_name} 未批准")
    return gate


def build_knowledge_sources_markdown(project_root: Path) -> str:
    lines = ["# knowledge_sources", ""]
    for source in KNOWLEDGE_SOURCES:
        lines.extend(
            [
                f"## {source.source_id}",
                f"- 标题：{source.title}",
                f"- 路径：{source.relative_path}",
                f"- 类型：{source.source_type}",
                f"- 摘要：{source.summary}",
                f"- 关联对象：{', '.join(source.objects)}",
                "",
            ]
        )
    return "\n".join(lines)


def build_knowledge_sources_json(project_root: Path) -> list[dict[str, Any]]:
    return [
        {
            "source_id": source.source_id,
            "title": source.title,
            "relative_path": source.relative_path,
            "source_type": source.source_type,
            "summary": source.summary,
            "objects": list(source.objects),
        }
        for source in KNOWLEDGE_SOURCES
    ]


def default_domain_terms_payload() -> dict[str, Any]:
    return {
        "project": PROJECT_NAME,
        "updated_at": now_iso(),
        "research_order": ["repo", "web", "user"],
        "terms": [
            {
                "term": "Wan2.7",
                "definition": "本项目中的多模态生成能力底座，用于承接图像与视频生成兑现。",
                "status": "needs_user_confirmation",
                "repo_source_ids": ["doc_project_prereseach", "sample_technical"],
                "external_sources": [],
                "user_confirmed": False,
                "notes": "项目口径优先于通用外部说法。",
            },
            {
                "term": "CoPaw",
                "definition": "本项目中的执行编排器，负责调度 skill 并承接人工审阅与资产回流。",
                "status": "needs_user_confirmation",
                "repo_source_ids": ["doc_project_prereseach", "official_source_findings"],
                "external_sources": [],
                "user_confirmed": False,
                "notes": "官方能力层与项目实现映射必须分开。",
            },
            {
                "term": "AgentScope",
                "definition": "CoPaw 的运行底座与框架，用于承载 agent 组织、消息协同与工具能力。",
                "status": "needs_user_confirmation",
                "repo_source_ids": ["doc_project_prereseach", "official_source_findings"],
                "external_sources": [],
                "user_confirmed": False,
                "notes": "不能把项目链路冒充成官方默认架构。",
            },
        ],
    }


def domain_terms_markdown_from_payload(payload: dict[str, Any]) -> str:
    lines = [
        "# domain_terms",
        "",
        "## 研究优先级",
        "- 1. 先查仓库内正式文档和样例",
        "- 2. 仓库不足时再补外部资料",
        "- 3. 仍不能唯一确定时必须向用户求证",
        "- 4. 未获确认前不得把候选定义画成正式页面事实",
        "",
    ]
    for term in payload["terms"]:
        lines.extend(
            [
                f"## {term['term']}",
                f"- 定义：{term['definition']}",
                f"- 状态：{term['status']}",
                f"- 仓库来源：{', '.join(term['repo_source_ids'])}",
                f"- 用户确认：{'yes' if term['user_confirmed'] else 'no'}",
                f"- 备注：{term['notes']}",
                "",
            ]
        )
    return "\n".join(lines)


def research_protocol_markdown() -> str:
    return "\n".join(
        [
            "# research_protocol",
            "",
            "- 优先顺序：仓库资料 -> 联网资料 -> 用户澄清",
            "- 研究目标：先确认项目内定义，再决定是否需要外部补充",
            "- 页面规则：每一页图都必须与用户核对，未核对页不得进入 blueprint / visual / video",
            "- 持久化要求：长期定义落到 projects/wan2.7_tech_narrative_engine/knowledge/，单次任务快照落到 artifacts/<task_dir>/",
            "",
        ]
    )


def ensure_project_knowledge_files(project_root: Path) -> dict[str, Path]:
    knowledge_dir = project_root / PROJECT_KNOWLEDGE_DIR
    knowledge_dir.mkdir(parents=True, exist_ok=True)
    domain_terms_json = knowledge_dir / "domain_terms.json"
    domain_terms_md = knowledge_dir / "domain_terms.md"
    research_protocol_md = knowledge_dir / "research_protocol.md"
    if not domain_terms_json.exists():
        write_json(domain_terms_json, default_domain_terms_payload())
    payload = read_json(domain_terms_json)
    if not domain_terms_md.exists():
        write_markdown(domain_terms_md, domain_terms_markdown_from_payload(payload))
    if not research_protocol_md.exists():
        write_markdown(research_protocol_md, research_protocol_markdown())
    return {
        "domain_terms_json": domain_terms_json,
        "domain_terms_md": domain_terms_md,
        "research_protocol_md": research_protocol_md,
    }


def build_research_context_markdown(project_root: Path) -> str:
    payload = read_json(ensure_project_knowledge_files(project_root)["domain_terms_json"])
    lines = [
        "# research_context",
        "",
        "## 当前规则",
        "- 先查仓库内材料，再视需要补外网，最后向用户求证。",
        "- 每页图都必须在正式出图前完成用户核对。",
        "",
        "## 当前术语基线",
    ]
    for term in payload["terms"]:
        lines.extend(
            [
                f"### {term['term']}",
                f"- 当前定义：{term['definition']}",
                f"- 状态：{term['status']}",
                f"- 用户确认：{'yes' if term['user_confirmed'] else 'no'}",
                f"- 仓库来源：{', '.join(term['repo_source_ids'])}",
                "",
            ]
        )
    return "\n".join(lines)


def build_default_page_review_status() -> list[dict[str, Any]]:
    return [
        {
            "page_id": page["page_id"],
            "page_number": page["page_number"],
            "page_title": page["title"],
            "status": "awaiting_user_confirmation",
            "approved": False,
            "requires_user_confirmation": True,
            "approved_by": "",
            "approved_at": "",
            "notes": "每一页图都必须先与用户核对后再进入下游生成。",
        }
        for page in PAGE_DEFINITIONS
    ]


def normalize_page_review_status(statuses: list[dict[str, Any]] | None) -> list[dict[str, Any]]:
    default_lookup = {item["page_id"]: item for item in build_default_page_review_status()}
    if not statuses:
        return list(default_lookup.values())
    normalized: list[dict[str, Any]] = []
    existing_lookup = {item.get("page_id"): item for item in statuses if item.get("page_id")}
    for page in PAGE_DEFINITIONS:
        page_id = page["page_id"]
        merged = dict(default_lookup[page_id])
        merged.update(existing_lookup.get(page_id, {}))
        normalized.append(merged)
    return normalized


def page_review_status_lookup(statuses: list[dict[str, Any]]) -> dict[str, dict[str, Any]]:
    return {item["page_id"]: item for item in normalize_page_review_status(statuses)}


def unresolved_page_review_items(statuses: list[dict[str, Any]]) -> list[dict[str, Any]]:
    return [item for item in normalize_page_review_status(statuses) if not item.get("approved")]


def build_page_roles_markdown() -> str:
    lines = ["# 页面职责表", ""]
    for page in PAGE_DEFINITIONS:
        lines.extend(
            [
                f"## 第 {page['page_number']} 页",
                f"- 页面编号：`{page['page_id']}`",
                f"- 页面名称：{page['title']}",
                f"- 页面定位：{page['role']}",
                f"- 页面目标：{page['must_prove']}",
                "",
            ]
        )
    return "\n".join(lines)


def build_page_contracts_markdown(page_review_statuses: list[dict[str, Any]] | None = None) -> str:
    status_lookup = page_review_status_lookup(page_review_statuses or [])
    lines = ["# page_contracts", ""]
    for page in PAGE_DEFINITIONS:
        review_status = status_lookup[page["page_id"]]
        gap = "none" if review_status.get("approved") else "用户尚未完成本页核对"
        lines.extend(
            [
                f"## {page['page_id']}",
                f"- page_number: {page['page_number']}",
                f"- page_title: {page['title']}",
                f"- page_role: {page['role']}",
                f"- must_prove: {page['must_prove']}",
                f"- required_objects: {', '.join(page['required_objects'])}",
                f"- required_relations: {'; '.join(page['required_relations'])}",
                f"- forbidden_distortions: {'; '.join(page['forbidden_distortions'])}",
                f"- knowledge_sources: {', '.join(page['knowledge_source_ids'])}",
                f"- confirmation_status: {review_status['status']}",
                f"- confirmed_by: {review_status.get('approved_by', '') or 'pending'}",
                f"- open_knowledge_gaps: {gap}",
                "",
            ]
        )
    return "\n".join(lines)


def build_knowledge_gaps_markdown(page_review_statuses: list[dict[str, Any]] | None = None) -> str:
    unresolved = unresolved_page_review_items(page_review_statuses or [])
    lines = [
        "# knowledge_gaps",
        "",
        "## 总体结论",
        "- 仓库内已有可供研究的正式材料，但找到来源不等于完成逐页确认。",
    ]
    if unresolved:
        lines.extend(["- 当前仍有逐页核对缺口，未完成用户确认前不得进入 blueprint / visual / video。", "", "## 阻塞页"])
        for item in unresolved:
            lines.append(f"- {item['page_id']}：{item['page_title']} 尚未完成用户核对")
        lines.append("")
        return "\n".join(lines)
    lines.extend(["- 当前逐页核对已完成，可继续进入下游。", "", "## 阻塞页", "- none", ""])
    return "\n".join(lines)


def build_page_visual_specs_markdown(page_review_statuses: list[dict[str, Any]] | None = None) -> str:
    status_lookup = page_review_status_lookup(page_review_statuses or [])
    lines = ["# page_visual_specs", ""]
    for page in PAGE_DEFINITIONS:
        review_status = status_lookup[page["page_id"]]
        lines.extend(
            [
                f"## {page['page_id']}",
                f"- page_title: {page['title']}",
                f"- layout_template: {page['layout_template']}",
                f"- diagram_mode: {page['diagram_mode']}",
                f"- text_density: {page['text_density']}",
                f"- allowed_freestyle: {page['allowed_freestyle']}",
                f"- zones: {', '.join(zone['name'] for zone in page['zones'])}",
                f"- required_labels: {', '.join(page['required_labels'])}",
                f"- module_cards: {', '.join(card['title'] for card in page['module_cards'])}",
                f"- visual_goal: {page['visual_goal']}",
                f"- confirmation_status: {review_status['status']}",
                f"- confirmed_by: {review_status.get('approved_by', '') or 'pending'}",
                "",
            ]
        )
    return "\n".join(lines)


def build_diagram_blueprints_markdown() -> str:
    lines = ["# diagram_blueprints", ""]
    for page in PAGE_DEFINITIONS:
        lines.extend(
            [
                f"## 第 {page['page_number']} 页",
                f"- 页面编号：{page['page_id']}",
                f"- 页面名称：{page['title']}",
                f"- 图例策略：{page['layout_template']}",
                f"- 节点：{', '.join(card['title'] for card in page['module_cards'])}",
                f"- 连线：{'; '.join(page['required_relations']) if page['required_relations'] else 'none'}",
                "",
            ]
        )
    return "\n".join(lines)


def build_storyboard_markdown() -> str:
    lines = ["# storyboard_draft", "", "## 视频总时长目标", "- 55-65 秒", ""]
    for page in select_video_pages():
        lines.extend(
            [
                f"## {page['scene_title']}",
                f"- 输入页面：{page['title']}",
                f"- 场景目标：{page['scene_goal']}",
                "- 过渡方式：fade",
                "- 时长：5 秒",
                f"- 字幕重点：{page['subtitle_focus']}",
                "",
            ]
        )
    return "\n".join(lines)


def build_knowledge_resolution_markdown() -> str:
    lines = ["# knowledge_resolution", "", "## 已关闭知识缺口", "- 所有页面契约均具备正式知识来源。", ""]
    for page in PAGE_DEFINITIONS:
        lines.extend([f"## {page['page_id']}", "- 状态：closed", "- 说明：允许进入 visual_blueprint 阶段。", ""])
    return "\n".join(lines)


def build_review_checklist_markdown() -> str:
    return "\n".join(
        [
            "# review_checklist",
            "",
            "- 第 3 页是否完整保留 Copaw 与 AgentScope 的层级、对象和连线。",
            "- 第 4 页是否清楚表达六个 skill 与正式产物、状态闸门的关系。",
            "- 第 7 页是否讲清 AI短剧工厂、三层能力、Copaw、AgentScope、六个项目 skill 与 Wan2.7 的主证据关系。",
            "- 第 8 页是否完整保留三次用户核对闸门。",
            "- 第 11 页是否只在收束页完整使用整首诗。",
            "",
        ]
    )


def build_style_board_markdown() -> str:
    return "\n".join(
        [
            "# style_board",
            "",
            "- 视觉方向：技术主导，叙事包裹。",
            "- 色彩：米白底，蓝金点题，辅以深灰结构线。",
            "- 字体策略：优先保证中文可读性，其次再做风格增强。",
            "- 图形策略：结构图优先信息层级和标签准确，不删关键文字。",
            "",
        ]
    )


def scene_plan_markdown(selected_pages: list[dict[str, Any]]) -> str:
    lines = ["# scene_plan", "", "- 总时长目标：55 秒左右", ""]
    for index, page in enumerate(selected_pages, start=1):
        lines.extend(
            [
                f"## scene_{index}",
                f"- page_id: {page['page_id']}",
                f"- title: {page['scene_title']}",
                f"- goal: {page['scene_goal']}",
                f"- subtitle_focus: {page['subtitle_focus']}",
                "",
            ]
        )
    return "\n".join(lines)


def shot_list_markdown(selected_pages: list[dict[str, Any]]) -> str:
    lines = ["# shot_list", ""]
    for index, page in enumerate(selected_pages, start=1):
        lines.extend(
            [
                f"## shot_{index}",
                f"- page_id: {page['page_id']}",
                "- duration_seconds: 5",
                "- transition: fade",
                f"- note: {page['visual_goal']}",
                "",
            ]
        )
    return "\n".join(lines)


def voiceover_markdown(selected_pages: list[dict[str, Any]]) -> str:
    lines = ["# voiceover_script", ""]
    for index, page in enumerate(selected_pages, start=1):
        lines.extend([f"## scene_{index}", page["subtitle_focus"], ""])
    return "\n".join(lines)


def subtitles_srt(selected_pages: list[dict[str, Any]]) -> str:
    lines: list[str] = []
    current_seconds = 0
    for index, page in enumerate(selected_pages, start=1):
        start = _format_srt_time(current_seconds)
        current_seconds += 5
        end = _format_srt_time(current_seconds)
        lines.extend([str(index), f"{start} --> {end}", page["subtitle_focus"], ""])
    return "\n".join(lines)


def build_submission_markdown(final_video_path: str, selected_pages: list[dict[str, Any]]) -> str:
    lines = [
        "# submission",
        "",
        "## 项目说明",
        "- 项目名称：Wan2.7 驱动的 Copaw 技术叙事引擎",
        "- 主线：Wan2.7 -> Copaw -> AgentScope -> 成为 AI 时代的参与者",
        f"- 最终视频：`{final_video_path}`",
        "",
        "## 关键页面",
    ]
    for page in selected_pages:
        lines.append(f"- {page['title']}：{page['must_prove']}")
    lines.extend(["", "## 收束宣言", f"- {PARTICIPANT_MANIFESTO}", "- 让 Wan2.7 真正进入创作、生产与沉淀的链路之中。", ""])
    return "\n".join(lines)


def build_showcase_summary_markdown(selected_pages: list[dict[str, Any]]) -> str:
    lines = ["# showcase_material_summary", "", "## 页面摘要"]
    for page in selected_pages:
        lines.append(f"- {page['title']}：{page['subtitle_focus']}")
    lines.extend(["", "## 收束", "- 当 Wan2.7 真正进入链路，参与者才真正进入 AI 时代。", ""])
    return "\n".join(lines)


def select_video_pages() -> list[dict[str, Any]]:
    page_numbers = {1, 2, 3, 4, 6, 8, 10, 11}
    return [page for page in PAGE_DEFINITIONS if page["page_number"] in page_numbers]


def page_lookup() -> dict[str, dict[str, Any]]:
    return {page["page_id"]: page for page in PAGE_DEFINITIONS}


def _format_srt_time(seconds: int) -> str:
    minutes, sec = divmod(seconds, 60)
    return f"00:{minutes:02d}:{sec:02d},000"
