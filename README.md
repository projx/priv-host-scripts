# Bootstrap Scripts

Nothing top secret here, just a backup of my Gitlab repo I use to bootstrap a couple of VMs in my homelab.

## Base
Base server setup, such as package install, disable IPv6 etc

wget https://raw.githubusercontent.com/projx/priv-host-scripts/main/gfs_setup.sh -O - | sh
wget https://raw.githubusercontent.com/projx/priv-host-scripts/main/kube_setup.sh -O - | sh

## DNS
Add GFS entries to the hosts file 

wget https://raw.githubusercontent.com/projx/priv-host-scripts/main/host_setup.py -O - | python3

