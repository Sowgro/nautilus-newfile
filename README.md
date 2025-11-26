# nautilus-newfile
Adds a "New File..." option to the context menu of nautilus
![screenshot.png](screenshot.png)

### Installation
- Install Python bindings for Nautilus extension API: 
	- Fedora: `sudo dnf install nautilus-python`
	- Arch: `sudo pacman -Sy nautilus-python`
	- Ubuntu/Debian: `sudo apt update && sudo apt install python3-nautilus`
- Copy both `nautilus-newfile.py` and `new-file-dialog.ui` to `~/.local/share/nautilus-python/extensions`

### Limitations
- ~~No filename validation is run (needs implementation)~~ 🎉**Now implemented**
- Modal is not attached to the nautilus window (limitation of the nautilus extensions api)
- The newly created file is not automatically selected (limitation of the nautilus extensions api)
