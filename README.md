# dotfiles — Arch visual setup (Qtile • Alacritty • Rofi • Picom • GTK • LightDM)

These are my personal **dotfiles** to make a fresh Arch install look clean and consistent.

The repository has two purposes:
1) **Personalization (visual setup)** — ✅ fully covered here.  
2) **System functionality** (audio, multi‑monitor helpers, mounts, etc.) — ⏳ *placeholder for later.*

---

## Preconditions (be explicit)

- You have a working **Arch Linux** installation using **X11**.  
- Your user can run commands with **sudo**.  
- You have **internet** access.  
- You either have **git** already, or you’ll install it below.

---

## Get the repository

Pick a folder (your home is fine), then clone and enter the repo:

```bash
cd ~
git clone https://github.com/dondutra/dotfiles.git
cd dotfiles
```

You can delete this folder after finishing because configs are copied into your home.

---

## Repository layout (placeholder)

Everything lives under the top-level `dotfiles/` folder and mirrors where files should end up under your system.  
*(A proper tree will be added later.)*

---

## Install required packages

### 0) Fully update your system first

```bash
sudo pacman -Syu
```

### 1) Install core/native packages (single command)

> If a package is already present, `--needed` will skip it.  
> This list mirrors `dotfiles/packages/native.txt`.

```bash
sudo pacman -S --needed base-devel git openssh unzip htop fastfetch exa brightnessctl xorg xorg-xinit lightdm lightdm-gtk-greeter qtile rofi feh alacritty xterm thunar code firefox vlc imv papirus-icon-theme pulseaudio pavucontrol pamixer volumeicon network-manager-applet cbatticon ttf-dejavu ttf-liberation noto-fonts noto-fonts-extra noto-fonts-cjk noto-fonts-emoji ttf-ubuntu-mono-nerd ttf-font-awesome ttf-nerd-fonts-symbols ttf-nerd-fonts-symbols-mono
```

> Make sure you also have the correct GPU driver for your hardware (e.g., `xf86-video-amdgpu`, `nvidia`). Install it if needed.

### 2) Install **yay** (AUR helper)

> Requires `base-devel` and `git` (installed above). We’ll build the binary package from the AUR:

```bash
cd ~
git clone https://aur.archlinux.org/yay-bin.git
cd yay-bin
makepkg -si
cd ..
rm -rf yay-bin
```

### 3) Install GTK theme **Material‑Black‑Plum** (AUR)

```bash
yay -S material-black-plum-theme
```

We’ll point GTK to this theme in the settings files below.

### 4) (Optional) Graphical login

If you want a login screen instead of `startx`, we’ll use **LightDM** with **lightdm‑gtk‑greeter**.

---

## Back up your current config (recommended)

```bash
mkdir -p ~/dotfiles_backup
cp -r ~/.config ~/dotfiles_backup/ 2>/dev/null || true
cp -r ~/.xprofile ~/.gtkrc-2.0 ~/.bashrc ~/dotfiles_backup/ 2>/dev/null || true
```

---

## Copy these dotfiles into place (simplified)

From the repository root (`dotfiles/`):

```bash
# Create config dir if missing
mkdir -p ~/.config

# Copy configs (simple, explicit)
cp -r home/.config/* ~/.config/
cp home/.xprofile ~/
cp home/.gtkrc-2.0 ~/
cp home/.bashrc ~/
```

Make the autostart script executable (Qtile may call it):

```bash
chmod +x ~/.config/qtile/autostart.sh 2>/dev/null || true
```

> You can **remove** the cloned `dotfiles/` folder later if you want. Your system uses the copies in your home.

---

## Adjust the configs manually (use `nano`)

Open and edit files as needed. Keep things simple and explicit.

- **Qtile**
  - `nano ~/.config/qtile/config.py`  
    - Set your preferred terminal if it’s not Alacritty.  
    - **Wallpaper:** the wallpaper is set **inside Qtile’s config** (feh is **not** used for wallpaper). Point it to an image under `~/.config/wallpapers/`.  
    - Review keybindings and layouts.
  - `nano ~/.config/qtile/autostart.sh`  
    - Add tray apps/services you want, e.g.:
      ```bash
      volumeicon &
      nm-applet &
      cbatticon &
      ```

