import {
  convertToExcalidrawElements,
  exportToSvg,
  restore,
  serializeAsJSON,
} from '@excalidraw/excalidraw';

async function sceneSpecToSceneJson(spec) {
  const elements = convertToExcalidrawElements(spec.elements, { regenerateIds: false });
  return serializeAsJSON(elements, spec.appState || {}, {}, 'local');
}

async function sceneJsonToSvg(sceneJson) {
  const data = typeof sceneJson === 'string' ? JSON.parse(sceneJson) : sceneJson;
  const restored = restore(data, null, null, { refreshDimensions: true, repairBindings: true });
  const svg = await exportToSvg({
    elements: restored.elements,
    appState: {
      ...restored.appState,
      exportBackground: true,
      exportPadding: 24,
      exportScale: 1,
      exportEmbedScene: true,
      viewBackgroundColor: restored.appState.viewBackgroundColor || '#f7f4ee',
      exportWithDarkMode: false,
      frameRendering: { enabled: true, name: true, outline: true, clip: true },
    },
    files: restored.files || {},
    exportPadding: 24,
    renderEmbeddables: true,
  });
  svg.setAttribute('data-exporter', 'wan27-excalidraw');
  return `${svg.outerHTML.replace('<metadata>', '<!-- svg-source:excalidraw --><metadata>')}`;
}

window.Wan27ExcalidrawExporter = {
  async serializeScene(spec) {
    return sceneSpecToSceneJson(spec);
  },
  async exportScene(spec) {
    const sceneJson = await sceneSpecToSceneJson(spec);
    const svg = await sceneJsonToSvg(sceneJson);
    return { sceneJson, svg, source: 'excalidraw' };
  },
  async exportFromSceneJson(sceneJson) {
    return sceneJsonToSvg(sceneJson);
  },
};
