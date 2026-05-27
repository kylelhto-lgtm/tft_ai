from PIL import Image, ImageDraw
import numpy as np
from scipy.ndimage import label

# -------------------------
# LOAD IMAGE
# -------------------------
img = Image.open("highlighted.png").convert("RGB")
arr = np.array(img)

# -------------------------
# EDGE MASK
# -------------------------
target = np.array([0, 255, 0])
tol = 30

mask = np.all(np.abs(arr - target) <= tol, axis=-1)

# -------------------------
# CONNECT COMPONENTS
# -------------------------
structure = np.ones((3, 3))
labeled, num = label(mask, structure=structure)

print("Components found:", num)

# -------------------------
# COMPUTE CENTERS
# -------------------------
centers = []
min_size = 200

for i in range(1, num + 1):
    ys, xs = np.where(labeled == i)

    if len(xs) < min_size:
        continue

    cx = np.mean(xs)
    cy = np.mean(ys)

    centers.append((cx, cy))

print("Hex centers:", len(centers))

# -------------------------
# 4-POINT SOFT MODEL
# -------------------------
def soft_quad_points(cx, cy, scale=20):
    """
    Cross-shaped 4-anchor model:
    - left
    - right
    - up
    - down
    """

    return [
        (cx, cy),               # center

        (cx - scale, cy),      # left
        (cx + scale, cy),      # right

        (cx, cy - scale),      # up
        (cx, cy + scale),      # down
    ]

# -------------------------
# DRAW RESULT
# -------------------------
draw = ImageDraw.Draw(img)

all_hex_models = []

for i, (cx, cy) in enumerate(centers):

    anchors = soft_quad_points(cx, cy, scale=20)
    all_hex_models.append(anchors)

    # center (RED)
    draw.ellipse((cx - 5, cy - 5, cx + 5, cy + 5), fill="red")

    # anchors (BLUE)
    for ax, ay in anchors[1:]:
        draw.ellipse((ax - 3, ay - 3, ax + 3, ay + 3), fill="blue")

    draw.text((cx + 6, cy + 6), str(i), fill="white")

# -------------------------
# SAVE
# -------------------------
img.save("generated_images/hex_four_point_overlay.png")
img.show()