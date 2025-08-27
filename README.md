# dotfiles — Arch visual setup (Qtile • Alacritty • Rofi • Picom • GTK • LightDM)

This repo shows **how to install my Arch setup** (and, in the future, **switch between my themes**) — it does **not** teach how to create or customize dotfiles from scratch.

The repository has two purposes:
1) **Personalization (visual setup)** — ✅ fully covered here.  
2) **System functionality** (audio, multi‑monitor helpers, mounts, etc.) — ⏳ *placeholder for later.*

---

## Preconditions

- A fresh **Arch Linux** installation. 
- Your user can run commands with **sudo**.  
- Internet access and basic shell usage.

---

## Get the repository

Pick a folder (I'll assume you put it in your home), then clone and enter the repo:

```bash
cd ~
git clone https://github.com/dondutra/dotfiles.git
cd dotfiles
```

You can delete this folder after finishing because configs are copied into your home.

---

## Install the packages

### 0) Update first

```bash
sudo pacman -Syu
```

### 1) Install core/native packages (single command)

> If a package is already present, `--needed` will skip it.  
> This list mirrors `dotfiles/packages/native.txt`.

```bash
sudo pacman -S --needed base-devel git rsync openssh unzip htop fastfetch exa brightnessctl xorg xorg-xinit lightdm lightdm-slick-greeter lightdm-gtk-greeter qtile picom rofi feh alacritty xterm thunar code firefox vlc imv papirus-icon-theme pulseaudio pavucontrol pamixer volumeicon network-manager-applet cbatticon ttf-dejavu ttf-liberation noto-fonts noto-fonts-extra noto-fonts-cjk noto-fonts-emoji ttf-ubuntu-mono-nerd ttf-font-awesome ttf-nerd-fonts-symbols ttf-nerd-fonts-symbols-mono
```

> Install the proper GPU driver for your hardware (e.g., `xf86-video-amdgpu`, `nvidia`) if needed.

### 2) Install **yay** (AUR helper)

Requires `base-devel` and `git` (installed via the native list above).

```bash
cd ~
git clone https://aur.archlinux.org/yay-bin.git
cd yay-bin
makepkg -si
cd ..
rm -rf yay-bin
```

### 3) AUR packages (from `packages/aur.txt`)

> This list mirrors `dotfiles/packages/native.txt`.

```bash
yay -S ccat zen-browser-bin sublime-text gtk-theme-material-black
```
---

## Enable login manager LightDM

1) Enable LightDM:
   ```bash
   sudo systemctl enable lightdm.service
   sudo systemctl set-default graphical.target
   ```

---

## Reboot & continue to lightdm

> Note: Rebooting here may save you from a lot of problems later.
```bash
reboot
```

Now the login manager (lightdm) should open. Enter your credentials. Default qtile session should start.

---

## Place the dotfiles

> Note: default qtile keybinding for opening a terminal {super (windows) + enter}. Alternatively: {ctrl + alt + F2}
```bash
# Sync the dotfiles
rsync -avh ~/dotfiles/home/ ~/

# Ensure autostart script is executable (Qtile may call it)
chmod +x ~/.config/qtile/autostart.sh 2>/dev/null || true
```

---

## Copy my LightDM configs
```bash
sudo rsync -avh ~/dotfiles/etc/lightdm/ /etc/lightdm/
```

---

## Reboot
```bash
reboot
```

**Everything should be working as expected now. If everything is fine you may leave the guide here. If something is failing, below we cover some troubleshooting.**

---

## Entering QTile without a display manager (use **startx**)

> Sometimes, lightdm is the only problem and qtile is fine. If you don't need a graphical login but you want everything else you may want to proceed as follows:

1) Create or edit `~/.xinitrc`:
   ```bash
   nano ~/.xinitrc
   ```
   Put this as the last line and save:
   ```bash
   [ -f ~/.xprofile ] && . ~/.xprofile
   exec qtile start
   ```
   This loads your session environment when using startx

2) Start X:
   ```bash
   startx
   ```

3) Since you started it manually, you will need to run .xprofile manually as well:
   ```bash
   cd ~
   chmod +x .xprofile
   ~/.xprofile
   ```

> If `startx` says **command not found**, install `xorg-xinit`:
> ```bash
> sudo pacman -S xorg-xinit
> ```

Now, each time you want the qtile session after a reboot, run:
```bash
  startx && ~/.xprofile
```

---

## Troubleshooting

- **“Failed to start Light Display Manager”**
  - Confirm X11 is installed (`xorg`/`xorg-server`), and a greeter is selected in `/etc/lightdm/lightdm.conf`.
  - See logs: `journalctl -u lightdm --no-pager`

- **No Qtile option on the login screen**
  - Ensure `qtile` is installed and `/usr/share/xsessions/qtile.desktop` exists (provided by the package).

- **Black screen / glitches**
  - Install the appropriate GPU driver for your hardware (e.g., `xf86-video-amdgpu`, `nvidia`).

- **Wallpaper doesn’t change**
  - Open `~/.config/qtile/config.py` and verify the wallpaper path is valid under `~/.config/wallpapers/`.  
  - Note: this setup does **not** rely on `feh` for wallpaper.

- **Audio stack (correct)**  
  - This setup uses **PulseAudio** packages (`pulseaudio`, `pavucontrol`, `pamixer`, `volumeicon`).  
  - If you want **PipeWire**, replace these with PipeWire equivalents yourself (not covered here).

> If nothing of above works, try starting all over again. If still not working, welcome to Archlinux ;)

---

## Part 2 — System functionality (placeholder)

This section will later cover:
- PulseAudio basics and tweaks
- Multiple monitors (quick helpers)
- Auto-mounting removable drives
- Everyday CLI tools and services

> Not implemented yet.

---

## Cleanup (optional)

Once you confirm everything works, you can remove the cloned repository:

```bash
cd ~
rm -rf ~/dotfiles
```

---

## License

MIT — no warranty.
