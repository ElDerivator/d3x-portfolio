// Captura headless vía CDP (sin deps). node 22 trae fetch + WebSocket nativos.
import { writeFileSync } from 'node:fs';

const PORT = 9222;
const URL = process.argv[2] || 'http://localhost:8090/';
const OUT = process.argv[3] || '/tmp/portfolio_hero.png';
const WAIT = Number(process.argv[4] || 8000);

const sleep = (ms) => new Promise(r => setTimeout(r, ms));

// localizar un target de página
let target;
for (let i = 0; i < 20; i++) {
  try {
    const list = await (await fetch(`http://localhost:${PORT}/json`)).json();
    target = list.find(t => t.type === 'page' && t.webSocketDebuggerUrl);
    if (target) break;
  } catch (e) {}
  await sleep(500);
}
if (!target) { console.error('no target'); process.exit(2); }

const ws = new WebSocket(target.webSocketDebuggerUrl);
let id = 0;
const pending = new Map();
const send = (method, params = {}, timeout = 6000) => new Promise((res) => {
  const mid = ++id;
  const to = setTimeout(() => { pending.delete(mid); res(null); }, timeout);
  pending.set(mid, (r) => { clearTimeout(to); res(r); });
  ws.send(JSON.stringify({ id: mid, method, params }));
});
ws.addEventListener('message', (ev) => {
  let m; try { m = JSON.parse(typeof ev.data === 'string' ? ev.data : ev.data.toString()); } catch { return; }
  if (m.id && pending.has(m.id)) { pending.get(m.id)(m.result); pending.delete(m.id); }
});
await new Promise((r) => ws.addEventListener('open', r));

await send('Page.enable');
await send('Emulation.setDeviceMetricsOverride', { width: 1320, height: 960, deviceScaleFactor: 1, mobile: false });
await send('Page.navigate', { url: URL });
await sleep(WAIT); // tiempo real: carga glb + render swiftshader
const shot = await send('Page.captureScreenshot', { format: 'png' }, 20000);
if (shot && shot.data) {
  writeFileSync(OUT, Buffer.from(shot.data, 'base64'));
  console.log('OK', OUT);
} else {
  console.error('sin data'); process.exit(3);
}
ws.close();
process.exit(0);
