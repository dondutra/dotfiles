# Package Lists & Install Guide

Synced from `native.txt` and `aur.txt` on **2025-08-29**.

## Native (official repositories)

The following packages are expected from the Arch repositories.

| Package | What it's for |
|---|---|
| [base-devel](https://archlinux.org/packages/?q=base-devel) | Compilers and essential build tools (make, gcc, etc.). |
| [git](https://archlinux.org/packages/?q=git) | Distributed version control system. |
| [openssh](https://archlinux.org/packages/?q=openssh) | Secure shell client and server. |
| [rsync](https://archlinux.org/packages/?q=rsync) | Fast incremental file transfer and synchronization. |
| [unzip](https://archlinux.org/packages/?q=unzip) | Extract ZIP archives. |
| [htop](https://archlinux.org/packages/?q=htop) | Interactive process viewer. |
| [fastfetch](https://archlinux.org/packages/?q=fastfetch) | Fast system information summary. |
| [exa](https://archlinux.org/packages/?q=exa) | Modern replacement for `ls`. |
| [brightnessctl](https://archlinux.org/packages/?q=brightnessctl) | Control backlight brightness from the CLI. |
| [xorg](https://archlinux.org/packages/?q=xorg) | X.Org X11 display server (meta). |
| [xorg-xinit](https://archlinux.org/packages/?q=xorg-xinit) | Utilities to start X (e.g., `startx`). |
| [lightdm](https://archlinux.org/packages/?q=lightdm) | Display manager (login screen). |
| [lightdm-gtk-greeter](https://archlinux.org/packages/?q=lightdm-gtk-greeter) | GTK greeter for LightDM. |
| [lightdm-slick-greeter](https://archlinux.org/packages/?q=lightdm-slick-greeter) | Slick (GTK) greeter for LightDM. |
| [qtile](https://archlinux.org/packages/?q=qtile) | Tiling window manager written in Python. |
| [picom](https://archlinux.org/packages/?q=picom) | X compositor for transparency and shadows. |
| [rofi](https://archlinux.org/packages/?q=rofi) | Application launcher and dmenu replacement. |
| [alacritty](https://archlinux.org/packages/?q=alacritty) | GPU-accelerated terminal emulator. |
| [xterm](https://archlinux.org/packages/?q=xterm) | Lightweight X terminal emulator. |
| [thunar](https://archlinux.org/packages/?q=thunar) | Fast, simple file manager (Xfce). |
| [code](https://archlinux.org/packages/?q=code) | Utility/program package. |
| [vlc](https://archlinux.org/packages/?q=vlc) | Feature-rich media player. |
| [papirus-icon-theme](https://archlinux.org/packages/?q=papirus-icon-theme) | Utility/program package. |
| [pipewire](https://archlinux.org/packages/?q=pipewire) | Audio/video server (PulseAudio/JACK replacement). |
| [wireplumber](https://archlinux.org/packages/?q=wireplumber) | PipeWire session manager. |
| [pipewire-pulse](https://archlinux.org/packages/?q=pipewire-pulse) | Utility/program package. |
| [pipewire-alsa](https://archlinux.org/packages/?q=pipewire-alsa) | Utility/program package. |
| [pipewire-jack](https://archlinux.org/packages/?q=pipewire-jack) | Utility/program package. |
| [gst-plugin-pipewire](https://archlinux.org/packages/?q=gst-plugin-pipewire) | Utility/program package. |
| [pavucontrol](https://archlinux.org/packages/?q=pavucontrol) | PulseAudio/PipeWire volume control GUI. |
| [pamixer](https://archlinux.org/packages/?q=pamixer) | Audio volume control tool. |
| [pasystray](https://archlinux.org/packages/?q=pasystray) | Utility/program package. |
| [network-manager-applet](https://archlinux.org/packages/?q=network-manager-applet) | Utility/program package. |
| [cbatticon](https://archlinux.org/packages/?q=cbatticon) | Utility/program package. |
| [ttf-dejavu](https://archlinux.org/packages/?q=ttf-dejavu) | Font package. |
| [ttf-liberation](https://archlinux.org/packages/?q=ttf-liberation) | Font package. |
| [noto-fonts](https://archlinux.org/packages/?q=noto-fonts) | Font package. |
| [noto-fonts-extra](https://archlinux.org/packages/?q=noto-fonts-extra) | Font package. |
| [noto-fonts-cjk](https://archlinux.org/packages/?q=noto-fonts-cjk) | Font package. |
| [noto-fonts-emoji](https://archlinux.org/packages/?q=noto-fonts-emoji) | Font package. |
| [ttf-ubuntu-mono-nerd](https://archlinux.org/packages/?q=ttf-ubuntu-mono-nerd) | Font package. |
| [ttf-font-awesome](https://archlinux.org/packages/?q=ttf-font-awesome) | Font package. |
| [ttf-nerd-fonts-symbols](https://archlinux.org/packages/?q=ttf-nerd-fonts-symbols) | Font package. |
| [ttf-nerd-fonts-symbols-mono](https://archlinux.org/packages/?q=ttf-nerd-fonts-symbols-mono) | Font package. |
| [xcb-util-cursor](https://archlinux.org/packages/?q=xcb-util-cursor) | Utility/program package. |

**Install (pacman):**
```bash
sudo pacman -Syu --needed base-devel git openssh rsync unzip htop fastfetch exa brightnessctl xorg xorg-xinit lightdm lightdm-gtk-greeter lightdm-slick-greeter qtile picom rofi alacritty xterm thunar code vlc papirus-icon-theme pipewire wireplumber pipewire-pulse pipewire-alsa pipewire-jack gst-plugin-pipewire pavucontrol pamixer pasystray network-manager-applet cbatticon ttf-dejavu ttf-liberation noto-fonts noto-fonts-extra noto-fonts-cjk noto-fonts-emoji ttf-ubuntu-mono-nerd ttf-font-awesome ttf-nerd-fonts-symbols ttf-nerd-fonts-symbols-mono xcb-util-cursor
```

> Tip: Add `--noconfirm` to skip prompts, and remove packages you don't want before running.

---

## AUR (community) packages

These come from the Arch User Repository and require an AUR helper.

| Package | What it's for |
|---|---|
| [ccat](https://aur.archlinux.org/packages/ccat) | Colorizing cat (syntax highlighting). |
| [zen-browser-bin](https://aur.archlinux.org/packages/zen-browser-bin) | Firefox fork focused on performance and UX (prebuilt). |
| [sublime-text](https://aur.archlinux.org/packages/sublime-text) | Proprietary, fast code editor. |
| [gtk-theme-material-black](https://aur.archlinux.org/packages/gtk-theme-material-black) | Material Black GTK theme. |
| [bibata-cursor-theme-bin](https://aur.archlinux.org/packages/bibata-cursor-theme-bin) | Bibata cursor theme (prebuilt). |
| [discord](https://aur.archlinux.org/packages/discord) | Voice and chat app for communities and gaming. |

**Install (yay or another AUR helper):**
```bash
yay -S --needed ccat zen-browser-bin sublime-text gtk-theme-material-black bibata-cursor-theme-bin discord
```
> Note: You may replace `yay` with your preferred helper (e.g., `paru`) if you use another one.
