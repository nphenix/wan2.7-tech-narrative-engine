const fs = require('fs');
const path = require('path');
const diagrams = require('./diagram_svgs.cjs');

const POEM = '湛湛长空，乱云飞度，吹尽繁红无数。正当年，紫金空铸，万里黄沙无觅处。沉江望极，狂涛乍起，惊飞一滩鸥鹭。鲜衣怒马少年郎，不负昭华行且知。';
const POEM_HTML = ['湛湛长空，乱云飞度，吹尽繁红无数。', '正当年，紫金空铸，万里黄沙无觅处。', '沉江望极，狂涛乍起，惊飞一滩鸥鹭。', '鲜衣怒马少年郎，不负昭华行且知。'].join('<br/>');
const CLOSING = '成为 AI 时代的参与者';

function loadPlaywright() {
  return require(path.join(__dirname, '..', '..', 'node', 'node_modules', 'playwright'));
}

function shell({ title, eyebrow, heading, dek, body, theme = 'paper', footerLeft = '', footerRight = '' }) {
  const themes = {
    paper: {
      bg: 'linear-gradient(135deg,#f7f1e5 0%,#f2ece3 35%,#e6eef7 100%)',
      panel: 'rgba(255,255,255,0.86)',
      ink: '#17202f',
      soft: '#56647a',
      line: 'rgba(23,32,47,0.12)',
      accent: '#bb7b2c',
      accentSoft: '#f4e1c6',
    },
    steel: {
      bg: 'linear-gradient(145deg,#f1f5f9 0%,#e8eef5 45%,#d6e3ef 100%)',
      panel: 'rgba(255,255,255,0.9)',
      ink: '#17202f',
      soft: '#526174',
      line: 'rgba(23,32,47,0.12)',
      accent: '#22577a',
      accentSoft: '#d7eaf5',
    },
    moss: {
      bg: 'linear-gradient(145deg,#edf4ef 0%,#e4efe6 40%,#d6e7dc 100%)',
      panel: 'rgba(253,255,253,0.9)',
      ink: '#16231d',
      soft: '#56665f',
      line: 'rgba(22,35,29,0.12)',
      accent: '#2c6a4b',
      accentSoft: '#d8eadf',
    },
    dusk: {
      bg: 'linear-gradient(135deg,#0f1624 0%,#1d2840 55%,#382d47 100%)',
      panel: 'rgba(18,25,39,0.78)',
      ink: '#f4efe6',
      soft: '#cdbfa9',
      line: 'rgba(244,239,230,0.1)',
      accent: '#f0b14a',
      accentSoft: 'rgba(240,177,74,0.16)',
    },
  };
  const t = themes[theme];
  return `<!doctype html>
<html lang="zh-CN">
<head>
  <meta charset="utf-8" />
  <title>${title}</title>
  <style>
    :root {
      --bg: ${t.bg};
      --panel: ${t.panel};
      --ink: ${t.ink};
      --soft: ${t.soft};
      --line: ${t.line};
      --accent: ${t.accent};
      --accent-soft: ${t.accentSoft};
    }
    * { box-sizing: border-box; }
    body {
      margin: 0;
      width: 1600px;
      height: 900px;
      overflow: hidden;
      font-family: "Microsoft YaHei UI", "Microsoft YaHei", "PingFang SC", sans-serif;
      color: var(--ink);
      background: var(--bg);
    }
    .noise {
      position: absolute;
      inset: 0;
      opacity: .06;
      background-image:
        radial-gradient(circle at 20% 20%, rgba(255,255,255,.9), transparent 30%),
        radial-gradient(circle at 80% 10%, rgba(255,255,255,.75), transparent 32%),
        radial-gradient(circle at 70% 80%, rgba(255,255,255,.5), transparent 26%);
    }
    .frame {
      position: relative;
      width: 1600px;
      height: 900px;
      padding: 28px;
    }
    .panel {
      position: relative;
      width: 100%;
      height: 100%;
      border-radius: 32px;
      background: var(--panel);
      border: 1px solid var(--line);
      box-shadow: 0 18px 60px rgba(15,23,42,.10);
      overflow: hidden;
    }
    .panel::before {
      content: "";
      position: absolute;
      inset: 0;
      background:
        linear-gradient(180deg, rgba(255,255,255,.4), transparent 180px),
        radial-gradient(circle at top right, rgba(255,255,255,.45), transparent 30%);
      pointer-events: none;
    }
    .chrome {
      position: absolute;
      inset: 0;
      padding: 34px 36px 76px;
    }
    .eyebrow {
      display: inline-flex;
      align-items: center;
      gap: 10px;
      padding: 10px 18px;
      border-radius: 999px;
      background: rgba(255,255,255,.7);
      border: 1px solid var(--line);
      font-size: 20px;
      font-weight: 800;
    }
    .eyebrow::before {
      content: "";
      width: 10px;
      height: 10px;
      border-radius: 999px;
      background: var(--accent);
      box-shadow: 0 0 0 6px var(--accent-soft);
    }
    h1 {
      margin: 20px 0 10px;
      font-size: 60px;
      line-height: 1.08;
      letter-spacing: -0.04em;
    }
    .dek {
      max-width: 1220px;
      margin: 0;
      color: var(--soft);
      font-size: 18px;
      line-height: 1.65;
    }
    .footer {
      position: absolute;
      left: 36px;
      right: 36px;
      bottom: 24px;
      display: flex;
      align-items: center;
      justify-content: space-between;
      color: var(--soft);
      font-size: 18px;
    }
    .footer strong { color: var(--accent); font-weight: 900; }
    .pill-row { display: flex; gap: 16px; flex-wrap: wrap; margin-top: 28px; }
    .pill {
      padding: 14px 20px;
      border-radius: 999px;
      background: rgba(255,255,255,.75);
      border: 1px solid var(--line);
      font-size: 18px;
      font-weight: 800;
      box-shadow: 0 8px 24px rgba(15,23,42,.05);
    }
    .grid-2 { display: grid; grid-template-columns: repeat(2, minmax(0,1fr)); gap: 22px; margin-top: 28px; }
    .grid-4 { display: grid; grid-template-columns: repeat(4, minmax(0,1fr)); gap: 18px; margin-top: 26px; }
    .card {
      position: relative;
      background: rgba(255,255,255,.82);
      border: 1px solid var(--line);
      border-radius: 26px;
      padding: 24px 24px 22px;
      box-shadow: 0 16px 44px rgba(15,23,42,.06);
    }
    .card::after {
      content: "";
      position: absolute;
      inset: 0 auto auto 0;
      width: 100%;
      height: 4px;
      background: linear-gradient(90deg, var(--accent), transparent);
      border-top-left-radius: 26px;
      border-top-right-radius: 26px;
    }
    .card h3, .card h4 { margin: 0 0 12px; font-size: 34px; line-height: 1.2; }
    .card p, .card li { margin: 0; color: var(--soft); font-size: 21px; line-height: 1.55; }
    .card ul { margin: 0; padding-left: 24px; }
    .split {
      display: grid;
      grid-template-columns: 1.18fr .82fr;
      gap: 24px;
      margin-top: 28px;
      min-height: 430px;
    }
    .hero {
      display: flex;
      flex-direction: column;
      justify-content: space-between;
      padding: 10px 6px 0 0;
    }
    .hero-quote {
      font-size: 50px;
      font-weight: 900;
      line-height: 1.08;
      letter-spacing: -0.04em;
      max-width: 760px;
    }
    .accent-stack {
      display: grid;
      gap: 18px;
      align-content: start;
    }
    .accent-box {
      padding: 22px;
      border-radius: 24px;
      background: linear-gradient(180deg, rgba(255,255,255,.92), rgba(255,255,255,.7));
      border: 1px solid var(--line);
      box-shadow: 0 14px 36px rgba(15,23,42,.08);
    }
    .accent-box h3 { margin: 0 0 12px; font-size: 26px; }
    .accent-box p { margin: 0; color: var(--soft); font-size: 19px; line-height: 1.55; }
    .metric {
      display: flex;
      align-items: baseline;
      gap: 10px;
      margin-bottom: 10px;
    }
    .metric .num { font-size: 42px; font-weight: 900; color: var(--accent); }
    .metric .label { font-size: 18px; font-weight: 800; color: var(--soft); }
    .diagram-shell {
      position: relative;
      margin-top: 26px;
      height: 540px;
      border-radius: 30px;
      background: linear-gradient(180deg, rgba(255,255,255,.8), rgba(255,255,255,.62));
      border: 1px solid var(--line);
      box-shadow: inset 0 1px 0 rgba(255,255,255,.7), 0 16px 44px rgba(15,23,42,.06);
      overflow: hidden;
    }
    .lane {
      position: absolute;
      top: 18px;
      bottom: 18px;
      border-radius: 24px;
      background: rgba(255,255,255,.42);
      border: 1px dashed rgba(23,32,47,.10);
    }
    .lane-head {
      position: absolute;
      left: 14px;
      top: 12px;
      padding: 8px 12px;
      border-radius: 14px;
      font-size: 16px;
      font-weight: 800;
      background: var(--accent-soft);
      color: var(--accent);
    }
    .node {
      position: absolute;
      padding: 18px 18px 16px;
      border-radius: 22px;
      background: rgba(255,255,255,.94);
      border: 1px solid var(--line);
      box-shadow: 0 12px 28px rgba(15,23,42,.08);
    }
    .node h4 {
      margin: 0 0 8px;
      font-size: 20px;
      line-height: 1.2;
    }
    .node p {
      margin: 0;
      color: var(--soft);
      font-size: 16px;
      line-height: 1.4;
      white-space: pre-line;
    }
    .mini {
      position: absolute;
      padding: 10px 14px;
      border-radius: 16px;
      font-size: 16px;
      font-weight: 800;
      background: rgba(255,255,255,.9);
      border: 1px solid var(--line);
      color: var(--accent);
    }
    .scenario-row {
      display: grid;
      grid-template-columns: repeat(4, minmax(0,1fr));
      gap: 16px;
      margin-top: 18px;
    }
    .scenario {
      padding: 16px 18px;
      border-radius: 20px;
      background: rgba(255,255,255,.72);
      border: 1px solid var(--line);
      font-size: 18px;
      font-weight: 800;
      text-align: center;
    }
    .diagram-host { display: grid; place-items: center; padding: 18px; }
    .diagram-host svg { width: 100%; height: 100%; }
    .poem-wrap {
      display: grid;
      place-items: center;
      height: calc(100% - 190px);
      padding: 0 90px;
      text-align: center;
    }
    .poem {
      margin: 0;
      max-width: 1160px;
      font-size: 36px;
      line-height: 1.92;
      letter-spacing: .06em;
      color: #f4efe6;
    }
    .closing {
      position: absolute;
      left: 36px;
      right: 36px;
      bottom: 38px;
      display: flex;
      justify-content: space-between;
      align-items: end;
    }
    .closing-main {
      font-size: 56px;
      font-weight: 900;
      color: var(--accent);
      letter-spacing: -0.03em;
    }
    .closing-note {
      max-width: 420px;
      text-align: right;
      color: var(--soft);
      font-size: 18px;
      line-height: 1.55;
    }
  </style>
</head>
<body>
  <div class="frame">
    <div class="noise"></div>
    <div class="panel">
      <div class="chrome">
        <div class="eyebrow">${eyebrow}</div>
        <h1>${heading}</h1>
        <p class="dek">${dek}</p>
        ${body}
        <div class="footer"><div>${footerLeft}</div><div><strong>${footerRight}</strong></div></div>
      </div>
    </div>
  </div>
</body>
</html>`;
}

