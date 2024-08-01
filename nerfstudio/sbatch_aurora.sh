#!/usr/bin/bash

#SBATCH -J nerfstudio-instant-ngp-custom-headset_only
#SBATCH --gres=gpu:1
#SBATCH --cpus-per-gpu=8
#SBATCH --mem-per-gpu=32G
#SBATCH -p batch_ugrad
#SBATCH -t 3-0
#SBATCH -w aurora-g6
#SBATCH -o logs/slurm-%A.out

squeue --job $SLURM_JOBID
cat $0

pwd
which python
hostname

ns-train instant-ngp --data ../../data/nerf_custom/240621_corridor_inpainting/ --vis viewer+wandb
# ns-train instant-ngp --data ../../data/nerf_custom/record3d_lab_simple/ --vis viewer+wandb
# ns-train depth-nerfacto --data ../../data/nerf_custom/umbrella_100_alphabg/

# ns-train nerfacto --data /data/csj000714/data/nerf_synthetic/lego
# ns-train garfield --data /data/csj000714/data/nerf_synthetic/lego
exit 0
