export MODEL_FLAGS="--image_size 32 --num_channels 64 --num_res_blocks 3 --scale_time_dim 0";
export DIFFUSION_FLAGS="--diffusion_steps 100 --noise_schedule linear";
export TRAIN_FLAGS="--lr 2e-5 --batch_size 4 --microbatch 1 --seq_len 16 --max_num_mask_frames 4 --uncondition_rate 0.25";
export OPENAI_LOGDIR=$PWD

python scripts/video_train.py --data_dir videos/ $MODEL_FLAGS $DIFFUSION_FLAGS $TRAIN_FLAGS