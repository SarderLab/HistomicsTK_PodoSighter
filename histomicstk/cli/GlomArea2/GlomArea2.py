print("Importing libraries...")

from histomicstk.cli.utils import CLIArgumentParser
import sys
sys.path.append("..")

import warnings
with warnings.catch_warnings():
    import numpy as np
    import openslide
    from skimage.transform import resize     
    from xml.dom import minidom
    from skimage.draw import polygon
    import sys
    from skimage.measure import label,regionprops
    from skimage.transform import rescale 

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

print("Loading main...")


'''Main'''
'''++++'''

def main(args):
    print("Running main code...")
    
    
    print(args.inputImageFilePAS)
    print(args.inputAnnotationFile)  
    
    
    sourcePAS2 = openslide.OpenSlide(args.inputImageFilePAS)
    sourcePAS = openslide.open_slide(args.inputImageFilePAS)   
    PASxmlpath = args.inputAnnotationFile   
  
    
    print("Extract binary mask from glom XML...") 
    PASmask = np.array(rescale(getMaskFromXml(sourcePAS,PASxmlpath), 1, anti_aliasing=False))    

    PAS_mpp = (float(sourcePAS.properties[openslide.PROPERTY_NAME_MPP_X])+float(sourcePAS.properties[openslide.PROPERTY_NAME_MPP_Y]))/2
    tomicron = PAS_mpp*4
    
    count = 1
    for region in regionprops(label(PASmask)):
        minr, minc, maxr, maxc = region.bbox
        GlomArea = (region.area)*tomicron*tomicron
        print("Glomerulus {} has an area of {:.2f} sq. microns".format(count,GlomArea))
        count+=1        


if __name__ == "__main__":
    main(CLIArgumentParser().parse_args())
