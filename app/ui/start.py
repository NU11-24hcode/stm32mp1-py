import gi

gi.require_version("Gtk", "3.0")
from gi.repository import Gtk


class MyWindow(Gtk.Window):
    def __init__(self):
        super().__init__(title="May the force be with you")
        
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
        
        self.y1_adjustment = Gtk.Adjustment(0, 0, 54, 1, 10, 0)
        self.y1_label = Gtk.Label("Valeur Y de départ")
        self.y1_axis = Gtk.SpinButton()
        self.y1_axis.set_adjustment(self.y1_adjustment)
        self.y1_box = Gtk.Box(spacing = 6)
        self.y1_box.pack_start(self.y1_label, True, True, 0)
        self.y1_box.pack_start(self.y1_axis, True, True, 0)
        self.simple_vol.pack_start(self.y1_box, True, True, 0)   
        
        self.x2_adjustment = Gtk.Adjustment(45, 0, 45, 1, 10, 0)
        self.x2_label = Gtk.Label("Valeur X d'arrivée")
        self.x2_axis = Gtk.SpinButton()
        self.x2_axis.set_adjustment(self.x2_adjustment)
        self.x2_box = Gtk.Box(spacing = 6)
        self.x2_box.pack_start(self.x2_label, True, True, 0)
        self.x2_box.pack_start(self.x2_axis, True, True, 0)
        self.simple_vol.pack_start(self.x2_box, True, True, 0)   
        
        self.y2_adjustment = Gtk.Adjustment(54, 0, 54, 1, 10, 0)
        self.y2_label = Gtk.Label("Valeur Y d'arrivée")
        self.y2_axis = Gtk.SpinButton()
        self.y2_axis.set_adjustment(self.y2_adjustment)
        self.y2_box = Gtk.Box(spacing = 6)
        self.y2_box.pack_start(self.y2_label, True, True, 0)
        self.y2_box.pack_start(self.y2_axis, True, True, 0)
        self.simple_vol.pack_start(self.y2_box, True, True, 0)   
        
        
        
        
        
        #TODO: choose origin and destination, then call Nicolas's function
        
        #Populates the third tab: Complex vol plan
        #TODO: pick a file, then call Lilian's function
        
        
        

    def on_button_clicked(self, widget):
        self.button.set_label('Click again!')


win = MyWindow()
win.set_border_width(10)
win.connect("destroy", Gtk.main_quit)
win.show_all()
Gtk.main()