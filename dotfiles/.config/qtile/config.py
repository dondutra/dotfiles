from libqtile import bar, layout, widget, hook
from libqtile.config import Key, Group, Match
from libqtile.lazy import lazy
import os, subprocess

mod = "mod4"  # Tecla SUPER
terminal = "xterm"  # Luego lo cambiamos por tu terminal favorita

# Lanzar autostart
@hook.subscribe.startup_once
def autostart():
    home = os.path.expanduser("~/.config/qtile/autostart.sh")
    subprocess.Popen([home])

# Teclas básicas
keys = [
    # Lanzadores
    Key([mod], "Return", lazy.spawn(terminal), desc="Terminal"),
    Key([mod], "d", lazy.spawn("rofi -show drun"), desc="Rofi (si lo instalas)"),
    Key([mod, "shift"], "r", lazy.restart(), desc="Restart qtile"),
    Key([mod, "shift"], "q", lazy.shutdown(), desc="Logout Qtile"),

    # Foco
    Key([mod], "h", lazy.layout.left()),
    Key([mod], "l", lazy.layout.right()),
    Key([mod], "j", lazy.layout.down()),
    Key([mod], "k", lazy.layout.up()),

    # Mover ventanas
    Key([mod, "shift"], "h", lazy.layout.shuffle_left()),
    Key([mod, "shift"], "l", lazy.layout.shuffle_right()),
    Key([mod, "shift"], "j", lazy.layout.shuffle_down()),
    Key([mod, "shift"], "k", lazy.layout.shuffle_up()),

    # Redimensionar
    Key([mod, "control"], "h", lazy.layout.grow_left()),
    Key([mod, "control"], "l", lazy.layout.grow_right()),
    Key([mod, "control"], "j", lazy.layout.grow_down()),
    Key([mod, "control"], "k", lazy.layout.grow_up()),
    Key([mod], "n", lazy.layout.normalize()),

    # Cambiar layout
    Key([mod], "space", lazy.next_layout(), desc="Next layout"),

    # Flotar puntualmente (para diálogos y casos raros)
    Key([mod], "f", lazy.window.toggle_floating(), desc="Toggle floating"),
]

# Grupos (workspaces) 1..9
groups = [Group(str(i)) for i in range(1, 10)]
for i in groups:
    keys.extend([
        Key([mod], i.name, lazy.group[i.name].toscreen()),
        Key([mod, "shift"], i.name, lazy.window.togroup(i.name)),
    ])

# Layouts: tiling principal y un floating de apoyo
layouts = [
    layout.MonadTall(border_focus="#7aa2f7", border_normal="#3b4261", border_width=2, margin=6),
    layout.Max(),
    layout.Floating(border_focus="#7aa2f7", border_normal="#3b4261", border_width=2),
]

# Widgets de la barra
def net_widget():
    # Si usas Wi-Fi: widget.Wlan(interface="wlp2s0", format="{essid} {percent:2.0%}")
    return widget.Net(format="{down} ↓↑ {up}", interface=None)  # ajusta interface si quieres

screens = [
    # Barra superior
    # Estética minimalista con un poquito de color
    # Tip: instala una nerd font para mejores iconos (lo añadimos al script luego)
    type("Screen", (), {})()
]
from libqtile import Screen
screens = [
    Screen(
        top=bar.Bar(
            [
                widget.GroupBox(
                    highlight_method="block",
                    inactive="#a9b1d6",
                    active="#e5e9f0",
                    this_current_screen_border="#7aa2f7",
                    block_highlight_text_color="#1a1b26",
                    rounded=True,
                    margin_x=4,
                    padding_x=6,
                ),
                widget.Prompt(),
                widget.Spacer(),

                # Reloj con "microcalendario" (abre gsimplecal al click)
                widget.Clock(format="%a %d %b %H:%M", mouse_callbacks={"Button1": lambda: lazy.spawn("gsimplecal")()}),

                widget.Spacer(length=12),
                widget.Battery(format="{char} {percent:2.0%}", charge_char="", discharge_char=" "),
                widget.Spacer(length=12),
                widget.PulseVolume(limit_max_volume=True, step=2),
                widget.Spacer(length=12),
                net_widget(),
                widget.Spacer(length=12),

                widget.Systray(),
                widget.Spacer(length=6),
            ],
            26,
            background="#1a1b26cc",  # barra semitransparente (cc ~ 80% opacidad)
            margin=[4, 6, 0, 6],
        ),
    ),
]

widget_defaults = dict(
    font="Sans",
    fontsize=12,
    padding=6,
)
extension_defaults = widget_defaults.copy()

# Flotantes por clase/tipo (diálogos, etc.)
floating_layout = layout.Floating(
    border_focus="#7aa2f7",
    float_rules=[
        *layout.Floating.default_float_rules,
        Match(title='Confirmation'),
        Match(wm_class='pavucontrol'),
        Match(wm_class='ssh-askpass'),
    ]
)

auto_fullscreen = True
focus_on_window_activation = "smart"
