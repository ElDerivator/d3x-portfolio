// Visor 3D del modelo de Luis Rivero (.glb) — three.js vendorizado, carga diferida.
// El modelo tiene versión light y dark (gradiente + luces) que sigue el tema del sitio.
import * as THREE from 'three';
import { GLTFLoader } from './vendor/three/GLTFLoader.js';
import { OrbitControls } from './vendor/three/OrbitControls.js';

// Paletas por tema: gradiente de marca + luces/material.
const THEMES = {
  dark:  { c1: 0x0a8f8a, c2: 0xe0a83a, hemiSky: 0xffffff, hemiGround: 0x223a4d, hemiInt: 1.15, keyInt: 1.5,  rimColor: 0x88aaff, rimInt: 0.85, metal: 0.25, rough: 0.5 },
  light: { c1: 0x0b7f7a, c2: 0xc9892a, hemiSky: 0xffffff, hemiGround: 0xc8d4dc, hemiInt: 1.3,  keyInt: 1.25, rimColor: 0x6688bb, rimInt: 0.5,  metal: 0.15, rough: 0.6 },
};
function currentTheme() {
  return document.documentElement.dataset.theme === 'light' ? 'light' : 'dark';
}

function initViewer(root) {
  const stage = root.querySelector('[data-model-stage]');
  const src = root.dataset.modelSrc;
  const reduceMotion = matchMedia('(prefers-reduced-motion: reduce)').matches;
  let started = false;

  function start() {
    if (started) return;
    started = true;
    root.classList.add('is-loading');

    const w = stage.clientWidth || 360;
    const h = stage.clientHeight || 420;

    const renderer = new THREE.WebGLRenderer({ antialias: true, alpha: true });
    renderer.setPixelRatio(Math.min(window.devicePixelRatio || 1, 2));
    renderer.setSize(w, h);
    renderer.outputColorSpace = THREE.SRGBColorSpace;
    stage.appendChild(renderer.domElement);

    const scene = new THREE.Scene();
    const camera = new THREE.PerspectiveCamera(38, w / h, 0.1, 2000);

    const hemi = new THREE.HemisphereLight(0xffffff, 0x223a4d, 1.15);
    scene.add(hemi);
    const key = new THREE.DirectionalLight(0xffffff, 1.5);
    key.position.set(3, 6, 5);
    scene.add(key);
    const rim = new THREE.DirectionalLight(0x88aaff, 0.8);
    rim.position.set(-4, 2, -5);
    scene.add(rim);

    const controls = new OrbitControls(camera, renderer.domElement);
    controls.enableDamping = true;
    controls.enablePan = false;
    controls.autoRotate = !reduceMotion;
    controls.autoRotateSpeed = 1.0;

    const meshInfos = []; // { colorAttr, posAttr, lo, rng, material }
    const cA = new THREE.Color(), cB = new THREE.Color(), tmpC = new THREE.Color();

    function applyTheme(themeName) {
      const t = THEMES[themeName] || THEMES.dark;
      hemi.color.setHex(t.hemiSky); hemi.groundColor.setHex(t.hemiGround); hemi.intensity = t.hemiInt;
      key.intensity = t.keyInt;
      rim.color.setHex(t.rimColor); rim.intensity = t.rimInt;
      cA.setHex(t.c1); cB.setHex(t.c2);
      meshInfos.forEach((mi) => {
        const arr = mi.colorAttr.array, p = mi.posAttr, n = p.count;
        for (let i = 0; i < n; i++) {
          tmpC.copy(cA).lerp(cB, (p.getZ(i) - mi.lo) / mi.rng);
          arr[i * 3] = tmpC.r; arr[i * 3 + 1] = tmpC.g; arr[i * 3 + 2] = tmpC.b;
        }
        mi.colorAttr.needsUpdate = true;
        mi.material.metalness = t.metal;
        mi.material.roughness = t.rough;
      });
    }

    const loader = new GLTFLoader();
    loader.load(src, (gltf) => {
      const model = gltf.scene;
      model.rotation.x = -Math.PI / 2; // 3MF Z-up -> three.js Y-up
      model.updateMatrixWorld(true);

      model.traverse((o) => {
        if (!o.isMesh) return;
        const g = o.geometry;
        g.computeBoundingBox();
        const lo = g.boundingBox.min.z, rng = (g.boundingBox.max.z - g.boundingBox.min.z) || 1;
        const p = g.attributes.position;
        const colorAttr = new THREE.BufferAttribute(new Float32Array(p.count * 3), 3);
        g.setAttribute('color', colorAttr);
        const material = new THREE.MeshStandardMaterial({ vertexColors: true });
        o.material = material;
        meshInfos.push({ colorAttr, posAttr: p, lo, rng, material });
      });

      applyTheme(currentTheme()); // color/luz según tema actual

      const box = new THREE.Box3().setFromObject(model);
      const size = box.getSize(new THREE.Vector3());
      const center = box.getCenter(new THREE.Vector3());
      model.position.sub(center);
      scene.add(model);

      const maxDim = Math.max(size.x, size.y, size.z);
      const dist = maxDim / (2 * Math.tan((Math.PI * camera.fov) / 360));
      camera.position.set(0, size.y * 0.05, dist * 1.25);
      controls.target.set(0, 0, 0);
      controls.minDistance = dist * 0.6;
      controls.maxDistance = dist * 3.5;
      controls.update();

      // Reacciona al cambio de tema del sitio (toggle ☾).
      const obs = new MutationObserver(() => applyTheme(currentTheme()));
      obs.observe(document.documentElement, { attributes: true, attributeFilter: ['data-theme'] });

      root.classList.remove('is-loading');
      root.classList.add('is-ready');
    }, undefined, (err) => {
      root.classList.remove('is-loading');
      root.classList.add('is-error');
      console.error('No se pudo cargar el modelo 3D:', err);
    });

    function onResize() {
      const nw = stage.clientWidth, nh = stage.clientHeight;
      if (!nw || !nh) return;
      camera.aspect = nw / nh;
      camera.updateProjectionMatrix();
      renderer.setSize(nw, nh);
    }
    window.addEventListener('resize', onResize);

    (function loop() {
      requestAnimationFrame(loop);
      controls.update();
      renderer.render(scene, camera);
    })();
  }

  const btn = root.querySelector('[data-model-load]');
  if (btn) btn.addEventListener('click', start);

  start(); // auto-carga inmediata
}

document.querySelectorAll('[data-model-viewer]').forEach(initViewer);
