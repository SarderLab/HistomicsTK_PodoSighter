# -*- coding: utf-8 -*-
"""
Created on Mon Feb 22 11:09:00 2021
Full pix2pix prediction
@author: d8@buffalo.edu
"""
import sys
sys.path.append("..")

import os
from readPAS_cropGlom import readPAS_cropGlom
import glob
from subprocess import call
import imageio
from skimage import io
from skimage.transform import resize
from skimage.util import img_as_ubyte
import argparse
import shutil
from create_podocyte_Outxml_pix2pix import create_podocyte_Outxml_pix2pix

from mask_to_xml import mask_to_xml
from xml_to_json import convert_xml_json

##python3 Complete_Pix2pix_Prediction.py -A0 '/hdd/d8/tmpUI/tmp3' -A1 '/hdd/d8/PAS_folder/JPH12.svs' -A2 '/hdd/d8/PAS_folder/JPH12.xml'
## -A3 '/hdd/d8/tmpUI/tmp2/checkpoint/HUMP57/latest_net_G.pth' -A4 '/hdd/d8/tmpUI/tmp2/checkpoint/HUMP57/latest_net_D.pth'
## -A5 'outxml1.xml' -A6 0.1 -A7 5 -A8 3 -A9 'human' -A10 'p57'


parser = argparse.ArgumentParser(description = '')
parser.add_argument('-A0','--inputfolder',type = str, metavar = '',required = True,help = 'folder name')
parser.add_argument('-A1','--inputsvs',type = str, metavar = '',required = True,help = 'image name')
parser.add_argument('-A2','--glomxml',type = str, metavar = '',required = True,help = ' glom xml')
parser.add_argument('-A3','--GeneratorModel',type = str, metavar = '',required = True,help = 'GeneratorModel')
parser.add_argument('-A4','--DiscriminatorModel',type = str, metavar = '',required = True,help = 'DiscriminatorModel')
parser.add_argument('-A5','--PASnucleiThreshold',type = float, metavar = '',required = True,help = 'PASnucleiThreshold')
parser.add_argument('-A6','--gauss_filt_size',type = int, metavar = '',required = True,help = 'gauss_filt_size')
parser.add_argument('-A7','--Disc_size',type = int, metavar = '',required = True,help = 'Disc_size')
parser.add_argument('-A8','--species',type = str, metavar = '',required = True,help = 'species')
parser.add_argument('-A9','--gpu_id',type = int, metavar = '',required = True,help = 'gpu_id')
parser.add_argument('-A10','--resolut',type = int, metavar = '',required = True,help = 'resolut')
parser.add_argument('-A11','--sz_thre',type = int, metavar = '',required = True,help = 'sz_thre')
parser.add_argument('-A12','--watershed_thre',type = float, metavar = '',required = True,help = 'watershed_thre')
parser.add_argument('-A13','--jsonout',type = str, metavar = '',required = True,help = 'jsonout')
parser.add_argument('-A14','--outxml1',type = str, metavar = '',required = True,help = 'outxml1')
parser.add_argument('-A15','--tissue_thickness',type = float, metavar = '',required = True,help = 'Tissue thickness')#new
parser.add_argument('-A16','--csvfilename',type = str, metavar = '',required = True,help = 'CSV file name')#new


args = parser.parse_args()


maintempfolder = args.inputfolder
svs_file_name = args.inputsvs
xml_file_name = args.glomxml
Gen_model_name = args.GeneratorModel
Disc_model_name = args.DiscriminatorModel
PASnucleiThreshold = args.PASnucleiThreshold
gauss_size = args.gauss_filt_size
size_disc = args.Disc_size
species_name = args.species
gpu_id_use = args.gpu_id
watershed_dist_thre= args.watershed_thre
size_thre = args.sz_thre
resol = args.resolut
tissue_thickness = args.tissue_thickness#new
csv_file_name = args.csvfilename#new

