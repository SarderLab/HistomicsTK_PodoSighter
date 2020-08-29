import os
from histomicstk.cli.utils import CLIArgumentParser

def main(args):
    print(args.inputImageFilePAS)
    print(args.inputImageFileIF)
    print(args.inputAnnotationFile)
    print(args.Podocyte_threshold)
    print(args.TranslationXY)
    cmd = "python3 ../plugin_podfolder/pod_plugin5.py --inputPASsvsname '{}' --inputIFsvsname '{}' --inputPASxmlname '{}' --orig_IF_Thre {} --TransXY {}".format(args.inputImageFilePAS, args.inputImageFileIF, args.inputAnnotationFile,args.Podocyte_threshold,args.TranslationXY)
    os.system(cmd)    

if __name__ == "__main__":
    main(CLIArgumentParser().parse_args())
