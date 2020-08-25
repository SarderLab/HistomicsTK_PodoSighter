# -*- coding: utf-8 -*-
"""
Created on Tue Aug 25 08:54:04 2020

@author: darsh
"""

import os
from histomicstk.cli.utils import CLIArgumentParser

def main(args):
    cmd = "python3 ../plugin_podfolder/pod_plugin4.py --inputPASsvsname '{}' --inputIFsvsname '{}' --inputPASxmlname '{}' --outfilename '{}' --orig_IF_Thre {} --Disc_size {} --TransXY {}".format(args.inputImageFilePAS, args.inputImageFileIF, args.inputAnnotationFile, args.outputAnnotationFile,args.Podocyte_threshold,args.DiscSize,args.TranslationXY)
    os.system(cmd)    

if __name__ == "__main__":
    main(CLIArgumentParser().parse_args())


