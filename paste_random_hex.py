import json
import random
from PIL import Image

# ---- load grid json ----
with open("hexes.json", "r") as f:
    data = json.load(f)

hexes = data["hexes"]

# ---- base image ----
img = Image.open("boards/default_hex.png").convert("RGBA")

# ---- sprite ----
tile = Image.open("sprites/chogath.png").convert("RGBA")
tile_w, tile_h = tile.size

# ---- pick random hex ----
h = random.choice(hexes)

cx = h["x"]
cy = h["y"]

# ---- optional fine-tuning ----
x_offset = 0
y_offset = 0

# ---- center paste position ----
paste_x = int(cx - tile_w / 2 + x_offset)
paste_y = int(cy - tile_h / 2 + y_offset)

# ---- paste ----
img.paste(tile, (paste_x, paste_y), tile)

img.save("output.png")
img.show()