import json
import random
import argparse
from pathlib import Path
from PIL import Image

# =========================================================
# CONFIG
# =========================================================

NUM_BOARDS = 30
MIN_CHAMPS = 1
MAX_CHAMPS = 10

SPRITE_SCALE = 0.12
OUTPUT_DIR = "generated_boards"
SEED = None
# =========================================================


def load_centers(path):
    with open(path, "r", encoding="utf-8") as f:
        data = json.load(f)

    centers = data.get("centers", [])
    if not centers:
        raise ValueError("No centers found in center_points.json")

    # centers are now normalized: [x_norm, y_norm]
    return centers


def load_sprites(sprite_dir):
    sprite_paths = list(sprite_dir.glob("*.png"))
    if not sprite_paths:
        raise ValueError(f"No PNG sprites found in {sprite_dir}")
    return sprite_paths


def paste_sprite(board, sprite_path, center_norm):
    # -------------------------
    # convert normalized -> pixel
    # -------------------------
    cx_norm, cy_norm = center_norm
    cx = cx_norm * board.width
    cy = cy_norm * board.height

    tile = Image.open(sprite_path).convert("RGBA")

    max_h = int(board.height * SPRITE_SCALE)

    if tile.height > max_h:
        scale = max_h / tile.height
        tile = tile.resize(
            (int(tile.width * scale), int(tile.height * scale)),
            Image.LANCZOS
        )

    tile_w, tile_h = tile.size

    paste_x = int(round(cx - tile_w / 2))
    paste_y = int(round(cy - tile_h / 2))

    board.paste(tile, (paste_x, paste_y), tile)

    return {
        "sprite": sprite_path.name,
        "center_norm": [cx_norm, cy_norm],
        "bbox": [
            paste_x,
            paste_y,
            paste_x + tile_w,
            paste_y + tile_h
        ]
    }


def generate_board(bg_path, centers, sprite_paths):
    board = Image.open(bg_path).convert("RGBA")

    max_champs_safe = min(MAX_CHAMPS, len(centers))
    num_champs = random.randint(MIN_CHAMPS, max_champs_safe)

    chosen_centers = random.sample(centers, num_champs)
    chosen_sprites = random.choices(sprite_paths, k=num_champs)

    placements = []

    for sprite_path, center in zip(chosen_sprites, chosen_centers):
        placements.append(paste_sprite(board, sprite_path, center))

    return board, placements


def main():
    parser = argparse.ArgumentParser()

    parser.add_argument("--num-boards", type=int, default=None)
    parser.add_argument("--min-champs", type=int, default=None)
    parser.add_argument("--max-champs", type=int, default=None)
    parser.add_argument("--seed", type=int, default=None)

    args = parser.parse_args()

    num_boards = args.num_boards or NUM_BOARDS
    min_champs = args.min_champs or MIN_CHAMPS
    max_champs = args.max_champs or MAX_CHAMPS
    seed = args.seed if args.seed is not None else SEED

    if seed is not None:
        random.seed(seed)

    repo = Path(__file__).resolve().parent

    # ✅ IMPORTANT CHANGE: use normalized file
    centers_path = repo / "center_points_normalized.json"

    bg_path = repo / "boards" / "default.png"
    sprite_dir = repo / "sprites"

    centers = load_centers(centers_path)
    sprite_paths = load_sprites(sprite_dir)

    output_dir = repo / OUTPUT_DIR
    output_dir.mkdir(parents=True, exist_ok=True)

    labels = []

    for i in range(num_boards):
        board, placements = generate_board(
            bg_path,
            centers,
            sprite_paths
        )

        filename = f"board_{i:05d}.png"
        save_path = output_dir / filename

        board.save(save_path)

        labels.append({
            "image": filename,
            "placements": placements
        })

        print(f"[{i+1}/{num_boards}] saved {filename}")

    with open(output_dir / "labels.json", "w", encoding="utf-8") as f:
        json.dump(labels, f, indent=2)

    print(f"\nDone -> {output_dir}")


if __name__ == "__main__":
    main()