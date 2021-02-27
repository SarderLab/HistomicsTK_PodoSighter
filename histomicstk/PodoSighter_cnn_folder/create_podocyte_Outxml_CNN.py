# -*- coding: utf-8 -*-
"""
Created on Mon Feb 22 11:33:18 2021

@author: darsh
"""
import openslide
import numpy as np
from getMaskFromXml import getMaskFromXml
from skimage.transform import rescale,resize 
import os
from skimage.measure import label,regionprops
import cv2
import matplotlib.pyplot as plt
import FNs
import lxml.etree as ET
from getPASnuclei import getPASnuclei
import imageio

def create_podocyte_Outxml_CNN(svsfile,xmlfile,crop_size,resdir,PAS_nuc_thre,size_thre,gauss_filt_size,watershed_dist_thre,disc_size,resol):
    
    print("Reading PAS file...")
    Imagename = os.path.basename(svsfile).split('.')[0]
    sourcePAS = openslide.open_slide(svsfile)
    print("Opening WSIs in mid resolution...")
    PAS = np.array(sourcePAS.read_region((0,0),1,sourcePAS.level_dimensions[1]),dtype = "uint8")
    PAS = PAS[:,:,0:3]    
    
    '''XML annotation to mask'''
    '''======================'''  
    print("Converting Glom xml to mask...")    
    PASmask = rescale(getMaskFromXml(sourcePAS,xmlfile), 1, anti_aliasing=False)*1
    highres_w = crop_size/4

    if resol == 0:
        TPI_F = np.zeros((sourcePAS.level_dimensions[0][1],sourcePAS.level_dimensions[0][0]))
    else:
        TPI_F = np.zeros((sourcePAS.level_dimensions[1][1],sourcePAS.level_dimensions[1][0]))
    print(TPI_F.shape)
    
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
    
        print("Analyzing patches...")
        '''========================================='''
        
        if crop_imgPAS.shape == (highres_w*4,highres_w*4,3):
            countPatch += 1
            filename = Imagename +'_'+str(countPatch)  
            print(filename) 
            
            cnn_out_name = 'b'+"'"+filename+".png'"+".png"
            
            fil_name = resdir+ cnn_out_name           
            predicted_im = imageio.imread(fil_name)
#            predicted_im = resize(predicted_im, (crop_imgPAS[:,:,0].shape),anti_aliasing=True)
            
            '''Segment pix2pix detected podocyte nuclei'''
            '''========================================='''            

            predicted_mask = predicted_im==2*1

            
            '''Segment PAS nuclei'''
            '''========================================='''
            AllPAS = (getPASnuclei(crop_imgPAS[:,:,0:3],Glommask2,PAS_nuc_thre,size_thre,gauss_filt_size,watershed_dist_thre,disc_size))*1

            LabelPAS = label(AllPAS)
            FakePodPASmask = np.zeros(AllPAS.shape)            
            count2 = 1
            for reg in LabelPAS:
                eachIm = (LabelPAS == count2)*1
                eachImprops = regionprops(eachIm)
                N_area = [eprop.area for eprop in eachImprops]
                count2+=1
                if not N_area:
                    continue
                else:
                    if (np.sum(eachIm*predicted_mask*1)>int(0.7*float(N_area[0]))):
                        FakePodPASmask = FakePodPASmask + eachIm
                  
            del predicted_im
            

            if resol ==0:
                if Imagename[0:3]=='NTN':
                    try:
                        FakePodPASmask = np.fliplr(np.rot90(FakePodPASmask,3))
                        TPI_F[int(pty-(highres_w/2))*4:int(pty+(highres_w/2))*4,int(ptx-(highres_w/2))*4:int(ptx+(highres_w/2))*4] = FakePodPASmask
                    except:
                        continue
                else:
                    try:
                        TPI_F[int(ptx-(highres_w/2))*4:int(ptx+(highres_w/2))*4,int(pty-(highres_w/2))*4:int(pty+(highres_w/2))*4] = FakePodPASmask
                    except:
                        continue
            else:
                nuc_mask = rescale(FakePodPASmask, 0.25, anti_aliasing=False,preserve_range=True)
                nuc_mask = cv2.threshold(nuc_mask, 0.01, 255, cv2.THRESH_BINARY)[1]
                if Imagename[0:3]=='NTN':
                    try:
                        nuc_mask = np.fliplr(np.rot90(nuc_mask,3))
                        TPI_F[int(pty-(highres_w/2)):int(pty+(highres_w/2)),int(ptx-(highres_w/2)):int(ptx+(highres_w/2))] = nuc_mask
                    except:
                        continue
                else:
                    try:
                        TPI_F[int(ptx-(highres_w/2)):int(ptx+(highres_w/2)),int(pty-(highres_w/2)):int(pty+(highres_w/2))] = nuc_mask
                    except:
                        continue
#                
            
           
      

    print('Generating pix2pix output xml...')
    '''========================================='''
    if resol == 0 and Imagename[0:3]=='NTN':        
        TP2 = cv2.threshold((TPI_F), 0.5, 255, cv2.THRESH_BINARY)[1] 
        TP2 = np.transpose(TP2)

    elif resol == 0:        
        TP2 = cv2.threshold((TPI_F), 0.5, 255, cv2.THRESH_BINARY)[1]    
    elif resol == 1 and Imagename[0:3]=='NTN':        
        TP2 = cv2.threshold((TPI_F), 0.5, 255, cv2.THRESH_BINARY)[1]  
        TP2 = np.transpose(TP2)
    elif resol == 1:
        TP2 = cv2.threshold((TPI_F), 0.5, 255, cv2.THRESH_BINARY)[1]
    
    offset={'X': 0,'Y': 0}    
    maskPoints,_ = cv2.findContours(np.array((np.uint8(TP2))), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    pointsList = []
    for j in range(np.shape(maskPoints)[0]):
        pointList = []
        for i in range(np.shape(maskPoints[j])[0]):
            point = {'X': (maskPoints[j][i][0][0]) + offset['X'], 'Y': (maskPoints[j][i][0][1]) + offset['Y']}
            pointList.append(point)
        pointsList.append(pointList)
    Annotations = ET.Element('Annotations', attrib={'MicronsPerPixel': '0.136031'})
    col1 = str(65280)
    Annotations = FNs.xml_add_annotation(Annotations=Annotations,annotationID=1,LC = col1)
    
    for i in range(np.shape(pointsList)[0]):
        pointList = pointsList[i]
        Annotations = FNs.xml_add_region(Annotations=Annotations, pointList=pointList)    
          
    

    return TP2

