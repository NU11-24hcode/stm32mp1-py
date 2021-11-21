import gi

gi.require_version("Gtk", "3.0")
from gi.repository import Gtk


class MyWindow(Gtk.Window):
    def __init__(self):
        super().__init__(title="Hello World")

        self.button = Gtk.Button(label="Click Here")
        self.button.connect("clicked", self.on_button_clicked)
        self.add(self.button)
        
        self.x1_adjustment = Gtk.Adjustment(0, 0, 45, 1, 10, 0)
        self.x1_label = Gtk.Label("Valeur X de départ")
        self.x1_axis = Gtk.SpinButton()
        self.x1_axis.set_adjustment(self.x1_adjustment)
        
        self.add(self.x1_axis)
        
        print(self.x1_axis.get_value_as_int())

    def on_button_clicked(self, widget):
        print("Hello World")


win = MyWindow()
win.connect("destroy", Gtk.main_quit)
win.show_all()
Gtk.main()