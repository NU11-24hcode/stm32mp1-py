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
        self.simple_vol = Gtk.Box(spacing = 6)
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