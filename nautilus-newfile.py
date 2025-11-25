import os
import gi
gi.require_version('Adw', '1')
gi.require_version("Gtk", "4.0")
from gi.repository import Nautilus, GObject, Adw, Gtk, Gio
from typing import List

MAX_FILENAME_BYTES = 255

@Gtk.Template(filename=os.path.join(__file__, "../new-file-dialog.ui"))
class NewFileDialog(Adw.Dialog):
    __gtype_name__ = "NewFileDialog"
    
    name_entry: Adw.EntryRow = Gtk.Template.Child()
    create_button: Gtk.Button = Gtk.Template.Child()
    warning_revealer: Gtk.Revealer = Gtk.Template.Child()
    warning_label: Gtk.Label = Gtk.Template.Child()
    
    fileinfo: Gio.FileInfo = None

    def __init__(self, fileinfo):
        super().__init__()
        self.fileinfo = fileinfo
        self.validate_input()

    @Gtk.Template.Callback()
    def on_name_changed(self, widget):
        self.validate_input()

    def validate_input(self):
        filename = self.name_entry.get_text()
        
        if not filename:
            self.update_warning_ui(False, False)
            return
            
        if "/" in filename:
            self.update_warning_ui(False, True, "File name cannot contain '/'")
            return
        
        name_bytes = filename.encode('utf-8')
        if len(name_bytes) > MAX_FILENAME_BYTES:
            self.update_warning_ui(False, True, "File name is too long")
            return
            
        current_dir: Gio.File = self.fileinfo.get_location()
        target_file = current_dir.get_child(filename)
        if target_file.query_exists(None):
            self.update_warning_ui(False, True, "File already exists")
            return
            
        self.update_warning_ui(True, False)

    @Gtk.Template.Callback()
    def on_create_clicked(self, _):
        # Avoid using the Enter key to bypass button disabling
        if not self.create_button.get_sensitive():
            return
        f: Gio.File = (self.fileinfo.get_location())
        name = self.name_entry.get_text()
        if name:
            try:
                f.get_child(name).create(Gio.FileCreateFlags.NONE, None)
                self.close()
            except Exception as e:
                self.update_warning_ui(True, True, f"Failed to create: {e}")
                
    def update_warning_ui(self, enable_create_button: bool, is_warning: bool, warning_message: str = ""):
        self.create_button.set_sensitive(enable_create_button)
        self.warning_revealer.set_reveal_child(is_warning)
        if is_warning:
            self.warning_label.set_text(warning_message)
            self.name_entry.add_css_class('warning')       
        else:
            self.name_entry.remove_css_class('warning')

class NautilusNewfile(GObject.GObject, Nautilus.MenuProvider):

    def show_dialog(self, _, fileinfo):
        dialog = NewFileDialog(fileinfo)
        dialog.present()

    def get_background_items(self, fileinfo: Gio.FileInfo) -> List[Nautilus.MenuItem]:
        menuitem = Nautilus.MenuItem(name="newfile", label="New File...")
        menuitem.connect('activate', self.show_dialog, fileinfo)
        return [menuitem,]
