#!/bin/bash

# Vars
TEMP_DIR=$(mktemp -d) || { echo "Failed to create temp directory"; exit 1; }
YAY_URL="https://aur.archlinux.org/yay-git.git"
DOTFILES_URL="https://github.com/jorgeorc/dotfiles"

# function to install pacman packages
install_pacman_packages(){
  for package in "$@"; do
    if ! pacman -Q "$package" &>/dev/null; then
      echo "installing $package..."
      sudo pacman -S --noconfirm "$package"
    else
      echo "$package is already installed"
    fi
  done
}

# function to install yay packages
install_yay_packages() {
  for package in "$@"; do
    if ! yay -Q "$package" &>/dev/null; then
      echo "Installing $package..."
      yay -S --noconfirm "$package"
    else
      echo "$package is already installed"
    fi
  done
}

PACMAN_PACKAGES=(
  brightnessctl cbatticon diskie git gtk3 kitty libnotify network-manager-applet
  notification-daemon noto-fonts-emoji ntfs-3g pamixer pavucontrol picom pulse-audio
  python-psutil rofi scrot tree unzip volumeicon xclip xorg xorg-xinit yazi
  discord lxappearance neofetch neovim obsidian
  ttf-jetbrains-mono-nerd speech-dispatcher timer
)

install_pacman_packages "${PACMAN_PACKAGES[@]}"


# install yay
if ! pacman -Q "yay"; then
  git clone "$YAY_URL" "$TEMP_DIR/yay-git/" || { echo "Failed to clone repo"; exit 1; }
  cd "$TEMP_DIR/yay-git/" || { echo "Failed to enter directory"; exit 1; }
  makepkg -si || { echo "Build and install failed"; exit 1; }
else
  echo "yay is already installed"
fi

# install yay packages
install_yay_packages spotify lolcat

git clone "$DOTFILES_URL" "$TEMP_DIR/dotfiles" || {
  echo "Failed to clone dotfiles"
  exit 1
}

copy_config_dir() {
  local src_dir="$1"
  local dest_dir="$HOME/.config/$2"
  mkdir -p "$dest_dir"
  cp -r "$TEMP_DIR/dotfiles/.config/$2/"* "$dest_dir/"
}

for config in qtile rofi kitty neofetch; do
  copy_config_dir "$TEMP_DIR/dotfiles/.config/$config" "$config"
done

# Set zshrc
cp "$TEMP_DIR/dotfiles/.zshrc" "$HOME"

trap "rm -rf $TEMP_DIR" EXIT
