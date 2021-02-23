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
from col_deconv_HPAS import col_deconv_HPAS
from scipy.ndimage.morphology import binary_opening, binary_fill_holes

def create_p2p_outxml(svsfile,xmlfile,crop_size,resdir,PAS_nuc_thre,gauss_filt_size,Disc_size):
    
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
    
    TPI_F = np.zeros(PAS[:,:,0].shape)

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
        Glommask2 = resize(Glommask_1,(highres_w*4,highres_w*4),anti_aliasing=True)*1
        Glommask2 = cv2.threshold((Glommask2), 0.1, 255, cv2.THRESH_BINARY)[1]    
    
        print("Analyzing patches...")
        '''========================================='''
        
        if crop_imgPAS.shape == (highres_w*4,highres_w*4,3):
            countPatch += 1
            filename = Imagename +'_'+str(countPatch)  
            print(filename)           
            
            fil_name = resdir+ filename           
            predicted_im = plt.imread(fil_name+'_fake_B'+'.png')
            predicted_im = resize(predicted_im[:,:,0:3], (crop_imgPAS[:,:,0:3].shape),anti_aliasing=True)
            
            '''Segment pix2pix detected podocyte nuclei'''
            '''========================================='''            
            ch1 = cv2.threshold(predicted_im[:,:,0], 0.1, 255, cv2.THRESH_BINARY)[1]
            ch4yell = cv2.threshold(predicted_im[:,:,1],0.1 , 255, cv2.THRESH_BINARY_INV)[1]
            ch1final = (cv2.bitwise_and(cv2.convertScaleAbs(ch4yell),cv2.convertScaleAbs(ch1)))
            
            ch2 = cv2.threshold(predicted_im[:,:,2], 0.1, 255, cv2.THRESH_BINARY)[1]
            ch3 = (cv2.bitwise_and(cv2.convertScaleAbs(ch2),cv2.convertScaleAbs(Glommask2)))
            predicted_mask = (cv2.bitwise_and(cv2.convertScaleAbs(ch1final),cv2.convertScaleAbs(ch3)))
            
            '''Segment PAS nuclei'''
            '''========================================='''
            hemMask = col_deconv_HPAS(crop_imgPAS[:,:,0:3])
            hemMask= (hemMask+abs(np.amin(hemMask,axis = None)))
            kernel = np.ones((gauss_filt_size,gauss_filt_size),np.float32)/25
            hemMask = cv2.filter2D(hemMask,-1,kernel)
            
            AllPAS = ((hemMask>PAS_nuc_thre)*Glommask2)        

            AllPAS = binary_opening(AllPAS, structure=np.ones((Disc_size,Disc_size))).astype(np.int) 
            AllPAS = binary_fill_holes(AllPAS).astype(int)
            AllPAS = binary_opening(AllPAS, structure=np.ones((Disc_size,Disc_size))).astype(np.int) 

            LabelPAS = label(AllPAS)
            FakePodPASmask = np.zeros(AllPAS.shape)            
            count2 = 1
            for reg in LabelPAS:
                eachIm = (LabelPAS == count2)*1
                count2+=1
                if (np.sum(eachIm*predicted_mask*1)>0):
                    FakePodPASmask = FakePodPASmask + eachIm
                  
            del predicted_im
            
            FakePodPASmask = resize(FakePodPASmask, (highres_w,highres_w),anti_aliasing=True)
#            predicted_mask = resize(predicted_mask, (highres_w,highres_w),anti_aliasing=True)
            
            TPI_F[int(ptx-(highres_w/2)):int(ptx+(highres_w/2)),int(pty-(highres_w/2)):int(pty+(highres_w/2))] = FakePodPASmask
            

       

    print('Generating pix2pix output xml...')
    '''========================================='''
    TP2 = cv2.threshold((TPI_F), 0.5, 255, cv2.THRESH_BINARY)[1]    
    TP_HR = rescale(TP2, 1, anti_aliasing=False)
    
    offset={'X': 0,'Y': 0}    
    maskPoints,_ = cv2.findContours(np.array((np.uint8(TP_HR))), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    pointsList = []
    for j in range(np.shape(maskPoints)[0]):
        pointList = []
        for i in range(np.shape(maskPoints[j])[0]):
            point = {'X': (maskPoints[j][i][0][0]*4) + offset['X'], 'Y': (maskPoints[j][i][0][1]*4) + offset['Y']}
            pointList.append(point)
        pointsList.append(pointList)
    Annotations = ET.Element('Annotations', attrib={'MicronsPerPixel': '0.136031'})
    col1 = str(65280)
    Annotations = FNs.xml_add_annotation(Annotations=Annotations,annotationID=1,LC = col1)
    
    for i in range(np.shape(pointsList)[0]):
        pointList = pointsList[i]
        Annotations = FNs.xml_add_region(Annotations=Annotations, pointList=pointList)    
      
    xml_data = ET.tostring(Annotations, pretty_print=True)
#    f = open(output_anno_file, 'wb')
#    f.write(xml_data)
#    f.close()
    return xml_data


