// Minecraft Java-Edition static-model viewer for the Pokefind wiki.
//
// Reads a JSON model file (cuboid `elements`, per-face UVs in 0..16 space,
// optional `rotation` per element) plus its texture atlas, and renders an
// orbit-controlled three.js scene. Designed for the static base-skin models
// in /static/models-3d/regular/<species>/<species>.json — no animation
// support, no entity transforms, no item-display variants.
//
// Usage on a page:
//   <div data-mc-model="/models-3d/regular/bulbasaur/bulbasaur.json"
//        class="mc-model-viewer"></div>
//
// The container's first <canvas> child is reused if present, otherwise one
// is created. Loading is lazy: the viewer initializes on first viewport
// intersection so off-screen species don't pay the cost.

// Bare specifiers route through the page-level importmap (in
// _default/baseof.html), which points "three" and "three/addons/" at
// jsdelivr. Earlier hardcoded https://esm.sh/three URLs sometimes failed
// to load on mobile networks, leaving the viewer blank.
import * as THREE from 'three';
import { OrbitControls } from 'three/addons/controls/OrbitControls.js';

// ---------- Java-MC face order (matches the JSON spec) ----------
// Each face is a quad over the cuboid spanned by `from` → `to`. Per Mojang's
// model spec, every face's four vertices are emitted in a consistent
// texture-relative order: top-left, top-right, bottom-right, bottom-left
// (when looking at the face from outside the cuboid). That makes the UV
// mapping a single hard-coded pattern regardless of axis.
//
// Cuboid corners indexed 0..7 by the bits xyz (0=from, 1=to per axis):
//   0: (fx, fy, fz)   1: (tx, fy, fz)   2: (fx, ty, fz)   3: (tx, ty, fz)
//   4: (fx, fy, tz)   5: (tx, fy, tz)   6: (fx, ty, tz)   7: (tx, ty, tz)
const FACE_DEFS = {
  //         [ TL, TR, BR, BL ] of the texture region, mapped to corner indices.
  down:  [4, 5, 1, 0],   // -y, view from below
  up:    [2, 3, 7, 6],   // +y, view from above
  north: [3, 2, 0, 1],   // -z, view from -z toward +z
  south: [6, 7, 5, 4],   // +z
  west:  [2, 6, 4, 0],   // -x
  east:  [7, 3, 1, 5],   // +x
};

const UV_UNIT = 16; // Java models always express UV in 0..16 pixel-units.

