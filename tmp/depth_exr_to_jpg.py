import numpy as np
import OpenEXR as exr
import Imath

from matplotlib import pyplot as plt

import os

def readEXR(filename):
    """Read color + depth data from EXR image file.
    
    Parameters
    ----------
    filename : str
        File path.
        
    Returns
    -------
    img : RGB or RGBA image in float32 format. Each color channel
          lies within the interval [0, 1].
          Color conversion from linear RGB to standard RGB is performed
          internally. See https://en.wikipedia.org/wiki/SRGB#The_forward_transformation_(CIE_XYZ_to_sRGB)
          for more information.
          
    Z : Depth buffer in float32 format or None if the EXR file has no Z channel.
    """
    
    exrfile = exr.InputFile(filename)
    header = exrfile.header()
    print(header)
    
    dw = header['dataWindow']
    isize = (dw.max.y - dw.min.y + 1, dw.max.x - dw.min.x + 1)
    
    channelData = dict()
    
    # convert all channels in the image to numpy arrays
    for c in header['channels']:
        C = exrfile.channel(c, Imath.PixelType(Imath.PixelType.FLOAT))
        C = np.fromstring(C, dtype=np.float32)
        C = np.reshape(C, isize)
        
        channelData[c] = C

    # # Read EXR RGBD Format
    # colorChannels = ['R', 'G', 'B', 'A'] if 'A' in header['channels'] else ['R', 'G', 'B']
    # img = np.concatenate([channelData[c][...,np.newaxis] for c in colorChannels], axis=2)
    
    # # linear to standard RGB
    # img[..., :3] = np.where(img[..., :3] <= 0.0031308,
    #                         12.92 * img[..., :3],
    #                         1.055 * np.power(img[..., :3], 1 / 2.4) - 0.055)
    
    # # sanitize image to be in range [0, 1]
    # img = np.where(img < 0.0, 0.0, np.where(img > 1.0, 1, img))
    
    # # Read EXR D Format
    # Z = None if 'Z' not in header['channels'] else channelData['Z']
    Z = channelData['R']
    min_Z = min(map(min, Z))
    max_Z = max(map(max, Z))
    # print(Z)
    # print("min: ", min_Z)
    # print("max: ", max_Z)

    Z = (Z - min_Z) / (max_Z - min_Z) * 255
    # print(Z)
    # print("min: ", min_Z)
    # print("max: ", max_Z)
    
    # return img, Z
    return Z

def read_depth_exr_file(filepath):
    # exrfile = exr.InputFile(filepath.as_posix())
    exrfile = exr.InputFile(filepath)
    raw_bytes = exrfile.channel('R', Imath.PixelType(Imath.PixelType.FLOAT))
    depth_vector = np.frombuffer(raw_bytes, dtype=np.float32)
    height = exrfile.header()['displayWindow'].max.y + 1 - exrfile.header()['displayWindow'].min.y
    width = exrfile.header()['displayWindow'].max.x + 1 - exrfile.header()['displayWindow'].min.x
    depth_map = np.reshape(depth_vector, (height, width))
    return depth_map



if __name__ == "__main__":
    base_path = "./nerf_custom/record3d_lab_simple/EXR_RGBD/depth/"
    file_list = os.listdir(base_path)

    os.makedirs(base_path.replace("/EXR_RGBD/", "/"), exist_ok=True)

    for file in file_list:
        # Z = read_depth_exr_file(filename)
        Z = readEXR(base_path + file)

        file_num = str(int(file.split('.')[0]) + 1).zfill(5)
        file = "frame_" + file_num + '.jpg'
        file_path = base_path + file
        file_path = file_path.replace("/EXR_RGBD/", "/")
        plt.imsave(file_path, Z)
    # plt.imshow(Z)
    # plt.show()

    # img = plt.imread(filename_img)
    # plt.imsave("rgb.jpg", img)