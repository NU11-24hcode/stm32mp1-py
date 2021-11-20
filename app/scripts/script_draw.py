import time
from ctypes import *
class maClass () :
    def __init__(self):
        so_libpolargraph = "/home/root/libpolargraph.so"
        self.libpolargraph = CDLL(so_libpolargraph)
        
        self.libpolargraph.pen_up()
        
        self.libpolargraph.draw_init()
        
        self.libpolargraph.draw_goto(c_float(15),c_float(45))
        
        self.libpolargraph.pen_down()
        
        self.libpolargraph.draw_line(c_float(465),c_float(45))
        
        self.libpolargraph.draw_line(c_float(465),c_float(495))
        
        self.libpolargraph.draw_line(c_float(15),c_float(495))
        
        self.libpolargraph.draw_line(c_float(15),c_float(45))
        
        self.libpolargraph.pen_up()
        
         self.libpolargraph.draw_goto(c_float(0),c_float(0))
        
        self.libpolargraph.draw_close()

maClass()
