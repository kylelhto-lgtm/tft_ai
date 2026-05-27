from PIL import Image

# load image
img = Image.open("boards/default_hex.png").convert("RGB")

# choose pixel location
x, y = 681, 406  # <-- change this

# get pixel value
rgb = img.getpixel((x, y))

print("RGB at", (x, y), "=", rgb)