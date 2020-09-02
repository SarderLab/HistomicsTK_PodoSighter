import os
from histomicstk.cli.utils import CLIArgumentParser

def main(args2):     
    
    cmd = "python3 ../plugin_podfolder/glom_plugin_temp.py -P '{}' -L '{}' -C '{}' -M '{}'".format(args2.inputImageFilePAS, args2.inputAnnotationFile,args2.csvFile,args2.outputAnnotationFile)
    os.system(cmd)    

if __name__ == "__main__":
    main(CLIArgumentParser().parse_args())
