# from PIL import Image

# # base image
# img = Image.open("boards/default_hex.png").convert("RGBA")

# # png you want to paste (must have transparency ideally)
# tile = Image.open("sprites/chogath.png").convert("RGBA")

# # hex points
# points = [
#     (570, 400),
#     (620, 420),
#     (615, 470),
#     (550, 490),
#     (500, 470),
#     (510, 420)
# ]

# # get bounding box of hex
# xs = [p[0] for p in points]
# ys = [p[1] for p in points]

# min_x, max_x = min(xs), max(xs)
# min_y, max_y = min(ys), max(ys)

# width = max_x - min_x
# height = max_y - min_y

# # resize tile to fit hex area
# tile = tile.resize((width, height))

# # paste directly
# img.paste(tile, (min_x, min_y), tile)

# img.save("output.png")
# img.show()

from PIL import Image

# base image
img = Image.open("boards/default_hex.png").convert("RGBA")

# png you want to paste (must have transparency ideally)
tile = Image.open("sprites/chogath.png").convert("RGBA")

points = [
    (570, 400),
    (620, 420),
    (615, 470),
    (550, 490),
    (500, 470),
    (510, 420)
]

# ---- compute centroid ----
cx = sum(p[0] for p in points) / len(points)
cy = sum(p[1] for p in points) / len(points)

tile_w, tile_h = tile.size

# 🔥 fine-tune offsets (tweak these)
x_offset = 8   # move right
y_offset = 12  # move up

# final paste position (centered)
paste_x = int(cx - tile_w / 2 + x_offset)
paste_y = int(cy - tile_h / 2 - y_offset)

img.paste(tile, (paste_x, paste_y), tile)

img.save("output.png")
img.show()