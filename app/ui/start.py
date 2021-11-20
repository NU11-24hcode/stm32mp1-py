import gi
import time
from ctypes import *

gi.require_version("Gtk", "3.0")
from gi.repository import Gtk, GdkPixbuf


class MyWindow(Gtk.Window):
    def __init__(self):
        super().__init__(title="May the force be with you")
        self.maximize()
        
        #Creates the notebook, ie the global page with tabs
        self.notebook = Gtk.Notebook()
        self.add(self.notebook)

        #Creates one box for each tab
        self.arrow_box = Gtk.Box(spacing=6)
        self.simple_vol = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing = 20)
        self.file_picker = Gtk.Box(spacing=6)
        
        #Creates three tabs, each containing the corresponding box
        self.notebook.append_page(self.arrow_box, Gtk.Label(label="Contrôle"))
        self.notebook.append_page(self.simple_vol, Gtk.Label(label="Plan de vol simple"))
        self.notebook.append_page(self.file_picker, Gtk.Label(label="Plan de vol complexe"))
        
        
        #Populates the first tab: Controle with arrows
               
        self.up_arrow = Gtk.Button(label="Up")
        self.arrow_box.pack_start(self.up_arrow, True, True, 0)
        
        self.right_arrow = Gtk.Button(label="Right")
        self.arrow_box.pack_start(self.right_arrow, True, True, 0)
        
        self.down_arrow = Gtk.Button(label="Down")
        self.arrow_box.pack_start(self.down_arrow, True, True, 0)
        
        self.left_arrow = Gtk.Button(label="Left")
        self.arrow_box.pack_start(self.left_arrow, True, True, 0)
        
        
        
        #Populates the second tab: Simple vol plan
        
        self.explanation_label = Gtk.Label.new("L'objectif de cette partie est de faire un plan de vol simple.")
        self.simple_vol.pack_start(self.explanation_label, True, True, 0)        
        
        self.x1_adjustment = Gtk.Adjustment.new(0, 0, 48, 1, 10, 0)
        self.x1_label = Gtk.Label.new("Valeur X de départ")
        self.x1_axis = Gtk.SpinButton()
        self.x1_axis.set_adjustment(self.x1_adjustment)
        self.x1_box = Gtk.Box(spacing = 6)
        self.x1_box.pack_start(self.x1_label, True, True, 0)
        self.x1_box.pack_start(self.x1_axis, True, True, 0)
        self.simple_vol.pack_start(self.x1_box, True, True, 0)   
        
        self.y1_adjustment = Gtk.Adjustment.new(0, 0, 54, 1, 10, 0)
        self.y1_label = Gtk.Label.new("Valeur Y de départ")
        self.y1_axis = Gtk.SpinButton()
        self.y1_axis.set_adjustment(self.y1_adjustment)
        self.y1_box = Gtk.Box(spacing = 6)
        self.y1_box.pack_start(self.y1_label, True, True, 0)
        self.y1_box.pack_start(self.y1_axis, True, True, 0)
        self.simple_vol.pack_start(self.y1_box, True, True, 0)   
        
        self.x2_adjustment = Gtk.Adjustment.new(48, 0, 48, 1, 10, 0)
        self.x2_label = Gtk.Label.new("Valeur X d'arrivée")
        self.x2_axis = Gtk.SpinButton()
        self.x2_axis.set_adjustment(self.x2_adjustment)
        self.x2_box = Gtk.Box(spacing = 6)
        self.x2_box.pack_start(self.x2_label, True, True, 0)
        self.x2_box.pack_start(self.x2_axis, True, True, 0)
        self.simple_vol.pack_start(self.x2_box, True, True, 0)   
        
        self.y2_adjustment = Gtk.Adjustment.new(54, 0, 54, 1, 10, 0)
        self.y2_label = Gtk.Label.new("Valeur Y d'arrivée")
        self.y2_axis = Gtk.SpinButton()
        self.y2_axis.set_adjustment(self.y2_adjustment)
        self.y2_box = Gtk.Box(spacing = 6)
        self.y2_box.pack_start(self.y2_label, True, True, 0)
        self.y2_box.pack_start(self.y2_axis, True, True, 0)
        self.simple_vol.pack_start(self.y2_box, True, True, 0)
        
        self.validate_button = Gtk.Button(label="Valider") 
        self.validate_button.connect("clicked", self.on_button_clicked, self.x1_axis,self.y1_axis,self.x2_axis,self.y2_axis)  
        self.simple_vol.pack_start(self.validate_button, True, True, 0)
        
       
        #Populates the third tab: Complex vol plan
        
        self.image = GdkPixbuf.Pixbuf.new_from_file('padme.jpg')
        self.image_renderer = Gtk.Image.new_from_pixbuf(self.image)
        self.image2 = GdkPixbuf.Pixbuf.new_from_file('tagada.jpg')
        self.image_renderer2 = Gtk.Image.new_from_pixbuf(self.image2)

        self.file_picker.pack_start(self.image_renderer, True, True, 0)
        #self.file_picker.pack_start(self.image_renderer2, True, True, 0)
        
        
        

    def on_button_clicked(self, widget, x1_axis, y1_axis, x2_axis, y2_axis):
        widget.set_sensitive(False)
        x1 = x1_axis.get_value_as_int()
        y1 = y1_axis.get_value_as_int()
        x2 = x2_axis.get_value_as_int()
        y2 = y2_axis.get_value_as_int()
        print("The pen must go from ["+str(x1)+","+str(y1)+"] to ["+str(x2)+","+str(y2)+"].")
            
        so_libpolargraph = "/home/root/libpolargraph.so"
        self.libpolargraph = CDLL(so_libpolargraph)
        self.libpolargraph.pen_up()
        self.libpolargraph.draw_init()
        self.libpolargraph.draw_goto(c_float(x1*10),c_float(y1*10))
        self.libpolargraph.pen_down()
        self.libpolargraph.draw_line(c_float(x2*10),c_float(y2*10))
        self.libpolargraph.pen_up()
        self.libpolargraph.draw_goto(c_float(240),c_float(270))
        self.libpolargraph.draw_close()
        
        widget.set_sensitive(True)
        


win = MyWindow()
win.set_border_width(10)
win.connect("destroy", Gtk.main_quit)
win.show_all()
Gtk.main()
