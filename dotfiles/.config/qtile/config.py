import os
import subprocess
from libqtile import bar, layout, widget, hook, qtile
from libqtile.config import Key, Group, Match, Screen
from libqtile.lazy import lazy

# Detect if we are in a VM
def _is_vm():
    try:
        with open(os.path.expanduser("~/.config/dotfiles/env")) as f:
            for line in f:
                if line.strip().startswith("IS_VM="):
                    return line.strip().split("=", 1)[1] == "1"
    except FileNotFoundError:
        return False

# Mod key: Alt in VM, Super on real hardware
mod = "mod1" if _is_vm() else "mod4"

# Default terminal
terminal = "alacritty"

# Autostart script (runs once at startup)
@hook.subscribe.startup_once
def autostart():
    home = os.path.expanduser("~/.config/qtile/autostart.sh")
    subprocess.Popen([home])

# Keybindings
keys = [
    # Launch terminal
    Key([mod], "Return", lazy.spawn(terminal), desc="Launch terminal"),
    Key([mod], "m", lazy.spawn("rofi -show drun"), desc="Rofi app launcher"),

    # Restart / reload Qtile
    Key([mod, "shift"], "r", lazy.restart(), desc="Restart Qtile (full)"),
    Key([mod, "control"], "r", lazy.reload_config(), desc="Reload Qtile config"),

    # Quit Qtile session
    Key([mod, "shift"], "q", lazy.shutdown(), desc="Logout from Qtile"),

    # Close focused window
    Key([mod], "w", lazy.window.kill(), desc="Close focused window"),

    # Focus movement
    Key([mod], "h", lazy.layout.left(), desc="Move focus left"),
    Key([mod], "l", lazy.layout.right(), desc="Move focus right"),
    Key([mod], "j", lazy.layout.down(), desc="Move focus down"),
    Key([mod], "k", lazy.layout.up(), desc="Move focus up"),

    # Move windows
    Key([mod, "shift"], "h", lazy.layout.shuffle_left(), desc="Move window left"),
    Key([mod, "shift"], "l", lazy.layout.shuffle_right(), desc="Move window right"),
    Key([mod, "shift"], "j", lazy.layout.shuffle_down(), desc="Move window down"),
    Key([mod, "shift"], "k", lazy.layout.shuffle_up(), desc="Move window up"),

    # Resize windows
    Key([mod, "control"], "h", lazy.layout.grow_left(), desc="Grow window to the left"),
    Key([mod, "control"], "l", lazy.layout.grow_right(), desc="Grow window to the right"),
    Key([mod, "control"], "j", lazy.layout.grow_down(), desc="Grow window down"),
    Key([mod, "control"], "k", lazy.layout.grow_up(), desc="Grow window up"),
    Key([mod], "n", lazy.layout.normalize(), desc="Normalize window sizes"),

    # Change layout / toggle floating
    Key([mod], "space", lazy.next_layout(), desc="Switch to next layout"),
    Key([mod], "f", lazy.window.toggle_floating(), desc="Toggle floating mode"),
]

# Workspaces 1..9
groups = [Group(str(i)) for i in range(1, 10)]
for i in groups:
    keys.extend([
        Key([mod], i.name, lazy.group[i.name].toscreen(), desc=f"Switch to group {i.name}"),
        Key([mod, "shift"], i.name, lazy.window.togroup(i.name), desc=f"Move window to group {i.name}"),
    ])

# Layouts
layouts = [
    layout.MonadTall(border_focus="#7aa2f7", border_normal="#3b4261", border_width=2, margin=6),
    layout.Max(),
    layout.Floating(border_focus="#7aa2f7", border_normal="#3b4261", border_width=2),
]

# Network widget helper
def net_widget():
    # Adjust 'interface' to your NIC if needed; None = auto
    return widget.Net(format="{down} ↓↑ {up}", interface="enp0s3")

# Bar widgets
bar_widgets = [
    widget.GroupBox(
        highlight_method="block",
        inactive="#a9b1d6",
        active="#e5e9f0",
        this_current_screen_border="#7aa2f7",
        block_highlight_text_color="#1a1b26",
        rounded=True,
        margin_x=4, padding_x=6,
    ),
    widget.Prompt(),
    widget.Spacer(),
    widget.Clock(
        format="%a %d %b %H:%M",
        mouse_callbacks={"Button1": lambda: qtile.cmd_spawn("gsimplecal")}
    ),
    widget.Spacer(length=12),
    widget.PulseVolume(limit_max_volume=True, step=2),
    widget.Spacer(length=12),
    net_widget(),
    widget.Spacer(length=12),
    widget.Systray(),
    widget.Spacer(length=6),
]

# Screens
screens = [
    Screen(
        top=bar.Bar(
            bar_widgets,
            26,
            background="#1a1b26cc",  # semi-transparent
            margin=[4, 6, 0, 6],
        ),
    ),
]

# Defaults
widget_defaults = dict(font="Sans", fontsize=12, padding=6)
extension_defaults = widget_defaults.copy()

# Floating layout rules
floating_layout = layout.Floating(
    border_focus="#7aa2f7",
    float_rules=[
        *layout.Floating.default_float_rules,
        Match(title='Confirmation'),
        Match(wm_class='pavucontrol'),
        Match(wm_class='ssh-askpass'),
    ]
)

# Behavior settings
auto_fullscreen = True
focus_on_window_activation = "smart"

