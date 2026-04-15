import json
import subprocess
import textwrap
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parents[2]
FONT_REG = Path(r'C:\Windows\Fonts\msyh.ttc')
FONT_BOLD = Path(r'C:\Windows\Fonts\msyhbd.ttc')
FONT_FALLBACK = Path(r'C:\Windows\Fonts\simhei.ttf')

POEM = '湛湛长空，乱云飞度，吹尽繁红无数。正当年，紫金空铸，万里黄沙无觅处。沉江望极，狂涛乍起，惊飞一滩鸥鹭。鲜衣怒马少年郎，不负昭华行且知。'
CLOSING = '成为 AI 时代的参与者'

SLIDES = [
    ('wan27_opening', 'Wan2.7 首屏引导图', 'Wan2.7 作为多模态能力底座，开启整套技术叙事。'),
    ('copaw_product_intro', 'Copaw 产品介绍图', 'Copaw 提供聊天式自然语言入口、工作区编排和多 Agent 协作。'),
    ('copaw_architecture', 'Copaw 技术架构图', '用准确的模块、边界和流向建立技术主证据。'),
    ('wan27_copaw_execution_flow', 'Wan2.7 × Copaw 执行链路图', '明确 3 个松耦合 Skill 与人工审阅的执行链。'),
    ('role_collaboration', '角色协作分工图', '解释技术 Agent、叙事导演 Agent 和 3 个 Skill 的边界。'),
    ('agentscope_ecosystem', 'AgentScope 生态信息图', '从单点系统扩展到生态视角。'),
    ('value_mapping', '作品价值映射图', '将作品机制映射到创意性、完成度、商业潜力与市场表现。'),
    ('participant_manifesto_keyframe', '参与者宣言关键帧', '以诗句和宣言完成时代参与感的收束。'),
]


def font(size: int, bold: bool = False):
    path = FONT_BOLD if bold and FONT_BOLD.exists() else FONT_REG if FONT_REG.exists() else FONT_FALLBACK
    return ImageFont.truetype(str(path), size)


def wrap(text: str, width: int) -> str:
    return '\n'.join(textwrap.wrap(text, width=width, break_long_words=False, break_on_hyphens=False))


def canvas(title: str, subtitle: str, bg: str = '#F5F3EE'):
    img = Image.new('RGB', (1600, 900), bg)
    d = ImageDraw.Draw(img)
    d.rounded_rectangle((50, 40, 1550, 860), radius=28, outline='#1C2433', width=4)
    d.text((90, 80), title, fill='#18202D', font=font(42, bold=True))
    d.text((90, 145), subtitle, fill='#4A5567', font=font(22))
    return img, d


def box(d, xy, title, lines, fill='#FFFFFF', outline='#1C2433'):
    d.rounded_rectangle(xy, radius=18, fill=fill, outline=outline, width=3)
    x1, y1, x2, y2 = xy
    d.text((x1 + 18, y1 + 14), title, fill='#18202D', font=font(24, bold=True))
    y = y1 + 52
    for line in lines:
        d.text((x1 + 18, y), line, fill='#2A3345', font=font(18))
        y += 30


def arrow(d, start, end, fill='#1C2433', width=4):
    d.line([start, end], fill=fill, width=width)
    ex, ey = end
    d.polygon([(ex, ey), (ex - 14, ey - 8), (ex - 14, ey + 8)], fill=fill)


def render_opening(out):
    img, d = canvas('Copaw 驱动的 Wan2.7 技术叙事引擎', '以 Wan2.7 为能力入口，以 Copaw 为编排核心，组织技术叙事。', '#F0E7DA')
    chips = ['Wan2.7 文生图', 'Wan2.7 图生视频', 'Copaw 多 Agent 编排', 'AgentScope 生态表达']
    x = 90
    y = 240
    for chip in chips:
        w = d.textlength(chip, font=font(24)) + 48
        d.rounded_rectangle((x, y, x + w, y + 48), radius=18, fill='#FFFFFF', outline='#1C2433', width=2)
        d.text((x + 24, y + 10), chip, fill='#18202D', font=font(24))
        x += w + 20
    d.multiline_text((90, 360), wrap('让复杂 AI 系统与 Agent 生态，从结构清晰走向传播有力。', 18), fill='#18202D', font=font(42, bold=True), spacing=14)
    d.text((90, 700), '主线：Wan2.7 -> Copaw -> AgentScope -> 成为 AI 时代的参与者', fill='#4A5567', font=font(24))
    img.save(out)


