# import json
# import random
# import argparse
# from pathlib import Path
# from PIL import Image


# # =========================================================
# # CONFIG DEFAULTS
# # =========================================================
# NUM_IMAGES = 10000
# MIN_CHAMPS = 1
# MAX_CHAMPS = 10
# SPRITE_SCALE = 0.12
# SEED = None
# TRAIN_SPLIT = 0.8
# # =========================================================


# def to_yolo(bbox, img_w, img_h):
#     x1, y1, x2, y2 = bbox

#     x_center = ((x1 + x2) / 2) / img_w
#     y_center = ((y1 + y2) / 2) / img_h
#     w = (x2 - x1) / img_w
#     h = (y2 - y1) / img_h

#     return x_center, y_center, w, h


# def load_centers(path):
#     with open(path, "r", encoding="utf-8") as f:
#         return json.load(f)["centers"]


# def load_sprites(sprite_dir):
#     return list(sprite_dir.glob("*.png"))


# def paste_sprite(board, sprite_path, center):
#     cx, cy = center

#     tile = Image.open(sprite_path).convert("RGBA")

#     max_h = int(board.height * SPRITE_SCALE)

#     if tile.height > max_h:
#         scale = max_h / tile.height
#         tile = tile.resize(
#             (int(tile.width * scale), int(tile.height * scale)),
#             Image.LANCZOS
#         )

#     w, h = tile.size

#     x = int(round(cx - w / 2))
#     y = int(round(cy - h / 2))

#     board.paste(tile, (x, y), tile)

#     return {
#         "sprite": sprite_path.name,
#         "bbox": [x, y, x + w, y + h]
#     }


# def generate_board(bg_path, centers, sprites, min_c, max_c):
#     board = Image.open(bg_path).convert("RGBA")

#     max_c = min(max_c, len(centers))
#     n = random.randint(min_c, max_c)

#     chosen_centers = random.sample(centers, n)
#     chosen_sprites = random.choices(sprites, k=n)

#     placements = []

#     for s, c in zip(chosen_sprites, chosen_centers):
#         placements.append(paste_sprite(board, s, c))

#     return board, placements


# def write_yolo_labels(label_path, placements, class_map, img_size):
#     img_w, img_h = img_size

#     lines = []

#     for obj in placements:
#         cls = class_map[obj["sprite"]]
#         x, y, w, h = to_yolo(obj["bbox"], img_w, img_h)
#         lines.append(f"{cls} {x:.6f} {y:.6f} {w:.6f} {h:.6f}")

#     with open(label_path, "w") as f:
#         f.write("\n".join(lines))


# def main():
#     parser = argparse.ArgumentParser()

#     parser.add_argument("--num-images", type=int, default=None)
#     parser.add_argument("--min-champs", type=int, default=None)
#     parser.add_argument("--max-champs", type=int, default=None)
#     parser.add_argument("--seed", type=int, default=None)
#     parser.add_argument("--output-dir", default="yolo_dataset")

#     args = parser.parse_args()

#     num_images = args.num_images or NUM_IMAGES
#     min_champs = args.min_champs or MIN_CHAMPS
#     max_champs = args.max_champs or MAX_CHAMPS
#     seed = args.seed or SEED

#     if seed is not None:
#         random.seed(seed)

#     repo = Path(__file__).resolve().parent

#     centers_path = repo / "finding_hexes" / "center_points.json"
#     bg_path = repo / "boards" / "default.png"
#     sprite_dir = repo / "sprites"

#     centers = load_centers(centers_path)
#     sprite_paths = load_sprites(sprite_dir)

#     output_dir = repo / args.output_dir

#     # clean dataset each run (IMPORTANT)
#     if output_dir.exists():
#         for p in output_dir.rglob("*"):
#             if p.is_file():
#                 p.unlink()

#     output_dir.mkdir(parents=True, exist_ok=True)

#     # -------------------------
#     # CLASS MAP
#     # -------------------------
#     sprite_names = sorted([p.name for p in sprite_paths])
#     class_map = {name: i for i, name in enumerate(sprite_names)}

#     with open(output_dir / "classes.json", "w") as f:
#         json.dump(class_map, f, indent=2)

#     # create folders
#     train_img_dir = output_dir / "images/train"
#     val_img_dir = output_dir / "images/val"
#     train_lbl_dir = output_dir / "labels/train"
#     val_lbl_dir = output_dir / "labels/val"

#     for d in [train_img_dir, val_img_dir, train_lbl_dir, val_lbl_dir]:
#         d.mkdir(parents=True, exist_ok=True)

#     split_idx = int(num_images * TRAIN_SPLIT)

#     print(f"Generating {num_images} images...")

#     for i in range(num_images):

#         board, placements = generate_board(
#             bg_path,
#             centers,
#             sprite_paths,
#             min_champs,
#             max_champs
#         )

#         filename = f"board_{i:05d}.png"

#         if i < split_idx:
#             img_path = train_img_dir / filename
#             label_path = train_lbl_dir / filename.replace(".png", ".txt")
#         else:
#             img_path = val_img_dir / filename
#             label_path = val_lbl_dir / filename.replace(".png", ".txt")

#         board.save(img_path)

#         write_yolo_labels(
#             label_path,
#             placements,
#             class_map,
#             board.size
#         )

#         print(f"[{i+1}/{num_images}] saved {filename}")

#     # -------------------------
#     # data.yaml
#     # -------------------------
#     yaml_text = f"""path: {output_dir}
# train: images/train
# val: images/val

# names:
# """

#     for name, idx in class_map.items():
#         yaml_text += f"  {idx}: {name.replace('.png','')}\n"

