import os
import cv2
import imutils

def img2mp4(paths, pathOut, fps=10, rotate=True):
    frame_array = []
    for path in paths:
        img = cv2.imread(path)
        
        # Rotate image by 90 degrees if specified
        if rotate:
            img = imutils.rotate_bound(img, -90)

        frame_array.append(img)

    # Determine size from first frame
    height, width, layers = frame_array[0].shape
    size = (width, height)
    out = cv2.VideoWriter(pathOut, cv2.VideoWriter_fourcc(*'DIVX'), fps, size)
    
    for frame in frame_array:
        out.write(frame)
    out.release()

def concat_and_save(concat_paths, pathOut, fps=10):
    frame_array = []
    for paths in zip(*concat_paths):
        # Load and rotate each image by 90 degrees
        imgs_rotated = [imutils.rotate_bound(cv2.imread(path), -90) for path in paths]

        # Concatenate images horizontally
        img_concat = cv2.hconcat(imgs_rotated)

        # Append concatenated frame
        frame_array.append(img_concat)

    # Define video size from concatenated image dimensions
    height, width, layers = frame_array[0].shape
    size = (width, height)
    out = cv2.VideoWriter(pathOut, cv2.VideoWriter_fourcc(*'DIVX'), fps, size)
    
    for frame in frame_array:
        out.write(frame)
    out.release()

# Paths and configuration
path = "./nerfstudio/outputs/"
scene = "classroom2_inpainting/" 
scene_path = {
    "classroom1/": "240516_classroom1/instant-ngp/2024-05-16_131104/images/",
    "classroom1_inpainting/": "240516_classroom1_inpainting/instant-ngp/2024-05-30_075321/images/",
    "classroom2/": "240516_classroom2/instant-ngp/2024-05-16_133805/images/",
    "classroom2_inpainting/": "240516_classroom2_inpainting/instant-ngp/2024-05-30_063220/images/"
}
output_path = "./docs/static/videos/"

results = ["rgb", "rgb_gt", "depth", "depth_gt"]
paired_results = {"gt": ["rgb_gt", "depth_gt"], "result": ["rgb", "depth"]}

# Save individual videos
for result in results:
    paths = sorted(os.listdir(path + scene_path[scene] + result))
    paths = [path + scene_path[scene] + result + "/" + p for p in paths]

    img2mp4(paths, output_path + scene + result + ".mp4", fps=6)

# Save concatenated videos
for result_name, result_keys in paired_results.items():
    concat_paths = []
    for result in result_keys:
        paths = sorted(os.listdir(path + scene_path[scene] + result))
        paths = [path + scene_path[scene] + result + "/" + p for p in paths]
        print(paths)
        concat_paths.append(paths)

    # output_path = path + scene + result_name + ".mp4"
    concat_and_save(concat_paths, output_path + scene + result_name + ".mp4", fps=6)