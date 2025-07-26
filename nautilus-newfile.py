import os
import gi
gi.require_version('Adw', '1')
gi.require_version("Gtk", "4.0")
from gi.repository import Nautilus, GObject, Adw, Gtk, Gio
from typing import List

@Gtk.Template(filename=os.path.join(__file__, "../new-file-dialog.ui"))
class NewFileDialog(Adw.Dialog):
    __gtype_name__ = "NewFileDialog"
    name_entry: Adw.EntryRow = Gtk.Template.Child()
    fileinfo: Gio.FileInfo = None

    def __init__(self, fileinfo):
        super().__init__()
        self.fileinfo = fileinfo

    @Gtk.Template.Callback()
    def on_create_clicked(self, _):
        f: Gio.File = (self.fileinfo.get_location())
        f.get_child(self.name_entry.get_text()).create(Gio.FileCreateFlags(0), None)
        self.close()

class NautilusNewfile(GObject.GObject, Nautilus.MenuProvider):

    def show_dialog(self, _, fileinfo):
        dialog = NewFileDialog(fileinfo)
        dialog.present()

    def get_background_items(self, fileinfo: Gio.FileInfo) -> List[Nautilus.MenuItem]:
        menuitem = Nautilus.MenuItem(name="newfile", label="New File...")
        menuitem.connect('activate', self.show_dialog, fileinfo)
        return [menuitem,]