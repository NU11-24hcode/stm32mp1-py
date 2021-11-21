from ctypes import *
from svgpathtools import *
import os.path as osp
import subprocess as sp

class svgNanoparser :
    def __init__(self):
        print('Init')
    
    def extractCoordinates(self, imageSvg):
        filename = "nanosvg_arm"
        file = osp.abspath(filename)
        img = osp.abspath(imageSvg)
        print(img)
        output = sp.run([file, img])

svg = svgNanoparser()


svg.extractCoordinates("nano.svg")