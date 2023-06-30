#!/bin/bash

add-apt-repository -y ppa:gluster/glusterfs-11
apt update
apt install -y glusterfs-server nfs-common inetutils-traceroute net-tools lynx open-vm-tools git python3 duperemove
sleep 5

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
## Create the GFS volume
mkdir -p /store/gfs/
mkdir -p /store/local/
mkdir -p /store/nas/