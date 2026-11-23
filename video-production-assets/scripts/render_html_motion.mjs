#!/usr/bin/env node
// Deterministic HTML motion renderer: installed Chrome (CDP) + ffmpeg, no npm dependencies.
//
// Piece contract: index.html exposes
//   window.__motion = { width, height, fps, duration, seek(t) }
// where seek(t) sets the whole frame from time t (seconds) alone. No network requests.
//
// Usage:
//   node render_html_motion.mjs PIECE.html OUT.mp4 [--frames A:B] [--contact-sheet N]
//        [--audio APPROVED.wav] [--verify-frames K] [--chrome PATH]
// Writes OUT.mp4, OUT.render-report.json and, with --contact-sheet, OUT.contact.png.
// Exit 0 on success; non-zero with a reason on stderr. A failed run leaves no OUT.mp4.

import { spawn, execFileSync } from 'node:child_process';
import { createHash } from 'node:crypto';
import { mkdtempSync, rmSync, writeFileSync, readFileSync, renameSync, existsSync, mkdirSync } from 'node:fs';
import { tmpdir } from 'node:os';
import { join, resolve, dirname, basename, extname } from 'node:path';
import { pathToFileURL } from 'node:url';

function fail(message) {
  const error = new Error(message);
  error.userFacing = true;
  throw error;
}

function parseArgs(argv) {
  const args = { positional: [], verify: 4, contact: 0, frames: null, audio: null, chrome: null };
  for (let i = 0; i < argv.length; i++) {
    const flag = argv[i];
    const next = () => { if (i + 1 >= argv.length) fail(`missing value for ${flag}`); return argv[++i]; };
    if (flag === '--frames') {
      const [a, b] = next().split(':').map(Number);
      if (!Number.isInteger(a) || !Number.isInteger(b) || a < 0 || b <= a) fail('--frames needs A:B with 0 <= A < B');
      args.frames = [a, b];
    } else if (flag === '--contact-sheet') args.contact = Number(next());
    else if (flag === '--verify-frames') args.verify = Number(next());
    else if (flag === '--audio') args.audio = resolve(next());
    else if (flag === '--chrome') args.chrome = next();
    else if (flag.startsWith('--')) fail(`unknown option ${flag}`);
    else args.positional.push(flag);
  }
  if (args.positional.length !== 2) fail('usage: render_html_motion.mjs PIECE.html OUT.mp4 [options]');
  return args;
}

function findChrome(explicit) {
  const candidates = [explicit, process.env.CHROME_PATH, 'google-chrome', 'google-chrome-stable', 'chromium', 'chromium-browser'];
  for (const name of candidates.filter(Boolean)) {
    try {
      const path = name.includes('/') ? name : execFileSync('which', [name], { encoding: 'utf8' }).trim();
      if (path && existsSync(path)) return path;
    } catch { /* try next */ }
  }
  fail('Chrome not found; pass --chrome PATH');
}

const sha256 = (data) => createHash('sha256').update(data).digest('hex');

async function launch(chromePath, profile) {
  const chrome = spawn(chromePath, [
    '--headless=new', '--remote-debugging-port=0', `--user-data-dir=${profile}`, '--disable-gpu',
    '--hide-scrollbars', '--force-device-scale-factor=1', '--no-first-run', '--no-default-browser-check',
    '--font-render-hinting=none', '--disable-extensions', '--mute-audio', 'about:blank',
  ], { stdio: ['ignore', 'ignore', 'pipe'] });
  const endpoint = await new Promise((resolveEndpoint, reject) => {
    let buffer = '';
    const timer = setTimeout(() => reject(new Error('Chrome did not start')), 20000);
    chrome.stderr.on('data', (chunk) => {
      buffer += chunk;
      const match = buffer.match(/DevTools listening on (ws:\/\/[^\s]+)/);
      if (match) { clearTimeout(timer); resolveEndpoint(match[1]); }
    });
    chrome.on('exit', (code) => reject(new Error(`Chrome exited early (${code})`)));
  });
  return { chrome, port: new URL(endpoint).port };
}

