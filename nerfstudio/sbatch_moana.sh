#!/usr/bin/bash

#SBATCH -J nerfstudio-zipnerf-custom-umbrella_100_alphabg
#SBATCH --gres=gpu:1
#SBATCH --cpus-per-gpu=8
#SBATCH --mem-per-gpu=32G
#SBATCH -p batch_eebme_ugrad
#SBATCH -t 3-0
#SBATCH -w moana-y2
#SBATCH -o logs/slurm-%A.out

squeue --job $SLURM_JOBID
cat $0

pwd
which python
hostname

ns-train zipnerf --data ../../data/nerf_custom/umbrella_100_alphabg/

# ns-train nerfacto --data /data/csj000714/data/nerf_synthetic/lego
# ns-train garfield --data /data/csj000714/data/nerf_synthetic/lego
exit 0
