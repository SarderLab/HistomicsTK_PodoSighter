import os
from histomicstk.cli.utils import CLIArgumentParser

def main(args2):     
    
#    cmd = "python3 ../PodoSighter_pix2pix_folder/Complete_Pix2pix_Prediction.py -A1 '{}' -A2 '{}' -A3 {} -A4 '{}' -A5 '{}' -A6 '{}' -A7 '{}' -A8 '{}' -A9 {} -A10 '{}' -A11 '{}' ".format(args2.inputImageFile, args2.inputAnnotationFile1,args2.slider, args2.outputAnnotationFile1 ,args2.outputAnnotationFile2 , args2.csvFile)
#python3 Complete_Pix2pix_Prediction.py -A0 '/hdd/d8/tmpUI/tmp3' -A1 '/hdd/d8/PAS_folder/JPH12.svs' -A2 '/hdd/d8/PAS_folder/JPH12.xml' -A3 '/hdd/d8/tmpUI/tmp2/checkpoint/HUMP57/latest_net_G.pth' -A4 '/hdd/d8/tmpUI/tmp2/checkpoint/HUMP57/latest_net_D.pth' -A5 'outxml1.xml' -A6 0.1 -A7 5 -A8 3 -A9 'human' -A10 'p57'
    
    cmd = "python3 ../PodoSighter_pix2pix_folder/Complete_Pix2pix_Prediction.py -A0 '{}' -A1 '{}' -A2 '{}' -A3 '{}' -A4 '{}' -A5 '{}' -A6 {} -A7 {} -A8 {} -A9 '{}' -A10 '{}'".format(args2.inputFolder, args2.inputImageFile,args2.inputAnnotationFile1, args2.TrainedGeneratorModel ,args2.TrainedDiscriminatorModel,args2.outputAnnotationFile1, args2.PASnucleiThreshold,args2.gauss_filt_size, args2.Disc_size ,args2.species,args2.stain)

    os.system(cmd)    

if __name__ == "__main__":
    main(CLIArgumentParser().parse_args())