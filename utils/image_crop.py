import cv2
import numpy as np
import os
import sys

# Divide the images into 512 by 512
def divide_image(image):
    # get the image size
    h, w = image.shape[:2]
    # define the step size
    step = 512
    # step_h = int(step/h * step)
    # step_w = int(step/w * step)
    # print(step_h, step_w)

    image_expend = np.zeros((h+step, w+step, 3), dtype=np.uint8)
    image_expend[:h, :w] = image
    image = image_expend

    # create the list to store the images
    images = []
    # loop through the image
    for i in range(0, h+step, step):
        for j in range(0, w+step, step):
            # get the image
            img = image[i:i+step, j:j+step]
            # check the size
            if img.shape[0] == step and img.shape[1] == step:
                images.append(img)
    return images

# merge the images
def merge_image(images):
    # get the image size
    h, w = images[0].shape[:2]
    # create the image
    image = np.zeros((h, w, 3), dtype=np.uint8)
    # loop through the images
    for i in range(0, h, 512):
        for j in range(0, w, 512):
            # get the image
            img = images.pop(0)
            # put the image
            image[i:i+512, j:j+512] = img
    return image

if __name__ == "__main__":
    argv = sys.argv
    if len(argv) != 2:
        print("please write dataset name. e.g. python image_crop.py 240508_classroom")
        
    base_path = "nerf_custom/" + argv[1] + "/EXR_RGBD/"
    folder_path_rgb = base_path + "rgb"
    folder_path_mask = base_path + "mask"

    os.makedirs(base_path + "rgb_crop", exist_ok=True)
    os.makedirs(base_path + "mask_crop", exist_ok=True)

    list_files = os.listdir(base_path + "rgb")
    for file in list_files:
        if file == ".DS_Store":
            continue
        file_path = folder_path_rgb + "/" + file
        img = cv2.imread(file_path)
        images = divide_image(img)
        for (i, image) in enumerate(images):
            # formatting the file name to have the same length
            cv2.imwrite(base_path + "rgb_crop/" + file.replace(".jpg", "_{:02d}.jpg".format(i)), image)

        file_path = folder_path_mask + "/" + file
        img = cv2.imread(file_path)
        images = divide_image(img)
        for (i, image) in enumerate(images):
            cv2.imwrite(base_path + "mask_crop/" + file.replace(".jpg", "_{:02d}.jpg".format(i)), image)

        print("Finish mask: ", file)
