#!/bin/bash

apt install -y git-core curl fonts-powerline zsh
chsh -s $(which zsh)

## Install Oh My Zsh and plugins
sh -c "$(curl -fsSL https://raw.githubusercontent.com/ohmyzsh/ohmyzsh/master/tools/install.sh)" "" --unattended
git clone https://github.com/zsh-users/zsh-autosuggestions.git ~/.oh-my-zsh/custom/plugins/zsh-autosuggestions

## Install Powerlevel10k
git clone --depth=1 https://github.com/romkatv/powerlevel10k.git ${ZSH_CUSTOM:-$HOME/.oh-my-zsh/custom}/themes/powerlevel10k

## sed -i 's/ZSH_THEME="[^"]*/ZSH_THEME="powerlevel10k\/powerlevel10k/g' .zshrc
wget https://raw.githubusercontent.com/projx/priv-host-scripts/main/zshrc_config -O ~/.zshrc