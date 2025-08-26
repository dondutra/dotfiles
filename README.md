# dotfiles — Arch visual setup (Qtile • Alacritty • Rofi • Picom • GTK • LightDM)

This repo shows **how to install my Arch setup** (and, in the future, **switch between my themes**) — it does **not** teach how to create or customize dotfiles from scratch.

The repository has two purposes:
1) **Personalization (visual setup)** — ✅ fully covered here.  
2) **System functionality** (audio, multi‑monitor helpers, mounts, etc.) — ⏳ *placeholder for later.*

---

## Preconditions

- A working **Arch Linux** installation using **X11**.  
- Your user can run commands with **sudo**.  
- Internet access and basic shell usage.

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

## Repository layout (actual tree)

Everything below lives under the top-level **`dotfiles/`** folder:

```
dotfiles/
├─ etc/
│  └─ lightdm/
│     └─ slick-greeter.conf
├─ home/
│  ├─ .bashrc
│  ├─ .gtkrc-2.0
│  ├─ .xprofile
│  └─ .config/
│     ├─ alacritty/
│     │  └─ alacritty.toml
│     ├─ gtk-3.0/
│     │  └─ settings.ini
│     ├─ gtk-4.0/
│     │  └─ settings.ini
│     ├─ picom/
│     │  └─ picom.conf
│     ├─ qtile/
│     │  ├─ autostart.sh
│     │  └─ config.py
│     ├─ rofi/
│     │  ├─ config.rasi
│     │  └─ themes/
│     │     ├─ onedark.rasi
│     │     └─ slate.rasi
│     └─ wallpapers/
│        ├─ 31.jpg
│        ├─ 69.jpeg
│        ├─ 71.png
│        ├─ 85.jpg
│        ├─ monokuma-eye.png
│        ├─ monokuma-stare.jpg
│        ├─ monokuma_military.jpg
│        ├─ monokumas.jpg
│        ├─ osagechan.jpeg
│        ├─ osagechan2.png
│        └─ shinobu.png
├─ packages/
│  ├─ aur.txt
│  └─ native.txt
└─ README.md
```

---

## Install the packages

### 0) Update first

```bash
sudo pacman -Syu
```

### 1) Native repo packages (from `packages/native.txt`)

The list is **one package per line** (simplified format). This installs them **sequentially, one by one**, skipping already-installed ones.

```bash
while IFS= read -r pkg; do
  [[ -z "$pkg" ]] && continue
  sudo pacman -S --needed "$pkg"
done < ./packages/native.txt
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

Also **one package per line**. Installed **sequentially** with `yay`:

```bash
while IFS= read -r pkg; do
  [[ -z "$pkg" ]] && continue
  yay -S --needed "$pkg"
done < ./packages/aur.txt
```

This typically includes the GTK theme **Material-Black-Plum**. If it’s not in your list, install it explicitly:

```bash
yay -S material-black-plum-theme
```

---

## Place the dotfiles

From the repository root (`dotfiles/`):

```bash
# Create config dir if missing
mkdir -p ~/.config

# Copy everything in one go
cp -r home/.config/* ~/.config/
cp home/.xprofile ~/
cp home/.gtkrc-2.0 ~/
cp home/.bashrc ~/

# Ensure autostart script is executable (Qtile may call it)
chmod +x ~/.config/qtile/autostart.sh 2>/dev/null || true
```

If you installed **LightDM** and want to use the slick-greeter configuration shipped here:

```bash
sudo mkdir -p /etc/lightdm
sudo cp etc/lightdm/slick-greeter.conf /etc/lightdm/
```

> If you prefer **lightdm-gtk-greeter**, set it in `/etc/lightdm/lightdm.conf`.

---

## Start Qtile

Choose **one** of the two approaches below.

### A) With **LightDM** (graphical login)

1) Install and enable LightDM (if you haven’t already):
   ```bash
   sudo pacman -S --needed lightdm lightdm-gtk-greeter
   sudo systemctl enable lightdm.service
   sudo systemctl set-default graphical.target
   ```

2) Select **Qtile** on the login screen.

To ensure the correct greeter/session, copy (inside repo dotfiles):
```bash
sudo cp -r etc/lightdm/ /etc/
```

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
