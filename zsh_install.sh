#!/bin/bash

echo "Installing ZSH and Oh My Zsh, setting as default shell"
echo "ZSH Installation: Install zsh and font deb packages"
apt install -y git-core curl fonts-powerline zsh


## Install Oh My Zsh and plugins
echo "Install ZSH: Oh My Zsh and plugins"
sh -c "$(curl -fsSL https://raw.githubusercontent.com/ohmyzsh/ohmyzsh/master/tools/install.sh)" "" --unattended
git clone https://github.com/zsh-users/zsh-autosuggestions.git $HOME/.oh-my-zsh/custom/plugins/zsh-autosuggestions

## Install Powerlevel10k
echo "ZSH Installation: Installing Powerlevel10k"
git clone --depth=1 https://github.com/romkatv/powerlevel10k.git ${ZSH_CUSTOM:-$HOME/.oh-my-zsh/custom}/themes/powerlevel10k

## Set the 10k theme...
# sed -i 's/ZSH_THEME="[^"]*/ZSH_THEME="powerlevel10k\/powerlevel10k/g' .zshrc

echo "ZSH Installation: Grabbing zshrc and p10k.zsh configuration files"
wget https://raw.githubusercontent.com/projx/priv-host-scripts/main/zsh/zshrc_config -O $HOME/.zshrc
wget https://raw.githubusercontent.com/projx/priv-host-scripts/main/zsh/p10k.zsh -O $HOME/.p10k.zsh

## Set the default shell
#chsh -s $(which zsh)
echo "exec " $(which zsh) >> $HOME/.bashrc

