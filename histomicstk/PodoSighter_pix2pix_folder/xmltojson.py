import json
import xml.etree.ElementTree as ET

import logging
logging.basicConfig()


def xmltojson(root):

    colorList = ["rgb(0, 255, 128)", "rgb(0, 255, 255)", "rgb(255, 255, 0)", "rgb(255, 128, 0)", "rgb(0, 128, 255)",
                 "rgb(0, 0, 255)", "rgb(0, 102, 0)", "rgb(153, 0, 0)", "rgb(0, 153, 0)", "rgb(102, 0, 204)",
                 "rgb(76, 216, 23)", "rgb(102, 51, 0)", "rgb(128, 128, 128)", "rgb(0, 153, 153)", "rgb(0, 0, 0)"]

    l_size = list(root)
    if len(l_size) == 1:
        # print(len(l_size))
        data = dict()
        ann = root.find('Annotation')
        attr = ann.find('Attributes')
        name = attr.find('Attribute').get('Name')
        element = []
        reg = ann.find('Regions')
        for i in reg.findall('Region'):
            eleDict = dict()
            eleDict["closed"] = True
            eleDict["fillColor"] = "rgba(11, 156, 49, 0.8)"
            eleDict["lineColor"] = colorList[0]
            eleDict["lineWidth"] = 2
            points = []
            ver = i.find('Vertices')
            for j in ver.findall('Vertex'):
                eachPoint = []
                eachPoint.append(float(j.get('X')))
                eachPoint.append(float(j.get('Y')))
                eachPoint.append(float(j.get('Z')))
                points.append(eachPoint)
            eleDict["points"] = points
            eleDict["type"] = "polyline"
            element.append(eleDict)
        data["elements"] = element
        data["name"] = name

        return data

    elif len(l_size) > 1:
        # print(len(l_size))
        data = []
        for n, child in enumerate(root, start=0):
            dataDict = dict()
            attr = child.find('Attributes')
            name = attr.find('Attribute').get('Name')
            element = []
            reg = child.find('Regions')
            for i in reg.findall('Region'):
                eleDict = dict()
                eleDict["closed"] = True
                eleDict["fillColor"] = "rgba(11, 156, 49, 0.8)"
                eleDict["lineColor"] = colorList[n % 15]
                eleDict["lineWidth"] = 2
                points = []
                ver = i.find('Vertices')
                for j in ver.findall('Vertex'):
                    eachPoint = []
                    eachPoint.append(float(j.get('X')))
                    eachPoint.append(float(j.get('Y')))
                    eachPoint.append(float(j.get('Z')))
                    points.append(eachPoint)
                eleDict["points"] = points
                eleDict["type"] = "polyline"
                element.append(eleDict)
            dataDict["elements"] = element
            dataDict["name"] = name
            data.append(dataDict)

        return data

    else:
        raise ValueError('Check the format of json file')



