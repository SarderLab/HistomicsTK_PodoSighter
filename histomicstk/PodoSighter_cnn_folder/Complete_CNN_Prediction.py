import os
import sys
import shutil
from readPAS_cropGlom import readPAS_cropGlom
import argparse
from create_podocyte_Outxml_CNN import create_podocyte_Outxml_CNN

from mask_to_xml import mask_to_xml
from xml_to_json import convert_xml_json

import sys
sys.path.append("../HistomicsTK_PodoSighter/histomicstk/PodoSighter_cnn_folder/")
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
parser.add_argument('-A7','--PASnucleiThreshold',type = float, metavar = '',required = True,help = 'PASnucleiThreshold')
parser.add_argument('-A8','--gauss_filt_size',type = int, metavar = '',required = True,help = 'gauss_filt_size')
parser.add_argument('-A9','--Disc_size',type = int, metavar = '',required = True,help = 'Disc_size')
parser.add_argument('-A10','--resolut',type = int, metavar = '',required = True,help = 'resolution')
parser.add_argument('-A11','--sz_thre',type = int, metavar = '',required = True,help = 'sz_thre')
parser.add_argument('-A12','--watershed_thre',type = float, metavar = '',required = True,help = 'watershed_thre')
parser.add_argument('-A13','--jsonout',type = str, metavar = '',required = True,help = 'jsonout')
parser.add_argument('-A14','--outxml1',type = str, metavar = '',required = True,help = 'outxml1')


args = parser.parse_args()

maintempfolder = args.inputfolder
svs_file_name = args.inputsvs
xml_file_name = args.glomxml
Model = args.Model
Modelchkpt = args.Modelchkpt
Modelidx = args.Modelidx
species_name = args.species
PAS_nuc_thre = args.PASnucleiThreshold
gauss_filt_size = args.gauss_filt_size
size_disc = args.Disc_size
resol = args.resolut
size_thre = args.sz_thre
watershed_dist_thre = args.watershed_thre

#shutil.rmtree(maintempfolder)
#os.mkdir(maintempfolder)

print(maintempfolder)
print(svs_file_name)
print(xml_file_name)
print(Model)
print(Modelchkpt)
print(Modelidx)
print(species_name)
print(PAS_nuc_thre)
print(gauss_filt_size)
print(size_disc)
print(resol)
print(watershed_dist_thre)
print(args.jsonout)
print(args.outxml1)


try:
    if species_name =='human':
        crop_size = 1200    
    elif species_name =='rat':
        crop_size = 800    
    elif species_name =='mouse':
        crop_size = 800
except:
    print("Incorrect species. Try again")
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

cmd3 = "python ../PodoSighter_cnn_folder/build_tf_record_glomData.py --val_image_folder "+cropFolderPAS+" --val_image_label_folder "+cropFolderGlom+" --output_dir "+tfrecord_dir
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

cmd5 = "python3 ../deeplab/vis.py \
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
TP_HR= create_podocyte_Outxml_CNN(svsfile,xmlfile,crop_size,resdir_exact,PAS_nuc_thre,size_thre,gauss_filt_size,watershed_dist_thre,size_disc,resol)

from skimage import exposure

TP_HR = exposure.rescale_intensity(TP_HR, in_range='image', out_range=(0,1))

if args.resolut==0:
    downsample_factor=1
else:
    downsample_factor=4  

import cv2
import FNs
import numpy as np
import lxml.etree as ET
import json
from xmltojson import xmltojson
   
offset={'X': 0,'Y': 0}    
maskPoints,_ = cv2.findContours(np.array((np.uint8(TP_HR))), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
pointsList = []
for j in range(np.shape(maskPoints)[0]):
    pointList = []
    for i in range(np.shape(maskPoints[j])[0]):
        point = {'X': (maskPoints[j][i][0][0]*downsample_factor) + offset['X'], 'Y': (maskPoints[j][i][0][1]*downsample_factor) + offset['Y']}
        pointList.append(point)
    pointsList.append(pointList)
Annotations = ET.Element('Annotations', attrib={'MicronsPerPixel': '0.136031'})
col1 = str(65280)
Annotations = FNs.xml_add_annotation(Annotations=Annotations,annotationID=1,LC = col1)

for i in range(np.shape(pointsList)[0]):
    pointList = pointsList[i]
    Annotations = FNs.xml_add_region(Annotations=Annotations, pointList=pointList)  

xml_data = ET.tostring(Annotations, pretty_print=True)
f = open(args.outxml1, 'wb')
f.write(xml_data)
f.close()

tree = ET.parse(args.outxml1)
root = tree.getroot()

json_data = xmltojson(root)
with open(args.jsonout, 'w') as annotation_file:
    json.dump(json_data, annotation_file, indent=2, sort_keys=False)