def render_product_intro(out):
    img, d = canvas('Copaw 产品介绍图', 'Copaw 是聊天式自然语言入口，也是工作区级技能编排中枢。', '#E9F0F2')
    box(d, (90, 240, 500, 650), '用户价值', ['自然语言发起任务', '补充澄清控制在 1~2 轮', '面向项目工作区编排'], fill='#FFFFFF')
    box(d, (590, 240, 1010, 650), '核心能力', ['多 Agent 协作', '动态 Skill 装配', '任务目录归档', '结果回传'], fill='#FFFFFF')
    box(d, (1100, 240, 1510, 650), '本次作品角色', ['承接 Wan2.7 主题任务', '协调 Skill 1 / 2 / 3', '统一沉淀图文视频产物'], fill='#FFFFFF')
    img.save(out)


def render_architecture(out):
    img, d = canvas('Copaw 技术架构图', '技术主证据：输入、编排、Agent、Skill 与产物归档。', '#F5F7FA')
    box(d, (80, 250, 300, 370), '用户入口', ['自然语言请求'])
    box(d, (360, 250, 640, 370), 'Copaw 编排层', ['任务初判', '澄清', '任务目录'])
    box(d, (720, 180, 1020, 300), '技术 Agent', ['技术骨架', '硬约束'])
    box(d, (720, 330, 1020, 450), '叙事导演 Agent', ['叙事顺序', '风格收束'])
    box(d, (1100, 150, 1450, 260), 'Skill 1', ['文稿', '底稿', '分镜草案'])
    box(d, (1100, 300, 1450, 410), '人工审阅', ['review_gate.json'])
    box(d, (1100, 450, 1450, 560), 'Skill 2', ['8 张静态图'])
    box(d, (1100, 600, 1450, 710), 'Skill 3', ['视频成片', '提交文档'])
    box(d, (360, 520, 760, 700), '产物归档层', ['drafts/', 'images/', 'video/', 'docs/', 'meta/'])
    arrow(d, (300, 310), (360, 310))
    arrow(d, (640, 310), (720, 240))
    arrow(d, (640, 310), (720, 390))
    arrow(d, (1020, 240), (1100, 205))
    arrow(d, (1020, 390), (1100, 205))
    arrow(d, (1275, 260), (1275, 300))
    arrow(d, (1275, 410), (1275, 450))
    arrow(d, (1275, 560), (1275, 600))
    arrow(d, (1100, 655), (760, 610))
    img.save(out)


def render_execution_flow(out):
    img, d = canvas('Wan2.7 × Copaw 执行链路图', '3 个松耦合 Skill 与人工审阅，确保高成本调用可控。', '#F6F1F8')
    nodes = [
        '用户', 'Copaw', '技术 Agent', '叙事导演 Agent', 'Skill 1', '人工审阅', 'Skill 2', 'Skill 3', '产物'
    ]
    xs = [70, 220, 390, 610, 860, 1030, 1210, 1380, 1520]
    for i, node in enumerate(nodes):
        x = xs[i]
        d.rounded_rectangle((x, 360, x + (120 if i < 8 else 60), 440), radius=16, fill='#FFFFFF', outline='#1C2433', width=2)
        d.text((x + 12, 388), node, fill='#18202D', font=font(18, bold=True))
        if i < len(nodes) - 1:
            arrow(d, (x + (120 if i < 8 else 60), 400), (xs[i + 1], 400))
    d.text((1180, 250), '北京地域 wan2.7-image / wan2.7-image-pro', fill='#7B2CBF', font=font(22, bold=True))
    d.text((1360, 510), '北京地域 wan2.7-i2v', fill='#0F766E', font=font(22, bold=True))
    img.save(out)


def render_role_collaboration(out):
    img, d = canvas('角色协作分工图', '边界清楚，避免技术事实被叙事稀释。', '#EEF4EC')
    columns = [
        ('技术 Agent', ['定义技术骨架', '锁定硬约束']),
        ('叙事导演 Agent', ['组织表达顺序', '控制结尾收束']),
        ('Skill 1', ['文稿包', '结构底稿', '分镜草案']),
        ('Skill 2', ['静态图生成', '文字质检']),
        ('Skill 3', ['正式分镜', '视频成片', '交付文档']),
    ]
    x = 70
    for title, lines in columns:
        box(d, (x, 260, x + 270, 660), title, lines, fill='#FFFFFF')
        x += 295
    img.save(out)


def render_ecosystem(out):
    img, d = canvas('AgentScope 生态信息图', '从单点系统表达扩展到生态视角。', '#EFF3F8')
    box(d, (620, 320, 980, 500), 'AgentScope', ['生态核心对象', '承接 Agent 生态表达'], fill='#FFFFFF')
    around = [
        ((180, 180, 480, 300), 'Copaw', ['聊天入口', '工作区编排']),
        ((1120, 180, 1420, 300), 'Wan2.7', ['文生图', '图生视频']),
        ((180, 560, 480, 680), '开发者', ['布道', '演示', '复用']),
        ((1120, 560, 1420, 680), 'Agent 工作流', ['协作', '编排', '场景化']),
    ]
    for rect, title, lines in around:
        box(d, rect, title, lines, fill='#FFFFFF')
    arrow(d, (480, 240), (620, 390))
    arrow(d, (1120, 240), (980, 390))
    arrow(d, (480, 620), (620, 430))
    arrow(d, (1120, 620), (980, 430))
    img.save(out)


