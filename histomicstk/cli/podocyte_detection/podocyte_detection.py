"""
Created on Tue Aug 18 15:27:29 2020

@author: d8@buffalo.edu
"""
import numpy as np
import openslide
from skimage.transform import rescale 
import cv2
from skimage.transform import warp, SimilarityTransform
import lxml.etree as ET
from xml.dom import minidom
from skimage import transform as tf
from skimage.draw import polygon

from histomicstk.cli.utils import CLIArgumentParser
#from histomicstk.cli import utils
#import os

#'''Inputs'''
#'''++++++'''
#
#orig_IF_Thre = 0.4
#Disc_size = 3
#txfinal,tyfinal = 211, -375
#
#inputPASsvsname = '24_PAS.svs' 
#inputIFsvsname = '24_IF.svs'
#inputPASxmlname = '24_PAS.xml'
#
#outfilename = '24_pod.xml'
#
#
#'''Functions'''
#'''+++++++++'''


def RegisterWSIs(IF,txfinal,tyfinal):
    
    tform_newstar = tf.SimilarityTransform(scale=None, rotation=None, translation=(txfinal,tyfinal))
    FinalregIF = tf.warp(IF[:,:,0:3], inverse_map=tform_newstar.inverse)

    return (FinalregIF)

def getMaskFromXml(source,xmlpath):
    [l,m] = source.level_dimensions[0]
    xml = minidom.parse(xmlpath)
    mask = np.zeros((m,l),'uint8');
    regions_ = xml.getElementsByTagName("Region")
    regions, region_labels = [], []
    for region in regions_:
        vertices = region.getElementsByTagName("Vertex")
        attribute = region.getElementsByTagName("Attribute")
        if len(attribute) > 0:
            r_label = attribute[0].attributes['Value'].value
        else:
            r_label = region.getAttribute('Text')
        region_labels.append(r_label)
        coords = np.zeros((len(vertices), 2))
        for i, vertex in enumerate(vertices):
            coords[i][0] = vertex.attributes['X'].value
            coords[i][1] = vertex.attributes['Y'].value
        regions.append(coords)
        [rr,cc] = polygon(np.array([i[1] for i in coords]),np.array([i[0] for i in coords]),mask.shape)
        mask[rr,cc] = 255
    print(source.level_dimensions[1])
    mask = cv2.resize(mask, dsize=source.level_dimensions[1], interpolation=cv2.INTER_CUBIC)
    mask = mask/255
    return mask#>0.5

def xml_add_annotation(Annotations, annotationID=None,LC = None): # add new annotation
    if annotationID == None: # not specified
        annotationID = len(Annotations.findall('Annotation')) + 1
    Annotation = ET.SubElement(Annotations, 'Annotation', attrib={'Type': '4', 'Visible': '1', 'ReadOnly': '0', 'Incremental': '0', 'LineColorReadOnly': '0', 'LineColor': str(LC), 'Id': str(annotationID), 'NameReadOnly': '0'})
    Regions = ET.SubElement(Annotation, 'Regions')
    return Annotations

def xml_add_region(Annotations, pointList, annotationID=-1, regionID=None): # add new region to annotation
    Annotation = Annotations[annotationID]
    Regions = Annotation.find('Regions')
    if regionID == None: # not specified
        regionID = len(Regions.findall('Region')) + 1
    Region = ET.SubElement(Regions, 'Region', attrib={'NegativeROA': '0', 'ImageFocus': '-1', 'DisplayId': '1', 'InputRegionId': '0', 'Analyze': '0', 'Type': '0', 'Id': str(regionID)})
    Vertices = ET.SubElement(Region, 'Vertices')
    for point in pointList: # add new Vertex
        ET.SubElement(Vertices, 'Vertex', attrib={'X': str(point['X']), 'Y': str(point['Y']), 'Z': '0'})
    ET.SubElement(Vertices, 'Vertex', attrib={'X': str(pointList[0]['X']), 'Y': str(pointList[0]['Y']), 'Z': '0'})
    return Annotations




'''Main'''
'''++++'''

def main(args):

    print("Parse arguments...")
