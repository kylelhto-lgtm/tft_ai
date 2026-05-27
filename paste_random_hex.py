import json
import random
import argparse
from pathlib import Path
from PIL import Image


def main():
    parser = argparse.ArgumentParser(description="Paste a sprite onto a random hex center from center_points.json")
    parser.add_argument("--sprite", default="chogath.png", help="sprite filename inside sprites/ (default: teemo.png)")
    parser.add_argument("--center-index", type=int, default=None, help="optional index of center to use (0-based)")
    parser.add_argument("--output", default="finding_hexes/generated_images/paste_random_sprite.png", help="output image path")
    args = parser.parse_args()

    repo = Path(__file__).resolve().parent

    centers_file = repo / "finding_hexes" / "center_points.json"
    if not centers_file.exists():
        raise FileNotFoundError(f"center_points.json not found at {centers_file}")

    with centers_file.open("r", encoding="utf-8") as f:
        data = json.load(f)

    centers = data.get("centers") or data.get("centers", [])
    if not centers:
        raise ValueError("No centers found in center_points.json")

    # choose center
    if args.center_index is None:
        cx, cy = random.choice(centers)
    else:
        idx = args.center_index
        if idx < 0 or idx >= len(centers):
            raise IndexError("center-index out of range")
        cx, cy = centers[idx]

    # base/background image
    bg_path = repo / "boards" / "default_hex.png"
    if not bg_path.exists():
        raise FileNotFoundError(f"Background image not found: {bg_path}")

    img = Image.open(bg_path).convert("RGBA")

    # sprite
    sprite_path = repo / "sprites" / args.sprite
    if not sprite_path.exists():
        raise FileNotFoundError(f"Sprite not found: {sprite_path}")

    tile = Image.open(sprite_path).convert("RGBA")

    # scale sprite if too tall relative to board
    max_h = int(img.height * 0.12)
    if tile.height > max_h:
        scale = max_h / tile.height
        tile = tile.resize((int(tile.width * scale), int(tile.height * scale)), Image.LANCZOS)

    tile_w, tile_h = tile.size

    paste_x = int(round(cx - tile_w / 2))
    paste_y = int(round(cy - tile_h / 2))

    img.paste(tile, (paste_x, paste_y), tile)

    out_path = Path(args.output)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    img.save(out_path)

    print(f"Pasted {args.sprite} at ({cx}, {cy}) -> saved {out_path}")


if __name__ == "__main__":
    main()
