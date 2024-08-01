import cv2 
  
base_path = "nerf_custom/240621_corridor/EXR_RGBD/"
rgb_path = base_path + "rgb/0.jpg"
mask_path = base_path + "mask/0.jpg"

img1 = cv2.imread(rgb_path) 
img2 = cv2.imread(mask_path) 

img2 = cv2.resize(img2, img1.shape[1::-1]) 

alpha = 0.7
dst = cv2.addWeighted(img1, alpha , img2, 1-alpha, 0) 
cv2.imwrite('output/image_mask_blending.png', dst) 