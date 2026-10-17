// Browser-only deterministic thumbnail overlay. No generation or remote submission.
export async function bake({src, lines, W, H, preset = 'beast', fontFamily,
  fontWeight, stylesheet, strokeRatio, out = 'baked.png', download = true}) {
  const presets = ['beast', 'fire', 'neon-lime', 'clean-glass', 'marker'];
  if (!presets.includes(preset)) throw new RangeError(`Unknown overlay preset: ${preset}`);
  if (!Number.isInteger(W) || !Number.isInteger(H) || W <= 0 || H <= 0)
    throw new RangeError('W and H must be positive integer pixel dimensions');
  if (!Array.isArray(lines) || !lines.length || lines.some(line => typeof line.text !== 'string' || !line.text.trim()))
    throw new TypeError('Each headline line requires nonblank text');
  fontFamily ??= preset === 'clean-glass' ? 'Inter' : 'Anton';
  fontWeight ??= preset === 'clean-glass' ? 800 : 400;
  stylesheet ??= fontFamily === 'Anton'
    ? 'https://fonts.googleapis.com/css2?family=Anton&display=swap'
    : fontFamily === 'Inter' ? 'https://fonts.googleapis.com/css2?family=Inter:wght@800&display=swap' : undefined;
  const fontPx = Math.round(H * 0.16);
  const font = `${fontWeight} ${fontPx}px "${fontFamily}"`;
  if (stylesheet) {
    const link = document.createElement('link');
    link.rel = 'stylesheet';
    link.href = stylesheet;
    await new Promise((resolve, reject) => {
      link.onload = resolve;
      link.onerror = () => reject(new Error(`Font stylesheet failed: ${stylesheet}`));
      document.head.appendChild(link);
    });
  }
  // CSS must arrive before FontFaceSet.load; otherwise an undeclared face can resolve as fallback.
  const faces = await document.fonts.load(font, lines.map(line => line.text).join(' '));
  await document.fonts.ready;
  if (!document.fonts.check(font)) throw new Error(`Requested font is not ready: ${fontFamily}`);
  const image = new Image();
  image.crossOrigin = 'anonymous';
  await new Promise((resolve, reject) => {
    image.onload = resolve;
    image.onerror = () => reject(new Error('Background image could not be loaded'));
    image.src = src;
  });
  const canvas = document.createElement('canvas');
  canvas.width = W;
  canvas.height = H;
  const ctx = canvas.getContext('2d');
  if (!ctx) throw new Error('Canvas 2D is unavailable');
  const scale = Math.max(W / image.naturalWidth, H / image.naturalHeight);
  const dw = image.naturalWidth * scale, dh = image.naturalHeight * scale;
  ctx.drawImage(image, (W - dw) / 2, (H - dh) / 2, dw, dh);
  // Preserve the unlettered background for each glass pill's real backdrop sample.
  let backdrop;
  if (preset === 'clean-glass') {
    backdrop = document.createElement('canvas');
    backdrop.width = W; backdrop.height = H;
    backdrop.getContext('2d').drawImage(canvas, 0, 0);
  }
  ctx.font = font;
  ctx.textAlign = 'center';
  ctx.textBaseline = 'alphabetic';
  ctx.letterSpacing = `${-0.01 * fontPx}px`;
  const lineH = fontPx * 1.16;
  const cx = W / 2;
  let y = H * 0.90 - (lines.length - 1) * lineH;
  for (const line of lines) {
    const metrics = ctx.measureText(line.text);
    const ascent = metrics.actualBoundingBoxAscent;
    const descent = metrics.actualBoundingBoxDescent;
    const paddingX = fontPx * (preset === 'clean-glass' ? 0.5 : 0.18);
    const paddingY = fontPx * 0.12;
    const x = cx - metrics.width / 2 - paddingX;
    const top = y - ascent - paddingY;
    const width = metrics.width + 2 * paddingX;
    const height = ascent + descent + 2 * paddingY;
    if (x < W * 0.03 || x + width > W * 0.97 || top < H * 0.03 || top + height > H * 0.97)
      throw new RangeError('Headline exceeds safe frame bounds; revise text, line breaks or dimensions');
    if (preset === 'clean-glass' || preset === 'marker') {
      ctx.save();
      ctx.shadowColor = 'rgba(0,0,0,.5)';
      ctx.shadowBlur = preset === 'clean-glass' ? H * 0.035 : 0;
      ctx.shadowOffsetY = H * 0.012;
      ctx.fillStyle = preset === 'marker' ? '#D4FF3F' : 'rgba(20,20,25,.45)';
      ctx.beginPath();
      ctx.roundRect(x, top, width, height, preset === 'clean-glass' ? fontPx * 0.2 : 0);
      ctx.fill();
      ctx.restore();
      if (backdrop) {
        ctx.save();
        ctx.beginPath(); ctx.roundRect(x, top, width, height, fontPx * 0.2); ctx.clip();
        ctx.filter = `blur(${H * 16 / 720}px)`;
        ctx.drawImage(backdrop, 0, 0);
        ctx.filter = 'none';
        ctx.fillStyle = 'rgba(20,20,25,.45)'; ctx.fillRect(x, top, width, height);
        ctx.restore();
      }
    } else {
      ctx.save();
      const strokeWidth = fontPx * (strokeRatio ?? (preset === 'neon-lime' ? 0.1 : 0.11));
      if (strokeWidth > 0) ctx.lineWidth = strokeWidth;
      ctx.lineJoin = 'round';
      ctx.strokeStyle = preset === 'fire' ? '#1a0a00' : preset === 'neon-lime' ? '#0a1400' : '#000';
      ctx.shadowColor = preset === 'fire' ? 'rgba(255,120,0,.55)' : preset === 'neon-lime' ? 'rgba(180,255,40,.7)' : 'rgba(0,0,0,.55)';
      ctx.shadowBlur = H * (preset === 'beast' ? 0.033 : 0.036);
      ctx.shadowOffsetY = preset === 'neon-lime' ? 0 : H * 0.019;
      if (strokeWidth > 0) ctx.strokeText(line.text, cx, y);
      ctx.restore();
    }
    const gradient = line.gradient ?? (preset === 'fire' ? [[0, '#FFE24B'], [0.45, '#FF9A1F'], [1, '#FF2E2E']] : null);
    if (gradient) {
      const fill = ctx.createLinearGradient(0, y - fontPx, 0, y);
      for (const [stop, color] of gradient) fill.addColorStop(stop, color);
      ctx.fillStyle = fill;
    } else ctx.fillStyle = line.color ?? (preset === 'marker' ? '#0a0a0a' : preset === 'neon-lime' ? '#D4FF3F' : '#fff');
    ctx.fillText(line.text, cx, y);
    y += lineH;
  }
  // SecurityError is intentionally propagated; null is an export failure, not a PNG.
  const blob = await new Promise((resolve, reject) => canvas.toBlob(
    value => value ? resolve(value) : reject(new Error('PNG export returned a null blob')), 'image/png'));
  if (download) {
    const url = URL.createObjectURL(blob);
    const anchor = document.createElement('a');
    anchor.download = out; anchor.href = url; anchor.click();
    setTimeout(() => URL.revokeObjectURL(url), 1000);
  }
  return {blob, canvas, preset, fontFamily, fontWeight,
    loadedFaces: faces.map(face => ({family: face.family, status: face.status}))};
}
