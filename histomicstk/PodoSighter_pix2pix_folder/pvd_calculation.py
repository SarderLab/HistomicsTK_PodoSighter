# -*- coding: utf-8 -*-
"""
Created on Mon Feb 22 11:33:18 2021

@author: darsh
"""
import numpy as np
from skimage.transform import rescale,resize 
import os
from skimage.measure import label,regionprops
import matplotlib.pyplot as plt

def pvd_calculation(FakePodPASmask,Glommask2,PAS_mpp,tissue_thickness):
    
    k = 0.72
    
    pod_counts = np.max(label(FakePodPASmask))
    
    cd = []
    for region in regionprops(label(FakePodPASmask)):
        minr, minc, maxr, maxc = region.bbox
        pod_h = maxr-minr
        pod_w = maxc-minc
        pod_mean_cd = np.mean([pod_h,pod_w])
        cd.append(pod_mean_cd)
        
    apparent_cd = (np.mean(cd))*PAS_mpp
    
    true_D = (apparent_cd-tissue_thickness+np.sqrt(((apparent_cd-tissue_thickness)**2)+(4*apparent_cd*tissue_thickness*k)))/(2*k)
    
    CF = 1/(true_D/tissue_thickness+1)
    
    
    for region in regionprops(label(Glommask2)):
        GlomArea = (region.area)*PAS_mpp*PAS_mpp

    pvd = ((pod_counts*CF)/(np.max(GlomArea)*tissue_thickness))*10000
    
    return [tissue_thickness,np.max(GlomArea),pod_counts,apparent_cd,k,true_D, CF,pvd]