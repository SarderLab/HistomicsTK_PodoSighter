import cv2
import numpy as np
import lxml.etree as ET

def get_contour_points(mask, offset={'X': 0,'Y': 0}):
    # returns a dict pointList with point 'X' and 'Y' values
    # input greyscale binary image
    maskPoints, contours = cv2.findContours(np.array(mask), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    pointsList = []
    for j in range(np.shape(maskPoints)[0]):
        pointList = []
        for i in range(np.shape(maskPoints[j])[0]):
            point = {'X': maskPoints[j][i][0][0] + offset['X'], 'Y': maskPoints[j][i][0][1] + offset['Y']}
            pointList.append(point)
        pointsList.append(pointList)
    return pointsList

### functions for building an xml tree of annotations ###
def xml_create(): # create new xml tree
    # create new xml Tree - Annotations
    Annotations = ET.Element('Annotations', attrib={'MicronsPerPixel': '0.136000'})
    return Annotations

def xml_add_annotation(Annotations, annotationID=None,LC = None): # add new annotation
    # add new Annotation to Annotations
    # defualts to new annotationID
    if annotationID == None: # not specified
        annotationID = len(Annotations.findall('Annotation')) + 1
#    print(annotationID)
    Annotation = ET.SubElement(Annotations, 'Annotation', attrib={'Type': '4', 'Name': 'Pods','Visible': '1', 'ReadOnly': '0', 'Incremental': '0', 'LineColorReadOnly': '0', 'LineColor': str(LC), 'Id': str(annotationID), 'NameReadOnly': '0'})
    Attributes = ET.SubElement(Annotation, 'Attributes')
    Attribute = ET.SubElement(Attributes, 'Attribute', attrib={'Id': '0', 'Name': 'Pod', 'Value': ''})
    Regions = ET.SubElement(Annotation, 'Regions')
    return Annotations

def xml_add_region(Annotations, pointList, annotationID=-1, regionID=None): # add new region to annotation
    # add new Region to Annotation
    # defualts to last annotationID and new regionID
    Annotation = Annotations[annotationID]
    Regions = Annotation.find('Regions')
    if regionID == None: # not specified
        regionID = len(Regions.findall('Region')) + 1
#    print(regionID)
    Region = ET.SubElement(Regions, 'Region', attrib={'NegativeROA': '0', 'ImageFocus': '-1', 'DisplayId': '1', 'InputRegionId': '0', 'Analyze': '0', 'Type': '0', 'Id': str(regionID)})
    Vertices = ET.SubElement(Region, 'Vertices')
    for point in pointList: # add new Vertex
        ET.SubElement(Vertices, 'Vertex', attrib={'X': str(point['X']), 'Y': str(point['Y']), 'Z': '0'})
    # add connecting point
    ET.SubElement(Vertices, 'Vertex', attrib={'X': str(pointList[0]['X']), 'Y': str(pointList[0]['Y']), 'Z': '0'})
    return Annotations

def xml_save(Annotations, filename):
    xml_data = ET.tostring(Annotations, pretty_print=True)
    #xml_data = Annotations.toprettyxml()
    f = open(filename, 'w')
    f.write(xml_data)
    f.close()
    
