#!/bin/bash

# Check if the script is run with root privileges
if [ "$EUID" -ne 0 ]; then
  echo "Please run this script as root."
  exit 1
fi

# Disable systemd-resolved
systemctl stop systemd-resolved
systemctl disable systemd-resolved

# Remove the /etc/resolv.conf symlink
rm -f /etc/resolv.conf

# Create a new /etc/resolv.conf with Cloudflare's DNS servers
cat <<EOL > /etc/resolv.conf
# adguard DNS servers
nameserver 10.10.50.111
nameserver 10.10.50.111
EOL

# Restart the network manager to apply the changes
systemctl restart NetworkManager

echo "systemd-resolved disabled and /etc/resolv.conf configured with Cloudflare DNS."