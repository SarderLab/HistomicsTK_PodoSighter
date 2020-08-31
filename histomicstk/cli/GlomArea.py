import os
from histomicstk.cli.utils import CLIArgumentParser

def main(args2):    
     
    cmd = "python3 ../plugin_podfolder/glom_plugin7.py -P '{}' -L '{}'".format(args2.inputImageFilePAS, args2.inputAnnotationFile)
    os.system(cmd)    

if __name__ == "__main__":
    main(CLIArgumentParser().parse_args())
