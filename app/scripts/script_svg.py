
from ctypes import *

import svgNanoparser_arm as svgparser

class svgDrawer () :
    def __init__(self):
        so_libpolargraph = "/home/root/libpolargraph.so"
        #so_libpolargraph = "/home/atelier/Documents/24hcode/polargraph_sources/libpolargraph.so"
        self.libpolargraph = CDLL(so_libpolargraph)
        
        svg = svgparser.svgNanoparser()
        
        self.libpolargraph.draw_init()
        
        self.libpolargraph.pen_up()
        
        self.libpolargraph.draw_goto(c_float(240),c_float(270))
        
        #svg.extractCoordinates("../ressources/epreuve7_boom_2.svg")
        svg.extractCoordinates("nano.svg")
        
        file = open("coordinates.txt", "r")
        
        Lines = file.readlines()
        
        coords = []
        drawing = False
        
        for line in Lines:
            if('NEXT' in line):
                print('Lever')
                drawing = False
                self.libpolargraph.pen_up()
            else:
                print("Dessine")
                coords = line.split(",")
                coords[0] = float(coords[0])
                coords[1] = float(coords[1])
                print('(%.2f, %.2f)', coords[0], coords[1])
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
        
        input('Test')

svgDrawer()