function openingSlide() {
  return shell({
    title: 'Wan2.7 首屏引导图',
    eyebrow: 'Wan2.7 多模态内容引擎',
    heading: '让复杂技术主题变成可理解、可传播的视觉叙事',
    dek: 'Wan2.7 把文生图、图像编辑和图生视频放在同一条能力链上，让产品介绍、架构讲解和生态表达更容易进入多模态传播。',
    theme: 'paper',
    footerLeft: 'Wan2.7 / CoPaw / AgentScope',
    footerRight: '文生图 / 图像编辑 / 图生视频',
    body: `
      <div class="pill-row">
        <div class="pill">Wan2.7 文生图</div>
        <div class="pill">Wan2.7 图像编辑</div>
        <div class="pill">Wan2.7 图生视频</div>
        <div class="pill">多模态内容生产</div>
      </div>
      <div class="split">
        <div class="hero">
          <div class="hero-quote">从一个主题出发，直接生成能被看懂、被记住、被传播的表达。</div>
          <div class="card" style="max-width:700px">
            <h3>为什么这套分工重要</h3>
            <p>Wan2.7 不只是用来生成一张好看的图，它是把产品介绍、架构讲解、生态概览和短视频串到同一创作链路上的能力底座。</p>
          </div>
        </div>
        <div class="accent-stack">
          <div class="accent-box">
            <div class="metric"><span class="num">01</span><span class="label">图像入口</span></div>
            <p>先用主视觉和信息图建立第一眼认知。</p>
          </div>
          <div class="accent-box">
            <div class="metric"><span class="num">02</span><span class="label">结构清晰</span></div>
            <p>把复杂系统拆成可阅读的层次，让观众真正看懂。</p>
          </div>
          <div class="accent-box">
            <div class="metric"><span class="num">03</span><span class="label">视频叙事</span></div>
            <p>再把图像推进成视频，让内容从说明走向叙事。</p>
          </div>
        </div>
      </div>`,
  });
}

