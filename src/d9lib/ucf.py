"""UCF (Update Configuration File) utilities for d9 packages."""

import os
import subprocess
from typing import Optional


def ucf_install(source: str, destination: str, package: str) -> None:
    """
    Install a configuration file using UCF.

    UCF (Update Configuration File) manages configuration files that may
    be modified by users, similar to conffiles but for files outside /etc.

    Args:
        source: Path to the source file
        destination: Path where the file should be installed
        package: Package name (for tracking)

    Example:
        >>> ucf_install(
        ...     '/var/cache/d9-tmux/tmux.conf',
        ...     '/etc/tmux.conf',
        ...     'd9-tmux'
        ... )
    """
    subprocess.run(['ucf', '--debconf-ok', source, destination], check=True)
    subprocess.run(['ucfr', package, destination], check=True)


def ucf_remove(destination: str, package: str, purge: bool = False) -> None:
    """
    Remove a UCF-managed configuration file.

    Args:
        destination: Path to the configuration file
        package: Package name
        purge: If True, use --purge flag to remove the file

    Example:
        >>> ucf_remove('/etc/tmux.conf', 'd9-tmux', purge=True)
    """
    if purge:
        subprocess.run(['ucf', '--purge', destination], check=False)
        subprocess.run(['ucfr', '--purge', package, destination], check=False)
    else:
        subprocess.run(['ucfr', package, destination], check=False)
