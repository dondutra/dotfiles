import json
import os
import subprocess
import sys
from libqtile.command.client import InteractiveCommandClient

def manage_theme():
    path = os.path.expanduser("~/.config/qtile/themes.json")
    with open(path, "r") as f:
        data = json.load(f)

    themes = list(data["themes"].keys())
    current = data["current_theme"]

    # Argument handling
    is_autostart = "autostart" in sys.argv
    is_dont_cycle = "dont_cycle" in sys.argv or is_autostart

    # 1. Update theme selection if cycling
    if not is_dont_cycle:
        current = themes[(themes.index(current) + 1) % len(themes)]
        data["current_theme"] = current
        with open(path, "w") as f:
            json.dump(data, f, indent=4)

    # 2. Set wallpaper (using full path and repeating for multi-head stability)
    wall = os.path.expanduser(data["themes"][current]["wallpaper"])
    subprocess.Popen(["feh", "--bg-fill", wall, "--bg-fill", wall])

    # 3. Apply GTK theme if you have that implemented
    gtk = data["themes"][current].get("gtk_theme")
    if gtk:
        subprocess.Popen(["gsettings", "set", "org.gnome.desktop.interface", "gtk-theme", gtk])

    # 4. Restart Qtile ONLY if NOT in autostart
    if not is_autostart:
        try:
            InteractiveCommandClient().restart()
        except Exception:
            pass

if __name__ == "__main__":
    manage_theme()