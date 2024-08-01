# python test.py \
# 	--mixing 0 \
# 	--batchSize 1 \
# 	--nThreads 1 \
# 	--name comod-ffhq-512 \
# 	--dataset_mode testimage \
# 	--image_dir ./ffhq_debug/images \
# 	--mask_dir ./ffhq_debug/masks \
#         --output_dir ./ffhq_debug \
# 	--load_size 512 \
# 	--crop_size 512 \
# 	--z_dim 512 \
# 	--model comod \
# 	--netG comodgan \
#         --which_epoch co-mod-gan-ffhq-9-025000 \
# 	${EXTRA} \

if [ "$1" ]; then
	data=$1
else
	data="240516_classroom2"
fi 

python test.py \
	--mixing 0 \
	--batchSize 1 \
	--nThreads 1 \
	--name comod-places-512 \
	--dataset_mode testimage \
	--image_dir ../../data/nerf_custom/$data/EXR_RGBD/rgb_crop \
	--mask_dir ../../data/nerf_custom/$data/EXR_RGBD/mask_crop \
    --output_dir ../../data/nerf_custom/$data/EXR_RGBD/inpainting_crop \
	--load_size 512 \
	--crop_size 512 \
	--z_dim 512 \
	--model comod \
	--netG comodgan \
    --which_epoch co-mod-gan-places2-050000 \
	${EXTRA} \
