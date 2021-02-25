import os

cmd = "python3 eval.py \
    --logtostderr \
    --eval_split=\"val\" \
    --model_variant=\"xception_65\" \
    --atrous_rates=6 \
    --atrous_rates=12 \
    --atrous_rates=18 \
    --output_stride=16 \
    --decoder_output_stride=4 \
    --train_crop_size=\"256,256\" \
    --dataset=\"PC1\" \
    --checkpoint_dir=\"./models/train_log\" \
    --eval_logdir=\"./models/eval_log\" \
    --dataset_dir=\"/hdd/d8/dplb/PC1/tfrecord\""

os.system(cmd)  