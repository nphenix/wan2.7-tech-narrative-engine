const fs = require('fs');
const path = require('path');

const SVG_DIR = path.join(__dirname, 'lightweight_svgs');
const FILENAMES = [
  'copaw_architecture.svg',
  'wan27_copaw_execution_flow.svg',
  'role_collaboration.svg',
  'agentscope_ecosystem.svg',
];

const COLORS = {
  bg: '#f8f7f2',
  ink: '#1f2937',
  soft: '#5b6777',
  line: '#94a3b8',
  blue: '#3a6ea5',
  blueFill: '#eaf2fb',
  teal: '#2f7f73',
  tealFill: '#e7f6f2',
  amber: '#b7791f',
  amberFill: '#fff4de',
  rose: '#b8566d',
  roseFill: '#fdecef',
};

function ensureDir(dirPath) {
  fs.mkdirSync(dirPath, { recursive: true });
}

function escapeXml(value) {
  return String(value)
    .replace(/&/g, '&amp;')
    .replace(/</g, '&lt;')
    .replace(/>/g, '&gt;')
    .replace(/"/g, '&quot;')
    .replace(/'/g, '&apos;');
}

function svgShell({ width = 1200, height = 520, content }) {
  return `<?xml version="1.0" encoding="UTF-8"?>
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 ${width} ${height}" width="${width}" height="${height}" data-source="lightweight-diagram">
  <!-- svg-source:lightweight -->
  <defs>
    <marker id="arrow-blue" markerWidth="10" markerHeight="10" refX="8" refY="5" orient="auto">
      <path d="M0,0 L10,5 L0,10 z" fill="${COLORS.blue}" />
    </marker>
    <marker id="arrow-teal" markerWidth="10" markerHeight="10" refX="8" refY="5" orient="auto">
      <path d="M0,0 L10,5 L0,10 z" fill="${COLORS.teal}" />
    </marker>
    <marker id="arrow-amber" markerWidth="10" markerHeight="10" refX="8" refY="5" orient="auto">
      <path d="M0,0 L10,5 L0,10 z" fill="${COLORS.amber}" />
    </marker>
    <marker id="arrow-rose" markerWidth="10" markerHeight="10" refX="8" refY="5" orient="auto">
      <path d="M0,0 L10,5 L0,10 z" fill="${COLORS.rose}" />
    </marker>
    <marker id="arrow-soft" markerWidth="10" markerHeight="10" refX="8" refY="5" orient="auto">
      <path d="M0,0 L10,5 L0,10 z" fill="${COLORS.soft}" />
    </marker>
  </defs>
  <rect width="100%" height="100%" rx="28" fill="${COLORS.bg}" />
  ${content}
</svg>`;
}

function textBlock(x, y, lines, { size = 20, weight = 700, fill = COLORS.ink, lineHeight = 1.28, align = 'middle' } = {}) {
  const firstY = y - ((lines.length - 1) * size * lineHeight) / 2;
  return lines
    .map((line, index) => {
      const yy = firstY + index * size * lineHeight;
      return '<text x="' + x + '" y="' + yy + '" fill="' + fill + '" font-family="Microsoft YaHei UI, Microsoft YaHei, PingFang SC, sans-serif" font-size="' + size + '" font-weight="' + weight + '" text-anchor="' + align + '" dominant-baseline="middle">' + escapeXml(line) + '</text>';
    })
    .join('\n');
}

function box(x, y, width, height, lines, opts = {}) {
  const stroke = opts.stroke || COLORS.line;
  const fill = opts.fill || '#ffffff';
  const radius = opts.radius || 20;
  const size = opts.size || 20;
  const label = Array.isArray(lines) ? lines : [lines];
  return `<g>
  <rect x="${x}" y="${y}" width="${width}" height="${height}" rx="${radius}" fill="${fill}" stroke="${stroke}" stroke-width="2.5" />
  ${textBlock(x + width / 2, y + height / 2, label, { size, fill: opts.textFill || COLORS.ink, weight: opts.weight || 700 })}
</g>`;
}

function groupBox(x, y, width, height, title) {
  return `<g>
  <rect x="${x}" y="${y}" width="${width}" height="${height}" rx="24" fill="#ffffff" stroke="${COLORS.line}" stroke-width="2.5" />
  <rect x="${x + 16}" y="${y + 12}" width="126" height="34" rx="16" fill="#ffffff" />
  ${textBlock(x + 79, y + 29, [title], { size: 17, weight: 800, fill: COLORS.soft })}
</g>`;
}

function note(x, y, width, height, lines) {
  return box(x, y, width, height, lines, {
    stroke: COLORS.amber,
    fill: COLORS.amberFill,
    radius: 16,
    size: 15,
    weight: 700,
  });
}

function arrow(x1, y1, x2, y2, label = '', color = COLORS.blue) {
  const marker = color === COLORS.teal ? 'arrow-teal' : color === COLORS.amber ? 'arrow-amber' : color === COLORS.rose ? 'arrow-rose' : color === COLORS.soft ? 'arrow-soft' : 'arrow-blue';
  const mx = (x1 + x2) / 2;
  const my = (y1 + y2) / 2;
  return `<g>
  <line x1="${x1}" y1="${y1}" x2="${x2}" y2="${y2}" stroke="${color}" stroke-width="3" marker-end="url(#${marker})" />
  ${label ? textBlock(mx, my - 12, [label], { size: 15, fill: color, weight: 800 }) : ''}
</g>`;
}

function architectureSvg() {
  return svgShell({
    content: [
      groupBox(42, 122, 156, 258, '入口层'),
      groupBox(226, 122, 170, 258, 'CoPaw 工作区'),
      groupBox(420, 96, 240, 310, '运行时'),
      groupBox(686, 122, 174, 258, '技能工具'),
      groupBox(886, 122, 178, 258, '多智能体'),
      box(72, 218, 98, 80, ['用户', '渠道'], { stroke: COLORS.blue, fill: COLORS.blueFill }),
      box(254, 218, 114, 80, ['工作区'], { stroke: COLORS.blue, fill: COLORS.blueFill }),
      box(456, 148, 168, 58, ['执行器'], { stroke: COLORS.blue, fill: COLORS.blueFill }),
      box(456, 220, 168, 88, ['记忆 / 上下文', 'MCP / 通道'], { stroke: COLORS.teal, fill: COLORS.tealFill, size: 18 }),
      box(456, 322, 168, 58, ['定时 / 跟踪'], { stroke: COLORS.amber, fill: COLORS.amberFill, size: 18 }),
      box(716, 178, 118, 60, ['技能'], { stroke: COLORS.teal, fill: COLORS.tealFill }),
      box(704, 264, 142, 72, ['命令行 / 浏览器'], { stroke: COLORS.blue, fill: COLORS.blueFill, size: 18 }),
      box(916, 178, 118, 60, ['协调器'], { stroke: COLORS.rose, fill: COLORS.roseFill }),
      box(916, 264, 118, 60, ['归档结果'], { stroke: COLORS.amber, fill: COLORS.amberFill, size: 18 }),
      arrow(170, 258, 254, 258, '进入', COLORS.blue),
      arrow(368, 258, 456, 177, '', COLORS.blue),
      arrow(368, 258, 456, 264, '', COLORS.teal),
      arrow(368, 258, 456, 351, '', COLORS.amber),
      arrow(624, 177, 716, 208, '调用', COLORS.teal),
      arrow(624, 264, 704, 300, '', COLORS.soft),
      arrow(624, 351, 704, 300, '', COLORS.soft),
      arrow(834, 208, 916, 208, '', COLORS.rose),
      arrow(975, 238, 975, 264, '', COLORS.amber),
    ].join('\n'),
  });
}

function executionFlowSvg() {
  return svgShell({
    content: [
      groupBox(36, 146, 152, 224, '输入'),
      groupBox(210, 120, 316, 250, 'CoPaw 编排'),
      groupBox(550, 146, 186, 224, '草稿技能'),
      groupBox(760, 120, 332, 250, 'Wan2.7 北京地域'),
      box(66, 236, 92, 64, ['主题输入'], { stroke: COLORS.blue, fill: COLORS.blueFill, size: 18 }),
      box(238, 236, 104, 64, ['CoPaw'], { stroke: COLORS.blue, fill: COLORS.blueFill }),
      box(376, 176, 116, 58, ['技术角色'], { stroke: COLORS.teal, fill: COLORS.tealFill, size: 17 }),
      box(376, 276, 116, 58, ['叙事角色'], { stroke: COLORS.rose, fill: COLORS.roseFill, size: 17 }),
      box(580, 196, 128, 60, ['草稿与蓝图'], { stroke: COLORS.teal, fill: COLORS.tealFill, size: 18 }),
      box(590, 282, 108, 50, ['人工审校'], { stroke: COLORS.amber, fill: COLORS.amberFill, size: 17 }),
      box(794, 170, 122, 60, ['二阶段出图'], { stroke: COLORS.blue, fill: COLORS.blueFill, size: 18 }),
      box(954, 170, 122, 60, ['三阶段视频'], { stroke: COLORS.rose, fill: COLORS.roseFill, size: 18 }),
      note(790, 268, 290, 82, ['CoPaw 负责把事情讲清楚', 'Wan2.7 负责图像与视频生成']),
      arrow(158, 268, 238, 268, '', COLORS.blue),
      arrow(342, 268, 376, 205, '', COLORS.teal),
      arrow(342, 268, 376, 305, '', COLORS.rose),
      arrow(492, 205, 580, 226, '', COLORS.teal),
      arrow(492, 305, 580, 226, '', COLORS.rose),
      arrow(644, 256, 644, 282, '', COLORS.amber),
      arrow(698, 307, 794, 200, '通过后', COLORS.blue),
      arrow(916, 200, 954, 200, '', COLORS.rose),
    ].join('\n'),
  });
}

function roleSvg() {
  return svgShell({
    content: [
      groupBox(24, 128, 152, 270, 'CoPaw'),
      groupBox(194, 128, 152, 270, '技术角色'),
      groupBox(364, 128, 152, 270, '叙事角色'),
      groupBox(534, 128, 150, 270, '文稿阶段'),
      groupBox(702, 128, 150, 270, '出图阶段'),
      groupBox(870, 128, 170, 270, 'Wan2.7'),
      box(52, 246, 96, 56, ['任务编排'], { stroke: COLORS.blue, fill: COLORS.blueFill, size: 18 }),
      box(222, 210, 96, 56, ['事实边界'], { stroke: COLORS.teal, fill: COLORS.tealFill, size: 18 }),
      box(392, 282, 96, 56, ['观看顺序'], { stroke: COLORS.rose, fill: COLORS.roseFill, size: 18 }),
      box(560, 246, 98, 56, ['文稿包'], { stroke: COLORS.teal, fill: COLORS.tealFill, size: 18 }),
      box(728, 222, 98, 56, ['静态图'], { stroke: COLORS.blue, fill: COLORS.blueFill, size: 18 }),
      box(728, 304, 98, 56, ['镜头稿'], { stroke: COLORS.rose, fill: COLORS.roseFill, size: 18 }),
      box(896, 206, 118, 60, ['图像生成'], { stroke: COLORS.blue, fill: COLORS.blueFill, size: 18 }),
      box(896, 294, 118, 60, ['视频生成'], { stroke: COLORS.rose, fill: COLORS.roseFill, size: 18 }),
      arrow(148, 274, 222, 238, '', COLORS.teal),
      arrow(148, 274, 392, 310, '', COLORS.rose),
      arrow(318, 238, 560, 274, '', COLORS.teal),
      arrow(488, 310, 560, 274, '', COLORS.rose),
      arrow(658, 274, 728, 250, '', COLORS.blue),
      arrow(658, 274, 728, 332, '', COLORS.rose),
      arrow(826, 250, 896, 236, '', COLORS.blue),
      arrow(826, 332, 896, 324, '', COLORS.rose),
    ].join('\n'),
  });
}

function ecosystemSvg() {
  return svgShell({
    content: [
      groupBox(362, 120, 286, 248, 'AgentScope 核心'),
      box(416, 200, 178, 68, ['AgentScope'], { stroke: COLORS.teal, fill: COLORS.tealFill, size: 24 }),
      box(70, 110, 158, 60, ['CoPaw'], { stroke: COLORS.blue, fill: COLORS.blueFill }),
      box(70, 226, 158, 60, ['HiClaw'], { stroke: COLORS.rose, fill: COLORS.roseFill }),
      box(70, 342, 158, 60, ['Wan2.7'], { stroke: COLORS.amber, fill: COLORS.amberFill }),
      box(792, 84, 246, 56, ['AgentScope Studio'], { stroke: COLORS.blue, fill: COLORS.blueFill, size: 17 }),
      box(792, 154, 246, 56, ['AgentScope Runtime'], { stroke: COLORS.teal, fill: COLORS.tealFill, size: 17 }),
      box(792, 224, 246, 56, ['agentscope-bricks'], { stroke: COLORS.amber, fill: COLORS.amberFill, size: 17 }),
      box(792, 294, 246, 56, ['agentscope-samples'], { stroke: COLORS.soft, fill: '#ffffff', size: 17 }),
      box(792, 364, 246, 56, ['agentscope-java'], { stroke: COLORS.rose, fill: COLORS.roseFill, size: 17 }),
      arrow(228, 140, 416, 224, '', COLORS.blue),
      arrow(228, 256, 416, 234, '', COLORS.rose),
      arrow(228, 372, 416, 244, '', COLORS.amber),
      arrow(594, 224, 792, 112, '', COLORS.blue),
      arrow(594, 232, 792, 182, '', COLORS.teal),
      arrow(594, 240, 792, 252, '', COLORS.amber),
      arrow(594, 248, 792, 322, '', COLORS.soft),
      arrow(594, 256, 792, 392, '', COLORS.rose),
    ].join('\n'),
  });
}function buildSvg(filename) {
  const map = {
    'copaw_architecture.svg': architectureSvg,
    'wan27_copaw_execution_flow.svg': executionFlowSvg,
    'role_collaboration.svg': roleSvg,
    'agentscope_ecosystem.svg': ecosystemSvg,
  };
  const fn = map[filename];
  if (!fn) {
    throw new Error('unknown lightweight diagram: ' + filename);
  }
  return fn();
}

function createDiagramSvgs() {
  return FILENAMES.map((filename) => ({
    filename,
    svg: buildSvg(filename),
    source: 'lightweight',
  }));
}

async function writeDiagramSvgs(taskDir) {
  ensureDir(SVG_DIR);
  const outDir = path.join(taskDir, 'output', 'svg');
  ensureDir(outDir);
  const written = [];
  for (const item of createDiagramSvgs()) {
    const canonical = path.join(SVG_DIR, item.filename);
    const target = path.join(outDir, item.filename);
    fs.writeFileSync(canonical, item.svg, 'utf8');
    fs.writeFileSync(target, item.svg, 'utf8');
    written.push(target);
  }
  return written;
}

module.exports = {
  createDiagramSvgs,
  writeDiagramSvgs,
};