#     with open(output_dir / "data.yaml", "w") as f:
#         f.write(yaml_text)

#     print("\nDONE")
#     print(f"Dataset saved to: {output_dir}")


# if __name__ == "__main__":
#     main()

import json
import random
import argparse
from pathlib import Path
from PIL import Image

# =========================================================
# CONFIG DEFAULTS
# =========================================================
NUM_IMAGES = 10000
MIN_CHAMPS = 1
MAX_CHAMPS = 10
SPRITE_SCALE = 0.12
SEED = None
TRAIN_SPLIT = 0.8
# =========================================================


def to_yolo(bbox, img_w, img_h):
    x1, y1, x2, y2 = bbox

    x_center = ((x1 + x2) / 2) / img_w
    y_center = ((y1 + y2) / 2) / img_h
    w = (x2 - x1) / img_w
    h = (y2 - y1) / img_h

    return x_center, y_center, w, h


# =========================
# NORMALIZED LOAD
# =========================
def load_centers(path):
    with open(path, "r", encoding="utf-8") as f:
        data = json.load(f)

    centers = data["centers"]

    # ensure format: [[x_norm, y_norm], ...]
    cleaned = []
    for c in centers:
        if isinstance(c, dict):
            cleaned.append([c["x_norm"], c["y_norm"]])
        else:
            cleaned.append(c)

    return cleaned


def load_sprites(sprite_dir):
    return list(sprite_dir.glob("*.png"))


# =========================
# NORMALIZED → PIXEL HERE
# =========================
def paste_sprite(board, sprite_path, center_norm):
    cx_norm, cy_norm = center_norm

    # convert to pixel space
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

    w, h = tile.size

    x = int(round(cx - w / 2))
    y = int(round(cy - h / 2))

    board.paste(tile, (x, y), tile)

    return {
        "sprite": sprite_path.name,
        "bbox": [x, y, x + w, y + h]
    }


def generate_board(bg_path, centers, sprites, min_c, max_c):
    board = Image.open(bg_path).convert("RGBA")

    max_c = min(max_c, len(centers))
    n = random.randint(min_c, max_c)

    chosen_centers = random.sample(centers, n)
    chosen_sprites = random.choices(sprites, k=n)

    placements = []

    for s, c in zip(chosen_sprites, chosen_centers):
        placements.append(paste_sprite(board, s, c))

    return board, placements


def write_yolo_labels(label_path, placements, class_map, img_size):
    img_w, img_h = img_size

    lines = []

    for obj in placements:
        cls = class_map[obj["sprite"]]
        x, y, w, h = to_yolo(obj["bbox"], img_w, img_h)
        lines.append(f"{cls} {x:.6f} {y:.6f} {w:.6f} {h:.6f}")

    with open(label_path, "w") as f:
        f.write("\n".join(lines))


# =========================
# MAIN
# =========================
def main():
    parser = argparse.ArgumentParser()

    parser.add_argument("--num-images", type=int, default=None)
    parser.add_argument("--min-champs", type=int, default=None)
    parser.add_argument("--max-champs", type=int, default=None)
    parser.add_argument("--seed", type=int, default=None)
    parser.add_argument("--output-dir", default="yolo_dataset")

    args = parser.parse_args()

    num_images = args.num_images or NUM_IMAGES
    min_champs = args.min_champs or MIN_CHAMPS
    max_champs = args.max_champs or MAX_CHAMPS
    seed = args.seed or SEED

    if seed is not None:
        random.seed(seed)

    repo = Path(__file__).resolve().parent

    centers_path = repo / "center_points_normalized.json"
    bg_path = repo / "boards" / "default.png"
    sprite_dir = repo / "sprites"

    centers = load_centers(centers_path)
    sprite_paths = load_sprites(sprite_dir)

    output_dir = repo / args.output_dir

    if output_dir.exists():
        for p in output_dir.rglob("*"):
            if p.is_file():
                p.unlink()

    output_dir.mkdir(parents=True, exist_ok=True)

    sprite_names = sorted([p.name for p in sprite_paths])
    class_map = {name: i for i, name in enumerate(sprite_names)}

    with open(output_dir / "classes.json", "w") as f:
        json.dump(class_map, f, indent=2)

    train_img_dir = output_dir / "images/train"
    val_img_dir = output_dir / "images/val"
    train_lbl_dir = output_dir / "labels/train"
    val_lbl_dir = output_dir / "labels/val"

    for d in [train_img_dir, val_img_dir, train_lbl_dir, val_lbl_dir]:
        d.mkdir(parents=True, exist_ok=True)

    split_idx = int(num_images * TRAIN_SPLIT)

    print(f"Generating {num_images} images...")

    for i in range(num_images):

        board, placements = generate_board(
            bg_path,
            centers,
            sprite_paths,
            min_champs,
            max_champs
        )

        filename = f"board_{i:05d}.png"

        if i < split_idx:
            img_path = train_img_dir / filename
            label_path = train_lbl_dir / filename.replace(".png", ".txt")
        else:
            img_path = val_img_dir / filename
            label_path = val_lbl_dir / filename.replace(".png", ".txt")

        board.save(img_path)

        write_yolo_labels(
            label_path,
            placements,
            class_map,
            board.size
        )

        print(f"[{i+1}/{num_images}] saved {filename}")

    yaml_text = f"""path: {output_dir}
train: images/train
val: images/val

names:
"""

    for name, idx in class_map.items():
        yaml_text += f"  {idx}: {name.replace('.png','')}\n"

    with open(output_dir / "data.yaml", "w") as f:
        f.write(yaml_text)

    print("\nDONE")
    print(f"Dataset saved to: {output_dir}")


if __name__ == "__main__":
    main()