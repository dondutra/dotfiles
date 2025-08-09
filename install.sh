#!/usr/bin/env bash
set -euo pipefail

# === Variables ===
REPO_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
ENV_FILE="$HOME/.config/dotfiles/env"

msg(){ printf "\n\033[1;32m==>\033[0m %s\n" "$*"; }

# === Detect Arch Linux ===
require_arch(){
  command -v pacman >/dev/null || { echo "This installer requires Arch Linux (pacman)."; exit 1; }
}

# === Detect if running in a VM ===
detect_vm(){
  mkdir -p "$HOME/.config/dotfiles"   # <-- create folder first
  if hostnamectl | grep -iq "virtualbox\|vmware\|kvm"; then
    echo "IS_VM=1" > "$ENV_FILE"
  else
    echo "IS_VM=0" > "$ENV_FILE"
  fi
}

# === Install native packages with pacman ===
install_native(){
  local list="$REPO_DIR/packages-native.txt"

  # Ensure file exists
  [ -f "$list" ] || { msg "Creating empty packages-native.txt"; touch "$list"; return 0; }
  [ -s "$list" ] || { msg "No native packages to install."; return 0; }

  msg "Installing native packages (pacman)"
  sudo pacman -Syu --noconfirm
  sudo pacman -S --needed --noconfirm $(grep -v '^\s*#' "$list" | tr '\n' ' ') || true
}

# === Install paru if missing ===
ensure_paru(){
  command -v paru >/dev/null && return 0
  msg "Installing paru (AUR helper)"
  sudo pacman -S --needed --noconfirm base-devel git
  local tmp; tmp="$(mktemp -d)"
  pushd "$tmp" >/dev/null
  git clone https://aur.archlinux.org/paru.git
  cd paru
  makepkg -si --noconfirm
  popd >/dev/null
  rm -rf "$tmp"
}

# === Install AUR packages with paru ===
install_aur(){
  local list="$REPO_DIR/packages-aur.txt"

  # Ensure file exists
  [ -f "$list" ] || { msg "Creating empty packages-aur.txt"; touch "$list"; return 0; }
  [ -s "$list" ] || { msg "No AUR packages to install."; return 0; }

  msg "Installing AUR packages (paru)"
  paru -S --needed --noconfirm --skipreview $(grep -v '^\s*#' "$list" | tr '\n' ' ') || true
}

# === Symlink dotfiles ===
link_dotfile(){
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
  [ -d "$REPO_DIR/dotfiles/.config/qtile" ] && link_dotfile ".config/qtile" "$HOME/.config/qtile"
  [ -d "$REPO_DIR/dotfiles/.config/picom" ] && link_dotfile ".config/picom" "$HOME/.config/picom"
  [ -d "$REPO_DIR/dotfiles/.config/alacritty" ] && link_dotfile ".config/alacritty" "$HOME/.config/alacritty"
  [ -f "$REPO_DIR/dotfiles/.zshrc" ] && link_dotfile ".zshrc" "$HOME/.zshrc"
  [ -f "$REPO_DIR/dotfiles/.gitconfig" ] && link_dotfile ".gitconfig" "$HOME/.gitconfig"
}

# === System tweaks and LightDM config ===
system_tweaks(){
  msg "Applying system tweaks"

  # Enable LightDM
  sudo systemctl enable lightdm || true

  # Configure greeter fallback
  if [ -f /etc/lightdm/lightdm-webkit2-greeter.conf ]; then
    msg "Using WebKit2 greeter"
    sudo sed -i 's/^#background_images =.*/background_images = \/usr\/share\/backgrounds/' /etc/lightdm/lightdm-webkit2-greeter.conf
  else
    msg "WebKit greeter not found, switching to GTK greeter"
    sudo pacman -S --needed --noconfirm lightdm-gtk-greeter
    sudo sed -i 's/^#greeter-session=.*/greeter-session=lightdm-gtk-greeter/' /etc/lightdm/lightdm.conf
  fi

  # Optional: change shell to zsh
  if command -v zsh >/dev/null 2>&1; then chsh -s "$(command -v zsh)" "$USER" || true; fi

  # Set keyboard layout to ES system-wide
  if command -v setxkbmap >/dev/null 2>&1; then setxkbmap es || true; fi
}

# === Main ===
main(){
  require_arch
  detect_vm
  install_native
  ensure_paru
  install_aur
  link_all
  system_tweaks
  msg "✅ Environment installation complete"
}

main "$@"