class Session {
  constructor(url) {
    this.ws = new WebSocket(url);
    this.id = 0;
    this.pending = new Map();
    this.listeners = [];
    this.ws.onmessage = (event) => {
      const message = JSON.parse(event.data);
      if (message.id && this.pending.has(message.id)) {
        const { ok, ko } = this.pending.get(message.id);
        this.pending.delete(message.id);
        message.error ? ko(new Error(`${message.error.message}`)) : ok(message.result);
      } else if (message.method) {
        for (const listener of this.listeners) listener(message);
      }
    };
  }
  open() { return new Promise((ok, ko) => { this.ws.onopen = ok; this.ws.onerror = () => ko(new Error('CDP connection failed')); }); }
  send(method, params = {}) {
    const id = ++this.id;
    this.ws.send(JSON.stringify({ id, method, params }));
    return new Promise((ok, ko) => this.pending.set(id, { ok, ko }));
  }
  on(listener) { this.listeners.push(listener); }
  waitFor(method, timeout = 30000) {
    return new Promise((ok, ko) => {
      const timer = setTimeout(() => ko(new Error(`timeout waiting for ${method}`)), timeout);
      this.on((message) => { if (message.method === method) { clearTimeout(timer); ok(message.params); } });
    });
  }
  close() { this.ws.close(); }
}

async function evaluate(session, expression) {
  const result = await session.send('Runtime.evaluate', { expression, awaitPromise: true, returnByValue: true });
  if (result.exceptionDetails) fail(`page error: ${result.exceptionDetails.exception?.description || result.exceptionDetails.text}`);
  return result.result.value;
}

async function capture(session, frame, fps) {
  await evaluate(session, `(async () => { window.__motion.seek(${frame} / ${fps});
    await new Promise((r) => requestAnimationFrame(() => requestAnimationFrame(r))); return true; })()`);
  const shot = await session.send('Page.captureScreenshot', { format: 'png', fromSurface: true, captureBeyondViewport: false });
  return Buffer.from(shot.data, 'base64');
}

function spread(count, first, last) {
  if (count <= 1 || last <= first) return [first];
  const picks = new Set();
  for (let j = 0; j < count; j++) picks.add(first + Math.round((j * (last - first)) / (count - 1)));
  return [...picks];
}

function probeDuration(path) {
  const out = execFileSync('ffprobe', ['-v', 'error', '-show_entries', 'format=duration', '-of', 'csv=p=0', path], { encoding: 'utf8' });
  return Number(out.trim());
}

