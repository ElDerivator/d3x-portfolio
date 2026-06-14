// Visor 3D del modelo de Luis Rivero (.glb) — three.js vendorizado, carga diferida.
import * as THREE from 'three';
import { GLTFLoader } from './vendor/three/GLTFLoader.js';
import { OrbitControls } from './vendor/three/OrbitControls.js';

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

    scene.add(new THREE.HemisphereLight(0xffffff, 0x223a4d, 1.15));
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

    const loader = new GLTFLoader();
    loader.load(src, (gltf) => {
      const model = gltf.scene;
      model.rotation.x = -Math.PI / 2; // 3MF Z-up -> three.js Y-up
      model.updateMatrixWorld(true);

      // Color: gradiente de marca (teal -> dorado) por altura del modelo (eje Z local).
      const cBottom = new THREE.Color(0x0a8f8a);
      const cTop = new THREE.Color(0xe0a83a);
      const tmpC = new THREE.Color();
      model.traverse((o) => {
        if (!o.isMesh) return;
        const g = o.geometry;
        g.computeBoundingBox();
        const lo = g.boundingBox.min.z, rng = (g.boundingBox.max.z - g.boundingBox.min.z) || 1;
        const p = g.attributes.position, n = p.count;
        const col = new Float32Array(n * 3);
        for (let i = 0; i < n; i++) {
          tmpC.copy(cBottom).lerp(cTop, (p.getZ(i) - lo) / rng);
          col[i * 3] = tmpC.r; col[i * 3 + 1] = tmpC.g; col[i * 3 + 2] = tmpC.b;
        }
        g.setAttribute('color', new THREE.BufferAttribute(col, 3));
        o.material = new THREE.MeshStandardMaterial({ vertexColors: true, metalness: 0.25, roughness: 0.5 });
      });

      const box = new THREE.Box3().setFromObject(model);
      const size = box.getSize(new THREE.Vector3());
      const center = box.getCenter(new THREE.Vector3());
      model.position.sub(center);
      scene.add(model);

      const maxDim = Math.max(size.x, size.y, size.z);
      const dist = maxDim / (2 * Math.tan((Math.PI * camera.fov) / 360));
      camera.position.set(0, size.y * 0.05, dist * 1.55);
      controls.target.set(0, 0, 0);
      controls.minDistance = dist * 0.6;
      controls.maxDistance = dist * 3.5;
      controls.update();

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

  // Auto-carga inmediata (el botón queda como fallback manual).
  start();
}

document.querySelectorAll('[data-model-viewer]').forEach(initViewer);
