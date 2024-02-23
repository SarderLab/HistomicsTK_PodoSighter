import numpy as np
import os
from tiffslide import TiffSlide
import pandas as pd
import cv2
from skimage.measure import label,regionprops
from skimage.measure import label,regionprops
from getMaskFromXml import getMaskFromXml
import matplotlib.pyplot as plt




file = 'C:/ops/performance_metrics_podosighter/JPH13/JPH13.svs'
sourcePAS = TiffSlide(file) #PAS image
filename = os.path.basename(file).split('.')[0]
mask_podosighter = getMaskFromXml(sourcePAS,'C:/ops/performance_metrics_podosighter/JPH13/podosighter.xml')  #Podosighter predictions
mask_glom = getMaskFromXml(sourcePAS,'C:/ops/performance_metrics_podosighter/JPH13/gloms.xml')   #Glom masks from PAS

mask_podocount = getMaskFromXml(sourcePAS,'C:/ops/performance_metrics_podosighter/JPH13/podocount.xml')  #Ground truth podocount predictions

nuclei = getMaskFromXml(sourcePAS,'C:/ops/performance_metrics_podosighter/JPH13/nuclei.xml') #all nuclei you can get them by running nucleidetection plugin under sarderlab/histomicstk



all_regions_podosighter= []
all_gloms = []
all_nuclei= []
all_regions_podocount = []
for reg in regionprops(label(mask_glom)): 
    minr, minc, maxr, maxc = reg.bbox
    ptx = (minr+maxr)/2
    pty = (minc+maxc)/2
    highres_w = 800

    rs_podosighter = mask_podosighter[int(ptx-(highres_w/2)):int(ptx+(highres_w/2)),int(pty-(highres_w/2)):int(pty+(highres_w/2))] 
    all_regions_podosighter.append(mask_glom[int(ptx-(highres_w/2)):int(ptx+(highres_w/2)),int(pty-(highres_w/2)):int(pty+(highres_w/2))]*rs_podosighter)

    rs_podocount = mask_podocount[int(ptx-(highres_w/2)):int(ptx+(highres_w/2)),int(pty-(highres_w/2)):int(pty+(highres_w/2))] 
    all_regions_podocount.append(mask_glom[int(ptx-(highres_w/2)):int(ptx+(highres_w/2)),int(pty-(highres_w/2)):int(pty+(highres_w/2))]*rs_podocount)

    rs_nuclei = nuclei[int(ptx-(highres_w/2)):int(ptx+(highres_w/2)),int(pty-(highres_w/2)):int(pty+(highres_w/2))] 
    all_nuclei.append(mask_glom[int(ptx-(highres_w/2)):int(ptx+(highres_w/2)),int(pty-(highres_w/2)):int(pty+(highres_w/2))]*rs_nuclei)

    all_gloms.append(mask_glom[int(ptx-(highres_w/2)):int(ptx+(highres_w/2)),int(pty-(highres_w/2)):int(pty+(highres_w/2))])

num_gloms = len(all_gloms)

fig, axs = plt.subplots(num_gloms, 2, figsize=(12, num_gloms*6))

for i in range(num_gloms):
    axs[i, 0].imshow(all_gloms[i], cmap='gray')
    axs[i, 0].imshow(all_regions_podosighter[i], cmap='Oranges', alpha=0.5)
    axs[i, 0].imshow(all_regions_podocount[i], cmap='plasma', alpha=0.4)
    axs[i, 0].set_title('Podosighter and Podocount Masks')
    axs[i, 0].axis('off')

    axs[i, 1].imshow(all_gloms[i], cmap='gray')
    axs[i, 1].imshow(all_regions_podosighter[i], cmap='Oranges', alpha=0.5)
    axs[i, 1].imshow(all_nuclei[i], cmap='viridis', alpha=0.4)
    axs[i, 1].imshow(all_regions_podocount[i], cmap='Blues', alpha=0.4)
    axs[i, 1].set_title('Podosighter, Podocount & Nuclei')
    axs[i, 1].axis('off')

plt.tight_layout()
plt.savefig(f'{filename}.png')
plt.show()

all_tp=[]
all_fp=[]
all_fn=[]
all_tn=[]
all_sensitivity=[]
all_specifity=[]
all_gloms=[]
glom_coord=[]

for k in range(len(regionprops(label(mask_glom)))):
    print("len(nuclei)",len(regionprops(label(all_nuclei[k]))))
    print("len(podosighter)",len(regionprops(label(all_regions_podosighter[k]))))
    print("len(podocount)",len(regionprops(label(all_regions_podocount[k]))))

    base = np.array(np.logical_or(all_nuclei[k],all_regions_podocount[k])*255, dtype='uint8')
    ret, thresh = cv2.threshold(base, 128, 255, 0)
    contours,_ = cv2.findContours(thresh,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_NONE)
    fp = 0
    tp = 0
    fn = 0
    tn = 0
    for i in range(len(contours)):
        cnt = contours[i]
        tmp = np.zeros_like(base)
        tmp = cv2.cvtColor(tmp, cv2.COLOR_GRAY2BGR)
        ret, thresh = cv2.threshold(base, 128, 255, 0)
        contours, _ = cv2.findContours(thresh,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_NONE)
        cv2.drawContours(tmp, [cnt], -1, (255,255,255), thickness=cv2.FILLED)
        tmp = cv2.cvtColor(np.array(tmp/255, dtype='uint8'), cv2.COLOR_BGR2GRAY)
        check_pod_pred = tmp*(all_regions_podosighter[k]*1)
        check_pod = tmp*(all_regions_podocount[k]*1)
        pod = np.sum(check_pod[:])>15
        pod_pred = np.sum(check_pod_pred[:])>15

        if pod & pod_pred:
            tp+=1
        elif pod:
            fn+=1
        elif pod_pred:
            fp+=1
        else:
            tn+=1
    all_tp.append(tp)
    all_fp.append(fp)
    all_fn.append(fn)
    all_tn.append(tn)
    all_sensitivity.append(round(tp/(tp+fn+0.01),2))
    all_specifity.append(round(tn/(tn+fp+0.01),2))
    all_gloms.append('glom_'+str(k))
    glom_coord.append(regionprops(label(mask_glom))[k].bbox)



dataframe = pd.DataFrame()
dataframe[f'{filename} gloms'] = all_gloms
dataframe['true_positives']=all_tp
dataframe['false_positives']=all_fp
dataframe['false_negatives']=all_fn
dataframe['true_negatives']=all_tn
dataframe['sensitivity']=all_sensitivity
dataframe['specifity']=all_specifity
dataframe['glom_bbox'] = glom_coord

dataframe.to_csv('C:/ops/performance_metrics_podosighter/performance.csv', index=False, mode='a')

