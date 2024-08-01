# Non-Glare NeRF

## 1) Prepare Dataset: depth custom data using iPhone Record3D App
0. Environment Setup for using nerfstudio
Ref. [nerfstudio/README.md](./nerfstudio/README.md)

1. Extract record3d (EXR + JPG sequence) </br>
```ns-process-data record3d --data nerf_custom/record3d_lab_simple/EXR_RGBD/ --output-dir nerf_custom/record3d_lab_simple/ --max_dataset_size 400```

3. depth exr format to npy format </br>
```python depth_exr_to_npy.py 240508_classroom```


## 2) Masking Inpainting using co-mod-gan-pytorch
0. Environment Setup for using co-mod-gan-pytorch
Ref. [co-mod-gan-pytorch/README.md](./co-mod-gan-pytorch/README.md)

1. Glare Masking using OpenCV </br>
```python glare_mask.py 240508_classroom```

2. Image Crop for inpainting (Commonly inpainting algorithms supported 512x512 size) </br>
```python image_crop.py 240508_classroom```

3. inpainting </br>
```./test.sh 240508_classroom```

4. Image merge </br>
```python image_merge.py 240508_classroom```


## 3) NeRF Train & Visualize using nerfstudio
1. nerfstudio train & eval </br>
```ns-train instant-ngp --data ../../data/nerf_custom/record3d_lab_simple/ --vis viewer+wandb```

2. nerfstudio eval </br>
```ns-eval --load-config=outputs/240508_classroom/instant-ngp/2024-05-15_230307/config.yml --output-path=outputs/240508_classroom/instant-ngp/2024-05-15_230307/output.json```

3. nerfstudio visualize </br>
```ns-viewer --load-config outputs/headset_alphabg/instant-ngp/2024-04-09_124400/config.yml --viewer.make-share-url True```

4. nerfstudio rendering </br>
```ns-render camera-path --load-config outputs/headset_alphabg/instant-ngp/2024-04-09_124400/config.yml --camera-path-filename /data/csj000714/repos/nerfstudio/../../data/nerf_custom/headset_alphabg/camera_paths/2024-04-18-12-55-14.json --output-path renders/headset_alphabg/2024-04-18-12-55-14.mp4```
```