- **Rofi**
  - `nano ~/.config/rofi/config.rasi`  
    - Choose a theme by setting the line to either `@theme "onedark"` or `@theme "slate"`.  
    - Themes live in `~/.config/rofi/themes/`.

- **Picom**
  - `nano ~/.config/picom/picom.conf`  
    - Tweak transparency, shadows, vsync to your preference.

- **Alacritty**
  - `nano ~/.config/alacritty/alacritty.toml`  
    - Change the font family/size if you prefer a different one.

- **GTK (apps look & feel)**
  - `nano ~/.config/gtk-3.0/settings.ini`
  - `nano ~/.config/gtk-4.0/settings.ini`  
    Set at least these to installed themes/fonts:
    ```ini
    gtk-theme-name=Material-Black-Plum
    gtk-icon-theme-name=Papirus
    gtk-font-name=Noto Sans 10
    ```
    If you choose another GTK theme, install it first.

- **LightDM (using lightdm‑gtk‑greeter)**
  - Edit `/etc/lightdm/lightdm.conf`:
    ```bash
    sudo nano /etc/lightdm/lightdm.conf
    ```
    Ensure:
    ```
    [Seat:*]
    greeter-session=lightdm-gtk-greeter
    user-session=qtile
    ```
  - (Optional) Edit the greeter’s appearance:
    ```bash
    sudo nano /etc/lightdm/lightdm-gtk-greeter.conf
    ```

---

## Start Qtile

Choose **one** of the two approaches below.

### A) With **LightDM** (graphical login)

1) Enable LightDM to start at boot:
   ```bash
   sudo systemctl enable lightdm.service
   sudo systemctl set-default graphical.target
   ```

2) Reboot and on the login screen select the **Qtile** session.

> If LightDM fails to start, see **Troubleshooting** below—usually it’s a greeter setting or missing Xorg pieces.

### B) Without a display manager (use **startx**)

1) Create or edit `~/.xinitrc`:
   ```bash
   nano ~/.xinitrc
   ```
   Put this as the last line and save:
   ```
   exec qtile start
   ```

2) Start X:
   ```bash
   startx
   ```

> If `startx` says **command not found**, install `xorg-xinit`:
> ```bash
> sudo pacman -S xorg-xinit
> ```

---

## Troubleshooting

- **“Failed to start Light Display Manager”**
  - Confirm X11 is installed: `sudo pacman -S xorg` (meta) or `sudo pacman -S xorg-server`  
  - Confirm `lightdm-gtk-greeter` is installed and selected in `/etc/lightdm/lightdm.conf`  
  - See logs: `journalctl -u lightdm --no-pager`

- **No Qtile option on the login screen**
  - Ensure `qtile` is installed and `/usr/share/xsessions/qtile.desktop` exists (provided by the package). Reinstall `qtile` if needed.

- **Black screen / glitches**
  - Install the proper GPU driver for your hardware (e.g., `xf86-video-amdgpu`, `nvidia`).

- **Wallpaper doesn’t change**
  - Open `~/.config/qtile/config.py` and verify the wallpaper path is valid under `~/.config/wallpapers/`.
  - Remember: this setup does **not** use `feh` for wallpaper.

- **No tray icons**
  - Add `volumeicon`, `nm-applet`, and/or `cbatticon` to `~/.config/qtile/autostart.sh` (see above).

- **`startx` not found**
  - Install `xorg-xinit` and try again.

- **Fonts or icons look wrong**
  - Ensure the listed fonts are installed.  
  - Check GTK theme and icon theme names in `gtk-3.0` and `gtk-4.0` settings.

---

## Part 2 — System functionality (placeholder)

This section will later cover:
- Audio (PipeWire / ALSA basics)
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
