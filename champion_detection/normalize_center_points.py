import json

ORIG_W = 2560
ORIG_H = 1440

INPUT_FILE = "../finding_hexes/center_points.json"
OUTPUT_FILE = "center_points_normalized.json"

with open(INPUT_FILE, "r", encoding="utf-8") as f:
    data = json.load(f)

normalized_centers = []

for x, y in data["centers"]:
    normalized_centers.append([
        x / ORIG_W,
        y / ORIG_H
    ])

out = {
    "centers": normalized_centers
}

with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
    json.dump(out, f, indent=2)

print("Saved ->", OUTPUT_FILE)