#    inputPASsvsname = os.path.basename(args.inputImageFilePAS)
    inputPASsvsname = args.inputImageFilePAS
    sourcePAS = openslide.open_slide(inputPASsvsname)
    
#    inputIFsvsname = os.path.basename(args.inputImageFileIF)
    inputIFsvsname = args.inputImageFileIF
    sourceIF = openslide.open_slide(inputIFsvsname)
    
#    inputPASxmlname = os.path.basename(args.inputAnnotationFile)
    inputPASxmlname = args.inputAnnotationFile
    PASxmlpath = inputPASxmlname
    
    outfilename = args.outputAnnotationFile
    
    orig_IF_Thre = args.Podocyte_threshold
    Disc_size = args.DiscSize
#    txfinal,tyfinal = args.TranslationXY
    txfinal = args.TranslationXY[0]
    tyfinal = args.TranslationXY[1]
    
    print("Opening WSIs in mid resolution...")
    PAS = np.array(sourcePAS.read_region((0,0),1,sourcePAS.level_dimensions[1]),dtype = "uint8")
    IF = np.array(sourceIF.read_region((0,0),1,sourceIF.level_dimensions[1]),dtype = "uint8")
    
    print(" MPP + scaling... Rescaling PAS...")
    PAS_mpp = (float(sourcePAS.properties[openslide.PROPERTY_NAME_MPP_X])+float(sourcePAS.properties[openslide.PROPERTY_NAME_MPP_Y]))/2
    IF_mpp = (float(sourceIF.properties[openslide.PROPERTY_NAME_MPP_X])+float(sourceIF.properties[openslide.PROPERTY_NAME_MPP_Y]))/2
    Pas_downscale_value = PAS_mpp/IF_mpp 
    PAS_rescaled = rescale(PAS, Pas_downscale_value, anti_aliasing=False)        
    
    print("Extract binary mask from glom XML...") 
    PASmask = rescale(getMaskFromXml(sourcePAS,PASxmlpath), Pas_downscale_value, anti_aliasing=False)
         
    
    print("Registering...")  
    FinalregIF = RegisterWSIs(IF,txfinal,tyfinal)
    tformtest = SimilarityTransform(translation=(0,0))
    warped = warp(FinalregIF,tformtest,output_shape=PAS_rescaled[:,:,0:3].shape,preserve_range=True)
    
    print("Segmenting podocyte from IF...")  
    Podmask1 = np.uint8((warped[:,:,0]>orig_IF_Thre)*(PASmask)*1)    
    kernel_b = np.ones((Disc_size,Disc_size),np.uint8)
    Podmask = cv2.morphologyEx(Podmask1, cv2.MORPH_OPEN, kernel_b)   
    TP2 = cv2.threshold((Podmask), 0.5, 255, cv2.THRESH_BINARY)[1]
    
    TP_HR = rescale(TP2, (1/Pas_downscale_value), anti_aliasing=False)
    
    print("Converting podocyte mask to xml")
    offset={'X': 0,'Y': 0}            
    maskPoints,_ = cv2.findContours(np.array((np.uint8(TP_HR))), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    pointsList = []
    for j in range(np.shape(maskPoints)[0]):
        pointList = []
        for i in range(np.shape(maskPoints[j])[0]):
            point = {'X': (maskPoints[j][i][0][0]*4) + offset['X'], 'Y': (maskPoints[j][i][0][1]*4) + offset['Y']}
            pointList.append(point)
        pointsList.append(pointList)
    Annotations1 = ET.Element('Annotations', attrib={'MicronsPerPixel': '0.136031'})
    col1 = str(65280)
    Annotations1 = xml_add_annotation(Annotations=Annotations1,annotationID=1,LC = col1)
    
    for i in range(np.shape(pointsList)[0]):
        pointList = pointsList[i]
        Annotations1 = xml_add_region(Annotations=Annotations1, pointList=pointList)    
      
    xml_data = ET.tostring(Annotations1, pretty_print=True)
    f = open(outfilename, 'wb')
    f.write(xml_data)
    f.close()



if __name__ == "__main__":
    main(CLIArgumentParser().parse_args())
