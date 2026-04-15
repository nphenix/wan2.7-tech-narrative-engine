const path = require('path');

const PALETTE = {
  bg: '#2d2f39',
  ink: '#f4f1e8',
  blue: '#7fd3f7',
  blueFill: '#305a73',
  teal: '#8ad7b1',
  tealFill: '#35584d',
  amber: '#f3c46b',
  amberFill: '#705422',
  rose: '#f49ab0',
  roseFill: '#6c4050',
  whiteLine: '#e8e3d7',
  noteFill: '#7a5a25',
};

const FONT_FAMILY = {
  Virgil: 1,
  Helvetica: 2,
  Cascadia: 3,
  Excalifont: 4,
  Nunito: 5,
};

function commonShape(overrides = {}) {
  return {
    strokeColor: PALETTE.whiteLine,
    backgroundColor: 'transparent',
    fillStyle: 'hachure',
    strokeWidth: 2.2,
    strokeStyle: 'solid',
    roughness: 1.35,
    opacity: 100,
    angle: 0,
    ...overrides,
  };
}

function textLabel(text, fontSize = 22, strokeColor = PALETTE.ink, textAlign = 'center') {
  return {
    text,
    fontSize,
    fontFamily: FONT_FAMILY.Excalifont,
    textAlign,
    verticalAlign: 'middle',
    strokeColor,
    backgroundColor: 'transparent',
    fillStyle: 'solid',
    strokeWidth: 1,
    roughness: 0.35,
    opacity: 100,
    angle: 0,
  };
}

function rect({ id, x, y, width, height, text, strokeColor = PALETTE.whiteLine, backgroundColor = 'transparent', fontSize = 22, roughness = 1.2, fillStyle = 'hachure' }) {
  return {
    type: 'rectangle',
    id,
    x,
    y,
    width,
    height,
    ...commonShape({ strokeColor, backgroundColor, roughness, fillStyle }),
    label: text ? textLabel(text, fontSize) : undefined,
  };
}

function diamond({ id, x, y, width, height, text, strokeColor = PALETTE.rose, backgroundColor = PALETTE.roseFill, fontSize = 20 }) {
  return {
    type: 'diamond',
    id,
    x,
    y,
    width,
    height,
    ...commonShape({ strokeColor, backgroundColor, roughness: 1.1 }),
    label: textLabel(text, fontSize),
  };
}

function ellipse({ id, x, y, width, height, text, strokeColor = PALETTE.rose, backgroundColor = PALETTE.roseFill, fontSize = 22 }) {
  return {
    type: 'ellipse',
    id,
    x,
    y,
    width,
    height,
    ...commonShape({ strokeColor, backgroundColor, roughness: 1.15 }),
    label: textLabel(text, fontSize),
  };
}

function groupBox({ id, x, y, width, height, title, strokeColor = PALETTE.whiteLine }) {
  return rect({ id, x, y, width, height, text: title, strokeColor, backgroundColor: 'transparent', fontSize: 20, roughness: 1.15 });
}

function component({ id, x, y, width, height, title, strokeColor = PALETTE.blue, backgroundColor = PALETTE.blueFill, fontSize = 22 }) {
  return rect({ id, x, y, width, height, text: title, strokeColor, backgroundColor, fontSize, roughness: 1.0 });
}

function note({ id, x, y, width, height, text, strokeColor = PALETTE.amber, backgroundColor = PALETTE.noteFill }) {
  return rect({ id, x, y, width, height, text, strokeColor, backgroundColor, fontSize: 18, roughness: 1.0 });
}

function arrow({ id, startId, endId, label, strokeColor = PALETTE.whiteLine, points = [[0,0],[120,0]], endArrowhead = 'triangle' }) {
  return {
    type: 'arrow',
    id,
    x: 0,
    y: 0,
    points,
    startArrowhead: null,
    endArrowhead,
    strokeColor,
    backgroundColor: 'transparent',
    fillStyle: 'solid',
    strokeWidth: 2.4,
    strokeStyle: 'solid',
    roughness: 1.05,
    opacity: 100,
    start: startId ? { id: startId } : undefined,
    end: endId ? { id: endId } : undefined,
    label: label ? textLabel(label, 18, PALETTE.ink) : undefined,
  };
}

function scene(appState, elements) {
  return { appState, elements };
}

const COMMON_APP_STATE = {
  viewBackgroundColor: PALETTE.bg,
  currentItemFontFamily: FONT_FAMILY.Excalifont,
  currentItemStrokeColor: PALETTE.whiteLine,
  currentItemBackgroundColor: 'transparent',
  currentItemRoughness: 1.15,
  currentItemOpacity: 100,
  currentItemStrokeWidth: 2,
  currentItemFillStyle: 'hachure',
  currentItemStrokeStyle: 'solid',
  gridSize: null,
  theme: 'dark',
};

