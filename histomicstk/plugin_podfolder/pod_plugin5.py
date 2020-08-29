from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import sys
sys.path.append("..")

import warnings
with warnings.catch_warnings():
    warnings.filterwarnings("ignore",category=FutureWarning)
    warnings.filterwarnings("ignore",category=RuntimeWarning)
    import tensorflow as tf
    import numpy as np
    import openslide
    from skimage.transform import warp, SimilarityTransform, resize     
    import lxml.etree as ET
    from xml.dom import minidom
    from skimage.draw import polygon
    import sys
    from skimage import transform as tf2
    from skimage.morphology import remove_small_objects
    from skimage.measure import label,regionprops
    import os
    from skimage.transform import rescale 

'''+++++++++'''
print("Loading flags...")

flags = tf.app.flags

FLAGS = flags.FLAGS

flags.DEFINE_string('inputPASsvsname', '24_PAS.svs', 'PAS WSI name (24_PAS.svs)')
flags.DEFINE_string('inputIFsvsname', '24_IF.svs', 'IF WSI name (24_IF.svs)')
flags.DEFINE_string('inputPASxmlname', '24.xml', 'Glom xml file (24.xml)')
#flags.DEFINE_string('outfilename', '24_out.xml', '*.xml annotation filename (24_out.xml).')


flags.DEFINE_float('orig_IF_Thre', 0.4,
                  'Podocyte IF threshold, float type, between 0 - 1.',lower_bound=0, upper_bound=1)
#flags.DEFINE_float('Disc_size', 3,
#                  'Disc size, integer type.')
flags.DEFINE_list("TransXY", [211, -375], 'Translation parameters X and Y [211, -375]')

print("Done defining flags...")
print(FLAGS.inputPASsvsname)
inputPASsvsname1 = FLAGS.inputPASsvsname
inputIFsvsname1 = FLAGS.inputIFsvsname
inputPASxmlname1 = FLAGS.inputPASxmlname
#outfilename1 = FLAGS.outfilename

orig_IF_Thre1 = FLAGS.orig_IF_Thre
#Disc_size1 = FLAGS.Disc_size
TransXY1 = FLAGS.TransXY

print("Loading functions...")

def RegisterWSIs(IF,txfinal,tyfinal):
    
    tform_newstar = tf2.SimilarityTransform(scale=None, rotation=None, translation=(txfinal,tyfinal))
    FinalregIF = tf2.warp(IF[:,:,0:3], inverse_map=tform_newstar.inverse)

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

def main(unused_argv):
    
    print("Parse PAS input arguments...")
    print(FLAGS.inputPASsvsname)

    
    print("Parse IF input arguments...")
    print(FLAGS.inputIFsvsname)

    
    print("Parse PAS xml input arguments...")
    print(FLAGS.inputPASxmlname)
   
    
    print("Parse input arguments...")
    print(FLAGS.orig_IF_Thre)
    print(FLAGS.TransXY)

    
    inputPASsvsname = os.path.basename(FLAGS.inputPASsvsname)
    sourcePAS = openslide.open_slide(inputPASsvsname)
    
    inputIFsvsname = os.path.basename(FLAGS.inputIFsvsname)
    sourceIF = openslide.open_slide(inputIFsvsname)
    
    inputPASxmlname = os.path.basename(FLAGS.inputPASxmlname)
    PASxmlpath = inputPASxmlname
    
    
    orig_IF_Thre = FLAGS.orig_IF_Thre
    
    
    Disc_size = 9
    
    txfinal = FLAGS.TransXY[0]
    tyfinal = FLAGS.TransXY[1]
   
    
    print("Opening WSIs in mid resolution...")
    PAS = np.array(sourcePAS.read_region((0,0),1,sourcePAS.level_dimensions[1]),dtype = "uint8")
    IF = np.array(sourceIF.read_region((0,0),1,sourceIF.level_dimensions[1]),dtype = "uint8")
    
    print(" MPP + scaling... Rescaling PAS...")
    PAS_mpp = (float(sourcePAS.properties[openslide.PROPERTY_NAME_MPP_X])+float(sourcePAS.properties[openslide.PROPERTY_NAME_MPP_Y]))/2
    IF_mpp = (float(sourceIF.properties[openslide.PROPERTY_NAME_MPP_X])+float(sourceIF.properties[openslide.PROPERTY_NAME_MPP_Y]))/2
    Pas_downscale_value = PAS_mpp/IF_mpp 
    PAS_rescaled = rescale(PAS, Pas_downscale_value, anti_aliasing=False)        
    
    print("Extract binary mask from glom XML...") 
    PASmask = np.array(rescale(getMaskFromXml(sourcePAS,PASxmlpath), Pas_downscale_value, anti_aliasing=False))
    
    print("Registering...")  
    FinalregIF = RegisterWSIs(IF,txfinal,tyfinal)
    tformtest = SimilarityTransform(translation=(0,0))
    warped = warp(FinalregIF,tformtest,output_shape=PAS_rescaled[:,:,0:3].shape,preserve_range=True)
    
    print("Segmenting podocyte from IF...")  
    Podmask1 = np.uint8((warped[:,:,0]>orig_IF_Thre)*(PASmask)*1)    
    
    Podmask = np.array(remove_small_objects(label(Podmask1), min_size=Disc_size, connectivity=1, in_place=False))
    
    w = 256
    count = 1
    for region in regionprops(label(PASmask)):
        minr, minc, maxr, maxc = region.bbox
        GlomArea = (region.area)*0.52*0.52
        startr = int(int((minr+maxr)/2)-(w/2))
        stopr = int(int((minr+maxr)/2)+(w/2))
        startc = int(int((minc+maxc)/2)-(w/2))
        stopc = int(int((minc+maxc)/2)+(w/2))
#        Glommask2 = (PASmask[startr:stopr,startc:stopc])*1
        Podmask_small = (Podmask[startr:stopr,startc:stopc])*1
        Podcounts = len(regionprops(label(Podmask_small)))
        print("Glomerulus {} has an area of {:.2f} sq. microns and has {} podocytes.".format(count,GlomArea, Podcounts))
        count+=1
        


if __name__ == '__main__':
  tf.app.run()
  print('\n\nall done.')
    
