#!/usr/bin/env bash
set -euo pipefail

REPO_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

msg(){ printf "\n\033[1;32m==>\033[0m %s\n" "$*"; }
warn(){ printf "\n\033[1;33m!!\033[0m %s\n" "$*"; }

require_arch(){
  command -v pacman >/dev/null || { echo "This installer requires Arch (pacman)."; exit 1; }
}

detect_environment(){
  # Detect if we are running inside a virtual machine
  if systemd-detect-virt --quiet; then
    IS_VM=1
  else
    IS_VM=0
  fi
  export DOTFILES_IS_VM="$IS_VM"

  # Persist a simple env file other components can read (e.g. Qtile)
  mkdir -p "$HOME/.config/dotfiles"
  printf "IS_VM=%s\n" "$IS_VM" > "$HOME/.config/dotfiles/env"
  msg "Environment detected: IS_VM=${IS_VM}"
}

install_native(){
  local list="$REPO_DIR/packages-native.txt"
  [ -s "$list" ] || { msg "No native packages to install."; return 0; }
  msg "Installing native packages (pacman)"
  sudo pacman -Syu --noconfirm
  # shellcheck disable=SC2046
  sudo pacman -S --needed --noconfirm $(grep -v '^\s*#' "$list" | tr '\n' ' ') || true
}

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

install_aur(){
  local list="$REPO_DIR/packages-aur.txt"
  [ -s "$list" ] || { msg "No AUR packages to install."; return 0; }
  msg "Installing AUR packages (paru)"
  # shellcheck disable=SC2046
  paru -S --needed --noconfirm --skipreview $(grep -v '^\s*#' "$list" | tr '\n' ' ') || true
}

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
  # Qtile / Picom
  [ -d "$REPO_DIR/dotfiles/.config/qtile" ] && link_dotfile ".config/qtile" "$HOME/.config/qtile"
  [ -d "$REPO_DIR/dotfiles/.config/picom" ] && link_dotfile ".config/picom" "$HOME/.config/picom"
  # Terminal + Rofi
  [ -d "$REPO_DIR/dotfiles/.config/alacritty" ] && link_dotfile ".config/alacritty" "$HOME/.config/alacritty"
  [ -d "$REPO_DIR/dotfiles/.config/rofi" ] && link_dotfile ".config/rofi" "$HOME/.config/rofi"
  # Common extras
  [ -f "$REPO_DIR/dotfiles/.zshrc" ] && link_dotfile ".zshrc" "$HOME/.zshrc"
  [ -f "$REPO_DIR/dotfiles/.gitconfig" ] && link_dotfile ".gitconfig" "$HOME/.gitconfig"
  [ -d "$REPO_DIR/dotfiles/.config/nvim" ] && link_dotfile ".config/nvim" "$HOME/.config/nvim"
}

apply_system_files(){
  # Apply system config files (if you track any in repo/system/*)
  if [ -f "$REPO_DIR/system/lightdm-gtk-greeter.conf" ]; then
    msg "Applying LightDM GTK greeter config"
    sudo install -Dm644 "$REPO_DIR/system/lightdm-gtk-greeter.conf" /etc/lightdm/lightdm-gtk-greeter.conf
  fi
}

system_tweaks(){
  msg "System tweaks / services"
  # Enable LightDM login manager
  sudo systemctl enable lightdm || true

  # Optional: set default shell to zsh if available
  if command -v zsh >/dev/null 2>&1; then chsh -s "$(command -v zsh)" "$USER" || true; fi

  # Ensure X11 keyboard layout (system-wide you already set localectl)
  if command -v setxkbmap >/dev/null 2>&1; then setxkbmap es || true; fi
}

main(){
  require_arch
  detect_environment
  install_native
  ensure_paru
  install_aur
  link_all
  apply_system_files
  system_tweaks
  msg "✅ Environment installation complete"
}
main "$@"