def render_value_mapping(out):
    img, d = canvas('作品价值映射图', '把作品机制映射到评审四维。', '#FBF7ED')
    grid = [
        ((100, 230, 740, 470), '创意性 30%', ['技术结构 + 时代叙事', '不是单次出图 Demo']),
        ((860, 230, 1500, 470), '完成度 25%', ['图、文、视频、文档闭环', '任务目录和元数据一致']),
        ((100, 520, 740, 760), '商业潜力 25%', ['AI 产品发布', '生态宣传', '教育传播']),
        ((860, 520, 1500, 760), '市场表现 20%', ['首屏对题', '中段讲结构', '结尾有记忆点']),
    ]
    for rect, title, lines in grid:
        box(d, rect, title, lines, fill='#FFFFFF')
    img.save(out)


def render_manifesto(out):
    img, d = canvas('参与者宣言关键帧', '以诗句和宣言完成作品收束。', '#1B1E2A')
    d.multiline_text((110, 220), wrap(POEM, 20), fill='#F4EDE1', font=font(34), spacing=18)
    d.text((110, 710), CLOSING, fill='#F8C146', font=font(42, bold=True))
    img.save(out)


def make_images(task_dir: Path):
    img_dir = task_dir / 'output' / 'images'
    img_dir.mkdir(parents=True, exist_ok=True)
    render_opening(img_dir / 'wan27_opening.png')
    render_product_intro(img_dir / 'copaw_product_intro.png')
    render_architecture(img_dir / 'copaw_architecture.png')
    render_execution_flow(img_dir / 'wan27_copaw_execution_flow.png')
    render_role_collaboration(img_dir / 'role_collaboration.png')
    render_ecosystem(img_dir / 'agentscope_ecosystem.png')
    render_value_mapping(img_dir / 'value_mapping.png')
    render_manifesto(img_dir / 'participant_manifesto_keyframe.png')


def make_docs(task_dir: Path):
    docs_dir = task_dir / 'output' / 'docs'
    video_dir = task_dir / 'output' / 'video'
    docs_dir.mkdir(parents=True, exist_ok=True)
    submission = f'''# Copaw 驱动的 Wan2.7 技术叙事引擎

## 作品简介

以 Wan2.7 为能力入口，以 Copaw 为编排核心，通过 3 个松耦合 Skill 将复杂 AI 系统与 Agent 生态转译为图文和视频叙事内容。

## 输出物

- 8 张最终静态图
- 1 支介绍视频
- 结尾诗句与“{CLOSING}”收束

## 技术链路

- Skill 1：文稿、结构底稿、分镜草案
- Skill 2：静态图生成
- Skill 3：视频成片与交付组装

## 视频路径

`{video_dir / 'final_intro_video.mp4'}`
'''
    (docs_dir / 'submission.md').write_text(submission, encoding='utf-8')
    showcase = '\n'.join([f'- {sid}: output/images/{sid}.png' for sid, _, _ in SLIDES])
    (docs_dir / 'showcase_material_summary.md').write_text('# Showcase Materials\n\n' + showcase + '\n', encoding='utf-8')


def make_video(task_dir: Path):
    img_dir = task_dir / 'output' / 'images'
    video_dir = task_dir / 'output' / 'video'
    video_dir.mkdir(parents=True, exist_ok=True)
    concat = video_dir / 'slides.txt'
    order = [sid for sid, _, _ in SLIDES]
    lines = []
    for sid in order[:-1]:
        lines.append(f"file '{(img_dir / (sid + '.png')).resolve().as_posix()}'")
        lines.append('duration 4')
    lines.append(f"file '{(img_dir / (order[-1] + '.png')).resolve().as_posix()}'")
    lines.append('duration 6')
    lines.append(f"file '{(img_dir / (order[-1] + '.png')).resolve().as_posix()}'")
    concat.write_text('\n'.join(lines), encoding='utf-8')
    out = video_dir / 'final_intro_video.mp4'
    cmd = [
        'ffmpeg', '-y', '-f', 'concat', '-safe', '0', '-i', str(concat),
        '-vf', 'fps=30,format=yuv420p', '-pix_fmt', 'yuv420p', str(out)
    ]
    subprocess.run(cmd, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)


def main(task_dir: str):
    task = Path(task_dir)
    make_images(task)
    make_video(task)
    make_docs(task)
    meta = task / 'meta'
    meta.mkdir(parents=True, exist_ok=True)
    (meta / 'final_local_render.json').write_text(json.dumps({'status': 'completed', 'images': [s[0] for s in SLIDES], 'video': 'output/video/final_intro_video.mp4'}, ensure_ascii=False, indent=2), encoding='utf-8')


if __name__ == '__main__':
    import sys
    main(sys.argv[1])
