import time
from ctypes import *
class maClass () :
    def __init__(self):
        so_libpolargraph = "/home/root/libpolargraph.so"
        self.libpolargraph = CDLL(so_libpolargraph)
        
        
        self.libpolargraph.draw_init()
        
        self.libpolargraph.draw_home()
        
        
        self.libpolargraph.pen_down()
        
        self.libpolargraph.draw_line(c_float(200),c_float(200))
        
        self.libpolargraph.draw_line(c_float(250),c_float(200))
        
        self.libpolargraph.draw_line(c_float(250),c_float(250))
        
        self.libpolargraph.draw_line(c_float(200),c_float(250))
        
        self.libpolargraph.draw_line(c_float(200),c_float(200))
        
        self.libpolargraph.pen_up()
        
        """
        self.libpolargraph.draw_line(1,3)
        time.sleep(1)
        self.libpolargraph.draw_line(10,15)
        time.sleep(1)
        self.libpolargraph.draw_line(5,2)
        time.sleep(1)
        self.libpolargraph.draw_line(20,15)
        time.sleep(1)
        self.libpolargraph.draw_line(10,10)
        time.sleep(1)
        self.libpolargraph.draw_line(15,10)
        time.sleep(1)
        self.libpolargraph.draw_home(15,10)
        self.libpolargraph.pen_up()"""
        
        self.libpolargraph.draw_close()

maClass()
