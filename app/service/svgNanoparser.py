from ctypes import *
from svgpathtools import *
import os
import os.path as osp
import subprocess as sp

class svgNanoparser :
    def __init__(self):
        print('Init')
        """filename = "app/libs/example1"
        file = osp.abspath(filename)
        self.nanosvg = CDLL(file)"""

    def convert(self, imageSvg):
        print("parsing %s\n", imageSvg)
        image = self.nanosvg.nsvgParseFromFile(c_wchar_p(imageSvg), "mm", 96.0)
        if (image == None):
            print("Could not open SVG image.\n")
      
        w = image.width
        h = image.height
    
    def exec(self, imageSvg):
        filename = "app/libs/example1"
        file = osp.abspath(filename)
        img = osp.abspath(imageSvg)
        print(img)
        output = sp.run([file, img])

svg = svgNanoparser()


svg.exec("app/libs/nano.svg")