async function main() {
  const args = parseArgs(process.argv.slice(2));
  const piece = resolve(args.positional[0]);
  const output = resolve(args.positional[1]);
  if (!existsSync(piece)) fail(`piece not found: ${piece}`);
  const stem = join(dirname(output), basename(output, extname(output)));
  const started = Date.now();
  const profile = mkdtempSync(join(tmpdir(), 'html-motion-'));
  const { chrome, port } = await launch(findChrome(args.chrome), profile);
  let session;
  let work;
  const blocked = [];
  try {
    const versions = await (await fetch(`http://127.0.0.1:${port}/json/version`)).json();
    const target = await (await fetch(`http://127.0.0.1:${port}/json/new?about:blank`, { method: 'PUT' })).json();
    session = new Session(target.webSocketDebuggerUrl);
    await session.open();
    session.on((message) => {
      if (message.method !== 'Fetch.requestPaused') return;
      const { requestId, request } = message.params;
      if (/^(file|data|blob):/.test(request.url)) session.send('Fetch.continueRequest', { requestId });
      else { blocked.push(request.url); session.send('Fetch.failRequest', { requestId, errorReason: 'BlockedByClient' }); }
    });
    await session.send('Fetch.enable', { patterns: [{ urlPattern: '*' }] });
    await session.send('Page.enable');
    await session.send('Runtime.enable');
    const loaded = session.waitFor('Page.loadEventFired');
    await session.send('Page.navigate', { url: pathToFileURL(piece).href });
    await loaded;
    const spec = await evaluate(session, `(() => { const m = window.__motion;
      if (!m || typeof m.seek !== 'function') return null;
      return { width: m.width, height: m.height, fps: m.fps, duration: m.duration }; })()`);
    if (!spec) fail('piece does not expose window.__motion = {width, height, fps, duration, seek(t)}');
    for (const key of ['width', 'height', 'fps', 'duration']) {
      if (!(Number.isFinite(spec[key]) && spec[key] > 0)) fail(`window.__motion.${key} must be a positive number`);
    }
    if (!Number.isInteger(spec.width) || !Number.isInteger(spec.height) || spec.width % 2 || spec.height % 2) {
      fail('window.__motion width and height must be even integers');
    }
    await session.send('Emulation.setDeviceMetricsOverride', { width: spec.width, height: spec.height, deviceScaleFactor: 1, mobile: false });
    await evaluate(session, 'document.fonts.ready.then(() => true)');
    if (blocked.length) fail(`network requests are not allowed: ${blocked.join(', ')}`);

    const total = Math.round(spec.duration * spec.fps);
    const [first, last] = args.frames ?? [0, total];
    if (last > total) fail(`--frames end ${last} exceeds ${total} frames`);
    if (args.audio && args.frames) fail('--audio needs a full render, not a frame range');

    const checks = args.verify > 0 ? spread(args.verify, first, last - 1) : [];
    const forward = new Map();
    for (const frame of checks) forward.set(frame, sha256(await capture(session, frame, spec.fps)));
    for (const frame of [...checks].reverse()) {
      if (sha256(await capture(session, frame, spec.fps)) !== forward.get(frame)) fail(`nondeterministic frame ${frame}: seek(t) must depend on t alone`);
    }

    work = mkdtempSync(join(dirname(output), '.html-motion-'));
    const temp = join(work, 'video.mp4');
    const encode = spawn('ffmpeg', ['-v', 'error', '-y', '-f', 'image2pipe', '-framerate', String(spec.fps), '-c:v', 'png', '-i', '-',
      '-c:v', 'libx264', '-pix_fmt', 'yuv420p', '-r', String(spec.fps), '-movflags', '+faststart', temp], { stdio: ['pipe', 'ignore', 'pipe'] });
    let encodeError = '';
    encode.stderr.on('data', (chunk) => { encodeError += chunk; });
    const encoded = new Promise((ok) => encode.on('close', ok));
    const sheetFrames = args.contact > 0 ? new Set(spread(args.contact, first, last - 1)) : new Set();
    const sheetDir = join(work, 'sheet');
    mkdirSync(sheetDir);
    let sheetIndex = 0;
    for (let frame = first; frame < last; frame++) {
      const png = await capture(session, frame, spec.fps);
      if (blocked.length) fail(`network requests are not allowed: ${blocked.join(', ')}`);
      if (sheetFrames.has(frame)) writeFileSync(join(sheetDir, `${String(sheetIndex++).padStart(4, '0')}.png`), png);
      if (!encode.stdin.write(png)) await new Promise((ok) => encode.stdin.once('drain', ok));
    }
    encode.stdin.end();
    if ((await encoded) !== 0) fail(`ffmpeg encode failed: ${encodeError.trim()}`);

    let final = temp;
    if (args.audio) {
      const audioSeconds = probeDuration(args.audio);
      const videoSeconds = total / spec.fps;
      if (Math.abs(audioSeconds - videoSeconds) > 1 / spec.fps) {
        fail(`audio duration ${audioSeconds.toFixed(3)}s does not match video ${videoSeconds.toFixed(3)}s`);
      }
      final = join(work, 'muxed.mp4');
      execFileSync('ffmpeg', ['-v', 'error', '-y', '-i', temp, '-i', args.audio, '-map', '0:v', '-map', '1:a',
        '-c:v', 'copy', '-c:a', 'aac', '-b:a', '192k', '-movflags', '+faststart', final]);
    }
    if (sheetIndex) {
      const columns = Math.min(sheetIndex, 4);
      const rows = Math.ceil(sheetIndex / columns);
      const scale = Math.min(1, 480 / spec.width);
      execFileSync('ffmpeg', ['-v', 'error', '-y', '-framerate', '1', '-i', join(sheetDir, '%04d.png'), '-vf',
        `scale=${Math.round(spec.width * scale / 2) * 2}:-2,tile=${columns}x${rows}:padding=4`, '-frames:v', '1', `${stem}.contact.png`]);
    }
    renameSync(final, output);
    const report = {
      input_sha256: sha256(readFileSync(piece)), output: output, output_sha256: sha256(readFileSync(output)),
      frames: last - first, frame_range: [first, last], total_frames: total, fps: spec.fps, width: spec.width, height: spec.height,
      duration: spec.duration, audio: args.audio ? { path: args.audio, sha256: sha256(readFileSync(args.audio)) } : null,
      chrome: versions.Browser, ffmpeg: execFileSync('ffmpeg', ['-version'], { encoding: 'utf8' }).split('\n')[0],
      determinism: { checked: checks.length, pass: true }, contact_sheet: sheetIndex ? `${stem}.contact.png` : null,
      seconds: Math.round((Date.now() - started) / 100) / 10,
    };
    writeFileSync(`${stem}.render-report.json`, `${JSON.stringify(report, null, 2)}\n`);
    console.log(JSON.stringify({ output, frames: report.frames, output_sha256: report.output_sha256 }));
  } finally {
    session?.close();
    if (work) rmSync(work, { recursive: true, force: true });
    chrome.kill('SIGKILL');
    rmSync(profile, { recursive: true, force: true });
  }
}

main().catch((error) => {
  console.error(error.userFacing ? error.message : error.stack);
  process.exit(1);
});
