import time
from array import *
from ctypes import *
class maClass () :

            
    def goToSquare(self,x1,x2,y1,y2):
        xf=x2
        if x2 >= x1 :
            for x in range(x1,x2+1):
                self.libpolargraph.draw_line(c_float(x),c_float(y1))
        else :
            for x in range(x2,x1+1):
                self.libpolargraph.draw_line(c_float(x1-x),c_float(y1))
            xf=x1
        if y2 >= y1 :
            for y in range(y1,y2+1):
                self.libpolargraph.draw_line(c_float(xf),c_float(y))
        else :
            for y in range(y2,y1+1):
                self.libpolargraph.draw_line(c_float(xf),c_float(y1-y))
        


    def __init__(self):
        so_libpolargraph = "/home/root/libpolargraph_test.so"
        self.libpolargraph = CDLL(so_libpolargraph)    
        
        self.libpolargraph.draw_init()
        
        self.libpolargraph.draw_home()
        
        self.libpolargraph.pen_down()
        """        
        self.goTo(0,250,0,0)
        self.goTo(250,250,0,250)
        self.goTo(250,0,250,250)
        self.goTo(0,0,250,0)
        """
        self.libpolargraph.pen_up()
        
        self.goTo(0,240,0,270)
        
        self.libpolargraph.draw_close()


    def goTo(self,xa,xf,ya,yf):
        if xf >= xa :
            nbx = xf - xa
            s_x = 1.0
        else :
            nbx = xa - xf
            s_x = -1.0
        if yf >= ya :
            nby = yf - ya
            s_y = 1.0
        else :
            nby = ya - yf
            s_y = -1.0
        
        array_x = array('f',[])
        array_y = array('f',[])
        if nbx >= nby :
            pas_y = nby/nbx
            pas_x = 1.0
            iteration = nbx
        else :
            pas_x = nbx/nby
            pas_y = 1.0
            iteration = nby
        
        
        
        for i in range (iteration):
            array_x.append((xa + (pas_x * s_x)*i))
            array_y.append((ya + (pas_y * s_y)*i))
            print(array_x[i])
            print(array_y[i])
            self.libpolargraph.draw_line(c_float(array_x[i]),c_float(array_y[i]))
        
        
        
        
        


maClass()
