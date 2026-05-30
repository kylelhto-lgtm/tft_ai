import json

ORIG_W = 2560
ORIG_H = 1440

with open("../finding_hexes/hexes.json", "r") as f:
    data = json.load(f)

for hex_data in data["hexes"]:
    hex_data["x_norm"] = hex_data["x"] / ORIG_W
    hex_data["y_norm"] = hex_data["y"] / ORIG_H

    # Optional: remove pixel coords
    del hex_data["x"]
    del hex_data["y"]

with open("hex_coordinates_normalized.json", "w") as f:
    json.dump(data, f, indent=2)

print("Saved normalized coordinates.")