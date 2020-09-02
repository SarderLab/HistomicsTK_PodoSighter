import os
from histomicstk.cli.utils import CLIArgumentParser

def main(args2):    
    
    cmd = "python3 ../plugin_podfolder/pod_plugin6.py -P '{}' -F '{}' -L '{}' -T {} -Tx {} -Ty {}".format(args2.inputImageFilePAS, args2.inputImageFileIF, args2.inputAnnotationFile,args2.Podocyte_threshold,args2.TranslationX,args2.TranslationY)
    os.system(cmd)    

if __name__ == "__main__":
    main(CLIArgumentParser().parse_args())
