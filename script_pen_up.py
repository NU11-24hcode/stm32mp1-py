from ctypes import *
import time
class penUp () :
    def __init__(self):
        so_libpolargraph = "/home/root/libpolargraph.so"
        self.libpolargraph = CDLL(so_libpolargraph)

        self.libpolargraph.pen_up()

penUp()
