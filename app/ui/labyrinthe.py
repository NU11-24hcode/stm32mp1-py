import gi
import time
from ctypes import *

gi.require_version("Gtk", "3.0")
from gi.repository import Gtk, GdkPixbuf

import svgNanoparser_arm as svgparser


class MyWindow(Gtk.Window):
    def __init__(self):
        super().__init__(title="Welcome to the labyrinth!")
        self.maximize()
        
        #Creates the notebook, ie the global page with tabs
        self.notebook = Gtk.Notebook()
        self.add(self.notebook)

        #Creates one box for each tab
        self.arrow_box = Gtk.Box(spacing=6)
        self.simple_vol = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing = 20)
        self.file_picker = Gtk.Box(spacing=6)
        
        #Creates three tabs, each containing the corresponding box
        self.notebook.append_page(self.arrow_box, Gtk.Label(label="Labyrinthe"))
        self.notebook.append_page(self.simple_vol, Gtk.Label(label="Plan de vol simple"))
        self.notebook.append_page(self.file_picker, Gtk.Label(label="Padme <3"))

        
        #Populates the first tab: Controle with arrows       
        self.up_arrow = Gtk.Button(label="Up")
        self.arrow_box.pack_start(self.up_arrow, True, True, 0)
        self.up_arrow.connect("clicked", self.addCommand, 2)
        
        self.right_arrow = Gtk.Button(label="Right")
        self.arrow_box.pack_start(self.right_arrow, True, True, 0)
        self.right_arrow.connect("clicked", self.addCommand, 0)
        
        self.down_arrow = Gtk.Button(label="Down")
        self.arrow_box.pack_start(self.down_arrow, True, True, 0)
        self.down_arrow.connect("clicked", self.addCommand, 3)
        
        self.left_arrow = Gtk.Button(label="Left")
        self.arrow_box.pack_start(self.left_arrow, True, True, 0)
        self.left_arrow.connect("clicked", self.addCommand, 1)
        
        
        
        
        #Populates the second tab: Simple vol plan
        
        self.explanation_label = Gtk.Label("L'objectif de cette partie est de faire un plan de vol simple.")
        self.simple_vol.pack_start(self.explanation_label, True, True, 0)        
        
        self.x1_adjustment = Gtk.Adjustment(0, 0, 45, 1, 10, 0)
        self.x1_label = Gtk.Label("Valeur X de départ")
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
        
        self.x2_adjustment = Gtk.Adjustment.new(45, 0, 45, 1, 10, 0)
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
        
        self.file = Gtk.Button(label="Dessiner") 
        self.file.connect("clicked", self.file_picked_svg)  
        self.file_picker.pack_start(self.file, True, True, 0)
            
        
        
        
        
        self.pen_position = [2,2]
        
        
        self.casesNb = [
            [2,1,0,0,0,0,0,0,1,0],
            [0,1,1,1,1,1,0,0,1,0],
            [0,1,0,0,0,0,0,0,1,0],
            [0,1,0,0,1,0,0,0,1,0],
            [0,0,0,0,1,0,1,1,1,0],
            [0,1,0,0,1,0,0,0,1,0],
            [0,1,1,1,1,0,0,0,0,0],
            [0,1,0,0,1,1,1,1,0,0],
            [1,1,0,0,0,0,1,0,0,0],
            [0,0,0,3,0,0,0,0,0,0],
        ]

        self.starting_x_y = [0,0]
        self.current_x_y = [0,0]

        self.values=  ["Droite", "Gauche", "Haut", "Bas"]
        
        so_libpolargraph = "/home/root/libpolargraph.so"
        self.libpolargraph = CDLL(so_libpolargraph)
        self.libpolargraph.pen_up()
        self.libpolargraph.draw_init()
        numbers = [
            [0,0,40,0],
            [40,0,40,40],
            [40,40,0,40],
            [0,40,0,0],
            [6,0,6,16],
            [6,20,6,34],
            [18,12,18,30],
            [26,30,26,36],
            [34,0,34,24],
            [6,6,24,6],
            [24,18,34,18],
            [6,26,18,26],
            [18,30,32,30],
            [0,34,6,34]
        ]
        
        for line in numbers:
            self.drawSimpleLine(line[0], line[1], line[2], line[3])
            
        self.libpolargraph.pen_up()
        self.libpolargraph.draw_goto(c_float(20),c_float(20))
        self.libpolargraph.draw_close()
        
        
    def on_button_clicked(self, widget, x1_axis, y1_axis, x2_axis, y2_axis):
        widget.set_sensitive(False)
        x1 = x1_axis.get_value_as_int()
        y1 = y1_axis.get_value_as_int()
        x2 = x2_axis.get_value_as_int()
        y2 = y2_axis.get_value_as_int()
        print("The pen must go from ["+str(x1)+","+str(y1)+"] to ["+str(x2)+","+str(y2)+"].")
            
        self.libpolargraph.pen_up()
        self.libpolargraph.draw_init()
        self.libpolargraph.draw_goto(c_float(x1*10),c_float(y1*10))
        self.libpolargraph.pen_down()
        self.libpolargraph.draw_line(c_float(x2*10),c_float(y2*10))
        self.libpolargraph.pen_up()
        self.libpolargraph.draw_goto(c_float(240),c_float(270))
        
        widget.set_sensitive(True)
        

    def drawSimpleLine(self, x1, y1, x2, y2, continuous = True):
        self.libpolargraph.pen_up()
        self.libpolargraph.draw_goto(c_float(x1*10),c_float(y1*10))
        self.libpolargraph.pen_down()
        self.libpolargraph.draw_line(c_float(x2*10),c_float(y2*10))
        
        
    def addCommand(self, widget,  nb):
        tempCurrent = [self.current_x_y[0], self.current_x_y[1]]
        newposition = [self.pen_position[0], self.pen_position[1]]

        if nb == 0:
            tempCurrent[0]+=1
            newposition[0]+=4
        elif nb == 1:
            tempCurrent[0]-=1
            newposition[0]-=4
        elif nb == 2 :
            tempCurrent[1]-=1
            newposition[1]-=4
        elif nb == 3 :
            tempCurrent[1]+=1
            newposition[1]+=4

        caseValue = self.casesNb[tempCurrent[1]][tempCurrent[0]]
        
        if (caseValue==0):
            self.current_x_y = tempCurrent
            self.drawSimpleLine(self.pen_position[0], self.pen_position[1], newposition[0], newposition[1])
            self.pen_position = [newposition[0], newposition[1]]
        elif(caseValue==3):
            print("victoire!")
        else:
            print("ne peut pas aller là")
            
    def file_picked_svg(self, widget):
        so_libpolargraph = "/home/root/libpolargraph.so"
        #so_libpolargraph = "/home/atelier/Documents/24hcode/polargraph_sources/libpolargraph.so"
        self.libpolargraph = CDLL(so_libpolargraph)
        
        svg = svgparser.svgNanoparser()
        
        self.libpolargraph.draw_init()
        
        self.libpolargraph.pen_up()
        
        self.libpolargraph.draw_goto(c_float(240),c_float(270))
        
        #svg.extractCoordinates("epreuve7_boom_2.svg")
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
    

  
        


win = MyWindow()
win.set_border_width(10)
win.connect("destroy", Gtk.main_quit)
win.show_all()
Gtk.main()
