#!/bin/bash

# add-apt-repository -y ppa:gluster/glusterfs-11
# add-apt-repository -y ppa:gluster/glusterfs-10
apt update
apt install -y glusterfs-server inetutils-traceroute net-tools lynx glusterfs-server open-vm-tools git python3 duperemove
sleep 5

######################################
## Enable Gluster and fire it up!
sudo systemctl start glusterd
sudo systemctl enable glusterd

######################################
## Disable IPv6
sed -ie 's/GRUB_CMDLINE_LINUX=.*/GRUB_CMDLINE_LINUX="net.ifnames=0 ipv6.disable=1 biosdevname=0"/' /target/etc/default/grub
update-grub2

######################################
## Disable Swap, and remove from fstab
sudo swapoff -a
sed -e '/swap/ s/^#*/#/' -i /etc/fstab

######################################
## Disable firewall
ufw disable

######################################
## Enable deduplication
crontab -l | { cat; echo "* */6 * * * /usr/bin/duperemove -dr /gfs/ >/dev/null 2>&1"; } | crontab -

######################################
## Create the GFS volumes
mkdir -p /gfs/kube-svr
mkdir -p /gfs/kube-mgr