#!/bin/bash

set -e

# Update package list
apt-get update

# Install cloud-init and netplan.io
apt-get install -y cloud-init netplan.io

# Uninstall network-manager
apt-get remove -y network-manager

# Ensure /boot directory exists
mkdir -p /boot

# Create user-data file
cat <<EOF > /boot/user-data
#cloud-config
users:
  - name: dummy
    sudo: ['ALL=(ALL) NOPASSWD:ALL']
    shell: /bin/bash
    lock_passwd: false
chpasswd:
  expire: false
  users:
  - {name: dummy, password: pass, type: text}
ssh_pwauth: false
EOF

# Create meta-data file
cat <<EOF > /boot/meta-data
instance-id: nocloud
local-hostname: rpi-ci
EOF

# Ensure cloud-init configuration directory exists
mkdir -p /etc/cloud/cloud.cfg.d/

# Create 99_nocloud.cfg file
cat <<EOF > /etc/cloud/cloud.cfg.d/99_nocloud.cfg
datasource_list: [ NoCloud, None ]
datasource:
  NoCloud:
    seedfrom: /boot/firmware
EOF

# Ensure cloud-init run after disks are mounted
systemctl enable cloud-init-local.service

# Disable userconfig.service
systemctl disable userconfig.service || echo "userconfig.service not found, skipping."

# Enable cloud-init
systemctl enable cloud-init

# Remove init=/usr/lib/raspberrypi-sys-mods/firstboot from /boot/cmdline.txt
sed -i 's|init=/usr/lib/raspberrypi-sys-mods/firstboot||g' /boot/cmdline.txt

echo "Setup completed successfully!"