function diagramMarkup(filename) {
  const item = diagrams.createDiagramSvgs().find((entry) => entry.filename === filename);
  if (!item) {
    throw new Error(`missing diagram svg for ${filename}`);
  }
  return item.svg;
}

function productIntroSlide() {
  return shell({
    title: 'CoPaw 产品介绍图',
    eyebrow: 'AI 个人助理 / 多智能体协作',
    heading: 'CoPaw：懂你所需，伴你左右',
    dek: 'CoPaw 是面向真实工作场景的 AI 个人助理，支持本地或云端部署、多端接入、Skills 扩展、多智能体协作与多层安全防护。',
    theme: 'steel',
    footerLeft: '多端接入 / Skills / 多智能体 / 安全',
    footerRight: '你的 AI 个人助理',
    body: `
      <div class="split" style="grid-template-columns: 1.06fr .94fr; min-height:470px;">
        <div class="card" style="padding:28px 28px 24px; display:flex; flex-direction:column; justify-content:space-between;">
          <div>
            <h3>从聊天入口走向生产力入口</h3>
            <p style="font-size:24px;line-height:1.7">用户可以从自然语言对话开始，CoPaw 负责组织 workspace、加载合适的 Skills、协调多个 agent，并把图片、视频、文档和过程记录放在同一条任务链中。它不是单一机器人，而是可持续扩展的助理运行时。</p>
          </div>
          <div class="scenario-row">
            <div class="scenario">本地 / 云端部署</div>
            <div class="scenario">多端接入</div>
            <div class="scenario">Skills 扩展</div>
            <div class="scenario">结果可追溯</div>
          </div>
        </div>
        <div class="accent-stack">
          <div class="accent-box"><h3>由你掌控</h3><p>记忆、个性化和运行方式都在用户手中，可根据场景选择本地或云端部署。</p></div>
          <div class="accent-box"><h3>能力通过 Skills 持续扩展</h3><p>定时任务、文件处理、浏览器操作和自定义工作流都可以被封装成 Skills，按需加载。</p></div>
          <div class="accent-box"><h3>复杂任务可以协作</h3><p>多个独立 agent 可以在同一 workspace 内分担不同职责，让多步骤生产任务变得可控。</p></div>
        </div>
      </div>`,
  });
}

