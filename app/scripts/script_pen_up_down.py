
from ctypes import *
import time
class maClass () :
    def __init__(self):
        so_libpolargraph = "/home/root/libpolargraph.so"
        self.libpolargraph = CDLL(so_libpolargraph)

        print(type( self.libpolargraph))
        
        self.libpolargraph.pen_up()
        self.libpolargraph.pen_down()

maClass()