
from ctypes import *

import svgNanoparser_arm as svgparser

class svgDrawer () :
    def __init__(self):
        so_libpolargraph = "/home/root/libpolargraph.so"
        self.libpolargraph = CDLL(so_libpolargraph)
        
        svg = svgparser.svgNanoparser()
        
        self.libpolargraph.pen_up()
        
        self.libpolargraph.draw_init()
        
        self.libpolargraph.draw_goto(c_float(240),c_float(270))
        
        svg.extractCoordinates("nano.svg")
        
        file = open("coordinates.txt", "r")
        
        Lines = file.readlines()
        Lines.pop(0)
        
        coords = []
        drawing = False
        
        for line in Lines:
            if('NEXT' in line):
                print('Lever')
                drawing = False
                self.libpolargraph.pen_up()
            else:
                print(float(line))
                coords.append(float(line))
                if(len(coords) == 2):
                    print("Coords ready")
                    if(drawing == False):
                        self.libpolargraph.draw_goto(c_float(coords[0]),c_float(coords[1]))
                        drawing = True
                        self.libpolargraph.pen_down()
                    else:
                        self.libpolargraph.draw_line(c_float(coords[0]),c_float(coords[1]))
                    coords.clear()
        
        self.libpolargraph.pen_up()
        
        self.libpolargraph.draw_goto(c_float(240),c_float(270))
        
        self.libpolargraph.draw_close()

svgDrawer()