print(maintempfolder)
print(svs_file_name)
print(xml_file_name)
print(Gen_model_name)
print(Disc_model_name)
print(PASnucleiThreshold)
print(gauss_size)
print(size_disc)
print(species_name)
print(gpu_id_use)
print(watershed_dist_thre)
print(size_thre)
print(resol)
print(args.outxml1)
print(tissue_thickness)#new
print(csv_file_name)#new

try:
    if species_name =='human':
        Model_majorname = 'HUMP57'
        crop_size = 1200    
    elif species_name =='rat':
        Model_majorname = 'RATP57'
        crop_size = 800    
    elif species_name =='mouse':
        Model_majorname = 'MOUP57'
        crop_size = 800    
except:
    print("Incorrect species. Try again")
    sys.exit()

'''Create temporary directories'''
'''============================='''

cropFolderPAS = maintempfolder +'/cropPAS/'
cropFolderGlom = maintempfolder +'/cropGlom/'
chkpointdir_location = maintempfolder+'/checkpoint/'
Results_save_folder = maintempfolder+'/results/'
dstholdoutPAS = maintempfolder+'/domA/'
dstholdoutPAStest = dstholdoutPAS+'test/'
domABtemp = maintempfolder+'/domAB/'
domABtemptest = domABtemp+'test/'

os.mkdir(cropFolderPAS)
os.mkdir(cropFolderGlom)
os.mkdir(chkpointdir_location)
os.mkdir(Results_save_folder)
os.mkdir(dstholdoutPAS)
os.mkdir(dstholdoutPAStest)
os.mkdir(domABtemp)

'''Copy Gen Disc models to temp checkpoint dir'''
'''============================================'''
srcGen = Gen_model_name
srcDisc = Disc_model_name

dstGenDisc = chkpointdir_location + Model_majorname + '/'
os.mkdir(dstGenDisc)

shutil.copy(srcGen, (dstGenDisc+ '/latest_net_G.pth')) 
shutil.copy(srcDisc, (dstGenDisc+'/latest_net_D.pth')) 


'''Input'''
'''========='''
svsfile = svs_file_name
xmlfile = xml_file_name

PAS_nuc_thre = PASnucleiThreshold
gauss_filt_size = gauss_size
Disc_size = size_disc


'''Step 1: Crop svs file into glomeruli and masks'''
'''=============================================='''


Imagename = os.path.basename(svsfile).split('.')[0]
print(cropFolderPAS)

readPAS_cropGlom(svsfile,xmlfile,crop_size,cropFolderPAS,cropFolderGlom)


'''Step 2: Run pix2pix predictions'''
'''==============================='''

for f in glob.glob(cropFolderPAS+ '*.png'):
    im = io.imread(f)

    '''Resize to 256 for p2p'''
    im = resize(im,(256,256))
    im=img_as_ubyte(im)        
    
    '''patchname'''
    imname = os.path.basename(f)
    patchname = imname[:-4]
    print(patchname)
  
    imageio.imwrite(dstholdoutPAStest +patchname+'.png',im)

exit_code = call("python3 ../pix2pix/datasets/combine_A_and_B.py --fold_A "+ dstholdoutPAS +" --fold_B " + dstholdoutPAS +" --fold_AB "+domABtemp, shell=True)   
       
exit_code = call("python3 ../pix2pix/test.py --dataroot "+domABtemp+" --gpu_ids "+str(gpu_id_use)+" --name "+Model_majorname+" --checkpoints_dir "+chkpointdir_location+" --results_dir "+Results_save_folder+" --model pix2pix", shell=True)


'''Step 3: Save pix2pix predictions'''
'''==============================='''

resdir_exact = Results_save_folder+Model_majorname+"/test_latest/images/"
TP_HR= create_podocyte_Outxml_pix2pix(svsfile,xmlfile,crop_size,resdir_exact,PAS_nuc_thre,size_thre,gauss_filt_size,watershed_dist_thre,Disc_size,resol,tissue_thickness,csv_file_name)#new

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
