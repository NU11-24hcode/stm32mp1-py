
from ctypes import *
class penDown () :
    def __init__(self):
        so_libpolargraph = "/home/root/libpolargraph.so"
        self.libpolargraph = CDLL(so_libpolargraph)

        self.libpolargraph.draw_close()

penDown()
