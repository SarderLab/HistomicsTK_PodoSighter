import os
import sys
import shutil
from readPAS_cropGlom import readPAS_cropGlom
import argparse
from create_podocyte_Outxml_CNN import create_podocyte_Outxml_CNN

import json
import xml.etree.ElementTree as ET
from xmltojson import xmltojson
'''
python3 Complete_CNN_Prediction.py -A0 '/hdd/d8/dplb/tmp' -A1 '/hdd/d8/dplb/slides/JPH12.svs' -A2 '/hdd/d8/dplb/slides/JPH12.xml' -A3 '/hdd/d8/dplb/chkpt_folder/hump57_model.ckpt-50000.data-00000-of-00001' -A4 '/hdd/d8/dplb/chkpt_folder/hump57_checkpoint' -A5 '/hdd/d8/dplb/chkpt_folder/hump57_model.ckpt-50000.index' -A6 'human' -A7 'p57' -A8 'out1.xml' -A9 0.4 -A10 5 -A11 6 -A12 0 -A13 400 -A14 0.2
'''
parser = argparse.ArgumentParser(description = '')
parser.add_argument('-A0','--inputfolder',type = str, metavar = '',required = True,help = 'folder name')
parser.add_argument('-A1','--inputsvs',type = str, metavar = '',required = True,help = 'image name')
parser.add_argument('-A2','--glomxml',type = str, metavar = '',required = True,help = ' glom xml')
parser.add_argument('-A3','--Model',type = str, metavar = '',required = True,help = 'Model')
parser.add_argument('-A4','--Modelchkpt',type = str, metavar = '',required = True,help = 'Modelchkpt')
parser.add_argument('-A5','--Modelidx',type = str, metavar = '',required = True,help = 'Modelidx')
parser.add_argument('-A6','--species',type = str, metavar = '',required = True,help = 'species')
parser.add_argument('-A7','--stain',type = str, metavar = '',required = True,help = 'stain')
parser.add_argument('-A8','--outxml1',type = str, metavar = '',required = True,help = 'outxml1')
parser.add_argument('-A9','--PASnucleiThreshold',type = float, metavar = '',required = True,help = 'PASnucleiThreshold')
parser.add_argument('-A10','--gauss_filt_size',type = int, metavar = '',required = True,help = 'gauss_filt_size')
parser.add_argument('-A11','--Disc_size',type = int, metavar = '',required = True,help = 'Disc_size')
parser.add_argument('-A12','--resolut',type = int, metavar = '',required = True,help = 'resolut')
parser.add_argument('-A13','--sz_thre',type = int, metavar = '',required = True,help = 'sz_thre')
parser.add_argument('-A14','--watershed_thre',type = float, metavar = '',required = True,help = 'watershed_thre')
parser.add_argument('-A15','--jsonout',type = str, metavar = '',required = True,help = 'jsonout')


args = parser.parse_args()

maintempfolder = args.inputfolder
svs_file_name = args.inputsvs
xml_file_name = args.glomxml
Model = args.Model
Modelchkpt = args.Modelchkpt
Modelidx = args.Modelidx
species_name = args.species
stain_name = args.stain
output_anno_file_podocyte = args.outxml1
PAS_nuc_thre = args.PASnucleiThreshold
gauss_filt_size = args.gauss_filt_size
size_disc = args.Disc_size
resol = args.resolut
size_thre = args.sz_thre
watershed_dist_thre = args.watershed_thre
jout = args.jsonout

#shutil.rmtree(maintempfolder)
#os.mkdir(maintempfolder)

print(maintempfolder)
print(svs_file_name)
print(xml_file_name)
print(Model)
print(Modelchkpt)
print(Modelidx)
print(species_name)
print(stain_name)
print(args.outxml1)
print(PAS_nuc_thre)
print(gauss_filt_size)
print(size_disc)
print(resol)
print(size_thre)
print(watershed_dist_thre)
print(args.jsonout)

