import os
from histomicstk.cli.utils import CLIArgumentParser

def main(args2):

    #cmd = "python3 ../plugin_podfolder/pod_plugin6.py -P '{}' -F '{}' -L '{}' -T {} -Tx {} -Ty {}".format(args.inputImageFilePAS, args.inputImageFileIF, args.inputAnnotationFile,args.Podocyte_threshold,args.TranslationX,args.TranslationY)
    cmd = "python3 ../plugin_podfolder/pod_plugin6.py -P '/mnt/girder_worker/ae5d02f4c97b42a7b227b978472c5cc5/24_PAS.svs' -F '/mnt/girder_worker/ae5d02f4c97b42a7b227b978472c5cc5/24_IF.svs' -L '/mnt/girder_worker/ae5d02f4c97b42a7b227b978472c5cc5/24_PAS.xml' -T 0.4 -Tx 211 -Ty -375"
    os.system(cmd)    

if __name__ == "__main__":
    main(CLIArgumentParser().parse_args())
