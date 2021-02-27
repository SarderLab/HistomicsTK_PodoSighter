import openslide
import numpy as np
from getMaskFromXml import getMaskFromXml
from skimage.transform import rescale,resize 
import os
from skimage.measure import label,regionprops
import cv2
import imageio
import warnings

warnings.filterwarnings("ignore")


def readPAS_cropGlom(svsfile,xmlfile,crop_size,cropFolderPAS,cropFolderGlom):
    
    print("Reading PAS file...")
    Imagename = os.path.basename(svsfile).split('.')[0]
    sourcePAS = openslide.open_slide(svsfile)
    print("Opening WSIs in mid resolution...")
    PAS = np.array(sourcePAS.read_region((0,0),1,sourcePAS.level_dimensions[1]),dtype = "uint8")
    PAS = PAS[:,:,0:3]    
    
    '''XML annotation to mask'''
    '''======================'''  
    print("Converting Glom xml to mask...")    
    PASmaskmain = getMaskFromXml(sourcePAS,xmlfile)   
    PASmask = rescale(PASmaskmain, 1, anti_aliasing=False)*1
    
    flip_flag = 0
    if(PASmask.shape[0] ==sourcePAS.level_dimensions[1][1]):
        print("PAS and Mask mid resolution is flipped...")
        flip_flag = 1
        
    highres_w = crop_size/4
    
    countPatch  = 0
    c = 0
    for region in regionprops(label(PASmask)):
        c +=1
        minr, minc, maxr, maxc = region.bbox
        
        ptx = (minr+maxr)/2
        pty = (minc+maxc)/2
                
        centroids = [pty,ptx]    
        startx = int(max((centroids[0]-(highres_w/2))*4,0))
        starty = int(max((centroids[1]-(highres_w/2))*4,0))
        endx = int(highres_w*4)
        endy = int(highres_w*4)
       
        crop_imgPAS = np.array(sourcePAS.read_region(((startx),(starty)),0,((endx),(endy))),dtype = "uint8")
        crop_imgPAS = crop_imgPAS[:,:,0:3]
     
        
        Glommask_1 = PASmask[int(ptx-(highres_w/2)):int(ptx+(highres_w/2)),int(pty-(highres_w/2)):int(pty+(highres_w/2))]
        if crop_imgPAS[:,:,0].shape != (Glommask_1.shape[0]*4,Glommask_1.shape[1]*4):
            continue

        Glommask2 = resize(Glommask_1,(highres_w*4,highres_w*4),anti_aliasing=True)*1
        Glommask2 = cv2.threshold((Glommask2), 0.1, 255, cv2.THRESH_BINARY)[1]    
    
        print("Saving patches...") 
        if crop_imgPAS.shape == (highres_w*4,highres_w*4,3):
            countPatch += 1
            filename = Imagename +'_'+str(countPatch)  
            print(filename)           
            
            imageio.imwrite(cropFolderPAS +filename+ ".png",crop_imgPAS)
            imageio.imwrite(cropFolderGlom +filename+ ".png",Glommask2)

