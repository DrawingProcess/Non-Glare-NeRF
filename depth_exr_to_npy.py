# -*- coding:utf-8 -*-

"""
# https://gist.github.com/andres-fr/4ddbb300d418ed65951ce88766236f9c
Place this script on a directory and convert the .exr files it contains
into np.float32 matrices
"""

import os
import sys
import OpenEXR
import numpy as np

import json


def depth_exr_to_numpy(exr_path,
                       typemap={"HALF": np.float16, "FLOAT": np.float32}):
    """
    """
    print("[processing {}]".format(exr_path))
    # load EXR and extract shape
    exr = OpenEXR.InputFile(exr_path)
    print(exr.header())
    dw = exr.header()["dataWindow"]
    shape = (dw.max.y - dw.min.y + 1, dw.max.x - dw.min.x + 1)
    #
    arr_maps = {}
    for ch_name, ch in exr.header()["channels"].items():
        print("reading channel", ch_name)
        # This, and __str__ seem to be the only ways to get typename
        exr_typename = ch.type.names[ch.type.v]
        np_type = typemap[exr_typename]
        # convert channel to np array
        bytestring = exr.channel(ch_name, ch.type)
        arr = np.frombuffer(bytestring, dtype=np_type).reshape(shape)
        arr_maps[ch_name] = arr
    
        # nan_indices = np.isnan(arr)
        # print("nan_indices: ", nan_indices)
    # Z = arr_maps['R']
    # min_Z = min(map(min, Z))
    # max_Z = max(map(max, Z))
    # arr_maps['R'] = (Z - min_Z) / (max_Z - min_Z)
    #
    # rgb_equal = ((arr_maps["R"] == arr_maps["G"]).all() and
    #              (arr_maps["R"] == arr_maps["B"]).all())
    # assert rgb_equal, "this function assumes that R, G, B must be identical!"
    #
    return arr_maps["R"]


def plot_arr(arr):
    """
    arr has to be np.float32
    """
    print("plotting", arr.shape, arr.dtype, arr.min(), arr.max())
    import matplotlib.pyplot as plt
    plt.imshow(arr)
    plt.show()


def convert_depth_exr_files_to_np_float32(exr_path):
    """
    """
    return depth_exr_to_numpy(exr_path).astype(np.float32)

def transforms_depth(base_path):
    filename = base_path + "transforms.json"
    with open(filename, 'r') as f:
        data = json.load(f)
        for frame in data["frames"]:
            file_path = frame["file_path"].replace("images", "depth")
            frame["depth_file_path"] = file_path.replace(".jpg", ".npy")
        output = json.dumps(data, indent=4)

    with open(filename, 'w') as f:
        f.write(output)


if __name__ == "__main__":
    argv = sys.argv
    if len(argv) != 2:
        print("please write dataset name. e.g. python depth_exr_to_npy.py 240508_classroom")

    base_path = "./nerf_custom/" + argv[1] + "/"
    depth_path = base_path + "EXR_RGBD/depth/"
    file_list = os.listdir(depth_path)

    os.makedirs(depth_path.replace("/EXR_RGBD/", "/"), exist_ok=True)

    for file in file_list:
        np_arr = convert_depth_exr_files_to_np_float32(depth_path + file)

        file_num = str(int(file.split('.')[0]) + 1).zfill(5)
        file = "frame_" + file_num + '.npy'
        file_path = depth_path + file
        file_path = file_path.replace("/EXR_RGBD/", "/")
        np.save(file_path, np_arr)

    transforms_depth(base_path)

    # for arr in np_arrs:
    #     plot_arr(arr)