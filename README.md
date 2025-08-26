# dotfiles — Arch Linux visual setup (Qtile, Alacritty, Rofi, Picom, GTK, LightDM)

These are my personal **dotfiles** to make a fresh Arch install look clean and consistent.  
The repository serves two purposes:

1) **Personalization (visual setup)** — ✅ fully covered below.  
2) **System functionality (quality‑of‑life bits: audio, monitors, mounts, etc.)** — ⏳ *placeholder for later.*

> This guide assumes you already have Arch installed and can use `sudo` and `pacman`.

---

## What you’ll get

- **Qtile** window manager with my keybinds and autostart
- **Alacritty** terminal configuration
- **Rofi** app launcher with two bundled themes (`onedark` and `slate`)
- **Picom** compositor settings (transparency, shadows, animations toggles, etc.)
- **GTK 3 + 4** settings for apps (theme, icons, cursor)
- Optional **LightDM + slick-greeter** setup with my greeter config
- A small **wallpapers** collection

---

## Repository layout (actual paths & filenames)

Everything below lives under the top-level folder **`dotfiles/`**:

```
dotfiles/
├─ etc/
│  └─ lightdm/
│     └─ slick-greeter.conf
├─ home/
│  ├─ .bashrc
│  ├─ .config/
│  │  ├─ alacritty/
│  │  │  └─ alacritty.toml
│  │  ├─ gtk-3.0/
│  │  │  └─ settings.ini
│  │  ├─ gtk-4.0/
│  │  │  └─ settings.ini
│  │  ├─ picom/
│  │  │  └─ picom.conf
│  │  ├─ qtile/
│  │  │  ├─ autostart.sh
│  │  │  └─ config.py
│  │  └─ rofi/
│  │     ├─ config.rasi
│  │     └─ themes/
│  │        ├─ onedark.rasi
│  │        └─ slate.rasi
│  │  └─ wallpapers/
│  │     ├─ 31.jpg
│  │     ├─ 69.jpeg
│  │     ├─ 71.png
│  │     ├─ 85.jpg
│  │     ├─ monokuma-eye.png
│  │     ├─ monokuma-stare.jpg
│  │     ├─ monokuma_military.jpg
│  │     ├─ monokumas.jpg
│  │     ├─ osagechan.jpeg
│  │     ├─ osagechan2.png
│  │     └─ shinobu.png
│  ├─ .gtkrc-2.0
│  └─ .xprofile
├─ packages/
│  ├─ aur.txt
│  └─ native.txt
└─ README.md
```

> The `packages/` files are *references only*. We **do not** install from them automatically in this guide.

---

## 1) Install the required apps (manually, one by one)

Install each package as you need it. If something below is already installed, skip it.

```bash
sudo pacman -S qtile
sudo pacman -S alacritty
sudo pacman -S rofi
sudo pacman -S picom
```

Optional but recommended for wall­papers and fonts:

```bash
sudo pacman -S feh          # used by autostart.sh to set a background
sudo pacman -S noto-fonts   # general UI font coverage
sudo pacman -S noto-fonts-emoji
sudo pacman -S ttf-jetbrains-mono  # my terminal font; change later if you want
# If you want icon glyphs in menus/rofi:
sudo pacman -S ttf-font-awesome
```

### (Optional) Display manager

If you prefer to log in graphically:

```bash
sudo pacman -S lightdm
sudo pacman -S lightdm-slick-greeter
```

Enable LightDM so it starts at boot (you can also start it once manually after copying configs in step 3):

```bash
sudo systemctl enable lightdm.service
```

---

## 2) Back up your current config (recommended)

Create a quick backup before replacing files:

```bash
mkdir -p ~/dotfiles_backup
cp -r ~/.config ~/dotfiles_backup/ 2>/dev/null || true
cp -r ~/.xprofile ~/.gtkrc-2.0 ~/.bashrc ~/dotfiles_backup/ 2>/dev/null || true
```

---

## 3) Copy my configs into place

From the **root of this repository** (`dotfiles/`), run the following to copy things over.

> If a directory doesn’t exist yet, the command creates it first.

```bash
mkdir -p ~/.config
cp -r home/.config/alacritty ~/.config/
cp -r home/.config/gtk-3.0 ~/.config/
cp -r home/.config/gtk-4.0 ~/.config/
cp -r home/.config/picom ~/.config/
cp -r home/.config/qtile ~/.config/
cp -r home/.config/rofi ~/.config/
cp -r home/.config/wallpapers ~/.config/

cp home/.xprofile ~/
cp home/.gtkrc-2.0 ~/
cp home/.bashrc ~/
```

Make sure the autostart script is executable:

```bash
chmod +x ~/.config/qtile/autostart.sh
```

### LightDM greeter config (optional)

Only if you installed LightDM + slick-greeter above:

```bash
sudo mkdir -p /etc/lightdm
sudo cp etc/lightdm/slick-greeter.conf /etc/lightdm/
```

> You can start LightDM once to test, or simply reboot:
>
> ```bash
> sudo systemctl start lightdm
> ```

---

## 4) Edit configs *manually* (with `nano`) where needed

This setup is intentionally manual. Open files, read comments, and tweak as you like.

- **Qtile**
  - `nano ~/.config/qtile/config.py`  
    - Change `terminal` if you don’t use Alacritty.
    - Review keybindings and layouts.
  - `nano ~/.config/qtile/autostart.sh`  
    - It sets your wallpaper with `feh`. Point it to one of the images in `~/.config/wallpapers/` if you want a specific one.
    - Add any tray apps or services you want to start with Qtile.

- **Rofi**
  - `nano ~/.config/rofi/config.rasi`  
    - The config references a theme. To switch, open the file and set the theme line to either:
      - `@theme "onedark"` or
      - `@theme "slate"`
    - The themes live in `~/.config/rofi/themes/`.

- **Picom**
  - `nano ~/.config/picom/picom.conf`  
    - Adjust transparency, shadows, and vsync to your preference.

- **Alacritty**
  - `nano ~/.config/alacritty/alacritty.toml`  
    - Change the font family/size if you installed a different font.

- **GTK 3 & 4**
  - `nano ~/.config/gtk-3.0/settings.ini`
  - `nano ~/.config/gtk-4.0/settings.ini`  
    - Make sure the `gtk-theme-name`, `gtk-icon-theme-name`, and `gtk-font-name` values match themes you actually have installed. If you choose a different GTK theme, install it first.

- **LightDM greeter (optional)**
  - `sudo nano /etc/lightdm/slick-greeter.conf`  
    - Set the `background=` path to one of your wallpapers if you’d like a custom greeter background.

---

## 5) Start Qtile

- If you installed **LightDM**, choose the **Qtile** session on the login screen.  
- If you start X manually, create or update `~/.xinitrc` to exec Qtile:
  ```bash
  echo 'exec qtile start' >> ~/.xinitrc
  startx
  ```

---

## Troubleshooting tips

- If the wallpaper doesn’t set on login, verify `feh` is installed and the path in `autostart.sh` points to a real image.
- If apps look odd, check the GTK theme names in both `gtk-3.0` and `gtk-4.0` configs.
- If fonts look wrong in Alacritty/Rofi, make sure the referenced fonts are installed on your system.
- For LightDM background errors, confirm file permissions and the `background=` path in `slick-greeter.conf`.

---

## Part 2 — System functionality (placeholder)

This section will later cover:
- Audio (PipeWire / ALSA basics)
- Multi-monitor layout helpers
- Auto-mounting removable drives
- Useful services and CLI tools for a daily‑driver setup

> Not implemented yet — coming later.

---

## License

MIT — do whatever you want, but no warranty.
