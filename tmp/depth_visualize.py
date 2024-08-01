import cv2
import numpy as np

depth = cv2.imread('/home/sjchoi/nerf/data/nerf_custom/lab_simple/4ßäïßà»ßå»6ßäïßà╡ßå»ßäïßà⌐ßäîßàÑßå½5-09-poly/depth/13134671597.png')

print("depth.min(): ", depth.min())
print("depth.max(): ", depth.max())
depth = (depth - depth.min()) / (depth.max() - depth.min()) * 255.0
depth = depth.astype(np.uint8)

cv2.imwrite('depth.png', depth)