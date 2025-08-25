# ─────────────────────────────────────────────────────────────────────────────
# dondutra dotfiles — Qtile configuration
# yt:    youtube.com/@arkty
# github: github.com/dondutra
# Note: Free to use as long as this header remains, or there is an explicit
#       mention of the creator (dondutra).
# ─────────────────────────────────────────────────────────────────────────────

import os
import subprocess

from libqtile import bar, layout, qtile, widget
from libqtile.config import Click, Drag, Group, Key, Match, Screen
from libqtile.lazy import lazy
from libqtile import hook

# Mod key and preferred terminal
mod = "mod1"          # Use Mod1 (Alt). Use "mod4" for Super/Windows if preferred.
terminal = "alacritty"

# Run autostart script once per session (spawns your helpers)
@hook.subscribe.startup_once
def autostart():
    subprocess.Popen([os.path.expanduser("~/.config/qtile/autostart.sh")])

# ----------------------------------------------------------------------------- 
# Key bindings
# -----------------------------------------------------------------------------
keys = [
    # --- [WINDOWS] ---
    # Focus movement within the current layout
    Key([mod], "Left",  lazy.layout.left(),  desc="Focus left"),
    Key([mod], "Right", lazy.layout.right(), desc="Focus right"),
    Key([mod], "Down",  lazy.layout.down(),  desc="Focus down"),
    Key([mod], "Up",    lazy.layout.up(),    desc="Focus up"),
    Key([mod], "space", lazy.layout.next(),  desc="Focus next window"),

    # Move windows within the layout
    Key([mod, "shift"], "Left",  lazy.layout.shuffle_left(),  desc="Move window left"),
    Key([mod, "shift"], "Right", lazy.layout.shuffle_right(), desc="Move window right"),
    Key([mod, "shift"], "Down",  lazy.layout.shuffle_down(),  desc="Move window down"),
    Key([mod, "shift"], "Up",    lazy.layout.shuffle_up(),    desc="Move window up"),

    # Resize windows
    Key([mod, "control"], "Left",  lazy.layout.grow_left(),  desc="Grow to the left"),
    Key([mod, "control"], "Right", lazy.layout.grow_right(), desc="Grow to the right"),
    Key([mod, "control"], "Down",  lazy.layout.grow_down(),  desc="Grow down"),
    Key([mod, "control"], "Up",    lazy.layout.grow_up(),    desc="Grow up"),
    Key([mod], "n", lazy.layout.normalize(), desc="Reset window sizes"),

    # Layout/window state
    Key([mod], "Tab", lazy.next_layout(),               desc="Cycle layouts"),
    Key([mod], "w",   lazy.window.kill(),               desc="Close focused window"),
    Key([mod], "f",   lazy.window.toggle_fullscreen(),  desc="Toggle fullscreen"),
    Key([mod], "t",   lazy.window.toggle_floating(),    desc="Toggle floating"),

    # --- [LAUNCHERS] ---
    Key([mod], "Return", lazy.spawn(terminal),             desc="Launch terminal"),
    Key([mod], "m",      lazy.spawn("rofi -show drun"),    desc="App launcher (rofi)"),
    Key([mod], "b",      lazy.spawn("zen-browser"),        desc="Default browser"),
    Key([mod], "e",      lazy.spawn("thunar"),             desc="File manager"),

    # --- [VOLUME] ---
    Key([], "XF86AudioLowerVolume", lazy.spawn("pamixer --decrease 5")),
    Key([], "XF86AudioRaiseVolume", lazy.spawn("pamixer --increase 5")),
    Key([], "XF86AudioMute",        lazy.spawn("pamixer --toggle-mute")),

    # --- [BRIGHTNESS] ---
    Key([], "XF86MonBrightnessUp",   lazy.spawn("brightnessctl set +10%")),
    Key([], "XF86MonBrightnessDown", lazy.spawn("brightnessctl set 10%-")),

    # --- [CONTROL] ---
    Key([mod, "control"], "r", lazy.restart(),          desc="Restart Qtile"),
    Key([mod, "control"], "q", lazy.shutdown(),         desc="Shutdown Qtile"),
    Key([mod], "r",             lazy.spawncmd(),        desc="Command prompt"),
    Key([mod], "l",             lazy.spawn("dm-tool lock"), desc="Lock session"),
]

# ----------------------------------------------------------------------------- 
# Groups (workspaces)
# -----------------------------------------------------------------------------
groups = [Group(i) for i in ["", "󰖟", ""]]

