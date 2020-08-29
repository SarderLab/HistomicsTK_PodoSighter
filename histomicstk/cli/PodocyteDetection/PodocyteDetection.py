import os
from histomicstk.cli.utils import CLIArgumentParser

def main(args):

    cmd = "python3 ../plugin_podfolder/pod_plugin6.py -P '{}' -F '{}' -L '{}' -T {} -Tx {} -Ty {}".format(args.inputImageFilePAS, args.inputImageFileIF, args.inputAnnotationFile,args.Podocyte_threshold,args.TranslationX,args.TranslationY)
    os.system(cmd)    

if __name__ == "__main__":
    main(CLIArgumentParser().parse_args())
