"""Color scheme generation utilities for d9 packages."""

import colorsys
from typing import Tuple, Dict


def hsl_to_rgb(h: float, s: float, l: float) -> Tuple[int, int, int]:
    """
    Convert HSL to RGB.

    Args:
        h: Hue (0-360)
        s: Saturation (0.0-1.0)
        l: Lightness (0.0-1.0)

    Returns:
        Tuple of (r, g, b) values in 0-255 range

    Example:
        >>> hsl_to_rgb(210, 0.6, 0.3)
        (30, 76, 122)
    """
    r, g, b = colorsys.hls_to_rgb(h / 360.0, l, s)
    return int(r * 255), int(g * 255), int(b * 255)


def rgb_to_hex(r: int, g: int, b: int) -> str:
    """
    Convert RGB to hex color.

    Args:
        r: Red value (0-255)
        g: Green value (0-255)
        b: Blue value (0-255)

    Returns:
        Hex color string (e.g., '#0066cc')

    Example:
        >>> rgb_to_hex(0, 102, 204)
        '#0066cc'
    """
    return f"#{r:02x}{g:02x}{b:02x}"


def generate_color_scheme(hue: int) -> Dict[str, any]:
    """
    Generate a harmonious color scheme from a hue value.

    This generates a complete color scheme suitable for terminal
    applications, with appropriate contrast and visual hierarchy.

    Args:
        hue: HSL hue value (0-360)

    Returns:
        Dictionary with color values:
        - hue: Original hue value
        - status_bg: Status bar background
        - status_fg: Status bar foreground
        - active_bg: Active element background
        - active_fg: Active element foreground
        - border_color: Inactive border color
        - active_border_color: Active border color

    Example:
        >>> colors = generate_color_scheme(210)
        >>> colors['status_bg']
        '#1e4d7a'
    """
    # Status bar: medium saturation, medium-dark
    status_bg = rgb_to_hex(*hsl_to_rgb(hue, 0.6, 0.3))
    status_fg = rgb_to_hex(*hsl_to_rgb(hue, 0.2, 0.95))

    # Active window: high saturation, medium
    active_bg = rgb_to_hex(*hsl_to_rgb(hue, 0.8, 0.4))
    active_fg = rgb_to_hex(*hsl_to_rgb(hue, 0.1, 0.98))

    # Borders: medium saturation, medium-light
    border_color = rgb_to_hex(*hsl_to_rgb(hue, 0.4, 0.5))
    active_border_color = rgb_to_hex(*hsl_to_rgb(hue, 0.7, 0.6))

    return {
        'hue': hue,
        'status_bg': status_bg,
        'status_fg': status_fg,
        'active_bg': active_bg,
        'active_fg': active_fg,
        'border_color': border_color,
        'active_border_color': active_border_color,
    }
