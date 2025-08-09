import os
import subprocess
from libqtile import bar, layout, widget, hook, qtile
from libqtile.config import Key, Group, Match, Screen
from libqtile.lazy import lazy

# --- Environment helpers ------------------------------------------------------

def _is_vm() -> bool:
    """Return True if running inside a virtual machine (set by installer)."""
    try:
        env_file = os.path.expanduser("~/.config/dotfiles/env")
        with open(env_file) as f:
            for line in f:
                if line.strip().startswith("IS_VM="):
                    return line.strip().split("=", 1)[1] == "1"
    except FileNotFoundError:
        pass
    return False

def _pick_net_interface(default=None):
    """
    Pick a reasonable network interface name for the Net widget.
    Prefer a common VM nic if present; otherwise return None (auto).
    """
    candidates = ["enp0s3", "enp0s8", "eth0", "wlp2s0", "wlan0"]
    for c in candidates:
        if os.path.exists(f"/sys/class/net/{c}"):
            return c
    return default

# --- Core settings ------------------------------------------------------------

# Alt (mod1) on VMs to avoid Super conflicts on host; Super (mod4) on hardware.
mod = "mod1" if _is_vm() else "mod4"

terminal = "alacritty"

# --- Autostart ----------------------------------------------------------------

@hook.subscribe.startup_once
def autostart():
    """Run a one-shot autostart script."""
    path = os.path.expanduser("~/.config/qtile/autostart.sh")
    if os.path.isfile(path) and os.access(path, os.X_OK):
        subprocess.Popen([path])

# --- Keybindings --------------------------------------------------------------

keys = [
    # Launchers
    Key([mod], "Return", lazy.spawn(terminal), desc="Launch terminal"),
    Key([mod], "m", lazy.spawn("rofi -show drun"), desc="Rofi app launcher"),

    # Session / config control
    Key([mod, "shift"], "r", lazy.restart(), desc="Restart Qtile"),
    Key([mod, "control"], "r", lazy.reload_config(), desc="Reload Qtile config"),
    Key([mod, "shift"], "q", lazy.shutdown(), desc="Logout from Qtile"),
    Key([mod], "w", lazy.window.kill(), desc="Close focused window"),
    Key([mod], "l", lazy.spawn("/usr/bin/dm-tool switch-to-greeter"), desc="Lock screen (LightDM)"),

    # Focus movement (arrow keys)
    Key([mod], "Left",  lazy.layout.left(),  desc="Focus left"),
    Key([mod], "Right", lazy.layout.right(), desc="Focus right"),
    Key([mod], "Up",    lazy.layout.up(),    desc="Focus up"),
    Key([mod], "Down",  lazy.layout.down(),  desc="Focus down"),

    # Move windows (arrow keys)
    Key([mod, "shift"], "Left",  lazy.layout.shuffle_left(),  desc="Move window left"),
    Key([mod, "shift"], "Right", lazy.layout.shuffle_right(), desc="Move window right"),
    Key([mod, "shift"], "Up",    lazy.layout.shuffle_up(),    desc="Move window up"),
    Key([mod, "shift"], "Down",  lazy.layout.shuffle_down(),  desc="Move window down"),

    # Resize windows (arrow keys)
    Key([mod, "control"], "Left",  lazy.layout.grow_left(),  desc="Grow left"),
    Key([mod, "control"], "Right", lazy.layout.grow_right(), desc="Grow right"),
    Key([mod, "control"], "Up",    lazy.layout.grow_up(),    desc="Grow up"),
    Key([mod, "control"], "Down",  lazy.layout.grow_down(),  desc="Grow down"),
    Key([mod], "n", lazy.layout.normalize(), desc="Normalize window sizes"),

    # Layout
    Key([mod], "space", lazy.next_layout(), desc="Next layout"),
    Key([mod], "f", lazy.window.toggle_floating(), desc="Toggle floating"),
]

# --- Groups (workspaces) ------------------------------------------------------

groups = [Group(str(i)) for i in range(1, 10)]
for g in groups:
    keys += [
        Key([mod], g.name, lazy.group[g.name].toscreen(), desc=f"Switch to group {g.name}"),
        Key([mod, "shift"], g.name, lazy.window.togroup(g.name), desc=f"Move window to group {g.name}"),
    ]

# --- Layouts ------------------------------------------------------------------

layouts = [
    layout.MonadTall(border_focus="#7aa2f7", border_normal="#3b4261", border_width=2, margin=6),
    layout.Max(),
    layout.Floating(border_focus="#7aa2f7", border_normal="#3b4261", border_width=2),
]

# --- Widgets / Bar ------------------------------------------------------------

def net_widget():
    iface = _pick_net_interface()
    return widget.Net(format="{down} ↓↑ {up}", interface=iface)

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

screens = [
    Screen(
        top=bar.Bar(
            bar_widgets,
            26,
            background="#1a1b26cc",  # semi-transparent bar (no fades elsewhere)
            margin=[4, 6, 0, 6],
        ),
    ),
]

# --- Defaults / Behavior ------------------------------------------------------

widget_defaults = dict(font="Sans", fontsize=12, padding=6)
extension_defaults = widget_defaults.copy()

floating_layout = layout.Floating(
    border_focus="#7aa2f7",
    float_rules=[
        *layout.Floating.default_float_rules,
        Match(title="Confirmation"),
        Match(wm_class="pavucontrol"),
        Match(wm_class="ssh-askpass"),
    ],
)

auto_fullscreen = True
focus_on_window_activation = "smart"
