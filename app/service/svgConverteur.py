from ctypes import *
from svgpathtools import *

class svgConverteur :
    def __init__(self):
        file = ('C:/Users/vallee/Desktop/stm32mp1-py/app/libs/libnanosvg_win.so')
        self.nanosvg = CDLL(file)

    def convert(self, imageSvg):
        print("parsing %s\n", imageSvg)
	    image = self.nanosvg.nsvgParseFromFile(imageSvg, "mm", 96.0)
	    if (image == none) :
		    print("Could not open SVG image.\n")
      
	    w = image.width
	    h = image.height

svg = svgConverteur()

svg.convert("app/ressources/carresvg.svg")
