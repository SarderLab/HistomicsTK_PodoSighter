from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import sys
sys.path.append("..")

import numpy as np
import openslide
from skimage.transform import resize     
from xml.dom import minidom
from skimage.draw import polygon
import sys
from skimage.measure import label,regionprops
from skimage.transform import rescale 
import argparse
import lxml.etree as ET
import csv

'''+++++++++'''

parser = argparse.ArgumentParser(description = 'Glom areas from PAS')
parser.add_argument('-P','--inputpas',type = str, metavar = '',required = True,help = 'PAS image name')
parser.add_argument('-L','--pasxml',type = str, metavar = '',required = True,help = 'PAS glom xml name')
parser.add_argument('-C','--csvfilename',type = str, metavar = '', required = True, help = 'CSV file name')
parser.add_argument('-M','--xmloutname',type = str, metavar = '',required = True,help = 'XML output name')
args = parser.parse_args()
    
print("Loading functions...")

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
    mask = resize(mask,(source.level_dimensions[1][1],source.level_dimensions[1][0]), anti_aliasing=True)
    mask = mask/255
    return mask>0

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

print("Loading main...")


'''Main'''
'''++++'''

def Main():
    print("Running main code...")
    
    
    print(args.inputpas)
    print(args.pasxml)  
    
    

    sourcePAS = openslide.open_slide(args.inputpas)    

    PASxmlpath = args.pasxml   
  
    
    print("Extract binary mask from glom XML...") 
    PASmask = np.array(getMaskFromXml(sourcePAS,PASxmlpath))
   

    PAS_mpp = (float(sourcePAS.properties[openslide.PROPERTY_NAME_MPP_X])+float(sourcePAS.properties[openslide.PROPERTY_NAME_MPP_Y]))/2
    
    
    dimxscale = sourcePAS.level_dimensions[0][0]/np.shape(PASmask)[1]
    dimyscale = (sourcePAS.level_dimensions[0][1]/np.shape(PASmask)[0])
    finalscale = int((dimxscale+dimyscale)/2)
    
    tomicron = PAS_mpp*finalscale
    
    print("Scales...") 
    print(finalscale)

    count = 1
    ID_stack = []
    for region in regionprops(label(PASmask)):
        minr, minc, maxr, maxc = region.bbox
        GlomArea = (region.area)*tomicron*tomicron
        print("Glomerulus {} has an area of {:.2f} sq. microns".format(count,GlomArea))
        vals = [count,GlomArea]
        ID_stack.append(vals)
        count+=1        
        
    myFile = open(args.csvfilename, 'w')  
    with myFile:
        writer = csv.writer(myFile)
        writer.writerow(["Count", "Glomarea"])
        writer.writerows(ID_stack)

    '''Write xml'''
    '''========='''   
    
    offset={'X': 0,'Y': 0}    
    
    import cv2        
    maskPoints,_ = cv2.findContours(np.array((np.uint8(PASmask))), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    pointsList = []
    for j in range(np.shape(maskPoints)[0]):
        pointList = []
        for i in range(np.shape(maskPoints[j])[0]):
            point = {'X': (maskPoints[j][i][0][0]*finalscale) + offset['X'], 'Y': (maskPoints[j][i][0][1]*finalscale) + offset['Y']}
            pointList.append(point)
        pointsList.append(pointList)
    Annotations1 = ET.Element('Annotations', attrib={'MicronsPerPixel': '0.136031'})
    col1 = str(65280)
    Annotations1 = xml_add_annotation(Annotations=Annotations1,annotationID=1,LC = col1)
    
    for i in range(np.shape(pointsList)[0]):
        pointList = pointsList[i]
        Annotations1 = xml_add_region(Annotations=Annotations1, pointList=pointList)    
      
    xml_data = ET.tostring(Annotations1, pretty_print=True)
    f = open(args.xmloutname, 'wb')
    f.write(xml_data)
    f.close()


if __name__ == '__main__':
  Main()
  print('\n\nall done.')