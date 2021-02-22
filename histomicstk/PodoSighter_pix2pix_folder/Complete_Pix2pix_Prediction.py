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
from create_p2p_outxml import create_p2p_outxml
import glob
from subprocess import call
import imageio
from skimage import io
from skimage.transform import resize
from skimage.util import img_as_ubyte
import argparse
import shutil

##python3 Complete_Pix2pix_Prediction.py -A0 '/hdd/d8/tmpUI/tmp3' -A1 '/hdd/d8/PAS_folder/JPH12.svs' -A2 '/hdd/d8/PAS_folder/JPH12.xml'
## -A3 '/hdd/d8/tmpUI/tmp2/checkpoint/HUMP57/latest_net_G.pth' -A4 '/hdd/d8/tmpUI/tmp2/checkpoint/HUMP57/latest_net_D.pth'
## -A5 'outxml1.xml' -A6 0.1 -A7 5 -A8 3 -A9 'human' -A10 'p57'


parser = argparse.ArgumentParser(description = '')
parser.add_argument('-A0','--inputfolder',type = str, metavar = '',required = True,help = 'folder name')
parser.add_argument('-A1','--inputsvs',type = str, metavar = '',required = True,help = 'image name')
parser.add_argument('-A2','--glomxml',type = str, metavar = '',required = True,help = ' glom xml')
parser.add_argument('-A3','--GeneratorModel',type = str, metavar = '',required = True,help = 'GeneratorModel')
parser.add_argument('-A4','--DiscriminatorModel',type = str, metavar = '',required = True,help = 'DiscriminatorModel')
parser.add_argument('-A5','--outxml1',type = str, metavar = '',required = True,help = 'outxml1')
parser.add_argument('-A6','--PASnucleiThreshold',type = float, metavar = '',required = True,help = 'PASnucleiThreshold')
parser.add_argument('-A7','--gauss_filt_size',type = int, metavar = '',required = True,help = 'gauss_filt_size')
parser.add_argument('-A8','--Disc_size',type = int, metavar = '',required = True,help = 'Disc_size')
parser.add_argument('-A9','--species',type = str, metavar = '',required = True,help = 'species')
parser.add_argument('-A10','--stain',type = str, metavar = '',required = True,help = 'stain')

args = parser.parse_args()


maintempfolder = args.inputfolder
svs_file_name = args.inputsvs
xml_file_name = args.glomxml
Gen_model_name = args.GeneratorModel
Disc_model_name = args.DiscriminatorModel
output_anno_file_podocyte = args.outxml1
PASnucleiThreshold = args.PASnucleiThreshold
gauss_size = args.gauss_filt_size
size_disc = args.Disc_size
species_name = args.species
stain_name = args.stain

print(maintempfolder)
print(svs_file_name)
print(xml_file_name)
print(Gen_model_name)
print(Disc_model_name)
print(output_anno_file_podocyte)
print(PASnucleiThreshold)
print(gauss_size)
print(size_disc)
print(species_name)
print(stain_name)

try:
    if species_name =='human' and stain_name =='p57':
        Model_majorname = 'HUMP57'
        crop_size = 1200
    elif species_name =='human' and stain_name =='wt1':
        Model_majorname = 'HUMWT1'
        crop_size = 1200
    elif species_name =='rat' and stain_name =='p57':
        Model_majorname = 'RATP57'
        crop_size = 800
    elif species_name =='rat' and stain_name =='wt1':
        Model_majorname = 'RATWT1'
        crop_size = 800
    elif species_name =='mouse' and stain_name =='p57':
        Model_majorname = 'MOUP57'
        crop_size = 600
    elif species_name =='mouse' and stain_name =='wt1':
        Model_majorname = 'MOUWT1'
        crop_size = 600
except:
    print("Incorrect species or stain. Try again")
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

shutil.copy(srcGen, dstGenDisc) 
shutil.copy(srcDisc, dstGenDisc) 


'''Input'''
'''========='''
svsfile = svs_file_name
xmlfile = xml_file_name

PAS_nuc_thre = PASnucleiThreshold
gauss_filt_size = gauss_size
Disc_size = size_disc

output_anno_file = output_anno_file_podocyte


'''Step 1: Crop svs file into glomeruli and masks'''
'''=============================================='''

cropFolderPAS ='/hdd/d8/tmpUI/tmp2/cropPAS/'#tmpgirder/cropPAS/
cropFolderGlom ='/hdd/d8/tmpUI/tmp2/cropGlom/'#tmpgirder/cropGlom/
Imagename = os.path.basename(svsfile).split('.')[0]

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
       
exit_code = call("python3 ../pix2pix/test.py --dataroot "+domABtemp+" --name "+Model_majorname+" --checkpoints_dir "+chkpointdir_location+" --results_dir "+Results_save_folder+" --model pix2pix", shell=True)


'''Step 3: Save pix2pix predictions'''
'''==============================='''

resdir_exact = Results_save_folder+Model_majorname+"/test_latest/images/"
create_p2p_outxml(svsfile,xmlfile,crop_size,resdir_exact,PAS_nuc_thre,gauss_filt_size,Disc_size,output_anno_file)
