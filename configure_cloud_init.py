#!/usr/bin/env python3
import argparse
import os
import platform
import subprocess
import tempfile
from string import Template

ARCH = platform.machine()
CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))


def main():
    parser = argparse.ArgumentParser(description="Set up cloud-init on .img file.")
    parser.add_argument("img_file", help="Path to the image file.")

    parser.add_argument(
        "--user-data",
        default=os.path.join(CURRENT_DIR, "templates", "user-data"),
        help=(
            "Path to the file containing user-data content. "
            "If not provided, a default template will be used."
        ),
    )

    parser.add_argument(
        "--meta-data",
        default=os.path.join(CURRENT_DIR, "templates", "meta-data"),
        help=(
            "Path to the file containing meta-data content. "
            "If not provided, a default template will be used."
        ),
    )

    parser.add_argument(
        "--extra-script",
        default=None,
        help="Path to the script which will be additionally executed during cloud-init configuration.",
    )

    parser.add_argument(
        "--fs-label",
        default="bootfs",
        help="Value for the fs_label in cloud-init configuration. (default: bootfs)",
    )

    parser.add_argument(
        "--sandbox-script",
        default=os.path.join(CURRENT_DIR, "sandbox", "sandbox.sh"),
        help="Path to the sandbox.sh script file.",
    )

    args = parser.parse_args()

    try:
        with open(args.user_data, "r") as f:
            user_data = f.read()
    except Exception as e:
        print(f"Error reading user-data file: {e}")
        exit(1)

    try:
        with open(args.meta_data, "r") as f:
            meta_data = f.read()
    except Exception as e:
        print(f"Error reading meta-data file: {e}")
        exit(1)

    if args.extra_script:
        try:
            with open(args.extra_script, "r") as f:
                extra_script = f.read()
        except Exception as e:
            print(f"Error reading meta-data file: {e}")
            exit(1)
    else:
        extra_script = ""

    fs_label = args.fs_label

    # Read the shell script template
    script_dir = os.path.dirname(os.path.abspath(__file__))
    template_path = os.path.join(script_dir, "templates", "configure_cloud_init.sh")
    try:
        with open(template_path, "r") as file:
            template_content = file.read()
    except Exception as e:
        print(f"Error reading shell script template: {e}")
        exit(1)

    # Substitute the placeholders in the template using string.Template
    template = Template(template_content)
    rendered_script = template.substitute(
        USER_DATA_TEMPLATE=user_data,
        META_DATA_TEMPLATE=meta_data,
        FS_LABEL=fs_label,
        EXTRA_SCRIPT=extra_script,
    )

    # Create a temporary file to store the rendered script
    with tempfile.NamedTemporaryFile(delete=False, suffix=".sh") as temp_file:
        temp_file.write(rendered_script.encode("utf-8"))
        temp_path = temp_file.name

        print(f"Rendered script saved to {temp_path}")

    # Run the sandbox script with the required arguments
    command = (
        [
            "sudo",
            "bash",
            args.sandbox_script,
            args.img_file,
            "--script",
            temp_path,
        ],
    )

    if ARCH not in ["arm64", "aarch64"]:
        command.append("--arm64")

    try:
        subprocess.run(
            [
                "sudo",
                "bash",
                args.sandbox_script,
                args.img_file,
                "--script",
                temp_path,
            ],
            stdout=None,
            stderr=None,
            check=True,
        )
    except subprocess.CalledProcessError as e:
        print(f"Error executing sandbox script: {e}")
        exit(1)
    finally:
        # Delete the temporary file once the subprocess is done
        os.remove(temp_path)


if __name__ == "__main__":
    main()
