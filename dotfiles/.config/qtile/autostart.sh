#!/usr/bin/env bash
# Lanzar compositor (transparencias)
pgrep -x picom >/dev/null || picom --experimental-backends --config "$HOME/.config/picom/picom.conf" &

# Teclado a español (por si acaso; ya tenemos localectl, pero esto refuerza)
setxkbmap es

# Ajustes que quieras añadir aquí (nm-applet, etc.)
# pgrep -x nm-applet >/dev/null || nm-applet &
