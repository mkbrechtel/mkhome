#!/usr/bin/env python3
"""
mkosi configure script to dynamically add packages from all roles' apt.txt files.
This script reads the mkosi configuration as JSON from stdin, discovers all
apt.txt files in the roles directory, and adds their packages to the configuration.
"""

import json
import sys
from pathlib import Path


def read_apt_txt(file_path: Path) -> list[str]:
    """Read an apt.txt file and return a list of packages, filtering comments and blank lines."""
    packages = []
    with open(file_path, 'r') as f:
        for line in f:
            # Remove comments and whitespace
            line = line.split('#')[0].strip()
            if line:
                packages.append(line)
    return packages


def main():
    # Read the current mkosi configuration from stdin
    config = json.load(sys.stdin)

    # Find the script's directory using SRCDIR environment variable
    # mkosi sets $SRCDIR to the directory mkosi was invoked from
    import os
    srcdir = os.getenv('SRCDIR', Path(__file__).parent.resolve())
    roles_dir = Path(srcdir) / 'roles'

    # Find all apt.txt files in the roles directory
    apt_txt_files = list(roles_dir.glob('*/apt.txt'))

    # Collect all packages from apt.txt files
    all_packages = []
    for apt_txt in apt_txt_files:
        packages = read_apt_txt(apt_txt)
        all_packages.extend(packages)

    # Remove duplicates and sort
    all_packages = sorted(set(all_packages))

    # Get existing packages from config (if any)
    existing_packages = config.get('Packages', [])
    if isinstance(existing_packages, str):
        existing_packages = [pkg.strip() for pkg in existing_packages.split() if pkg.strip()]
    elif existing_packages is None:
        existing_packages = []

    # Combine and deduplicate
    combined_packages = sorted(set(existing_packages + all_packages))

    # Update the configuration
    config['Packages'] = combined_packages

    # Output the modified configuration as JSON to stdout
    json.dump(config, sys.stdout, indent=2)


if __name__ == '__main__':
    main()
