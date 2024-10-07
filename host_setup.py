#!/usr/bin/env python3

import argparse
import subprocess
import re
import shutil
import os

def backup_file(file_path):
    backup_path = f"{file_path}.bak"
    shutil.copy(file_path, backup_path)
    print(f"Backup created: {backup_path}")

def restore_file(file_path):
    backup_path = f"{file_path}.bak"
    if os.path.exists(backup_path):
        shutil.copy(backup_path, file_path)
        print(f"Restored from backup: {backup_path}")
    else:
        print(f"No backup found for {file_path}")

def set_hostname(hostname, apply_changes):
    try:
        subprocess.run(['sudo', 'hostnamectl', 'set-hostname', hostname], check=True)
        print(f"Hostname set to {hostname}")
        if apply_changes:
            subprocess.run(['sudo', 'systemctl', 'restart', 'systemd-hostnamed'], check=True)
            print("Hostname service restarted")
    except subprocess.CalledProcessError as e:
        print(f"Failed to set hostname: {e}")

def set_ips(octet, apply_changes):
    lan_ip = f"10.10.40.{octet}"
    storage_ip = f"10.10.110.{octet}"
    netplan_file = '/etc/netplan/50-cloud-init.yaml'

    try:
        backup_file(netplan_file)

        with open(netplan_file, 'r') as file:
            netplan_config = file.read()

        if '10.10.40.80' in netplan_config and '10.10.110.80' in netplan_config:
            netplan_config = re.sub(r'addresses:\n\s*- 10\.10\.40\.80\b', f'addresses:\n            - {lan_ip}', netplan_config)
            netplan_config = re.sub(r'addresses:\n\s*- 10\.10\.110\.80\b', f'addresses:\n            - {storage_ip}', netplan_config)

            with open(netplan_file, 'w') as file:
                file.write(netplan_config)

            if apply_changes:
                subprocess.run(['sudo', 'netplan', 'apply'], check=True)
                print(f"LAN IP set to {lan_ip} and Storage IP set to {storage_ip}")
        else:
            print("Required IPs not found in the configuration file.")
    except Exception as e:
        print(f"Failed to set IPs: {e}")

def main():
    parser = argparse.ArgumentParser(description='Setup host configuration')
    parser.add_argument('-n', '--hostname', type=str, help='Set the hostname')
    parser.add_argument('-i', '--ip-octet', type=int, help='Set the IP octet for LAN and Storage NICs')
    parser.add_argument('-r', '--rollback', action='store_true', help='Rollback to the backup files')
    parser.add_argument('-y', '--apply', action='store_true', help='Apply changes and restart services')

    args = parser.parse_args()

    if args.rollback:
        restore_file('/etc/netplan/50-cloud-init.yaml')
    else:
        if args.hostname:
            set_hostname(args.hostname, args.apply)
        if args.ip_octet:
            set_ips(args.ip_octet, args.apply)

if __name__ == "__main__":
    main()