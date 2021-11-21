from ctypes import *
import os.path as osp
import subprocess as sp

class svgNanoparser :
    def __init__(self):
        print('Init')
    
    def extractCoordinates(self, imageSvg):
        filename = "nanosvg"
        file = osp.abspath(filename)
        img = osp.abspath(imageSvg)
        print(img)
        output = sp.run([file, img])

#svg = svgNanoparser()


#svg.extractCoordinates("app/libs/nano.svg")