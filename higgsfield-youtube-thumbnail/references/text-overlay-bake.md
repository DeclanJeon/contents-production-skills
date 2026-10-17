# MrBeast text overlay & bake (HTML/CSS + canvas)

How to lay a MrBeast-style headline over the image and "bake" it into a flat PNG.
Two layers: (1) a **live HTML/CSS preview** to tune the text in a browser, (2) a
**canvas bake** — outlined/filled text re-rendered at the image's native resolution, with preset-specific effects implemented separately.

This is the implementation recipe for the 5 overlay styles named in the skill's Text policy.
Overlay is the default headline delivery and requires no generation credits, but legibility
still requires actual crop/small-preview inspection. Baked generation text requires an explicit ask.

## What makes text "MrBeast-y"

These six traits are house styling choices, not measured requirements for a creator's style or audience performance:

| Trait | Value | Why |
|---|---|---|
| Font | **Anton** (or Anton SC), one weight, reads `900`-heavy | fat condensed grotesk — the signature |
| Case | **ALL CAPS** | maximum density and aggression |
| Stroke | manual, **thick** (8–14% of cap size), drawn UNDER the fill | separates letters from any background |
| Shadow | hard, dark, offset down, blur shifted | "sticker" depth |
| Color | white / yellow→orange→red gradient / acid lime `#D4FF3F` | punchy contrast, reads in the feed |
| Tracking | tight (`-0.01…-0.02em`), line-height `0.9` | letters lock together like a logo |

Placement rules:
- **2–4 words max.** A headline, not a sentence.
- **Not on the face.** Text in a free quarter (bottom / corner / side).
- **Large.** Cap height 12–18% of frame height. When in doubt, bigger.
- **Margins:** keep text within the frame with comfortable padding, off the extreme edges.

## Layer 1 — live HTML/CSS preview

Feed the background into `--bg`, put the text in `<h1>`, tune it in a browser.

```html
<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<link href="https://fonts.googleapis.com/css2?family=Anton&display=swap" rel="stylesheet">
<style>
  :root {
    --bg: url('photo.jpg');   /* local path or image URL */
    --W: 1280px;              /* frame size (16:9 = 1280×720) */
    --H: 720px;
  }
  * { margin: 0; box-sizing: border-box; }
  #poster {
    position: relative;
    width: var(--W); height: var(--H);
    background: var(--bg) center/cover no-repeat;
    overflow: hidden;
    font-family: 'Anton', sans-serif;
  }
  /* text block — bottom-center, comfortable margin */
  #headline {
    position: absolute;
    left: 50%; bottom: 6%;
    transform: translateX(-50%);
    text-align: center;
    line-height: 0.9;
    letter-spacing: -0.01em;
    text-transform: uppercase;
    white-space: pre-line;         /* line breaks via \n in the text */
  }
  #headline .line {
    font-size: 120px;              /* ≈16% of 720 */
    color: #fff;
    /* CRITICAL: paint-order draws the stroke UNDER the fill — otherwise it eats the letters */
    -webkit-text-stroke: 14px #000;
    paint-order: stroke fill;
    /* hard "sticker" shadow */
    text-shadow: 0 8px 0 rgba(0,0,0,.35), 0 14px 24px rgba(0,0,0,.55);
  }
</style>
</head>
<body>
  <div id="poster">
    <div id="headline">
      <div class="line">I SPENT</div>
      <div class="line" style="color:#D4FF3F">100 DAYS</div>
    </div>
  </div>
</body>
</html>
```

> `paint-order: stroke fill` places the stroke behind the fill. Verify the chosen font/browser result rather than assuming that ordering alone makes text legible.

## 5 house presets (swap the `.line` block) — same 5 as the skill's Text policy

### Beast — white + thick black stroke (default)
```css
.line { color:#fff; -webkit-text-stroke:14px #000; paint-order:stroke fill;
        text-shadow:0 8px 0 rgba(0,0,0,.35), 0 14px 24px rgba(0,0,0,.55); }
```

