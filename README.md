# Non-Glare-NeRF: To prevent unwanted glare

This is the official implementation of our KSC 2024 paper Non-Glare NeRF: To prevent unwanted glare. Pull requests and issues are welcome.</br>

[Seongjun Choi](https://drawingprocess.github.io), [Hyoseok Hwang](https://sites.google.com/view/hyoseok-hwang)

[[`Paper`](https://arxiv.org/abs/2403.17537)] [[`Project`](https://drawingprocess.github.io/Non-Glare-NeRF/)]

<b>Abstract</b>: This paper proposes two approaches to solve the depth distortion problem that occurs on glare surfaces in the process of 3D reconstruction based on Neural Radiance Fields (NeRF). First, by introducing a preprocessing process using the Inpainting technique, distortion of texture and depth information due to Glare is alleviated. Second, a dataset that combines high-precision depth information and rich color information is constructed using the iPhone's LiDAR sensor and RGB camera. It was confirmed through experiments that the proposed method improves the 3D reconstruction performance of NeRF even in scenes where the Glare phenomenon exists.

## Requirements

The codebase is tested on
- python 3.7+
- GeForce RTX 3090

## 1) Prepare Dataset: depth custom data 

### i) Data Engine: Extract image & depth row data

Ref. [minsangKang/LiDAR-Map-App](https://github.com/minsangKang/LiDAR-Map-App)

### ii) Data Engine: iPhone Record3D App
Environment Setup for using nerfstudio (python 3.8.19, pytorch 2.1.2+cu118) </br>
```bash
conda create -n nerfstudio python==3.8
```
Ref. [nerfstudio/README.md](./nerfstudio/README.md)

Extract record3d (EXR + JPG sequence) </br>
```bash
ns-process-data record3d --data nerf_custom/record3d_lab_simple/EXR_RGBD/ --output-dir nerf_custom/record3d_lab_simple/ --max_dataset_size 400
```

depth exr format to npy format </br>
```bash
python utils/depth_exr_to_npy.py 240508_classroom
```


## 2) Masking Inpainting using co-mod-gan-pytorch
Environment Setup for using co-mod-gan-pytorch (python 3.7.16, pytorch 1.9.0+cu111) </br>
```bash
conda create -n stylegan2 python==3.7
```
Ref. [co-mod-gan-pytorch/README.md](./co-mod-gan-pytorch/README.md)

Glare Masking using OpenCV </br>
```bash
python utils/glare_mask.py 240508_classroom
```

Image Crop for inpainting (Commonly inpainting algorithms supported 512x512 size) </br>
```bash
python utils/image_crop.py 240508_classroom
```

inpainting </br>
```bash
./test.sh 240508_classroom
```

Image merge </br>
```bash
python utils/image_merge.py 240508_classroom
```


## 3) NeRF Train & Visualize using nerfstudio
nerfstudio train & eval </br>
```bash
ns-train instant-ngp --data ../../data/nerf_custom/record3d_lab_simple/ --vis viewer+wandb
```

nerfstudio eval </br>
```bash
ns-eval --load-config=outputs/240508_classroom/instant-ngp/2024-05-15_230307/config.yml --output-path=outputs/240508_classroom/instant-ngp/2024-05-15_230307/output.json
```

nerfstudio visualize </br>
```bash
ns-viewer --load-config outputs/headset_alphabg/instant-ngp/2024-04-09_124400/config.yml --viewer.make-share-url True
```

nerfstudio rendering </br>
```bash
ns-render camera-path --load-config outputs/headset_alphabg/instant-ngp/2024-04-09_124400/config.yml --camera-path-filename /data/csj000714/repos/nerfstudio/../../data/nerf_custom/headset_alphabg/camera_paths/2024-04-18-12-55-14.json --output-path renders/headset_alphabg/2024-04-18-12-55-14.mp4
```