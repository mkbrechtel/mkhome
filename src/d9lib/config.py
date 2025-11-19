"""Configuration management for d9 packages."""

import yaml
from pathlib import Path
from typing import Any, Optional


def load_config(package_name: str) -> dict:
    """
    Load central configuration from config.yaml.

    Args:
        package_name: Name of the d9 package (e.g., 'd9-tmux')

    Returns:
        Configuration dictionary
    """
    config_path = f'/usr/share/{package_name}/config.yaml'

    # Fall back to common config if package-specific doesn't exist
    if not Path(config_path).exists():
        config_path = '/usr/share/d9-common/config.yaml'

    try:
        with open(config_path) as f:
            return yaml.safe_load(f) or {}
    except FileNotFoundError:
        return {}


def get_config_value(config: dict, *keys: str, default: Any = None) -> Any:
    """
    Get a nested configuration value safely.

    Args:
        config: Configuration dictionary
        *keys: Path to the value (e.g., 'tmux', 'color_hue')
        default: Default value if key doesn't exist

    Returns:
        Configuration value or default

    Example:
        >>> config = {'tmux': {'color_hue': 210}}
        >>> get_config_value(config, 'tmux', 'color_hue', default=180)
        210
    """
    value = config
    for key in keys:
        if isinstance(value, dict):
            value = value.get(key)
        else:
            return default
    return value if value is not None else default
