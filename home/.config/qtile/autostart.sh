#!/bin/sh
picom --config ~/.config/picom/picom.conf &
python3 ~/.config/qtile/theme_selector.py dont_cycle &