function buildElementMesh(element, materialMap, textureWidth, textureHeight) {
  const [fx, fy, fz] = element.from;
  const [tx, ty, tz] = element.to;
  // 8 cuboid corners — order must match FACE_DEFS indices.
  const corners = [
    [fx, fy, fz], [tx, fy, fz],
    [fx, ty, fz], [tx, ty, fz],
    [fx, fy, tz], [tx, fy, tz],
    [fx, ty, tz], [tx, ty, tz],
  ];

  const positions = [];
  const uvs = [];
  const indices = [];
  const materialIndices = [];   // per-face material index (one per quad → 2 tris)
  const usedMaterials = [];     // mat ref objects in the order they appear

  let vertOffset = 0;
  for (const [face, cornerIdx] of Object.entries(FACE_DEFS)) {
    const f = element.faces?.[face];
    if (!f) continue;

    const texRef = (f.texture || '#0').replace(/^#/, '');
    const mat = materialMap[texRef] || materialMap['0'] || Object.values(materialMap)[0];
    if (!mat) continue;

    let matIndex = usedMaterials.indexOf(mat);
    if (matIndex < 0) {
      matIndex = usedMaterials.length;
      usedMaterials.push(mat);
    }

    // Push the quad's 4 corner positions
    for (const ci of cornerIdx) {
      positions.push(corners[ci][0], corners[ci][1], corners[ci][2]);
    }

    // Per-face UV is [u1, v1, u2, v2] — top-left and bottom-right of the
    // texture region in 0..16 pixel-units. Vertex order is TL/TR/BR/BL.
    let [u1, v1, u2, v2] = f.uv || [0, 0, UV_UNIT, UV_UNIT];
    u1 /= UV_UNIT; v1 /= UV_UNIT;
    u2 /= UV_UNIT; v2 /= UV_UNIT;
    // Three.js UV origin is bottom-left; MC's is top-left → flip V.
    const fv1 = 1 - v1;
    const fv2 = 1 - v2;
    let uvTL = [u1, fv1], uvTR = [u2, fv1], uvBR = [u2, fv2], uvBL = [u1, fv2];

    // Optional 90/180/270° UV rotation (rotates the texture about its centre)
    const rot = ((f.rotation || 0) % 360 + 360) % 360;
    if (rot === 90)  [uvTL, uvTR, uvBR, uvBL] = [uvBL, uvTL, uvTR, uvBR];
    else if (rot === 180) [uvTL, uvTR, uvBR, uvBL] = [uvBR, uvBL, uvTL, uvTR];
    else if (rot === 270) [uvTL, uvTR, uvBR, uvBL] = [uvTR, uvBR, uvBL, uvTL];

    uvs.push(uvTL[0], uvTL[1], uvTR[0], uvTR[1], uvBR[0], uvBR[1], uvBL[0], uvBL[1]);

    // Triangulate the quad TL-TR-BR-BL with CCW winding viewed from outside.
    // Vertex order in FACE_DEFS goes TL → TR → BR → BL clockwise from
    // outside, so we flip the winding to TL → BL → BR / TL → BR → TR.
    indices.push(
      vertOffset + 0, vertOffset + 3, vertOffset + 2,
      vertOffset + 0, vertOffset + 2, vertOffset + 1,
    );
    materialIndices.push(matIndex, matIndex);
    vertOffset += 4;
  }

  if (vertOffset === 0) return null;

  const geometry = new THREE.BufferGeometry();
  geometry.setAttribute('position', new THREE.Float32BufferAttribute(positions, 3));
  geometry.setAttribute('uv', new THREE.Float32BufferAttribute(uvs, 2));
  geometry.setIndex(indices);

  // Group triangles by material so we can use a multi-material mesh.
  let groupStart = 0;
  let lastMat = -1;
  for (let i = 0; i < materialIndices.length; i++) {
    if (materialIndices[i] !== lastMat) {
      if (lastMat !== -1) {
        geometry.addGroup(groupStart, i * 3 - groupStart, lastMat);
      }
      groupStart = i * 3;
      lastMat = materialIndices[i];
    }
  }
  if (lastMat !== -1) {
    geometry.addGroup(groupStart, materialIndices.length * 3 - groupStart, lastMat);
  }
  geometry.computeVertexNormals();

  const mesh = new THREE.Mesh(geometry, usedMaterials.length === 1 ? usedMaterials[0] : usedMaterials);

  // Apply element rotation. Two formats are supported:
  //   { axis: 'x'|'y'|'z', angle: deg,         origin: [x,y,z] } — legacy single-axis (Java MC native).
  //   { angles: [rx, ry, rz],                  origin: [x,y,z] } — 3-axis Euler XYZ (free-format
  //                                                                 bbmodel exports, e.g. Entei spikes).
  // Both wrap the cube in a pivot group positioned at `origin` so the
  // rotation pivots about that world point.
  if (element.rotation) {
    const { angle, axis, angles, origin } = element.rotation;
    const pivot = new THREE.Group();
    pivot.position.set(origin[0], origin[1], origin[2]);
    mesh.position.set(-origin[0], -origin[1], -origin[2]);
    if (Array.isArray(angles)) {
      pivot.rotation.set(
        THREE.MathUtils.degToRad(angles[0] || 0),
        THREE.MathUtils.degToRad(angles[1] || 0),
        THREE.MathUtils.degToRad(angles[2] || 0),
        'XYZ',
      );
    } else {
      const rad = (angle * Math.PI) / 180;
      if (axis === 'x') pivot.rotation.x = rad;
      else if (axis === 'y') pivot.rotation.y = rad;
      else if (axis === 'z') pivot.rotation.z = rad;
    }
    pivot.add(mesh);
    return pivot;
  }
  return mesh;
}

// Build a nested THREE.Group for a staged bone. Each bone records:
//   - parent-relative origin (group position)
//   - rotation [x,y,z] degrees, applied as Euler XYZ (matches Blockbench)
//   - elements: cubes already translated into bone-local coords
//   - children: sub-bones
// Cube meshes get added directly so their per-element rotation pivot still
// works; the bone group rotation then propagates through the whole subtree.
function buildBoneGroup(bone, materialMap, inheritedOpacity) {
  const group = new THREE.Group();
  if (bone.name) group.name = bone.name;
  const o = bone.origin || [0, 0, 0];
  group.position.set(o[0], o[1], o[2]);
  const r = bone.rotation || [0, 0, 0];
  if (r[0] || r[1] || r[2]) {
    group.rotation.set(
      THREE.MathUtils.degToRad(r[0]),
      THREE.MathUtils.degToRad(r[1]),
      THREE.MathUtils.degToRad(r[2]),
    );
  }
  // Honour `opacity` field on the bone — used to render Mewtwo's `shadow_*`
  // psychic-aura cubes (and similar VFX cubes on other species) translucent
  // instead of as solid colored blocks. Children inherit the parent's
  // opacity unless they declare their own. Materials are cloned per-bone so
  // we don't mutate the shared materialMap.
  let myOpacity = bone.opacity != null ? bone.opacity : inheritedOpacity;
  let childMaterialMap = materialMap;
  if (myOpacity != null && myOpacity < 1) {
    childMaterialMap = {};
    for (const [k, mat] of Object.entries(materialMap)) {
      const clone = mat.clone();
      clone.opacity = myOpacity;
      clone.transparent = true;
      clone.alphaTest = 0;
      clone.depthWrite = false;
      childMaterialMap[k] = clone;
    }
  }
  for (const el of bone.elements || []) {
    const m = buildElementMesh(el, childMaterialMap, 0, 0);
    if (m) group.add(m);
  }
  for (const child of bone.children || []) {
    group.add(buildBoneGroup(child, childMaterialMap, myOpacity));
  }
  return group;
}

async function loadTexture(url) {
  const loader = new THREE.TextureLoader();
  return new Promise((resolve, reject) => {
    loader.load(
      url,
      (tex) => {
        tex.magFilter = THREE.NearestFilter;
        tex.minFilter = THREE.NearestFilter;
        tex.colorSpace = THREE.SRGBColorSpace;
        resolve(tex);
      },
      undefined,
      reject,
    );
  });
}

async function buildModelGroup(modelUrl) {
  const res = await fetch(modelUrl);
  if (!res.ok) throw new Error(`Model fetch failed: ${res.status}`);
  const model = await res.json();

  // Resolve textures. Paths look like "pokemon_skins/regular/bulbasaur/bulbasaur".
  // Our assets live alongside the model at <model.json>'s parent — so each
  // texture path's last segment becomes the .png filename in that directory.
  const baseDir = modelUrl.substring(0, modelUrl.lastIndexOf('/'));
  const materialMap = {};
  const tex = model.textures || {};
  const seen = new Map();   // de-dupe identical texture refs into one material
  for (const [key, ref] of Object.entries(tex)) {
    // Don't skip 'particle' — some models (e.g. Kyurem) re-use the particle
    // ref as a face texture, and skipping it causes those faces to fall back
    // to the wrong material.
    if (seen.has(ref)) {
      materialMap[key] = seen.get(ref);
      continue;
    }
    const filename = ref.split('/').pop() + '.png';
    let texture = null;
    try {
      texture = await loadTexture(`${baseDir}/${filename}`);
    } catch {
      texture = null;
    }
    const mat = new THREE.MeshStandardMaterial({
      map: texture,
      transparent: true,
      alphaTest: 0.5,
      roughness: 1.0,
      metalness: 0.0,
      side: THREE.DoubleSide,
    });
    materialMap[key] = mat;
    seen.set(ref, mat);
  }

  const inner = new THREE.Group();
  // Animated species (Charizard, etc.) are staged with a `bones` tree —
  // nested groups whose origins/rotations match the Blockbench rig — so the
  // multi-axis rest-pose rotations on wings and arms render correctly. Plain
  // pokedex models keep using the flat `elements` list.
  if (Array.isArray(model.bones) && model.bones.length) {
    for (const b of model.bones) inner.add(buildBoneGroup(b, materialMap));
  } else {
    for (const el of model.elements || []) {
      const m = buildElementMesh(el, materialMap, 0, 0);
      if (m) inner.add(m);
    }
  }

  // Apply `display.gui.rotation`. We default to applying only the Y (yaw)
  // and Z (roll) components — the X component is usually MC's 3/4-view
  // inventory-icon pitch and makes the standalone viewer look as if the
  // species is leaning forward. Some models (notably Masquerain's static
  // summer/valentine variants) author their cuboids assuming the full
  // inventory rotation will compose with them, so they need X too. Opt
  // in via `model.wiki_apply_full_gui_rotation: true` in the JSON.
  const guiRot = (((model.display || {}).gui || {}).rotation) || null;
  const applyFull = model.wiki_apply_full_gui_rotation === true;
  const root = new THREE.Group();
  if (guiRot && Array.isArray(guiRot) && guiRot.length >= 3) {
    const [rx, ry, rz] = guiRot;
    inner.rotation.set(
      applyFull ? THREE.MathUtils.degToRad(rx) : 0,
      THREE.MathUtils.degToRad(ry),
      THREE.MathUtils.degToRad(rz),
    );
  }
  root.add(inner);

  // Center the bounding box at origin (after rotation). Java models live in
  // a 16-unit cube; recentre so orbit framing stays consistent.
  const box = new THREE.Box3().setFromObject(root);
  const center = box.getCenter(new THREE.Vector3());
  root.position.sub(center);
  return root;
}

// ====================================================================
// Shared singleton renderer.
//
// We allocate ONE WebGLRenderer per page and hop its <canvas> between
// viewer containers. Browsers cap WebGL contexts (8 on Chrome, 4 on
// some mobile Safari builds) and each context keeps a heavy GPU
// allocation alive — the per-form-tab renderer was crashing phones.
// With a single context the cost is constant regardless of how many
// pokedex tabs / dex pages exist.
//
// Each container still owns its own scene + camera + OrbitControls
// (so the user's orbit position survives tab switches), but they
// rebind to the shared canvas + renderer when activated.
// ====================================================================

const isMobile = window.matchMedia('(max-width: 768px)').matches
              || (window.matchMedia('(pointer: coarse)').matches
                  && (navigator.hardwareConcurrency || 8) <= 6);

let sharedRenderer = null;
let sharedCanvas = null;
let activeViewer = null;        // currently-mounted viewer state (see startViewer)
let rafScheduled = false;

function getSharedRenderer() {
  if (sharedRenderer) return sharedRenderer;
  // antialias off on mobile (huge pixel-shader cost on 3x DPI screens),
  // pixel ratio capped so a 360px CSS box doesn't get a 1080² backbuffer.
  sharedRenderer = new THREE.WebGLRenderer({
    antialias: !isMobile,
    alpha: true,
    powerPreference: 'low-power',
  });
  sharedRenderer.setPixelRatio(Math.min(window.devicePixelRatio || 1, isMobile ? 1.5 : 2));
  sharedCanvas = sharedRenderer.domElement;
  // The canvas needs to fill its current container; the container itself
  // sets the size via aspect-ratio CSS, so block-level + 100% is enough.
  sharedCanvas.style.display = 'block';
  sharedCanvas.style.width = '100%';
  sharedCanvas.style.height = '100%';
  return sharedRenderer;
}

function scheduleRender() {
  if (rafScheduled) return;
  rafScheduled = true;
  requestAnimationFrame(renderActive);
}

function renderActive() {
  rafScheduled = false;
  if (!activeViewer || !activeViewer.visible) return;
  const damping = activeViewer.controls.update();
  if (damping || activeViewer.needsRender) {
    sharedRenderer.render(activeViewer.scene, activeViewer.camera);
    activeViewer.needsRender = false;
    if (damping) scheduleRender();   // keep ticking until damping settles
  }
}

// Move the shared canvas + OrbitControls binding into `viewer`. The
// previously-active viewer keeps its scene/camera state but stops
// rendering until re-activated.
function activateViewer(viewer) {
  if (activeViewer === viewer) return;
  if (activeViewer) {
    activeViewer.controls.dispose();
    activeViewer.controls = null;
  }
  activeViewer = viewer;
  const renderer = getSharedRenderer();
  viewer.container.appendChild(sharedCanvas);
  // Fresh OrbitControls bound to the (now-reparented) canvas; restore
  // the camera position the previous controls left behind.
  const controls = new OrbitControls(viewer.camera, sharedCanvas);
  controls.enableDamping = true;
  controls.dampingFactor = 0.08;
  controls.target.copy(viewer.target);
  controls.addEventListener('change', () => {
    viewer.target.copy(controls.target);
    viewer.needsRender = true;
    scheduleRender();
  });
  viewer.controls = controls;

  // Size the renderer to the new container.
  const w = viewer.container.clientWidth || 320;
  const h = viewer.container.clientHeight || 320;
  renderer.setSize(w, h, false);
  viewer.camera.aspect = w / h;
  viewer.camera.updateProjectionMatrix();
  viewer.needsRender = true;
  scheduleRender();
}

// ====================================================================
// Per-container viewer state. The container owns scene + camera but not
// the renderer — that's the shared singleton above.
// ====================================================================

function startViewer(container) {
  const baseUrl = container.dataset.mcModel;
  if (!baseUrl) return;
  if (container.dataset.mcStarted === '1') {
    // Already initialized; just re-bind the shared canvas to it.
    if (container._mcViewer) activateViewer(container._mcViewer);
    return;
  }
  container.dataset.mcStarted = '1';
  container.classList.add('mc-model-loading');
  container.dataset.mcMessage = 'Loading model…';

  // The page passes every available skin URL in a single
  // `data-mc-model-skins` JSON attribute (per-skin attrs collided with
  // Hugo's html/template autoescape, which rewrote underscores).
  const skinUrls = { regular: baseUrl };
  if (container.dataset.mcModelSkins) {
    try {
      Object.assign(skinUrls, JSON.parse(container.dataset.mcModelSkins));
    } catch (e) {
      console.warn('mc-model-viewer: failed to parse data-mc-model-skins', e);
    }
  }

  const scene = new THREE.Scene();
  scene.add(new THREE.AmbientLight(0xffffff, 0.95));
  const dir = new THREE.DirectionalLight(0xffffff, 0.55);
  dir.position.set(8, 12, 8);
  scene.add(dir);

  const initialW = container.clientWidth || 320;
  const initialH = container.clientHeight || 320;
  const camera = new THREE.PerspectiveCamera(28, initialW / initialH, 0.1, 200);
  camera.position.set(22, 14, 28);

  // Per-viewer state object. `controls` is filled in by activateViewer
  // when this viewer becomes the active one; `target` persists the
  // OrbitControls focal point across activations.
  const viewer = {
    container,
    scene,
    camera,
    controls: null,
    target: new THREE.Vector3(0, 0, 0),
    needsRender: true,
    visible: true,
    currentGroup: null,
    cameraFramed: false,
    skinUrls,
  };
  container._mcViewer = viewer;

  function countMeshes(obj) {
    let n = 0;
    obj.traverse((o) => { if (o.isMesh) n++; });
    return n;
  }

  function disposeMaterial(mat) {
    if (!mat) return;
    if (Array.isArray(mat)) { mat.forEach(disposeMaterial); return; }
    if (mat.map && mat.map.dispose) mat.map.dispose();
    mat.dispose && mat.dispose();
  }

  function unmount(group) {
    if (!group) return;
    scene.remove(group);
    group.traverse((obj) => {
      if (obj.geometry && obj.geometry.dispose) obj.geometry.dispose();
      if (obj.material) disposeMaterial(obj.material);
    });
  }

  function loadSkin(url) {
    container.classList.remove('mc-model-error');
    return buildModelGroup(url).then((group) => {
      if (countMeshes(group) === 0) {
        container.dataset.mcMessage = 'model parsed but produced no geometry';
        container.classList.add('mc-model-error');
        container.classList.remove('mc-model-loading');
        return;
      }
      container.classList.remove('mc-model-loading');
      unmount(viewer.currentGroup);
      viewer.currentGroup = group;
      scene.add(group);
      if (!viewer.cameraFramed) {
        const box = new THREE.Box3().setFromObject(group);
        const size = box.getSize(new THREE.Vector3()).length();
        const d = size * 1.6;
        camera.position.set(-d * 0.45, d * 0.35, -d);
        camera.near = Math.max(d * 0.01, 0.1);
        camera.far = d * 10;
        camera.updateProjectionMatrix();
        viewer.target.set(0, 0, 0);
        if (viewer.controls) viewer.controls.target.set(0, 0, 0);
        viewer.cameraFramed = true;
      }
      viewer.needsRender = true;
      if (activeViewer === viewer) scheduleRender();
    }).catch((err) => {
      console.error('mc-model-viewer:', err);
      container.dataset.mcMessage = err.message || String(err);
      container.classList.add('mc-model-error');
      container.classList.remove('mc-model-loading');
    });
  }

  loadSkin(baseUrl);

  const panel = container.closest('.form-panel') || document;
  const buttons = panel.querySelectorAll('.mc-skin-btn');
  buttons.forEach((btn) => {
    btn.addEventListener('click', () => {
      const skin = btn.dataset.skin;
      const url = skinUrls[skin];
      if (!url) return;
      buttons.forEach((b) => {
        const active = b === btn;
        b.classList.toggle('active', active);
        b.setAttribute('aria-selected', active ? 'true' : 'false');
      });
      loadSkin(url);
    });
  });

  // Pause rendering when this viewer scrolls out of view; resume on re-entry.
  const visIo = new IntersectionObserver((entries) => {
    for (const entry of entries) {
      viewer.visible = entry.isIntersecting;
      if (viewer.visible && activeViewer === viewer) {
        viewer.needsRender = true;
        scheduleRender();
      }
    }
  }, { threshold: 0 });
  visIo.observe(container);

  // Take ownership of the shared canvas immediately; subsequent viewers
  // (other form tabs, etc.) only steal it when their tab is selected.
  activateViewer(viewer);
}

// Window-level resize forwards to the active viewer (the shared renderer
// is sized per-container, so only the active one cares).
window.addEventListener('resize', () => {
  if (!activeViewer || !sharedRenderer) return;
  const w = activeViewer.container.clientWidth || 320;
  const h = activeViewer.container.clientHeight || 320;
  sharedRenderer.setSize(w, h, false);
  activeViewer.camera.aspect = w / h;
  activeViewer.camera.updateProjectionMatrix();
  activeViewer.needsRender = true;
  scheduleRender();
}, { passive: true });

// Form-tab clicks need to re-bind the shared canvas to whichever viewer's
// tab just became active. The pokedex page swaps `.form-panel[hidden]`
// attributes — we listen for clicks on the tab buttons in the same panel
// and activate the matching viewer (if any).
document.addEventListener('click', (e) => {
  const tab = e.target.closest('.form-tab');
  if (!tab) return;
  const tabsParent = tab.closest('[role="tablist"]')?.parentElement || document;
  // Defer to next tick so the form-tab click handler in pokedex.js has
  // already toggled `[hidden]` and we can find the now-active panel.
  setTimeout(() => {
    const activePanel = tabsParent.querySelector('.form-panel.active, .form-panel:not([hidden])');
    if (!activePanel) return;
    const viewerEl = activePanel.querySelector('[data-mc-model]');
    if (!viewerEl) return;
    if (viewerEl._mcViewer) {
      // Existing viewer: re-bind the shared canvas to it.
      activateViewer(viewerEl._mcViewer);
    } else if (viewerEl.dataset.mcDeferred !== '1') {
      // Lazy-init on tab activation (desktop path).
      startViewer(viewerEl);
    }
  }, 0);
});

// Build the "Tap to load 3D model" placeholder. Mobile users get this so
// the WebGL pipeline never spins up unless they opt in.
function mountDeferredPlaceholder(container) {
  if (container.dataset.mcDeferred === '1') return;
  container.dataset.mcDeferred = '1';
  const btn = document.createElement('button');
  btn.type = 'button';
  btn.className = 'mc-model-load-btn';
  btn.textContent = 'Tap to load 3D model';
  btn.setAttribute('aria-label', 'Load interactive 3D model');
  container.appendChild(btn);
  btn.addEventListener('click', () => {
    btn.remove();
    container.dataset.mcDeferred = '';
    startViewer(container);
  });
}

function init() {
  const targets = document.querySelectorAll('[data-mc-model]');
  if (!targets.length) return;
  if (isMobile) {
    targets.forEach((el) => mountDeferredPlaceholder(el));
    return;
  }
  // Desktop: only auto-init the first viewer that scrolls into view. Other
  // viewers (form tabs that aren't the default) wait for their tab click —
  // the document-level tab listener above starts them lazily.
  const io = new IntersectionObserver((entries) => {
    for (const entry of entries) {
      if (entry.isIntersecting) {
        // Only one renderer; start the first visible viewer and let the
        // tab-click listener handle the rest as the user navigates.
        startViewer(entry.target);
        io.unobserve(entry.target);
        return;
      }
    }
  }, { rootMargin: '200px' });
  // Observe only viewers in the active panel — the rest will get started
  // on first tab-click. Picks the standard form's viewer on initial load.
  const initial = document.querySelector('.form-panel.active [data-mc-model], [data-mc-model]');
  if (initial) io.observe(initial);
}

if (document.readyState === 'loading') {
  document.addEventListener('DOMContentLoaded', init);
} else {
  init();
}
