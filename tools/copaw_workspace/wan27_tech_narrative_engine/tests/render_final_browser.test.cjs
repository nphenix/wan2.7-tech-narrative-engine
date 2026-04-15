const fs = require('fs');
const os = require('os');
const path = require('path');
const test = require('node:test');
const assert = require('node:assert/strict');

const renderer = require('../render_final_browser.cjs');

test('createSlides returns eight named slides', () => {
  const slides = renderer.createSlides();
  assert.equal(slides.length, 8);
  assert.deepEqual(
    slides.map((slide) => slide.filename),
    [
      'wan27_opening.png',
      'copaw_product_intro.png',
      'copaw_architecture.png',
      'wan27_copaw_execution_flow.png',
      'role_collaboration.png',
      'agentscope_ecosystem.png',
      'value_mapping.png',
      'participant_manifesto_keyframe.png',
    ],
  );
});

test('createDiagramSvgs returns four lightweight svg assets', () => {
  const svgs = renderer.createDiagramSvgs();
  assert.equal(svgs.length, 4);
  assert.deepEqual(
    svgs.map((item) => item.filename),
    [
      'copaw_architecture.svg',
      'wan27_copaw_execution_flow.svg',
      'role_collaboration.svg',
      'agentscope_ecosystem.svg',
    ],
  );

  for (const item of svgs) {
    assert.equal(item.source, 'lightweight');
    assert.match(item.svg, /<svg[\s\S]*viewBox=/);
    assert.match(item.svg, /svg-source:lightweight/i);
    assert.doesNotMatch(item.svg, /excalidraw/i);
  }
});

test('writeHtmlPreviews writes one html file per slide for manual review', async () => {
  const taskDir = fs.mkdtempSync(path.join(os.tmpdir(), 'wan27-render-'));
  const result = await renderer.writeHtmlPreviews(taskDir);
  assert.equal(result.length, 8);

  for (const filePath of result) {
    assert.equal(path.extname(filePath), '.html');
    assert.ok(fs.existsSync(filePath), `missing preview file: ${filePath}`);
  }
});

test('writeDiagramSvgs writes one svg file per structural diagram', async () => {
  const taskDir = fs.mkdtempSync(path.join(os.tmpdir(), 'wan27-diagram-'));
  const result = await renderer.writeDiagramSvgs(taskDir);
  assert.equal(result.length, 4);

  for (const filePath of result) {
    assert.equal(path.extname(filePath), '.svg');
    assert.ok(fs.existsSync(filePath), `missing svg file: ${filePath}`);
    assert.match(fs.readFileSync(filePath, 'utf8'), /svg-source:lightweight/i);
  }
});
