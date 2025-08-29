# dotfiles — Arch visual setup (Qtile • Alacritty • Rofi • Picom • GTK • LightDM)

This repo shows **how to install & use my Arch setup** — it does **not** teach how to create or customize dotfiles from scratch.

The repository has two purposes:
1) **Personalization (visual setup).**  
2) **System functionality (audio, multi‑monitor helpers, mounts, etc.)**

> Thereby, it may be seen as a whole personalized working Arch enviroment. Hence, I encourage you to check the packages you'll be installing so you can carefully add/remove exactly the ones you want.

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

See `packages/README.md` for installation steps covering both native Arch (pacman) and AUR packages.

## Enable system services

1) Enable LightDM:
   ```bash
   sudo systemctl enable lightdm.service
   sudo systemctl set-default graphical.target
   ```

2) Enable PipeWire:
   ```bash
   systemctl --user --now enable wireplumber.service
   systemctl --user restart pipewire pipewire-pulse
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

## Copy system configs (/etc)
```bash
sudo rsync -avh ~/dotfiles/etc/ /etc/
```
This copies the entire `etc` directory from the repo into `/etc`. It only adds/overwrites files, it does not delete existing files there.
---

## Reboot
```bash
reboot
```

**Everything should be working as expected now. If everything is fine you may leave the guide here and optionally cleanup as seen next.**

---

## Cleanup (optional)

Once you confirm everything works, you can remove the cloned repository:

```bash
cd ~
rm -rf ~/dotfiles
```

---

> Now installation is fully complete. Below we'll cover some useful tips you may want to know in order to use my personalized enviroment correctly.

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

## License

MIT — no warranty.
