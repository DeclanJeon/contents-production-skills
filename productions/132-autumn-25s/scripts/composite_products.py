"""Composite supplied product photographs over generated plates; preserve label artwork."""
import hashlib
import json
from pathlib import Path

from PIL import Image, ImageDraw, ImageFilter, ImageOps

ROOT = Path(__file__).resolve().parents[1]
SIZE = (1080, 1920)


def product(filename, height):
    source = Image.open(ROOT / "references" / filename).convert("RGBA")
    # Exclude near-transparent matte noise from extent, retaining the source alpha inside.
    bbox = source.getchannel("A").point(lambda p: 255 if p >= 64 else 0).getbbox()
    if bbox is None:
        raise ValueError(f"No visible product in {filename}")
    left, top, right, bottom = bbox
    bbox = (max(0, left - 3), max(0, top - 3), min(source.width, right + 3), min(source.height, bottom + 3))
    cut = source.crop(bbox)
    width = round(cut.width * height / cut.height)
    return cut.resize((width, height), Image.Resampling.LANCZOS), bbox


def compose(panel, plate_name, carton_name, bottle_center, bottle_bottom, carton_left, carton_bottom):
    plate = ImageOps.fit(Image.open(ROOT / "images" / plate_name).convert("RGB"), SIZE, method=Image.Resampling.LANCZOS)
    plate.save(ROOT / "images" / f"{panel}_background.png")
    layer = Image.new("RGBA", SIZE)
    bottle, bottle_bbox = product("ampoule-actual.png", 760)
    carton, carton_bbox = product(carton_name, 630)
    bottle_xy = (round(bottle_center - bottle.width / 2), bottle_bottom - bottle.height)
    carton_xy = (carton_left, carton_bottom - carton.height)
    shadow = Image.new("RGBA", SIZE)
    draw = ImageDraw.Draw(shadow)
    for x, y, width in [(carton_xy[0], carton_bottom, carton.width), (bottle_xy[0], bottle_bottom, bottle.width)]:
        draw.ellipse((x - 10, y - 12, x + width + 35, y + 24), fill=(0, 0, 0, 115))
    layer.alpha_composite(shadow.filter(ImageFilter.GaussianBlur(15)))
    layer.alpha_composite(carton, carton_xy)
    layer.alpha_composite(bottle, bottle_xy)
    layer.save(ROOT / "images" / f"{panel}_product_overlay.png")
    composite = Image.alpha_composite(plate.convert("RGBA"), layer).convert("RGB")
    output = ROOT / "images" / ("P01_SH01_hold.png" if panel == "P01" else "P10_SH05_hold.png")
    composite.save(output)
    return {"panel": panel, "plate": plate_name, "carton": carton_name, "bottle_crop": bottle_bbox,
            "carton_crop": carton_bbox, "bottle_xy": bottle_xy, "bottle_size": bottle.size,
            "carton_xy": carton_xy, "carton_size": carton.size, "output": str(output.relative_to(ROOT)),
            "sha256": hashlib.sha256(output.read_bytes()).hexdigest(), "size": SIZE,
            "method": "original supplied RGBA, proportional resize, contact shadow; no redrawn label"}


if __name__ == "__main__":
    records = [
        compose("P01", "P01_SH01_plate.png", "box-side.png", 360, 1260, 445, 1360),
        compose("P10", "P10_SH05_plate-2.png", "box-front.png", 330, 1165, 490, 1300),
    ]
    (ROOT / "qa" / "product-compositing.json").write_text(json.dumps(records, ensure_ascii=False, indent=2), encoding="utf-8")
    print(json.dumps(records, ensure_ascii=False, indent=2))
