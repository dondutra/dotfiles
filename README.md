# dotfiles — Manual installation guide (Arch Linux)

> **Scope:** This is the _only_ reference for installing my setup manually on a **fresh Arch Linux** with working internet and **git already installed**.  
> After finishing these steps, you can safely delete the repository because all configuration and assets will have been copied to their final locations.  
> An automated `install.sh` may come later; until then, use this guide.

---

## Package lists used by this guide

This guide installs exactly the packages listed in:
- `packages-native.txt` (official repos)
- `packages-aur.txt` (AUR)

You can open those two files to see or edit the lists before running the commands below.

---

## Recommended repository layout

Adopt this structure so that files mirror their final paths on disk. It makes manual installs simple and repeatable:

```
dotfiles/
├─ home/
│  └─ .config/
│     ├─ alacritty/alacritty.toml
│     ├─ gtk-3.0/settings.ini
│     ├─ picom/picom.conf
│     ├─ qtile/{autostart.sh, config.py}
│     ├─ rofi/{config.rasi, themes/*.rasi}
│     └─ wallpapers/
│        └─ <your_wallpapers_here>
├─ etc/
│  └─ lightdm/slick-greeter.conf
├─ packages-native.txt
├─ packages-aur.txt
└─ README.md
```

### One-time migration from the legacy layout (if your repo still has `config/` and `images/`)

Run once from the repo root (keeps git history with `git mv`). Skip if your repo already matches the layout above.

```bash
# From repository root
mkdir -p home/.config etc/lightdm

git mv config/alacritty         home/.config/alacritty
git mv config/gtk               home/.config/gtk-3.0
git mv config/picom             home/.config/picom
git mv config/qtile             home/.config/qtile
git mv config/rofi              home/.config/rofi
git mv images                   home/.config/wallpapers
git mv config/lightdm/slick-greeter.conf etc/lightdm/slick-greeter.conf

# Optional: clean up empty dirs
rmdir config 2>/dev/null || true
```

> Ensure that any hardcoded image paths in your configs (e.g., Qtile wallpaper) point to `~/.config/wallpapers/...` or adjust them accordingly.

---

## TL;DR — manual install (fresh Arch + internet + git)

```bash
# 0) Get the repository
git clone https://github.com/dondutra/dotfiles.git
cd dotfiles

# 1) Update system and install build tools (needed for AUR helpers)
sudo pacman -Syu --needed base-devel

# 2) Install packages from official repos (defined in packages-native.txt)
sudo pacman -S --needed $(grep -vE '^[[:space:]]*#|^[[:space:]]*$' packages-native.txt | tr '\n' ' ')

# 3) Install an AUR helper (paru used below; replace with yay if you prefer)
git clone https://aur.archlinux.org/paru.git
cd paru && makepkg -si && cd ..

# 4) Install AUR packages (defined in packages-aur.txt)
paru -S --needed $(grep -vE '^[[:space:]]*#|^[[:space:]]*$' packages-aur.txt | tr '\n' ' ')

# 5) Deploy user configuration to your HOME
mkdir -p ~/.config
cp -rT home/.config ~/.config
chmod +x ~/.config/qtile/autostart.sh  # make autostart executable

# 6) (Optional) If you want the greeter background system-wide, copy a wallpaper
#    and set it in slick-greeter.conf before installing it
#    Example:
#    sudo mkdir -p /usr/share/backgrounds/dondutra
#    sudo cp ~/.config/wallpapers/<your_image> /usr/share/backgrounds/dondutra/greeter.png
#    sudo sed -i "s|^background=.*|background=/usr/share/backgrounds/dondutra/greeter.png|" etc/lightdm/slick-greeter.conf

# 7) Install system-wide configuration
sudo install -Dm644 etc/lightdm/slick-greeter.conf /etc/lightdm/slick-greeter.conf

# 8) Enable the display manager and set default target to graphical
sudo systemctl enable lightdm.service
sudo systemctl set-default graphical.target

# 9) Refresh fonts (important for Nerd/emoji fonts)
fc-cache -rv

# 10) Reboot and log into Qtile
sudo reboot
```

---

## Detailed manual installation (with context and checks)

### 0) Preconditions

- Fresh Arch Linux.
- Working internet.
- `git` already installed (`pacman -S git` if not).

### 1) System update and build tools

AUR helpers require a compiler toolchain:

```bash
sudo pacman -Syu --needed base-devel
```

### 2) Official repo packages

Everything under `packages-native.txt` will be installed. Blank lines and `#` comments are ignored:

```bash
sudo pacman -S --needed $(grep -vE '^[[:space:]]*#|^[[:space:]]*$' packages-native.txt | tr '\n' ' ')
```

> Tip: If you plan to use NetworkManager applet (`network-manager-applet`) and you don’t already use NetworkManager, also do:
>
> ```bash
> sudo pacman -S --needed networkmanager
> sudo systemctl enable --now NetworkManager
> ```
>
> Otherwise, skip this (many fresh installs already have networking configured another way).

### 3) AUR packages

Install an AUR helper and then the packages from `packages-aur.txt`:

```bash
git clone https://aur.archlinux.org/paru.git
cd paru && makepkg -si && cd ..
paru -S --needed $(grep -vE '^[[:space:]]*#|^[[:space:]]*$' packages-aur.txt | tr '\n' ' ')
```

### 4) Copy user configuration to `$HOME`

Mirror the repo’s `home/.config` to your `~/.config` and ensure autostart is executable:

```bash
mkdir -p ~/.config
cp -rT home/.config ~/.config
chmod +x ~/.config/qtile/autostart.sh
```

### 5) Wallpapers and assets

Keep wallpapers alongside configs so the setup works after the repo is deleted:

```bash
mkdir -p ~/.config/wallpapers
cp -r home/.config/wallpapers/* ~/.config/wallpapers/ 2>/dev/null || true
```

Make sure your Qtile config points at an existing file under `~/.config/wallpapers/`.

### 6) System-wide LightDM config

Install the greeter config. If it references a specific background, either keep that path in your home (`~/.config/wallpapers/...`) or copy a system-wide image as shown in the TL;DR and update the `background=` line accordingly.

```bash
sudo install -Dm644 etc/lightdm/slick-greeter.conf /etc/lightdm/slick-greeter.conf
```

### 7) Enable services and finalize

```bash
sudo systemctl enable lightdm.service
sudo systemctl set-default graphical.target
fc-cache -rv
```

Reboot and select the **Qtile** session.

```bash
sudo reboot
```

---

## Verifications

- **Session type:** this setup targets X11. `echo "$XDG_SESSION_TYPE"` should print `x11` once logged in.  
- **Fonts:** verify Nerd and emoji fonts are visible: `fc-list | grep -i ubuntu` or `fc-list | grep -i noto`.  
- **Tray:** ensure a system tray is present in your Qtile bar for `nm-applet`, `cbatticon`, `volumeicon`, etc.  
- **Autostart:** confirm `~/.config/qtile/autostart.sh` includes your applets (`setxkbmap`, `nm-applet`, `cbatticon`, etc.) and is executable.

---

## Cleanup

You can now delete the repository if you like; your system is fully configured:

```bash
cd ~
rm -rf ~/dotfiles
```

---

## License & credits

Free to use as long as you keep a mention of the creator: **dondutra**.  
YouTube: https://youtube.com/@arkty · GitHub: https://github.com/dondutra