function architectureSlide() {
  return shell({
    title: 'CoPaw 架构图',
    eyebrow: '结构视图',
    heading: 'CoPaw 如何把聊天入口变成可运行的 AI 工作区',
    dek: '结构图只负责把关系讲清楚，终版美化交给草稿技能之后的 Wan2.7 流程。',
    theme: 'steel',
    footerLeft: '工作区 / 执行器 / 技能 / 多智能体',
    footerRight: '组件视图',
    body: `
      <div class="split" style="grid-template-columns:1.16fr .44fr; min-height:620px; gap:20px;">
        <div class="diagram-shell diagram-host" style="height:600px; margin-top:20px; background:linear-gradient(180deg, rgba(255,255,255,.88), rgba(255,255,255,.76));">${diagramMarkup('copaw_architecture.svg')}</div>
        <div class="accent-stack" style="margin-top:20px; gap:14px;">
          <div class="accent-box"><h3>入口</h3><p>工作区是从聊天入口进入可执行工作区的框架锚点。</p></div>
          <div class="accent-box"><h3>运行时</h3><p>执行器、记忆上下文与调度分别对应执行、状态与跟踪。</p></div>
          <div class="accent-box"><h3>扩展</h3><p>CoPaw 负责编排与协调，Wan2.7 不在这张图里承担美化职责。</p></div>
        </div>
      </div>`,
  });
}function executionFlowSlide() {
  return shell({
    title: 'Wan2.7 \u00d7 CoPaw \u6267\u884c\u94fe\u8def\u56fe',
    eyebrow: '\u6d41\u7a0b\u89c6\u56fe',
    heading: 'CoPaw \u8d1f\u8d23\u7ec4\u7ec7\u4e0e\u5b9a\u7a3f\uff0cWan2.7 \u8d1f\u8d23\u6b63\u5f0f\u751f\u6210',
    dek: '\u5148\u628a\u4e8b\u60c5\u8bb2\u6e05\u695a\uff0c\u518d\u8fdb\u5165 Wan2.7 \u7684\u56fe\u50cf\u548c\u89c6\u9891\u9636\u6bb5\u3002',
    theme: 'moss',
    footerLeft: '\u5317\u4eac\u5730\u57df: wan2.7-image / wan2.7-image-pro / wan2.7-i2v',
    footerRight: '\u6267\u884c\u94fe\u8def\u89c6\u56fe',
    body: `
      <div class="split" style="grid-template-columns:1.16fr .44fr; min-height:620px; gap:20px;">
        <div class="diagram-shell diagram-host" style="height:600px; margin-top:20px; background:linear-gradient(180deg, rgba(255,255,255,.88), rgba(255,255,255,.76));">${diagramMarkup('wan27_copaw_execution_flow.svg')}</div>
        <div class="accent-stack" style="margin-top:20px; gap:14px;">
          <div class="accent-box"><h3>CoPaw</h3><p>\u8d1f\u8d23\u4e3b\u9898\u7f16\u6392\u3001\u6280\u672f\u4e8b\u5b9e\u5bf9\u9f50\u548c\u8349\u7a3f\u5b9a\u7a3f\u3002</p></div>
          <div class="accent-box"><h3>Wan2.7</h3><p>\u8d1f\u8d23\u6839\u636e\u5df2\u901a\u8fc7\u5ba1\u9605\u7684\u8f93\u5165\u751f\u6210\u56fe\u50cf\u4e0e\u89c6\u9891\u3002</p></div>
          <div class="accent-box"><h3>\u95f8\u95e8</h3><p>\u4eba\u5de5\u5ba1\u9605\u662f\u628a\u4e24\u8005\u804c\u8d23\u5206\u5f00\u7684\u6b63\u5f0f\u754c\u7ebf\u3002</p></div>
        </div>
      </div>`,
  });
}

