# from PIL import Image
# import numpy as np

# img = Image.open("boards/default_hex.png").convert("RGB")
# arr = np.array(img)

# # target color
# target = np.array([60, 103, 100])

# # tolerance
# tol = 30

# # mask (RGB range check)
# mask = np.all(np.abs(arr - target) <= tol, axis=-1)

# # copy image for output
# output = arr.copy()

# # highlight matching pixels
# output[mask] = [0, 255, 0]  # green

# # convert back and save
# out_img = Image.fromarray(output)
# out_img.save("highlighted.png")
# out_img.show()

from PIL import Image
import numpy as np

img = Image.open("boards/default_hex.png").convert("RGB")
arr = np.array(img)

# -------------------------
# target color
# -------------------------
target = np.array([60, 103, 100])
tol = 30

color_mask = np.all(np.abs(arr - target) <= tol, axis=-1)

# -------------------------
# bounding box (EDIT THIS)
# -------------------------
x1, y1 = 628, 529   # top-left
x2, y2 = 1899, 976  # bottom-right

bbox_mask = np.zeros(arr.shape[:2], dtype=bool)
bbox_mask[y1:y2, x1:x2] = True

# -------------------------
# combine masks
# -------------------------
mask = color_mask & bbox_mask

# -------------------------
# output
# -------------------------
output = arr.copy()
output[mask] = [0, 255, 0]

out_img = Image.fromarray(output)
out_img.save("highlighted.png")
out_img.show()