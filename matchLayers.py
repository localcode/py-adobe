import os

from appscript import *
from mactypes import *

def matchLayers(inFilePaths, outFilePaths, fileType='.ai'):
    """Reads the graphic style of an open illustrator files, and edits a batch
    of files to match.

        Records the layer order, stroke, opacity, fill, and dash of each layer
        in the open file, and then edits in each layer in the batch of
        documents to match the settings of the open document. The open document
        must have at least the layers that exist in the batch of document.
    """

    find = app('Finder')
    il = app('Adobe Illustrator')

    # read the settings of the current document
    docName = il.current_document.name()
    doc1 = il.documents[docName]
    layers = doc1.layers()
    layerList = []
    opacityList = []
    colorList = []
    filledList = []
    strokedList = []
    strokeList = []
    fillList = []
    dashList = []
    strokeCapList = []
    strokeJoinList = []
    # loop through layers of current document
    # store a value for each layer
    for layer in layers:
        layerList.append(layer.name())
        item = layer.path_items()[0]
        opacityList.append(item.opacity())
        strokedList.append(item.stroked())
        filledList.append(item.filled())
        colorList.append(item.stroke_color())
        strokeList.append(item.stroke_width())
        fillList.append(item.fill_color())
        dashList.append(item.stroke_dashes())
        strokeCapList.append(item.stroke_cap())
        strokeJoinList.append(item.stroke_join())

    for i, inPath in enumerate(inFilePaths): # This is an appropriate place to limit the number of files

        outPath = outFilePaths[i]
        f = File(inPath)


        il.open(f)
        # switches the doc ref to the newly opened document
        doc = il.current_document()
        for j in range(len(layerList)):
            layerName = layerList[j]
            opacity = opacityList[j]
            color = colorList[j]
            stroke = strokeList[j]
            fill = fillList[j]
            dashes = dashList[j]
            stroked = strokedList[j]
            filled = filledList[j]
            caps = strokeCapList[j]
            joins = strokeJoinList[j]
            layer = doc.layers[layerName]
            try:
                layer.opacity.set(opacity)
                for item in layer.path_items():
                    item.stroked.set(stroked)
                    item.filled.set(filled)
                    if stroked:
                        item.stroke_color.set(color)
                        item.stroke_width.set(stroke)
                        item.stroke_dashes.set(dashes)
                        item.stroke_cap.set(caps)
                        item.stroke_join.set(joins)
                    if filled:
                        item.fill_color.set(fill)
                layer.move(to=doc.end)
            except:
                pass

        doc.save(in_=outPath )
        doc.close(saving=k.no)

if __name__=='__main__':

    layerstring = 'solids'
    inFolder = '/Volumes/BOOTCAMP/amigos/exports/'
    outFolder = '/Users/benjamin/projects/amigos/%s' % layerstring

    from mergeSketch01 import ids
    #ids = range(1,766)
    inFiles = ['%s%s.ai' % (i, layerstring) for i in ids]
    inFilePaths = [os.path.join(inFolder, p) for p in inFiles if layerstring in p]
    outFilePaths = [os.path.join(outFolder, p) for p in inFiles if layerstring in p]

    matchLayers( inFilePaths, outFilePaths )