### Fire — yellow→orange→red gradient
```css
.line { -webkit-text-stroke:14px #1a0a00; paint-order:stroke fill;
        background:linear-gradient(#FFE24B 0%, #FF9A1F 45%, #FF2E2E 100%);
        -webkit-background-clip:text; background-clip:text; color:transparent;
        filter:drop-shadow(0 0 22px rgba(255,120,0,.55)) drop-shadow(0 10px 0 rgba(0,0,0,.4)); }
```

### Neon Lime — acid lime + glow
```css
.line { color:#D4FF3F; -webkit-text-stroke:12px #0a1400; paint-order:stroke fill;
        text-shadow:0 0 26px rgba(180,255,40,.7), 0 10px 0 rgba(0,0,0,.4); }
```

### Clean Glass — Inter 800 on a frosted pill
```css
#headline { font-family:'Inter',sans-serif; }
.line { font-weight:800; color:#fff; letter-spacing:-0.02em;
        background:rgba(20,20,25,.45); backdrop-filter:blur(16px);
        padding:.12em .5em; border-radius:.2em;
        box-shadow:0 20px 60px rgba(0,0,0,.5); }
```

### Marker — black Anton on lime line-boxes
```css
.line { color:#0a0a0a; background:#D4FF3F; box-decoration-break:clone;
        padding:0 .18em; box-shadow:0 8px 0 rgba(0,0,0,.5); }
```

## Layer 2 — bake to PNG (canvas)

The [browser implementation](../scripts/bake-thumbnail.mjs) draws all five presets: outlined Beast, Fire gradient/glow, Neon Lime glow, Clean Glass rounded translucent pills with a blurred background sample, and Marker line boxes. These are deterministic house effects, not pixel-identical copies of another creator's graphics. Serve the package/module over a local HTTP origin; inspect the selected preset and exported PNG. Default Anton/Inter loading uses Google Fonts; an explicitly chosen installed/custom font may instead be supplied. A declared CSS family or successful FontFaceSet check alone does not prove every rendered glyph or prevent fallback.

Load the stylesheet and selected font before drawing; inspect the loaded face and glyph coverage. `document.fonts.load` does not itself validate every glyph.

```html
<script type="module">
import { bake } from '/higgsfield-youtube-thumbnail/scripts/bake-thumbnail.mjs';

const result = await bake({
  src: 'photo.jpg',
  W: 1280, H: 720,
  preset: 'fire', // beast | fire | neon-lime | clean-glass | marker
  lines: [{ text: '100 DAYS' }],
  out: 'baked.png',
});
// result.blob is an actual non-null PNG; result.loadedFaces reports loaded web faces.
// For inspection without a download, pass download:false and show result.canvas.
</script>
```

Mechanics that are easy to forget:
- **`strokeText` before `fillText`** — stroke under fill (the equivalent of `paint-order: stroke fill`).
- **`document.fonts.load(...)` + `await document.fonts.ready`** before the first draw — else the first frame bakes the system font.
- **`lineJoin='round'`** — removes sharp artifacts on the corners of a thick stroke.
- **`img.crossOrigin='anonymous'`** only when the background is a URL; for a local file
  (`<input type=file>` → `URL.createObjectURL`) it isn't needed and CORS doesn't block.
- Draw the shadow inside `save()/restore()`, else `shadowBlur` bleeds onto the fill and smears the color.

## 4K / retina export

For a sharp PNG larger than the preview, compute everything from the image's NATIVE size,
not from the preview viewport:

```js
bake({ src: '4k_render.png', W: 3840, H: 2160, lines: [...] });
```

Cap size, stroke and margins are all tied to `H` (in percent), so at 2160px everything scales itself.

## Font menu (Anton is the default — these are the overrides)

If the user asks for a different font, pick from this menu (all on Google Fonts, so they
load through the same mechanism as Anton). Named font → use it; "something else / not Anton"
→ pick the closest fit below and say which you chose.

**A — Punchy display options (house menu, not a usage ranking)**

