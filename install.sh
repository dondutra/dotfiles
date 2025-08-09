#!/usr/bin/env bash
set -euo pipefail

# --- Paths & helpers ---
REPO_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
ENV_FILE="$HOME/.config/dotfiles/env"
msg(){ printf "\n\033[1;32m==>\033[0m %s\n" "$*"; }
warn(){ printf "\n\033[1;33m!!\033[0m %s\n" "$*"; }

# --- Guards ---
require_arch(){
  command -v pacman >/dev/null || { echo "This installer requires Arch Linux (pacman)."; exit 1; }
}

# --- Environment detection (persisted for Qtile) ---
detect_environment(){
  mkdir -p "$HOME/.config/dotfiles"
  if systemd-detect-virt --quiet; then
    echo "IS_VM=1" > "$ENV_FILE"
  else
    echo "IS_VM=0" > "$ENV_FILE"
  fi
  msg "Environment detected: $(cat "$ENV_FILE")"
}

# --- Ensure package lists exist ---
ensure_lists(){
  [ -f "$REPO_DIR/packages-native.txt" ] || touch "$REPO_DIR/packages-native.txt"
  [ -f "$REPO_DIR/packages-aur.txt" ]     || touch "$REPO_DIR/packages-aur.txt"
}

# --- Native packages (pacman) ---
install_native(){
  local list="$REPO_DIR/packages-native.txt"
  if [ ! -s "$list" ]; then msg "No native packages to install."; return 0; fi
  msg "Installing native packages (pacman)"
  sudo pacman -Syu --noconfirm
  # shellcheck disable=SC2046
  sudo pacman -S --needed --noconfirm $(grep -v '^\s*#' "$list" | tr '\n' ' ') || true
}

# --- Paru (prebuilt) for AUR ---
ensure_paru(){
  command -v paru >/dev/null && return 0
  msg "Installing paru-bin (AUR helper, prebuilt)"
  sudo pacman -S --needed --noconfirm base-devel git
  local tmp; tmp="$(mktemp -d)"
  pushd "$tmp" >/dev/null
  git clone https://aur.archlinux.org/paru-bin.git
  cd paru-bin
  makepkg -si --noconfirm
  popd >/dev/null
  rm -rf "$tmp"
}

# --- AUR packages (paru) ---
install_aur(){
  local list="$REPO_DIR/packages-aur.txt"
  if [ ! -s "$list" ]; then msg "No AUR packages to install."; return 0; fi
  msg "Installing AUR packages (paru)"
  # shellcheck disable=SC2046
  paru -S --needed --noconfirm --skipreview $(grep -v '^\s*#' "$list" | tr '\n' ' ') || true
}

# --- Dotfile linking ---
link_dotfile(){
  # link_dotfile <path_under_repo_dotfiles> <absolute_destination>
  local src="$REPO_DIR/dotfiles/$1"
  local dst="$2"
  mkdir -p "$(dirname "$dst")"
  if [ -e "$dst" ] && [ ! -L "$dst" ]; then
    mv -f "$dst" "$dst.bak.$(date +%s)"
  fi
  ln -sfn "$src" "$dst"
}

link_all(){
  msg "Linking dotfiles (symlinks)"
  [ -d "$REPO_DIR/dotfiles/.config/qtile" ]      && link_dotfile ".config/qtile"      "$HOME/.config/qtile"
  [ -d "$REPO_DIR/dotfiles/.config/picom" ]      && link_dotfile ".config/picom"      "$HOME/.config/picom"
  [ -d "$REPO_DIR/dotfiles/.config/alacritty" ]  && link_dotfile ".config/alacritty"  "$HOME/.config/alacritty"
  [ -d "$REPO_DIR/dotfiles/.config/rofi" ]       && link_dotfile ".config/rofi"       "$HOME/.config/rofi"
  [ -f "$REPO_DIR/dotfiles/.zshrc" ]             && link_dotfile ".zshrc"             "$HOME/.zshrc"
  [ -f "$REPO_DIR/dotfiles/.gitconfig" ]         && link_dotfile ".gitconfig"         "$HOME/.gitconfig"
}

# --- System files from repo (optional) ---
apply_system_files(){
  # Example: LightDM GTK greeter config if tracked
  if [ -f "$REPO_DIR/system/lightdm-gtk-greeter.conf" ]; then
    msg "Applying LightDM GTK greeter config"
    sudo install -Dm644 "$REPO_DIR/system/lightdm-gtk-greeter.conf" /etc/lightdm/lightdm-gtk-greeter.conf
  fi
}

# --- Ensure a working display manager & session ---
ensure_qtile_session(){
  # Make sure a Qtile session file exists (LightDM uses /usr/share/xsessions)
  if [ ! -f /usr/share/xsessions/qtile.desktop ]; then
    msg "Creating /usr/share/xsessions/qtile.desktop"
    sudo install -d /usr/share/xsessions
    sudo tee /usr/share/xsessions/qtile.desktop >/dev/null <<'EOF'
[Desktop Entry]
Name=Qtile
Comment=Qtile Session
Exec=qtile start
Type=Application
Keywords=wm;tiling
EOF
  fi
}

ensure_greeter_gtk(){
  # Force a safe greeter by default (GTK)
  sudo pacman -S --needed --noconfirm lightdm lightdm-gtk-greeter
  if grep -q '^greeter-session=' /etc/lightdm/lightdm.conf 2>/dev/null; then
    sudo sed -i 's/^greeter-session=.*/greeter-session=lightdm-gtk-greeter/' /etc/lightdm/lightdm.conf
  else
    echo 'greeter-session=lightdm-gtk-greeter' | sudo tee -a /etc/lightdm/lightdm.conf >/dev/null
  fi
}

ensure_graphical_target(){
  sudo systemctl set-default graphical.target || true
}

enable_services(){
  sudo systemctl enable lightdm.service || true
}

# --- Main ---
main(){
  require_arch
  detect_environment
  ensure_lists
  install_native
  ensure_paru
  install_aur
  link_all
  apply_system_files
  ensure_qtile_session
  ensure_greeter_gtk
  ensure_graphical_target
  enable_services
  msg "✅ Environment installation complete. Reboot to enter the graphical login."
}
main "$@"
