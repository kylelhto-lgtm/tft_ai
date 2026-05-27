from PIL import Image, ImageDraw

img = Image.open("../boards/default.png").convert("RGB")
draw = ImageDraw.Draw(img)

# ---- GRID CONFIG ----
rows = 4
cols = 7

start_x = 562
start_y = 443

hex_w = 135
hex_h = 110

gap_x = 15
gap_y = 0

# ✅ correct pointy-top spacing
x_step = (hex_w * 0.75) + gap_x
y_step = (hex_h * 0.75) + gap_y


def hex_center(col, row):
    x = start_x + col * x_step

    if row % 2 == 1:
        x += hex_w / 2

    y = start_y + row * y_step

    return x, y


def hex_corners(cx, cy):
    w = hex_w / 2
    h = hex_h / 2

    return [
        (cx, cy - h),                  # top point
        (cx + w * 0.866, cy - h/2),
        (cx + w * 0.866, cy + h/2),
        (cx, cy + h),                  # bottom point
        (cx - w * 0.866, cy + h/2),
        (cx - w * 0.866, cy - h/2),
    ]


# ---- DRAW GRID ----
for r in range(rows):
    for c in range(cols):
        cx, cy = hex_center(c, r)
        draw.polygon(hex_corners(cx, cy), outline="lime", width=2)

img.save("generated_images/draw_all_hex.png")
img.show()