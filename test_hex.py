from PIL import Image, ImageDraw

# Load image
img = Image.open("boards/default.png").convert("RGB")

# Your 6 pixel coordinates (x, y)
points = [
    (570, 400),
    (620, 420),
    (615, 470),
    (550, 490),
    (500, 470),
    (510, 420)
]

draw = ImageDraw.Draw(img)

# Draw outline hexagon
draw.polygon(points, outline="lime", width=3)

# Optional: fill hexagon
# draw.polygon(points, fill=(0, 255, 0, 100))  # note: needs RGBA image for transparency

img.save("output.jpg")
img.show()