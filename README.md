# Raspberry Pi OS Cloud-Init Injector

This project automates the injection of cloud-init configuration into Raspberry Pi OS Lite image files. It uses a sandboxed environment to mount and modify the image, making it simple to prepare images for cloud-init based initialization.

## Features

- **Automated Injection:** Render and inject cloud-init configuration files (`user-data` and `meta-data`) into the image.
- **Sandboxed Environment:** Uses loop devices and chroot to safely modify image files.
- **ARM64 Support:** Optionally configures QEMU for ARM64 emulation on non-ARM systems.
- **Extensible:** Easily customize the cloud-init configuration with extra scripts and templates.

## Prerequisites

- **Operating System:** Linux (with root privileges)
- **Utilities:**
  - `bash`
  - `git`
  - `sudo`
  - `losetup`
  - `fdisk`
  - `mount`
  - `chroot`
- **Optional (for ARM64 emulation):**  
  - `qemu-user-static` (specifically `qemu-aarch64-static`)

## Installation

Clone the repository along with its submodules:

```bash
git clone --recursive https://github.com/KubaTaba1uga/python_set_up_cloud_init_on_raspberry_pi_os_without_boot.git
```

## Usage

### 1. Configure Cloud-Init on an Image

The main entry point is the Python script `configure_cloud_init.py`. It renders a shell script from a template that injects the provided cloud-init configuration into the image. By default, it uses the templates in the `templates/` directory.

**Basic Command:**

```bash
sudo python3 configure_cloud_init.py /path/to/image.img
```

## Repository Structure

- **`configure_cloud_init.py`**  
  Main script to render and inject cloud-init configuration.

- **`sandbox/`**  
  Contains the sandbox script (`sandbox.sh`) and related submodule for mounting and chroot operations.

- **`templates/`**  
  Templates for:
  - `configure_cloud_init.sh`: The shell script template that applies the cloud-init configuration.
  - `user-data`: Default cloud-init user configuration.
  - `meta-data`: Default cloud-init meta-data.

- **Documentation:**  
  Additional details and troubleshooting tips can be found in `sandbox/docs/`.

## License

This project is licensed under the [MIT License](LICENSE).

## Author

[KubaTaba1uga](https://github.com/KubaTaba1uga/)

