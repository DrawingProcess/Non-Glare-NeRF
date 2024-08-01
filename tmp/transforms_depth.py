import json

filename = "./nerf_custom/record3d_lab_simple/transforms.json"
with open(filename, 'r') as f:
    data = json.load(f)
    for frame in data["frames"]:
        file_path = frame["file_path"].replace("images", "depth")
        frame["depth_file_path"] = file_path.replace(".jpg", ".npy")
    output = json.dumps(data, indent=4)

with open(filename, 'w') as f:
    f.write(output)