for i, group in enumerate(groups):
    actual_key = str(i + 1)
    keys.extend(
        [
            # mod + number: go to group
            Key([mod], actual_key, lazy.group[group.name].toscreen(),
                desc=f"Switch to group {group.name}"),
            # mod + shift + number: move window to group and follow it
            Key([mod, "shift"], actual_key,
                lazy.window.togroup(group.name, switch_group=True),
                desc=f"Move focused window to group {group.name} and follow"),
        ]
    )

# ----------------------------------------------------------------------------- 
# Layouts
# -----------------------------------------------------------------------------
layout_conf = {
    'border_focus': '#d1b3fc',
    'border_width': 4,
    'margin': 8,
}

layouts = [
    #layout.Columns(border_focus_stack=["#d75f5f", "#8f3d3d"], border_width=4),
    layout.Columns(**layout_conf),
    layout.Max(),
    # Try more layouts by unleashing below layouts.
    # layout.Stack(num_stacks=2),
    # layout.Bsp(),
    # layout.Matrix(),
    # layout.MonadTall(),
    # layout.MonadWide(),
    # layout.RatioTile(),
    # layout.Tile(),
    # layout.TreeTab(),
    # layout.VerticalTile(),
    # layout.Zoomy(),
]

# ----------------------------------------------------------------------------- 
# Widgets / Bars / Screens
# -----------------------------------------------------------------------------
widget_defaults = dict(
    font="UbuntuMono Nerd Font Mono",
    fontsize=16,
    padding=3,
)
extension_defaults = widget_defaults.copy()

wall = os.path.expanduser("~/.config/wallpapers/black-landscape.png")
screens = [
    Screen(
        top=bar.Bar(
            [
                # widget.CurrentLayout(),
                widget.WindowName(
                    padding=12,
                    foreground="#d1b3fc",
                    font='UbuntuMono Nerd Font',
                    fontsize=15,
                    markup=True,
                    fmt="<b>{}</b>",
                ),
                widget.Spacer(),
                widget.GroupBox(
                    font='UbuntuMono Nerd Font Mono',
                    fontsize=36,
                    padding_x=10,
                    highlight_method='text',
                    this_current_screen_border="#d1b3fc",
                    active='#ffffff',   # groups with windows (not selected)
                    inactive='#7a7a7a', # empty groups
                    rounded=False,
                ),
                widget.Spacer(),
                widget.Systray(padding=12),
                widget.Clock(
                    padding=12,
                    format="%a %H:%M\n%d/%m/%Y",
                    font='UbuntuMono Nerd Font',
                    fontsize=14,
                    markup=True,
                    fmt="<b>{}</b>",
                ),
            ],
            35,  # bar height
            margin=[8, 8, 0, 8],  # top, right, bottom, left
            border_width=2,
            border_color='#9180bd',
        ),
        background="#7a7a7a",
        wallpaper=wall,
        wallpaper_mode="fill",
    ),
]

# ----------------------------------------------------------------------------- 
# Some default Qtile configs
# -----------------------------------------------------------------------------
# Drag floating layouts.
mouse = [
    Drag([mod], "Button1", lazy.window.set_position_floating(), start=lazy.window.get_position()),
    Drag([mod], "Button3", lazy.window.set_size_floating(), start=lazy.window.get_size()),
    Click([mod], "Button2", lazy.window.bring_to_front()),
]

dgroups_key_binder = None
dgroups_app_rules = []  # type: list
follow_mouse_focus = True
bring_front_click = False
floats_kept_above = True
cursor_warp = False
floating_layout = layout.Floating(
    float_rules=[
        # Run the utility of `xprop` to see the wm class and name of an X client.
        *layout.Floating.default_float_rules,
        Match(wm_class="confirmreset"),  # gitk
        Match(wm_class="makebranch"),  # gitk
        Match(wm_class="maketag"),  # gitk
        Match(wm_class="ssh-askpass"),  # ssh-askpass
        Match(title="branchdialog"),  # gitk
        Match(title="pinentry"),  # GPG key password entry
    ]
)
auto_fullscreen = True
focus_on_window_activation = "smart"
focus_previous_on_window_remove = False
reconfigure_screens = True

# If things like steam games want to auto-minimize themselves when losing
# focus, should we respect this or not?
auto_minimize = True

# When using the Wayland backend, this can be used to configure input devices.
wl_input_rules = None

# xcursor theme (string or None) and size (integer) for Wayland backend
wl_xcursor_theme = None
wl_xcursor_size = 24

# XXX: Gasp! We're lying here. In fact, nobody really uses or cares about this
# string besides java UI toolkits; you can see several discussions on the
# mailing lists, GitHub issues, and other WM documentation that suggest setting
# this string if your java app doesn't work correctly. We may as well just lie
# and say that we're a working one by default.
#
# We choose LG3D to maximize irony: it is a 3D non-reparenting WM written in
# java that happens to be on java's whitelist.
wmname = "LG3D"
