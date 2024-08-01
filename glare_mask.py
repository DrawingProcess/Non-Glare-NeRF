# https://rcvaram.medium.com/glare-removal-with-inpainting-opencv-python-95355aa2aa52
import cv2
import numpy as np
import skimage.measure as measure


import os
import sys

def create_mask(image):
    gray = cv2.cvtColor( image, cv2.COLOR_BGR2GRAY )
    blurred = cv2.GaussianBlur( gray, (9,9), 0 )
    # _,thresh_img = cv2.threshold( blurred, 180, 255, cv2.THRESH_BINARY)
    _,thresh_img = cv2.threshold( blurred, 200, 255, cv2.THRESH_BINARY)
    thresh_img = cv2.erode( thresh_img, None, iterations=2 )
    thresh_img  = cv2.dilate( thresh_img, None, iterations=4 )
    # perform a connected component analysis on the thresholded image,
    # then initialize a mask to store only the "large" components
    # labels = measure.label( thresh_img, neighbors=8, background=0 )
    labels = measure.label( thresh_img, connectivity=2, background=0 )
    mask = np.zeros( thresh_img.shape, dtype="uint8" )
    # loop over the unique components
    for label in np.unique( labels ):
        # if this is the background label, ignore it
        if label == 0:
            continue
        # otherwise, construct the label mask and count the
        # number of pixels
        labelMask = np.zeros( thresh_img.shape, dtype="uint8" )
        labelMask[labels == label] = 255
        numPixels = cv2.countNonZero( labelMask )
        # if the number of pixels in the component is sufficiently
        # large, then add it to our mask of "large blobs"
        if numPixels > 300:
            mask = cv2.add( mask, labelMask )
    return mask


if __name__ == "__main__":
    argv = sys.argv
    if len(argv) != 2:
        print("please write dataset name. e.g. python glare_mask.py 240508_classroom")
        
    base_path = "nerf_custom/" + argv[1] + "/EXR_RGBD/"
    os.makedirs(base_path + "mask", exist_ok=True)

    folder_path = base_path + "rgb"
    list_files = os.listdir(base_path + "rgb")
    for file in list_files:
        if file == ".DS_Store":
            continue
        file_path = folder_path + "/" + file
        img = cv2.imread(file_path)
        mask = create_mask(img)
        # cv2.imwrite(base_path + "mask/" + file, mask)
        mask = cv2.dilate(mask, None, iterations=8 )
        print("Finish mask: ", file)
        cv2.imwrite(base_path + "mask/" + file, mask)
