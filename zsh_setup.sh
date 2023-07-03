#!/bin/bash

chsh -s $(which zsh)

## Install Oh My Zsh and plugins
sh -c "$(curl -fsSL https://raw.githubusercontent.com/ohmyzsh/ohmyzsh/master/tools/install.sh)" "" --unattended
git clone https://github.com/zsh-users/zsh-autosuggestions.git ~/.oh-my-zsh/custom/plugins/zsh-autosuggestions

## Install Powerlevel10k
git clone --depth=1 https://github.com/romkatv/powerlevel10k.git ${ZSH_CUSTOM:-$HOME/.oh-my-zsh/custom}/themes/powerlevel10k

sed -i 's/ZSH_THEME="[^"]*/ZSH_THEME="powerlevel10k\/powerlevel10k/g' .zshrc
wget https://raw.githubusercontent.com/projx/priv-host-scripts/main/zshrc_config -O ~/.zshrc

#Powerlevel10k configuration wizard has been aborted. It will run again next time unless
#you define at least one Powerlevel10k configuration option. To define an option that
#does nothing except for disabling Powerlevel10k configuration wizard, type the following
#command:
#
#  echo 'POWERLEVEL9K_DISABLE_CONFIGURATION_WIZARD=true' >>! ~/.zshrc
#
#To run Powerlevel10k configuration wizard right now, type:
#
#  p10k configure