const specs = [
  scene({ ...COMMON_APP_STATE, name: 'copaw_architecture' }, [
    groupBox({ id: 'entry', x: 40, y: 180, width: 160, height: 230, title: 'Entry' }),
    groupBox({ id: 'workspace-group', x: 240, y: 150, width: 220, height: 260, title: 'Workspace' }),
    groupBox({ id: 'runtime', x: 510, y: 120, width: 255, height: 330, title: 'Runtime services' }),
    groupBox({ id: 'skills-group', x: 820, y: 180, width: 210, height: 220, title: 'Skills / Tools' }),
    groupBox({ id: 'agents', x: 1080, y: 170, width: 190, height: 240, title: 'Multi-Agent' }),
    ellipse({ id: 'user', x: 52, y: 48, width: 140, height: 140, text: 'User', strokeColor: PALETTE.rose, backgroundColor: PALETTE.roseFill }),
    component({ id: 'channel', x: 65, y: 255, width: 110, height: 72, title: 'Channel' }),
    component({ id: 'workspace-core', x: 292, y: 246, width: 118, height: 78, title: 'Workspace' }),
    component({ id: 'runner', x: 560, y: 168, width: 138, height: 62, title: 'Runner' }),
    component({ id: 'memory', x: 560, y: 248, width: 138, height: 82, title: 'Memory\nMCP', strokeColor: PALETTE.teal, backgroundColor: PALETTE.tealFill }),
    component({ id: 'cron', x: 560, y: 348, width: 138, height: 60, title: 'Cron', strokeColor: PALETTE.amber, backgroundColor: PALETTE.amberFill }),
    component({ id: 'skills', x: 866, y: 222, width: 120, height: 64, title: 'Skills', strokeColor: PALETTE.teal, backgroundColor: PALETTE.tealFill }),
    component({ id: 'tools', x: 866, y: 310, width: 120, height: 64, title: 'Shell / Browser', fontSize: 20 }),
    component({ id: 'manager', x: 1116, y: 224, width: 118, height: 66, title: 'Manager', strokeColor: PALETTE.rose, backgroundColor: PALETTE.roseFill }),
    component({ id: 'archive', x: 1116, y: 312, width: 118, height: 66, title: 'Artifacts', strokeColor: PALETTE.amber, backgroundColor: PALETTE.amberFill }),
    note({ id: 'arch-note-1', x: 246, y: 56, width: 210, height: 58, text: 'workspace is the runtime anchor' }),
    note({ id: 'arch-note-2', x: 851, y: 78, width: 188, height: 60, text: 'skills stay replaceable' }),
    note({ id: 'arch-note-3', x: 1038, y: 470, width: 210, height: 62, text: 'manager coordinates, not owns content' }),
    arrow({ id: 'a1', startId: 'user', endId: 'channel' }),
    arrow({ id: 'a2', startId: 'channel', endId: 'workspace-core', label: 'enter' }),
    arrow({ id: 'a3', startId: 'workspace-core', endId: 'runner', strokeColor: PALETTE.blue }),
    arrow({ id: 'a4', startId: 'workspace-core', endId: 'memory', strokeColor: PALETTE.teal }),
    arrow({ id: 'a5', startId: 'workspace-core', endId: 'cron', strokeColor: PALETTE.amber }),
    arrow({ id: 'a6', startId: 'runner', endId: 'skills', strokeColor: PALETTE.teal, label: 'invoke' }),
    arrow({ id: 'a7', startId: 'memory', endId: 'skills' }),
    arrow({ id: 'a8', startId: 'cron', endId: 'tools' }),
    arrow({ id: 'a9', startId: 'skills', endId: 'manager', strokeColor: PALETTE.rose }),
    arrow({ id: 'a10', startId: 'manager', endId: 'archive', strokeColor: PALETTE.amber }),
    arrow({ id: 'a11', startId: 'arch-note-1', endId: 'workspace-core', strokeColor: PALETTE.amber }),
    arrow({ id: 'a12', startId: 'arch-note-2', endId: 'skills', strokeColor: PALETTE.amber }),
    arrow({ id: 'a13', startId: 'arch-note-3', endId: 'manager', strokeColor: PALETTE.amber }),
  ]),
  scene({ ...COMMON_APP_STATE, name: 'wan27_copaw_execution_flow' }, [
    groupBox({ id: 'flow-intake', x: 50, y: 210, width: 175, height: 180, title: 'Input' }),
    groupBox({ id: 'flow-plan', x: 270, y: 160, width: 310, height: 250, title: 'Planning' }),
    groupBox({ id: 'flow-review', x: 630, y: 180, width: 180, height: 210, title: 'Draft' }),
    groupBox({ id: 'flow-generate', x: 860, y: 160, width: 350, height: 250, title: 'Wan2.7 Beijing' }),
    component({ id: 'topic', x: 95, y: 275, width: 90, height: 70, title: 'Topic' }),
    component({ id: 'copaw', x: 295, y: 275, width: 100, height: 64, title: 'CoPaw' }),
    component({ id: 'tech-agent', x: 430, y: 220, width: 100, height: 60, title: 'Tech Agent', strokeColor: PALETTE.teal, backgroundColor: PALETTE.tealFill, fontSize: 20 }),
    component({ id: 'story-agent', x: 430, y: 305, width: 100, height: 60, title: 'Story Agent', strokeColor: PALETTE.rose, backgroundColor: PALETTE.roseFill, fontSize: 20 }),
    component({ id: 'skill1', x: 665, y: 248, width: 112, height: 64, title: 'Skill 1', strokeColor: PALETTE.teal, backgroundColor: PALETTE.tealFill }),
    diamond({ id: 'gate', x: 690, y: 332, width: 78, height: 78, text: 'review?' }),
    component({ id: 'skill2', x: 905, y: 220, width: 118, height: 64, title: 'Skill 2 image', strokeColor: PALETTE.blue, backgroundColor: PALETTE.blueFill, fontSize: 20 }),
    component({ id: 'skill3', x: 1070, y: 220, width: 118, height: 64, title: 'Skill 3 video', strokeColor: PALETTE.rose, backgroundColor: PALETTE.roseFill, fontSize: 20 }),
    note({ id: 'wan-tag', x: 930, y: 328, width: 210, height: 72, text: 'wan2.7-image\nwan2.7-image-pro\nwan2.7-i2v' }),
    note({ id: 'flow-note-1', x: 268, y: 60, width: 220, height: 58, text: 'draft first, generate later' }),
    note({ id: 'flow-note-2', x: 1110, y: 80, width: 150, height: 58, text: 'Beijing only' }),
    arrow({ id: 'e1', startId: 'topic', endId: 'copaw' }),
    arrow({ id: 'e2', startId: 'copaw', endId: 'tech-agent', strokeColor: PALETTE.teal }),
    arrow({ id: 'e3', startId: 'copaw', endId: 'story-agent', strokeColor: PALETTE.rose }),
    arrow({ id: 'e4', startId: 'tech-agent', endId: 'skill1', strokeColor: PALETTE.teal }),
    arrow({ id: 'e5', startId: 'story-agent', endId: 'skill1', strokeColor: PALETTE.rose }),
    arrow({ id: 'e6', startId: 'skill1', endId: 'gate' }),
    arrow({ id: 'e7', startId: 'gate', endId: 'skill2', strokeColor: PALETTE.blue, label: 'yes' }),
    arrow({ id: 'e8', startId: 'skill2', endId: 'skill3' }),
    arrow({ id: 'e9', startId: 'flow-note-1', endId: 'skill1', strokeColor: PALETTE.amber }),
    arrow({ id: 'e10', startId: 'flow-note-2', endId: 'wan-tag', strokeColor: PALETTE.amber }),
  ]),
  scene({ ...COMMON_APP_STATE, name: 'role_collaboration' }, [
    groupBox({ id: 'lane-1', x: 48, y: 170, width: 180, height: 310, title: 'Tech Agent' }),
    groupBox({ id: 'lane-2', x: 250, y: 170, width: 180, height: 310, title: 'Narrative Agent' }),
    groupBox({ id: 'lane-3', x: 452, y: 170, width: 150, height: 310, title: 'Skill 1' }),
    groupBox({ id: 'lane-4', x: 624, y: 170, width: 150, height: 310, title: 'Skill 2' }),
    groupBox({ id: 'lane-5', x: 796, y: 170, width: 150, height: 310, title: 'Skill 3' }),
    groupBox({ id: 'lane-6', x: 968, y: 170, width: 190, height: 310, title: 'Outcome' }),
    component({ id: 'fact', x: 82, y: 245, width: 112, height: 58, title: 'fact boundary', fontSize: 18 }),
    component({ id: 'storyline', x: 284, y: 245, width: 112, height: 58, title: 'story order', strokeColor: PALETTE.rose, backgroundColor: PALETTE.roseFill, fontSize: 18 }),
    component({ id: 'draft-pack', x: 472, y: 305, width: 110, height: 58, title: 'draft pack', strokeColor: PALETTE.teal, backgroundColor: PALETTE.tealFill, fontSize: 18 }),
    component({ id: 'still-image', x: 644, y: 305, width: 110, height: 58, title: 'still image', fontSize: 18 }),
    component({ id: 'video', x: 816, y: 305, width: 110, height: 58, title: 'video', strokeColor: PALETTE.rose, backgroundColor: PALETTE.roseFill, fontSize: 18 }),
    rect({ id: 'result', x: 1004, y: 266, width: 120, height: 96, text: 'accurate\nclear\ndeliverable', strokeColor: PALETTE.amber, backgroundColor: PALETTE.amberFill, fontSize: 20 }),
    note({ id: 'role-note-1', x: 62, y: 62, width: 210, height: 60, text: 'facts cannot be rewritten' }),
    note({ id: 'role-note-2', x: 336, y: 86, width: 220, height: 60, text: 'narrative shapes viewing order' }),
    note({ id: 'role-note-3', x: 856, y: 82, width: 210, height: 60, text: 'handoff stays explicit' }),
    arrow({ id: 'r1', startId: 'fact', endId: 'storyline' }),
    arrow({ id: 'r2', startId: 'storyline', endId: 'draft-pack' }),
    arrow({ id: 'r3', startId: 'draft-pack', endId: 'still-image' }),
    arrow({ id: 'r4', startId: 'still-image', endId: 'video' }),
    arrow({ id: 'r5', startId: 'video', endId: 'result', strokeColor: PALETTE.amber }),
    arrow({ id: 'r6', startId: 'role-note-1', endId: 'fact', strokeColor: PALETTE.amber }),
    arrow({ id: 'r7', startId: 'role-note-2', endId: 'storyline', strokeColor: PALETTE.amber }),
    arrow({ id: 'r8', startId: 'role-note-3', endId: 'video', strokeColor: PALETTE.amber }),
  ]),
  scene({ ...COMMON_APP_STATE, name: 'agentscope_ecosystem' }, [
    component({ id: 'core', x: 544, y: 242, width: 170, height: 86, title: 'AgentScope', strokeColor: PALETTE.teal, backgroundColor: PALETTE.tealFill, fontSize: 26 }),
    groupBox({ id: 'core-frame', x: 492, y: 188, width: 274, height: 194, title: 'framework core' }),
    component({ id: 'copaw', x: 92, y: 154, width: 150, height: 72, title: 'CoPaw' }),
    component({ id: 'hiclaw', x: 92, y: 384, width: 150, height: 72, title: 'HiClaw', strokeColor: PALETTE.rose, backgroundColor: PALETTE.roseFill }),
    component({ id: 'studio', x: 1020, y: 154, width: 180, height: 72, title: 'AgentScope Studio', fontSize: 20 }),
    component({ id: 'wan', x: 1020, y: 384, width: 150, height: 72, title: 'Wan2.7', strokeColor: PALETTE.rose, backgroundColor: PALETTE.roseFill }),
    note({ id: 'eco-note-1', x: 266, y: 118, width: 170, height: 64, text: 'personal workspace' }),
    note({ id: 'eco-note-2', x: 804, y: 418, width: 170, height: 64, text: 'image / video output' }),
    note({ id: 'eco-note-3', x: 520, y: 72, width: 220, height: 64, text: 'AgentScope sits at the center' }),
    arrow({ id: 'g1', startId: 'copaw', endId: 'core', strokeColor: PALETTE.blue }),
    arrow({ id: 'g2', startId: 'hiclaw', endId: 'core', strokeColor: PALETTE.rose }),
    arrow({ id: 'g3', startId: 'core', endId: 'studio' }),
    arrow({ id: 'g4', startId: 'core', endId: 'wan' }),
    arrow({ id: 'g5', startId: 'eco-note-1', endId: 'copaw', strokeColor: PALETTE.amber }),
    arrow({ id: 'g6', startId: 'eco-note-2', endId: 'wan', strokeColor: PALETTE.amber }),
    arrow({ id: 'g7', startId: 'eco-note-3', endId: 'core', strokeColor: PALETTE.amber }),
  ]),
];

const filenames = ['copaw_architecture','wan27_copaw_execution_flow','role_collaboration','agentscope_ecosystem'];

function toSceneRecords() {
  return specs.map((spec, index) => ({
    id: filenames[index],
    filename: filenames[index] + '.svg',
    sceneFilename: filenames[index] + '.excalidraw.json',
    scene: spec,
  }));
}

module.exports = {
  toSceneRecords,
  FONT_FAMILY,
  PALETTE,
  EXCALIDRAW_DIR: path.join(__dirname, 'excalidraw_assets'),
  SVG_EXPORT_DIR: path.join(__dirname, 'excalidraw_exports'),
};
