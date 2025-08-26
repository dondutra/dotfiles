# dotfiles — Arch visual setup (Qtile • Alacritty • Rofi • Picom • GTK • LightDM)

These are my personal **dotfiles** to make a fresh Arch install look clean and consistent.

The repository has two purposes:
1) **Personalization (visual setup)** — ✅ fully covered here.  
2) **System functionality** (audio, multi-monitor helpers, mounts, etc.) — ⏳ *placeholder for later.*

---

## Before you start (clear preconditions)

- You have a working **Arch Linux** installation.  
- You can use `sudo`.  
- You have **internet** access.  
- You have **git** (install it if needed):
  ```bash
  sudo pacman -S git
  ```

> We target **X11** (not Wayland). If you later choose Wayland, you’ll need different steps.

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

## Install the required packages (one by one)

Install each of the following. If one is already installed, just skip it.

### X11 stack (needed for Qtile and/or LightDM)

```bash
sudo pacman -S xorg-server
```

If you **won’t** use a display manager and prefer `startx`, also install:

```bash
sudo pacman -S xorg-xinit
```

> Make sure you have a working video driver for your GPU (e.g., `xf86-video-amdgpu`, `nvidia`, or your laptop’s vendor driver). Install the appropriate one for your hardware if you don’t have it yet.

### Core apps

```bash
sudo pacman -S qtile
sudo pacman -S alacritty
sudo pacman -S rofi
sudo pacman -S picom
```

### Fonts (recommended)

```bash
sudo pacman -S noto-fonts
sudo pacman -S noto-fonts-emoji
sudo pacman -S ttf-jetbrains-mono     # terminal font I use – change later if you want
sudo pacman -S ttf-font-awesome       # optional: icons in menus/rofi
```

### (Optional) Graphical login

If you want a login screen instead of `startx`:

```bash
sudo pacman -S lightdm
sudo pacman -S lightdm-slick-greeter
```

---

## Back up your current config (recommended)

```bash
mkdir -p ~/dotfiles_backup
cp -r ~/.config ~/dotfiles_backup/ 2>/dev/null || true
cp -r ~/.xprofile ~/.gtkrc-2.0 ~/.bashrc ~/dotfiles_backup/ 2>/dev/null || true
```

---

## Copy these dotfiles into place (simple manual copy)

From the repository root (`dotfiles/`):

```bash
mkdir -p ~/.config
cp -r home/.config/alacritty ~/.config/
cp -r home/.config/gtk-3.0   ~/.config/
cp -r home/.config/gtk-4.0   ~/.config/
cp -r home/.config/picom     ~/.config/
cp -r home/.config/qtile     ~/.config/
cp -r home/.config/rofi      ~/.config/
cp -r home/.config/wallpapers ~/.config/

cp home/.xprofile ~/
cp home/.gtkrc-2.0 ~/
cp home/.bashrc ~/
```

Make the autostart script executable (Qtile may call it):

```bash
chmod +x ~/.config/qtile/autostart.sh
```

> You can now **remove** the cloned `dotfiles/` folder later if you want. Your system uses the copies in your home.

---

## Adjust the configs manually (use `nano`)

Open and edit files as needed. Keep things simple and explicit.

- **Qtile**
  - `nano ~/.config/qtile/config.py`  
    - Set your preferred terminal if it’s not Alacritty.  
    - **Wallpaper:** the config sets the wallpaper **inside Qtile** (no `feh` is required). Point it to one of the images in `~/.config/wallpapers/`.  
    - Review keybindings and layouts.
  - `nano ~/.config/qtile/autostart.sh`  
    - Add tray apps or services you want to start with the session.

- **Rofi**
  - `nano ~/.config/rofi/config.rasi`  
    - Choose a theme by setting the line to either `@theme "onedark"` or `@theme "slate"`.  
    - Themes live in `~/.config/rofi/themes/`.

- **Picom**
  - `nano ~/.config/picom/picom.conf`  
    - Tweak transparency, shadows, vsync to your preference.

- **Alacritty**
  - `nano ~/.config/alacritty/alacritty.toml`  
    - Change the font family/size if you installed a different font.

- **GTK (apps look & feel)**
  - `nano ~/.config/gtk-3.0/settings.ini`
  - `nano ~/.config/gtk-4.0/settings.ini`  
    - Ensure `gtk-theme-name`, `gtk-icon-theme-name`, and `gtk-font-name` reference themes you have installed. If unsure, use the defaults (e.g., `Adwaita` or `Adwaita-dark`).

- **LightDM greeter (optional)**
  - Copy the provided greeter configuration:
    ```bash
    sudo mkdir -p /etc/lightdm
    sudo cp etc/lightdm/slick-greeter.conf /etc/lightdm/
    ```
  - Then edit LightDM’s main config to select the greeter and (optionally) the default session:
    ```bash
    sudo nano /etc/lightdm/lightdm.conf
    ```
    Make sure these lines exist (uncomment or add them):
    ```
    [Seat:*]
    greeter-session=slick-greeter
    user-session=qtile
    ```
    If you prefer another greeter or session, set them accordingly.

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

> If LightDM fails to start, see **Troubleshooting** below—usually it’s a missing greeter setting in `/etc/lightdm/lightdm.conf` or missing Xorg packages.

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
  - Confirm X11 is installed: `sudo pacman -S xorg-server`
  - Confirm greeter is installed: `sudo pacman -S lightdm-slick-greeter`
  - Confirm it’s selected in `/etc/lightdm/lightdm.conf` (`greeter-session=slick-greeter`)
  - See logs: `journalctl -u lightdm --no-pager`

- **No Qtile option on the login screen**
  - Ensure `qtile` is installed and that `/usr/share/xsessions/qtile.desktop` exists (provided by the package). Reinstall `qtile` if needed.

- **`startx` not found**
  - Install `xorg-xinit` and try again.

- **Black screen / glitches**
  - Install the proper GPU driver for your hardware (e.g., `xf86-video-amdgpu`, `nvidia`).

- **Wallpaper doesn’t change**
  - Open `~/.config/qtile/config.py` and verify the path points to a real image under `~/.config/wallpapers/`. This setup does **not** use `feh`.

- **Fonts or icons look wrong**
  - Ensure the fonts listed above are installed.  
  - Check `gtk-3.0/gtk-4.0` `settings.ini` themes and icon themes actually exist on your system.

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