try:
    if species_name =='human' and stain_name =='p57':
        crop_size = 1200
    elif species_name =='human' and stain_name =='wt1':
        crop_size = 1200
    elif species_name =='rat' and stain_name =='p57':
        crop_size = 800
    elif species_name =='rat' and stain_name =='wt1':
        crop_size = 800
    elif species_name =='mouse' and stain_name =='p57':
        crop_size = 800
    elif species_name =='mouse' and stain_name =='wt1':
        crop_size = 800
except:
    print("Incorrect species or stain. Try again")
    sys.exit()
    
'''Create temporary directories'''
'''============================='''

cropFolderPAS = maintempfolder +'/Data/PC1/PodCNN1/Images/val'
cropFolderGlom = maintempfolder +'/Data/PC1/PodCNN1/labels/val'
tfrecord_dir = maintempfolder +'/Data/PC1/tfrecord'
chkpt_dir = maintempfolder+'/model/train_log'
vislogdir = maintempfolder+'/model/vis_log'

os.makedirs(cropFolderPAS+'/')
os.makedirs(cropFolderGlom)
os.makedirs(chkpt_dir)
os.makedirs(vislogdir)


'''Copy models to temp checkpoint dir'''
'''============================================'''
src1 = Model
src2 = Modelchkpt
src3 = Modelidx

dst123 = chkpt_dir + '/'

shutil.copy(src1, (dst123+'model.ckpt-50000.data-00000-of-00001')) 
shutil.copy(src2, (dst123+'checkpoint')) 
shutil.copy(src3, (dst123+'model.ckpt-50000.index')) 

'''Input'''
'''======'''
svsfile = svs_file_name
xmlfile = xml_file_name


'''Step 1: Crop svs file into glomeruli and masks'''
'''=============================================='''


Imagename = os.path.basename(svsfile).split('.')[0]

readPAS_cropGlom(svsfile,xmlfile,crop_size,cropFolderPAS+'/',cropFolderGlom+'/')


'''Step 2: Convert to tfrecord'''
'''==========================='''

cmd3 = "python build_tf_record_glomData.py --val_image_folder "+cropFolderPAS+" --val_image_label_folder "+cropFolderGlom+" --output_dir "+tfrecord_dir
os.system(cmd3)


'''Step 3: Test'''
'''==========================='''
test_folder = "\"val\""
cropsize = "\"{},{}\"".format(crop_size,crop_size)
data_dir =  "\"{}\"".format(tfrecord_dir)
chkptdirloc =  "\"{}\"".format(chkpt_dir)
vislogdirloc =  "\"{}\"".format(vislogdir)

print(os.getcwd())
#../pix2pix/datasets/combine_A_and_B
#/home/d8/dplb/research/deeplab/vis.py

cmd5 = "python3 ../Pod_DL/deeplab/vis.py \
    --logtostderr \
    --vis_split="+test_folder+" \
    --model_variant=\"xception_65\" \
    --atrous_rates=6 \
    --atrous_rates=12 \
    --atrous_rates=18 \
    --output_stride=16 \
    --decoder_output_stride=4 \
    --vis_crop_size="+cropsize+" \
    --max_number_of_iterations=1 \
    --dataset=\"PC1\" \
    --checkpoint_dir="+chkptdirloc+" \
    --vis_logdir="+vislogdirloc+" \
    --dataset_dir="+data_dir

os.system(cmd5)  


'''Step 5: Output display'''
'''==========================='''
resdir_exact = vislogdir+"/raw_segmentation_results/"

xml_data= create_podocyte_Outxml_CNN(svsfile,xmlfile,crop_size,resdir_exact,PAS_nuc_thre,size_thre,gauss_filt_size,watershed_dist_thre,size_disc,resol)
f = open(args.outxml1, 'wb')
f.write(xml_data)
f.close()

tree = ET.parse(args.outxml1)
root = tree.getroot()
annotation = xmltojson(root)
with open(args.jsonout, 'w') as annotation_file:
    json.dump(annotation, annotation_file, indent=2, sort_keys=False)
