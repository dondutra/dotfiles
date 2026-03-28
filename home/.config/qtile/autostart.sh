#!/bin/sh
picom --config ~/.config/picom/picom.conf &
python3 ~/.config/qtile/theme_selector.py autostart &
ADW_DEBUG_COLOR_SCHEME=prefer-dark mission-center &
redshift -O 3500 &
