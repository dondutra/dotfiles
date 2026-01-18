# Package List & Install Guide

Synced from `native.txt` and `aur.txt` on **29/08/2025**.

This README lists the packages split by **native (official repos)** and **AUR**.

## Native (pacman)
Install with pacman:
```bash
# Install all native packages (skip already-installed)
sudo pacman -S --needed --noconfirm \
  $(awk '{print $1}' native.txt)
```

| Package | What it’s for |
|---|---|
| [pipewire-alsa](https://archlinux.org/packages/extra/x86_64/pipewire-alsa/) | ALSA compatibility for PipeWire. |
| [rofi](https://archlinux.org/packages/extra/x86_64/rofi/) | App launcher / dmenu. |
| [pipewire](https://archlinux.org/packages/extra/x86_64/pipewire/) | Audio/video server. |
| [cbatticon](https://archlinux.org/packages/extra/x86_64/cbatticon/) | Battery tray icon. |
| [base-devel](https://archlinux.org/packages/core/any/base-devel/) | Build essentials meta package. |
| [brightnessctl](https://archlinux.org/packages/extra/x86_64/brightnessctl/) | Control screen brightness. |
| [ttf-dejavu](https://archlinux.org/packages/extra/any/ttf-dejavu/) | DejaVu TTF fonts. |
| [lightdm](https://archlinux.org/packages/extra/x86_64/lightdm/) | Display manager. |
| [rsync](https://archlinux.org/packages/extra/x86_64/rsync/) | Fast file sync/transfer. |
| [fastfetch](https://archlinux.org/packages/extra/x86_64/fastfetch/) | Fast system info fetch. |
| [ttf-font-awesome](https://archlinux.org/packages/extra/any/ttf-font-awesome/) | Font Awesome TTF. |
| [alacritty](https://archlinux.org/packages/extra/x86_64/alacritty/) | GPU‑accelerated terminal. |
| [gst-plugin-pipewire](https://archlinux.org/packages/extra/x86_64/gst-plugin-pipewire/) | GStreamer PipeWire plugin. |
| [htop](https://archlinux.org/packages/extra/x86_64/htop/) | Interactive process viewer. |
| [pipewire-jack](https://archlinux.org/packages/extra/x86_64/pipewire-jack/) | JACK replacement shim. |
| [ttf-liberation](https://archlinux.org/packages/extra/any/ttf-liberation/) | Liberation TTF fonts. |
| [lightdm-slick-greeter](https://archlinux.org/packages/extra/x86_64/lightdm-slick-greeter/) | LightDM greeter (slick). |
| [lightdm-gtk-greeter](https://archlinux.org/packages/extra/x86_64/lightdm-gtk-greeter/) | LightDM GTK greeter. |
| [exa](https://archlinux.org/packages/extra/x86_64/exa/) | Modern ls replacement. |
| [ttf-nerd-fonts-symbols-mono](https://archlinux.org/packages/extra/any/ttf-nerd-fonts-symbols-mono/) | Nerd Fonts symbols (mono). |
| [ttf-nerd-fonts-symbols](https://archlinux.org/packages/extra/any/ttf-nerd-fonts-symbols/) | Nerd Fonts symbols. |
| [network-manager-applet](https://archlinux.org/packages/extra/x86_64/network-manager-applet/) | NetworkManager tray applet. |
| [noto-fonts-cjk](https://archlinux.org/packages/extra/any/noto-fonts-cjk/) | Noto CJK fonts. |
| [noto-fonts-emoji](https://archlinux.org/packages/extra/any/noto-fonts-emoji/) | Noto Color Emoji. |
| [noto-fonts-extra](https://archlinux.org/packages/extra/any/noto-fonts-extra/) | Noto extra variants. |
| [noto-fonts](https://archlinux.org/packages/extra/any/noto-fonts/) | Noto fonts family. |
| [papirus-icon-theme](https://archlinux.org/packages/extra/any/papirus-icon-theme/) | Papirus icon theme. |
| [wireplumber](https://archlinux.org/packages/extra/x86_64/wireplumber/) | PipeWire session manager. |
| [pamixer](https://archlinux.org/packages/extra/x86_64/pamixer/) | PulseAudio CLI mixer. |
| [pipewire-pulse](https://archlinux.org/packages/extra/x86_64/pipewire-pulse/) | PulseAudio replacement shim. |
| [pasystray](https://archlinux.org/packages/extra/x86_64/pasystray/) | PulseAudio tray applet. |
| [udisks2](https://archlinux.org/packages/extra/x86_64/udisks2/) | Disk manipulation service. |
| [udiskie](https://archlinux.org/packages/extra/x86_64/udiskie/) | Disk automounter with systray icon. |
| [pavucontrol](https://archlinux.org/packages/extra/x86_64/pavucontrol/) | PulseAudio volume control GUI. |
| [openssh](https://archlinux.org/packages/core/x86_64/openssh/) | SSH client/server. |
| [qtile](https://archlinux.org/packages/extra/x86_64/qtile/) | Tiling window manager (Python). |
| [ttf-ubuntu-mono-nerd](https://archlinux.org/packages/extra/any/ttf-ubuntu-mono-nerd/) | Ubuntu Mono Nerd Font. |
| [vlc](https://archlinux.org/packages/extra/x86_64/vlc/) | Versatile media player. |
| [git](https://archlinux.org/packages/extra/x86_64/git/) | Version control system. |
| [code](https://archlinux.org/packages/extra/x86_64/code/) | VS Code (Code – OSS). |
| [xorg-xinit](https://archlinux.org/packages/extra/x86_64/xorg-xinit/) | X init scripts (startx). |
| [xterm](https://archlinux.org/packages/extra/x86_64/xterm/) | X terminal emulator. |
| [xorg](https://archlinux.org/groups/x86_64/xorg/) | X.Org server & drivers (group). |
| [picom](https://archlinux.org/packages/extra/x86_64/picom/) | X11 compositor. |
| [xcb-util-cursor](https://archlinux.org/packages/extra/x86_64/xcb-util-cursor/) | XCB cursor utility library. |
| [thunar](https://archlinux.org/packages/extra/x86_64/thunar/) | XFCE file manager. |
| [unzip](https://archlinux.org/packages/extra/x86_64/unzip/) | Zip extraction utility. |
| [feh](https://archlinux.org/packages/extra/x86_64/feh/) | Wallpaper manager. |

## AUR (yay or another helper)
Install with yay (or your preferred AUR helper):
```bash
# Install all AUR packages with yay (skip already-installed)
yay -S --needed --noconfirm \
  $(awk '{print $1}' aur.txt)
```

| Package | What it’s for |
|---|---|
| [bibata-cursor-theme-bin](https://aur.archlinux.org/packages/bibata-cursor-theme-bin) | Bibata cursor theme (binary). |
| [ccat](https://aur.archlinux.org/packages/ccat) | Colorizing cat (Go). |
| [discord](https://archlinux.org/packages/extra/x86_64/discord/) | Discord desktop client. |
| [gtk-theme-material-black](https://aur.archlinux.org/packages/gtk-theme-material-black) | Material‑style dark GTK theme. |
| [sublime-text](https://aur.archlinux.org/packages/sublime-text-4) | Sublime Text (stable). |
| [zen-browser-bin](https://aur.archlinux.org/packages/zen-browser-bin) | Zen Browser (binary). |

### Install `yay` (AUR helper)

```bash
# 1) Ensure build tools are present
sudo pacman -S --needed base-devel git

# 2) Build and install yay from AUR
cd ~
git clone https://aur.archlinux.org/yay.git
cd yay
makepkg -si

# 3) Remove leftovers (optional)
cd ~
rm -rf yay
```