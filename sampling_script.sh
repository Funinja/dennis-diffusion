export MODEL_FLAGS="--image_size 64 --num_channels 128 --num_res_blocks 3 --scale_time_dim 0";
export DIFFUSION_FLAGS="--diffusion_steps 1000 --noise_schedule linear";
export TRAIN_FLAGS="--lr 2e-5 --batch_size 8 --microbatch 2 --seq_len 16 --max_num_mask_frames 4 --uncondition_rate 0.25";
export SAMPLE_FLAGS="--batch_size 1 --num_samples 1 --timestep_respacing 5 --data_dir videos/";
export OPENAI_LOGDIR=$PWD

python3 scripts/video_sample.py --model_path ema_0.9999_500000.pt --data_dir videos/ --num_samples 1 --batch_size 1 --cond_frames 0,1,14,15, $MODEL_FLAGS $DIFFUSION_FLAGS
