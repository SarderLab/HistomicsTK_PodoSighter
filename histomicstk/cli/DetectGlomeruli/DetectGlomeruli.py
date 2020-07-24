import os
from histomicstk.cli.utils import CLIArgumentParser

def main(args):
    cmd = 'python3 vis.py --model_variant xception_65 --atrous_rates 6 --atrous_rates 12 --atrous_rates 18 --output_stride 16 --decoder_output_stride 4 --checkpoint_dir /home/brendonl/deeplab/glom-models-multiscale-7-16-20 --dataset_dir {} --vis_crop_size {} --wsi_downsample {}'.format(args.inputImageFile, args.patch_size, args.wsi_downsample)
    os.system(cmd)


if __name__ == "__main__":
    main(CLIArgumentParser().parse_args())
