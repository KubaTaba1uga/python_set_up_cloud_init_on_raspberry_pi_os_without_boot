# Raspberry OS Cloud Init

This repository provides an automated method to configure cloud-init for Raspberry Pi OS Lite images.

## Prerequisites
Ensure you have the following installed on your system:
- `bash`
- `sudo` privileges
- `git`

## Installation and Usage

1. Clone the required repositories:
   ```sh
   git clone https://github.com/KubaTaba1uga/bash_modify_img_file_without_boot/
   git clone https://github.com/KubaTaba1uga/raspberry_os_lite_cloud_init
   ```

2. Run the configuration script using `sandbox.sh`:
   ```sh
   sudo bash bash_modify_img_file_without_boot/sandbox.sh --arm64 --script raspberry_os_lite_cloud_init/configure_cloud_init.sh
   ```

## Description
This process modifies a Raspberry Pi OS Lite image by injecting the cloud-init configuration using a sandboxed environment. The script applies the necessary changes to enable cloud-init on the system.

## Notes
- By default, `configure_cloud_init.sh` applies an unsecure and dummy configuration, creating a user called `dummy` with the password set to `pass`. Ensure to modify this configuration before deployment.
- Ensure the script is executed with `sudo` permissions.
- This script is designed for ARM64 architecture (`--arm64` flag). Modify as needed for other architectures.
- Once your `.img` file is modified, you can run `sandbox.sh` again to modify `user-data` or `meta-data` as needed.

## License
This project is open-source under the MIT License.

## Author
[KubaTaba1uga](https://github.com/KubaTaba1uga/)


