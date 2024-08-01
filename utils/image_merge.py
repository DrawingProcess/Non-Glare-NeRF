import cv2
import numpy as np
import os
import sys

# merge the images
def merge_image(images, h, w):
    step = 512
    # create the image
    image = np.zeros((h+step, w+step, 3), dtype=np.uint8)
    # loop through the images
    for i in range(0, h, 512):
        for j in range(0, w, 512):
            # get the image
            img = images.pop(0)
            # put the image
            image[i:i+512, j:j+512] = img
    image = image[:h, :w]
    return image

if __name__ == "__main__":
    argv = sys.argv
    if len(argv) != 2:
        print("please write dataset name. e.g. python image_merge.py 240508_classroom")
        
    # read the image
    base_path = "nerf_custom/" + argv[1] + "/EXR_RGBD/"
    folder_path = base_path + "inpainting_crop"
    os.makedirs(base_path + "inpainting", exist_ok=True)

    target_path = "nerf_custom/" + argv[1] + "_inpainting/images/"
    os.makedirs(target_path, exist_ok=True)

    rgb_file = base_path + "rgb/0.jpg"
    h, w = cv2.imread(rgb_file).shape[:2]

    list_files = os.listdir(folder_path)
    list_files.sort()

    for file_num in range(0, len(list_files), 12):
        if list_files[file_num] == ".DS_Store":
            continue
        images = []
        for i in range(12):
            file_path = folder_path + "/" + list_files[file_num + i]
            img = cv2.imread(file_path)
            images.append(img)
        image = merge_image(images, h, w)
        # file format frame_00000.jpg, frame_00001.jpg, frame_00002.jpg, ... but list_files[file_num] is 0_00.jpg, 0_01.jpg, 0_02.jpg, ...
        file_num = list_files[file_num].split("_")[0]
        file_num = "{:05d}".format(int(file_num) + 1)
        filename = "frame_{}.jpg".format(file_num)
        cv2.imwrite(base_path + "inpainting/" + filename, image)
        cv2.imwrite(target_path + filename, image)
        print("Finish merge: ", filename)