function roleSlide() {
  return shell({
    title: 'CoPaw 与 Wan2.7 分工图',
    eyebrow: '分工视图',
    heading: 'CoPaw 与 Wan2.7 的分工必须画清楚',
    dek: '前者负责把事情讲清楚，后者负责图像与视频的正式生成。',
    theme: 'moss',
    footerLeft: '技术事实不能被叙事改写',
    footerRight: '角色分工视图',
    body: `
      <div class="split" style="grid-template-columns:1.16fr .44fr; min-height:620px; gap:20px;">
        <div class="diagram-shell diagram-host" style="height:600px; margin-top:20px; background:linear-gradient(180deg, rgba(255,255,255,.88), rgba(255,255,255,.76));">${diagramMarkup('role_collaboration.svg')}</div>
        <div class="accent-stack" style="margin-top:20px; gap:14px;">
          <div class="accent-box"><h3>CoPaw 职责</h3><p>技术角色、叙事角色和草稿技能都服务于“讲清楚”。</p></div>
          <div class="accent-box"><h3>Wan2.7 职责</h3><p>文稿包和镜头稿审定后，再进入图像与视频的正式生成。</p></div>
          <div class="accent-box"><h3>交接要点</h3><p>交给 Wan2.7 的不是想法，而是已经经过审校的标准输入。</p></div>
        </div>
      </div>`,
  });
}function ecosystemSlide() {
  return shell({
    title: 'AgentScope 生态信息图',
    eyebrow: '生态视图',
    heading: 'AgentScope 生态还可以补入更多官方开源项目',
    dek: '参考 AgentScope-AI 官方 GitHub 组织，当前页面除主框架外补入 Studio、Runtime、agentscope-bricks、agentscope-samples 与 agentscope-java。',
    theme: 'steel',
    footerLeft: 'AgentScope 官方仓库簇',
    footerRight: '生态上下文视图',
    body: `
      <div class="split" style="grid-template-columns:1.16fr .44fr; min-height:620px; gap:20px;">
        <div class="diagram-shell diagram-host" style="height:600px; margin-top:20px; background:linear-gradient(180deg, rgba(255,255,255,.88), rgba(255,255,255,.76));">${diagramMarkup('agentscope_ecosystem.svg')}</div>
        <div class="accent-stack" style="margin-top:20px; gap:14px;">
          <div class="accent-box"><h3>核心</h3><p>AgentScope 是主框架，连接 CoPaw、HiClaw 与 Wan2.7 这些当前叙事里的实际对象。</p></div>
          <div class="accent-box"><h3>开发与部署</h3><p>AgentScope Studio 对应可视化开发，AgentScope Runtime 对应运行与部署。</p></div>
          <div class="accent-box"><h3>可补生态</h3><p>agentscope-bricks、agentscope-samples 与 agentscope-java 更适合补充组件层、样例层和多语言入口。</p></div>
        </div>
      </div>`,
  });
}function valueSlide() {
  return shell({
    title: '价值映射图',
    eyebrow: '价值映射',
    heading: '这套链路的价值不止在生成，更在于讲清楚再放大传播',
    dek: '先把结构、流程和角色关系讲明白，再把昂贵生成放到正确阶段，整条链路才真正可复用。',
    theme: 'paper',
    footerLeft: '产品发布 / 技术布道 / 生态传播 / 活动物料',
    footerRight: '结构价值 + 传播价值',
    body: `
      <div class="grid-2" style="margin-top:34px;">
        <div class="card"><div class="metric"><span class="num">01</span><span class="label">讲清楚</span></div><p>架构图、执行链路图和生态图把复杂系统拆成可理解的认知层。</p></div>
        <div class="card"><div class="metric"><span class="num">02</span><span class="label">做得更快</span></div><p>文稿、底稿、静态图和视频分阶段生成，让贵调用发生在草案已经正确之后。</p></div>
        <div class="card"><div class="metric"><span class="num">03</span><span class="label">可安全复用</span></div><p>技能围绕任务目录协议组织，替换一套资料，就能生成新的产品故事。</p></div>
        <div class="card"><div class="metric"><span class="num">04</span><span class="label">更容易传播</span></div><p>从首屏主视觉到结尾收束，产出不只是资料，更是带有节奏和记忆点的传播内容。</p></div>
      </div>
      <div class="scenario-row" style="margin-top:24px; grid-template-columns: repeat(4, minmax(0,1fr));">
        <div class="scenario">AI 产品发布</div>
        <div class="scenario">智能体生态传播</div>
        <div class="scenario">技术教育传播</div>
        <div class="scenario">活动物料生成</div>
      </div>`,
  });
}function manifestoSlide() {
  return shell({
    title: '收束关键帧',
    eyebrow: '尾声',
    heading: '当结构被讲清楚，叙事也就自然向外展开',
    dek: '从 Wan2.7 的生成能力，到 CoPaw 的编排机制，再到 AgentScope 的生态视角，最后只需要一个平缓的落点。',
    theme: 'dusk',
    footerLeft: 'Wan2.7 / CoPaw / AgentScope',
    footerRight: '自然收束',
    body: `
      <div class="poem-wrap" style="height:calc(100% - 210px); padding:0 120px 40px;">
        <p class="poem" style="font-size:31px; line-height:1.92; max-width:1180px;">${POEM_HTML}</p>
      </div>
      <div class="closing" style="bottom:56px; align-items:flex-start;">
        <div class="closing-main" style="font-size:34px; line-height:1.52; max-width:760px; color:#f4efe6;"></div>
        <div class="closing-note" style="max-width:420px; text-align:right; font-size:20px; line-height:1.76;">真正有力量的技术传播，不止是展示能力，更是邀请人走进能力背后的时代。</div>
      </div>`,
  });
}function createSlides() {
  return [
    { filename: 'wan27_opening.png', htmlName: 'wan27_opening.html', html: openingSlide() },
    { filename: 'copaw_product_intro.png', htmlName: 'copaw_product_intro.html', html: productIntroSlide() },
    { filename: 'copaw_architecture.png', htmlName: 'copaw_architecture.html', html: architectureSlide() },
    { filename: 'wan27_copaw_execution_flow.png', htmlName: 'wan27_copaw_execution_flow.html', html: executionFlowSlide() },
    { filename: 'role_collaboration.png', htmlName: 'role_collaboration.html', html: roleSlide() },
    { filename: 'agentscope_ecosystem.png', htmlName: 'agentscope_ecosystem.html', html: ecosystemSlide() },
    { filename: 'value_mapping.png', htmlName: 'value_mapping.html', html: valueSlide() },
    { filename: 'participant_manifesto_keyframe.png', htmlName: 'participant_manifesto_keyframe.html', html: manifestoSlide() },
  ];
}

