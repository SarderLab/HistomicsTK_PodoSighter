import os
from histomicstk.cli.utils import CLIArgumentParser

def main(args):

    print(os.getcwd())

    model_file = args.inputModelFile
    try:
        model = model_file.split('.meta')
        assert len(model) == 2
        model = model[0]
    except:
        try:
            model = model_file.split('.index')
            assert len(model) == 2
            model = model[0]
        except:
            try:
                model = model_file.split('.data')
                assert len(model) == 2
                model = model[0]
            except:
                print('inputModelFile is not valid: exiting...')
                exit()

    cmd = 'python3 ../deeplab/vis.py --model_variant xception_65 --atrous_rates 6 --atrous_rates 12 --atrous_rates 18 --output_stride 16 --decoder_output_stride 4 --checkpoint_dir {} --dataset_dir {} --vis_crop_size {} --wsi_downsample {} --overlap_num {}'.format(model, args.inputImageFile, args.patch_size, args.wsi_downsample, args.patch_overlap)
    os.system(cmd)


if __name__ == "__main__":
    main(CLIArgumentParser().parse_args())
