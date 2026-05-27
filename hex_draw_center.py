from PIL import Image, ImageDraw
import numpy as np
from scipy.ndimage import label

# -------------------------
# LOAD IMAGE (edges already highlighted)
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

min_size = 200  # adjust if needed

for i in range(1, num + 1):
    ys, xs = np.where(labeled == i)

    if len(xs) < min_size:
        continue

    cx = np.mean(xs)
    cy = np.mean(ys)

    centers.append((cx, cy))

print("Hex centers:", len(centers))

# -------------------------
# DRAW ON IMAGE
# -------------------------
draw = ImageDraw.Draw(img)

for i, (cx, cy) in enumerate(centers):
    r = 5

    # red dot
    draw.ellipse(
        (cx - r, cy - r, cx + r, cy + r),
        fill="red"
    )

    # label
    draw.text((cx + 6, cy + 6), str(i), fill="white")

# -------------------------
# SAVE RESULT
# -------------------------
img.save("hex_centers_overlay.png")
img.show()

# from PIL import Image
# import numpy as np
# from scipy.ndimage import label

# # -------------------------
# # LOAD IMAGE
# # -------------------------
# img = Image.open("highlighted.png").convert("RGB")
# arr = np.array(img)

# # -------------------------
# # EDGE MASK
# # -------------------------
# target = np.array([0, 255, 0])
# tol = 30

# mask = np.all(np.abs(arr - target) <= tol, axis=-1)

# # -------------------------
# # CONNECT COMPONENTS
# # -------------------------
# structure = np.ones((3, 3))
# labeled, num = label(mask, structure=structure)

# # -------------------------
# # COMPUTE CENTERS
# # -------------------------
# centers = []
# min_size = 200

# for i in range(1, num + 1):
#     ys, xs = np.where(labeled == i)

#     if len(xs) < min_size:
#         continue

#     centers.append((np.mean(xs), np.mean(ys)))

# centers = np.array(centers)

# print("Hex centers:", len(centers))

# # -------------------------
# # ASSIGN EACH PIXEL TO NEAREST HEX
# # -------------------------
# h, w = mask.shape
# ys, xs = np.where(mask)

# assignment = np.full((h, w), -1, dtype=int)

# for y, x in zip(ys, xs):
#     dx = centers[:, 0] - x
#     dy = centers[:, 1] - y

#     nearest = np.argmin(dx*dx + dy*dy)
#     assignment[y, x] = nearest

# # -------------------------
# # COLORIZE OUTPUT
# # -------------------------
# output = np.zeros((h, w, 3), dtype=np.uint8)

# # generate distinct colors
# rng = np.random.default_rng(42)
# colors = rng.integers(50, 255, size=(len(centers), 3), dtype=np.uint8)

# for i in range(len(centers)):
#     output[assignment == i] = colors[i]

# # keep background black
# output[assignment == -1] = [0, 0, 0]

# # -------------------------
# # SAVE RESULT
# # -------------------------
# out_img = Image.fromarray(output)
# out_img.save("hex_regions_colored.png")
# out_img.show()