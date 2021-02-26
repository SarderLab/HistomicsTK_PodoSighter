# -*- coding: utf-8 -*-
"""
Created on Tue Feb 23 15:51:14 2021

@author: darsh
"""
import numpy as np
from skimage.color import separate_stains,hpx_from_rgb
from skimage.exposure import rescale_intensity
from skimage.morphology import remove_small_objects
from skimage.segmentation import watershed
from scipy import ndimage as ndi
from skimage.feature import peak_local_max
from skimage.measure import label
import cv2
from skimage import morphology

def getPASnuclei(im_PAS,Glommask,int_thre,size_thre,gauss_filt_size,watershed_dist_thre,disc_size):
    PASnuc = separate_stains(im_PAS, hpx_from_rgb)
    PASnuc_extract = rescale_intensity(PASnuc[:, :, 0], out_range=(0,1))
    
    kernel = np.ones((gauss_filt_size,gauss_filt_size),np.float32)/25
    PASnuc_extract = cv2.filter2D(PASnuc_extract,-1,kernel)
    
    PAS_nuclei = ((PASnuc_extract>int_thre)*1)
    PAS_nuc_label = label(PAS_nuclei)
    PAS_nuclei = morphology.opening(PAS_nuc_label, morphology.disk(disc_size))
    
    PAS_nuclei = remove_small_objects(label(PAS_nuclei), min_size=size_thre/3)

    label_nuc = label(PAS_nuclei)
    PAS_nuclei2 = remove_small_objects(label_nuc, min_size=size_thre)
   
    try:
        distance = ndi.distance_transform_edt(PAS_nuclei2)
        coords = peak_local_max(distance,min_distance=watershed_dist_thre, exclude_border=False, footprint=np.ones((2, 2)), labels=PAS_nuclei2)

        mask = np.zeros(distance.shape, dtype=bool)
        mask[tuple(coords.T)] = True
        markers, _ = ndi.label(mask)
        labels = watershed(-distance, markers, mask=PAS_nuclei,watershed_line=True)
        labels = remove_small_objects(labels, min_size=size_thre/5)#REst = 3, NTN = 5   

        singlenuc = ((PAS_nuclei>0)*1 - (PAS_nuclei2>0)*1)
        doublesepnuc = (labels>0)*1

        separatednucPAS = ((singlenuc + doublesepnuc)*Glommask)>0*1
    except:
        print('watershed fix')
        separatednucPAS = (PAS_nuclei*Glommask)>0*1
        
    
    err_nuclei = remove_small_objects(label(separatednucPAS), min_size=size_thre*6)
    final_out = (separatednucPAS>0)*1-(err_nuclei>0)*1
    return final_out

    
