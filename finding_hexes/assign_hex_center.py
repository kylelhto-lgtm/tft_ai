from PIL import Image
import numpy as np
from scipy.ndimage import label

# -------------------------
# LOAD IMAGE
# -------------------------
img = Image.open("generated_images/hexes_highlighted.png").convert("RGB")
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

centers = np.array(centers)

print("Hex centers:", len(centers))

# -------------------------
# TRUE SOFT ANCHORS (4-point model)
# -------------------------
def soft_quad_points(cx, cy, scale=20):
    return [
        (cx, cy),
        (cx - scale, cy),
        (cx + scale, cy),
        (cx, cy - scale),
        (cx, cy + scale),
    ]

hex_anchors = [
    soft_quad_points(cx, cy, scale=20)
    for cx, cy in centers
]

# -------------------------
# PIXEL → HEX ASSIGNMENT (SOFT SCORING)
# -------------------------
h, w = mask.shape
ys, xs = np.where(mask)

assignment = np.full((h, w), -1, dtype=np.int32)

for y, x in zip(ys, xs):

    best_hex = -1
    best_score = float("inf")

    for i, anchors in enumerate(hex_anchors):

        # 🔥 SOFT REGION SCORE (not min-distance)
        score = 0.0

        for ax, ay in anchors:
            dx = ax - x
            dy = ay - y
            score += dx * dx + dy * dy

        score /= len(anchors)  # normalize

        if score < best_score:
            best_score = score
            best_hex = i

    assignment[y, x] = best_hex

# -------------------------
# COLORIZE OUTPUT
# -------------------------
output = np.zeros((h, w, 3), dtype=np.uint8)

rng = np.random.default_rng(42)
colors = rng.integers(50, 255, size=(len(centers), 3), dtype=np.uint8)

for i in range(len(centers)):
    output[assignment == i] = colors[i]

output[assignment == -1] = [0, 0, 0]

# -------------------------
# DRAW CENTERS (DEBUG)
# -------------------------
out_img = Image.fromarray(output)

for i, (cx, cy) in enumerate(centers):
    # draw center point
    for dx in range(-3, 4):
        for dy in range(-3, 4):
            x = int(cx + dx)
            y = int(cy + dy)

            if 0 <= x < w and 0 <= y < h:
                out_img.putpixel((x, y), (255, 255, 255))

# -------------------------
# SAVE
# -------------------------
out_img.save("generated_images/hex_soft_anchor_final.png")
out_img.show()