| Font | Google Fonts weight | Vibe / use |
|---|---|---|
| Bebas Neue | 400 (reads bold) | tall narrow ALL-CAPS — a house Anton alternative |
| Oswald | 600–700 | condensed grotesk, a touch softer than Anton |
| Archivo Black | 400 (ultra-bold) | blocky, wide, very loud headline |

**B — Bold workhorse options (house menu, not measured popularity)**

| Font | Weight | Vibe / use |
|---|---|---|
| Montserrat | 900 (Black) | clean geometric sans, modern headline |
| Poppins | 800 (ExtraBold) | rounded geometric, friendly |
| Roboto Condensed | 700 (Bold) | neutral condensed workhorse |
| Inter | 800 | modern UI sans (same face as the Clean Glass preset) |
| Barlow Condensed | 800 (ExtraBold) | condensed, energetic |

**C — 5 aesthetic (girls' vlogs / soft-elegant)**

| Font | Weight | Vibe / use |
|---|---|---|
| Playfair Display | 700–900 | elegant high-contrast serif — classic "aesthetic" title |
| Cormorant Garamond | 600–700 | delicate refined serif, editorial feel |
| DM Serif Display | 400 | high-end display serif |
| Fraunces | 600–900 | soft "old-style" serif, trendy |
| Sacramento | 400 (script) | handwritten script — house default: accent/secondary line; verify actual ~120px legibility rather than asserting every script fails |

**How to swap (keep everything else):**
- HTML/CSS: `#headline { font-family: '<Family>', sans-serif; }` and set `.line { font-weight: <w>; }`; update the Google-Fonts `<link>` to that family.
- Canvas: pass `fontFamily`, `fontWeight` and, for a web font, its `stylesheet` URL to `bake`; the implementation awaits the stylesheet event before loading the selected face. Pass `strokeRatio` explicitly for a thinner/no-stroke override.
- Stroke / shadow / `paint-order` / tracking stay as in the presets — only the family (and weight) change.

**Stroke caveat by font class:** heavy condensed faces (Anton, Bebas Neue, Oswald, Archivo Black)
take the full 8–14% stroke. The delicate serifs and the script (Playfair, Cormorant, DM Serif,
Fraunces, Sacramento) CLOG with a thick stroke — drop it to 3–6% (or none) and lean on a soft
drop-shadow for separation instead. Sacramento (and any script) is an accent line, not the punch word.

## Quick check before baking

- [ ] Selected font/style matches the user's request (Anton/ALL CAPS/2–4 words are defaults, not overrides).
- [ ] Stroke matches the selected font: heavy display defaults may use thick outlines; delicate serif/script overrides use the thinner/no-stroke caveat above.
- [ ] Text does **not** cover the face; sits in a free quarter.
- [ ] Text within the frame, off the extreme edges (comfortable padding).
- [ ] One punchy color: white / fire gradient / lime — one per headline.
- [ ] Waited for the font to load before `fillText`.

## Evidence and export limits

Directly read API reference, 2026-10-17: [FontFaceSet.load](https://developer.mozilla.org/en-US/docs/Web/API/FontFaceSet/load) supports awaiting font loading but explicitly does not check individual glyph coverage; [canvas.toBlob](https://developer.mozilla.org/en-US/docs/Web/API/HTMLCanvasElement/toBlob) documents nullable export results and origin-clean restrictions. These contracts do not establish creator-style authenticity, popularity or legibility. Handle a null blob or a security exception as export failure, not a delivered PNG. Inspect the actual exported file at delivery size and the requested crop. The code sample alone is not browser-smoke evidence.

Additional direct reading (2026-10-16 UTC, `READ-PARTIAL`): [HTMLElement load event](https://developer.mozilla.org/en-US/docs/Web/API/HTMLElement/load_event), resource elements and Handling resources that have already loaded; FontFaceSet.load Parameters/Return value; toBlob Parameters/Exceptions. The implementation registers stylesheet load/error handlers before insertion, then awaits the selected font. The local five-preset export exercise used an explicit installed Arial Bold alias, not verified default Anton/Inter delivery; a failed web-font stylesheet remains a hard export error without silent font substitution.
