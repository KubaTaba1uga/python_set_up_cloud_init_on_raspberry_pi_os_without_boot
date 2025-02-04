#!/bin/bash
set -exu pipeline

# Update package list
apt-get update

# Install cloud-init and netplan.io
apt-get install -y cloud-init netplan.io

# Uninstall network-manager
apt-get remove -y network-manager

# Ensure /boot directory exists
mkdir -p /boot

# Create user-data file using template variable
cat <<EOF > /boot/user-data
$USER_DATA_TEMPLATE
EOF

# Create meta-data file using template variable
cat <<EOF > /boot/meta-data
$META_DATA_TEMPLATE
EOF

# Ensure cloud-init configuration directory exists
mkdir -p /etc/cloud/cloud.cfg.d/

# Create 99_nocloud.cfg file using fs_label variable
cat <<EOF > /etc/cloud/cloud.cfg.d/99_nocloud.cfg
datasource_list: [ NoCloud, None ]
datasource:
  NoCloud:
    fs_label: $FS_LABEL
EOF

# Ensure cloud-init runs after disks are mounted
systemctl enable cloud-init-local.service

# Disable userconfig.service (if present)
systemctl disable userconfig.service || echo "userconfig.service not found, skipping."

# Ensure we log into tty
systemctl set-default multi-user.target
systemctl enable getty@tty1.service

# Enable cloud-init
systemctl enable cloud-init

# Remove init=/usr/lib/raspberrypi-sys-mods/firstboot from /boot/cmdline.txt
sed -i 's|init=/usr/lib/raspberrypi-sys-mods/firstboot||g' /boot/cmdline.txt

$EXTRA_SCRIPT

echo "Setup completed successfully!"

