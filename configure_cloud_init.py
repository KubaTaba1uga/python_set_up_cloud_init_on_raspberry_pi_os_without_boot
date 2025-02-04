#!/usr/bin/env python3
import os
import argparse
import tempfile
import subprocess
from string import Template

def main():
    parser = argparse.ArgumentParser(
        description="Render cloud-init shell script with custom user-data, meta-data, and fs_label."
    )
    parser.add_argument(
        "--user-data",
        default="templates/user-data",
        help=("Path to the file containing user-data content. "
              "If not provided, a default template will be used.")
    )
    parser.add_argument(
        "--meta-data",
        default="templates/meta-data",
        help=("Path to the file containing meta-data content. "
              "If not provided, a default template will be used.")
    )
    parser.add_argument(
        "--fs-label",
        default="bootfs",
        help="Value for the fs_label in cloud-init configuration. (default: bootfs)"
    )
    parser.add_argument(
        "--sandbox-script",
        required=True,
        help="Path to the sandbox.sh script file."
    )
    parser.add_argument(
        "--img-file",
        required=True,
        help="Path to the image file."
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
        EXTRA_SCRIPT=""
    )

    # Create a temporary file to store the rendered script
    with tempfile.NamedTemporaryFile(delete=False, suffix=".sh") as temp_file:
        temp_file.write(rendered_script.encode("utf-8"))
        temp_path = temp_file.name

    print(f"Rendered script saved to {temp_path}")

    # Run the sandbox script with the required arguments
    try:
        subprocess.run([
            "sudo", "bash", args.sandbox_script, args.img_file, "--arm64", "--script", temp_path
        ], stdout=None, stderr=None, check=True)
    except subprocess.CalledProcessError as e:
        print(f"Error executing sandbox script: {e}")
        exit(1)

if __name__ == "__main__":
    main()



