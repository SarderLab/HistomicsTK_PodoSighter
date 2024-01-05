import os
import sys
from glob import glob
import girder_client
from ctk_cli import CLIArgumentParser

sys.path.append("..")
from deeplab.utils.mask_to_xml import xml_create, xml_add_annotation, xml_add_region, xml_save
from deeplab.utils.xml_to_mask import write_minmax_to_xml

def main(args2):         
    NAMES = ['gloms']

    base_dir_id = args2.inputFolder.split('/')[-2]
    file_name = args2.inputImageFile.split('/')[-1]

    gc = girder_client.GirderClient(apiUrl=args2.girderApiUrl)
    gc.setToken(args2.girderToken)
    files = list(gc.listItem(base_dir_id))
    # dict to link filename to gc id
    item_dict = dict()
    for file in files:
        d = {file['name']:file['_id']}
        item_dict.update(d)
    itemID = item_dict[file_name]

    # get files in folder
    xml_color=[65280]*(len(NAMES)+1)
    cwd = os.getcwd()
    print(cwd)
    os.chdir(cwd)

    tmp = args2.inputFolder

    ignore_label = len(NAMES)+1

    slidename = os.path.basename(args2.inputImageFile).split('.')[0]
    _ = os.system("printf '\n---\n\nFOUND: [{}]\n'".format(slidename))
    skipSlide = 0

    # get annotation
    annot = gc.get('/annotation/item/{}'.format(itemID), parameters={'sort': 'updated'})
    annot.reverse()
    annot = list(annot)
    _ = os.system("printf '\tfound [{}] annotation layers...\n'".format(len(annot)))

    # create root for xml file
    xmlAnnot = xml_create()

    # all compartments
    for class_,compart in enumerate(NAMES):

        compart = compart.replace(' ','')
        class_ +=1
        # add layer to xml
        xmlAnnot = xml_add_annotation(Annotations=xmlAnnot, xml_color=xml_color, annotationID=class_)

        # test all annotation layers in order created
        for iter,a in enumerate(annot):

            try:
                # check for annotation layer by name
                a_name = a['annotation']['name'].replace(' ','')
            except:
                a_name = None

            if a_name == compart:
                # track all layers present
                skipSlide +=1

                pointsList = []

                # load json data
                _ = os.system("printf '\tloading annotation layer: [{}]\n'".format(compart))

                a_data = a['annotation']['elements']

                for data in a_data:
                    pointList = []
                    points = data['points']
                    for point in points:
                        pt_dict = {'X': round(point[0]), 'Y': round(point[1])}
                        pointList.append(pt_dict)
                    pointsList.append(pointList)

                # write annotations to xml
                for i in range(len(pointsList)):
                    pointList = pointsList[i]
                    xmlAnnot = xml_add_region(Annotations=xmlAnnot, pointList=pointList, annotationID=class_)

                break

    if skipSlide != len(NAMES):
        _ = os.system("printf '\tThis slide is missing annotation layers\n'")
        _ = os.system("printf '\tSKIPPING SLIDE...\n'")
        del xmlAnnot

    _ = os.system("printf '\tFETCHING SLIDE...\n'")

    xml_path = '{}/{}.xml'.format(tmp, os.path.splitext(slidename)[0])
    _ = os.system("printf '\tsaving a created xml annotation file: [{}]\n'".format(xml_path))
    xml_save(Annotations=xmlAnnot, filename=xml_path)
    write_minmax_to_xml(xml_path) # to avoid trying to write to the xml from multiple workers
    del xmlAnnot
    os.system("ls -lh '{}'".format(tmp))

    # %%

        
    cmd = "python3 ../PodoSighter_cnn_folder/Complete_CNN_Prediction.py -A0 '{}' -A1 '{}' -A2 '{}' -A3 '{}' -A4 '{}' -A5 '{}' -A6 '{}' -A7 {} -A8 {} -A9 {} -A10 {} -A11 {} -A12 {} -A13 '{}' -A14 '{}' -A15 {} -A16 '{}'".format(args2.inputFolder, args2.inputImageFile, xml_path, args2.Model,args2.Modelchkpt,args2.Modelidx, args2.species, args2.PASnucleiThreshold,args2.gauss_filt_size, args2.Disc_size,args2.resolution,args2.size_thre,args2.watershed_thre,args2.tissue_thickness,args2.csvfilename,args2.girderApiUrl,args2.girderToken)

    os.system(cmd)    

if __name__ == "__main__":
    main(CLIArgumentParser().parse_args())