async function writeHtmlPreviews(taskDir) {
  await diagrams.writeDiagramSvgs(taskDir);
  const htmlDir = path.join(taskDir, 'output', 'html');
  fs.mkdirSync(htmlDir, { recursive: true });
  const slides = createSlides();
  const files = [];
  for (const slide of slides) {
    const filePath = path.join(htmlDir, slide.htmlName);
    fs.writeFileSync(filePath, slide.html, 'utf8');
    files.push(filePath);
  }
  return files;
}

async function render(taskDir) {
  const { chromium } = loadPlaywright();
  const slides = createSlides();
  await diagrams.writeDiagramSvgs(taskDir);
  await writeHtmlPreviews(taskDir);
  const outDir = path.join(taskDir, 'output', 'images');
  fs.mkdirSync(outDir, { recursive: true });
  const browser = await chromium.launch({ headless: true });
  const page = await browser.newPage({ viewport: { width: 1600, height: 900 }, deviceScaleFactor: 2 });
  for (const slide of slides) {
    await page.setContent(slide.html, { waitUntil: 'load' });
    await page.screenshot({ path: path.join(outDir, slide.filename) });
  }
  await browser.close();
}

module.exports = {
  createSlides,
  createDiagramSvgs: diagrams.createDiagramSvgs,
  writeDiagramSvgs: diagrams.writeDiagramSvgs,
  writeHtmlPreviews,
  render,
};

if (require.main === module) {
  render(process.argv[2]).catch((error) => {
    console.error(error);
    process.exit(1);
  });
}
























