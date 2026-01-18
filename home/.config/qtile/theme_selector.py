import json
import os
import subprocess
import sys
from libqtile.command.client import InteractiveCommandClient

def manage_theme():
    # Load configuration
    path = os.path.expanduser("~/.config/qtile/themes.json")
    with open(path, "r") as f:
        data = json.load(f)

    themes = list(data["themes"].keys())
    current = data["current_theme"]

    # Only cycle to the next theme if 'dont_cycle' argument is missing
    if len(sys.argv) < 2 or sys.argv[1] != "dont_cycle":
        current = themes[(themes.index(current) + 1) % len(themes)]
        data["current_theme"] = current
        with open(path, "w") as f:
            json.dump(data, f, indent=4)

    # Set wallpaper for all screens
    wall = os.path.expanduser(data["themes"][current]["wallpaper"])
    subprocess.Popen(["feh", "--bg-fill", wall])

    # Restart Qtile to apply color changes and refresh the bar
    try:
        InteractiveCommandClient().restart()
    except Exception:
        pass

if __name__ == "__main__":
    manage_theme()