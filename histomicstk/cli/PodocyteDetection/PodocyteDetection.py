import os
from histomicstk.cli.utils import CLIArgumentParser

def main(args2):
    print("cpython3 ../plugin_podfolder/pod_plugin6.py -P '{}' -F '{}' -L '{}' -T {} -Tx {} -Ty {}".format(args2.inputImageFilePAS, args2.inputImageFileIF, args2.inputAnnotationFile,args2.Podocyte_threshold,args2.TranslationX,args2.TranslationY))
    print("dpython3 ../plugin_podfolder/pod_plugin6.py -P '/mnt/girder_worker/ae5d02f4c97b42a7b227b978472c5cc5/24_PAS.svs' -F '/mnt/girder_worker/ae5d02f4c97b42a7b227b978472c5cc5/24_IF.svs' -L '/mnt/girder_worker/ae5d02f4c97b42a7b227b978472c5cc5/24_PAS.xml' -T 0.4 -Tx 211 -Ty -375))
    
    cmd = "python3 ../plugin_podfolder/pod_plugin6.py -P '{}' -F '{}' -L '{}' -T {} -Tx {} -Ty {}".format(args2.inputImageFilePAS, args2.inputImageFileIF, args2.inputAnnotationFile,args2.Podocyte_threshold,args2.TranslationX,args2.TranslationY)
    #cmd = "python3 ../plugin_podfolder/pod_plugin6.py -P '/mnt/girder_worker/ae5d02f4c97b42a7b227b978472c5cc5/24_PAS.svs' -F '/mnt/girder_worker/ae5d02f4c97b42a7b227b978472c5cc5/24_IF.svs' -L '/mnt/girder_worker/ae5d02f4c97b42a7b227b978472c5cc5/24_PAS.xml' -T 0.4 -Tx 211 -Ty -375"
    os.system(cmd)    

if __name__ == "__main__":
    main(CLIArgumentParser().parse_args())
