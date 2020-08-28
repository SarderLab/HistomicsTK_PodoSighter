import os
from histomicstk.cli.utils import CLIArgumentParser

def main(args):
    cmd = "python3 ../plugin_podfolder/pod_plugin4.py --inputPASsvsname '{}' --inputIFsvsname '{}' --inputPASxmlname '{}' --orig_IF_Thre {} --TransXY {}".format(args.inputImageFilePAS, args.inputImageFileIF, args.inputAnnotationFile,args.Podocyte_threshold,args.TranslationXY)
    os.system(cmd)    

if __name__ == "__main__":
    main(CLIArgumentParser().parse_args())
