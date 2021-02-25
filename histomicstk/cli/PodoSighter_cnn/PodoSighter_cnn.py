import os
from histomicstk.cli.utils import CLIArgumentParser

def main(args2):         
    
    #cmd = "python3 ../PodoSighter_pix2pix_folder/Complete_Pix2pix_Prediction.py -A0 '{}' -A1 '{}' -A2 '{}' -A3 '{}' -A4 '{}' -A5 '{}' -A6 {} -A7 {} -A8 {} -A9 '{}' -A10 '{}' -A11 {}".format(args2.inputFolder, args2.inputImageFile,args2.inputAnnotationFile1, args2.TrainedGeneratorModel ,args2.TrainedDiscriminatorModel,args2.outputAnnotationFile1, args2.PASnucleiThreshold,args2.gauss_filt_size, args2.Disc_size ,args2.species,args2.stain,args2.gpu_id)
    cmd = "python3 ../PodoSighter_cnn_folder/Complete_CNN_Prediction.py -A0 '{}' -A1 '{}' -A2 '{}' -A3 '{}' -A4 '{}' -A5 '{}' -A6 '{}' -A7 '{}' -A8 '{}' -A9 {} -A10 {} -A11 {} -A12 {} -A13 {} -A14 {} -A15 '{}'".format(args2.inputFolder, args2.inputImageFile,args2.inputAnnotationFile1, args2.Model,args2.Modelchkpt,args2.Modelidx, args2.species,args2.stain, args2.outputAnnotationFile1, args2.PASnucleiThreshold,args2.gauss_filt_size, args2.Disc_size,args2.resolut,args2.sz_thre,args2.watershed_thre,args2.outputAnnotationFile2)

    os.system(cmd)    

if __name__ == "__main__":
    main(CLIArgumentParser().parse_args())
