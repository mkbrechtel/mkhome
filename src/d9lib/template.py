"""Template rendering utilities for d9 packages."""

import os
from pathlib import Path
from jinja2 import Template


def render_template(template_path: str, output_path: str, **variables) -> None:
    """
    Render a Jinja2 template with variables.

    Args:
        template_path: Path to the Jinja2 template file
        output_path: Path where the rendered file should be written
        **variables: Variables to pass to the template

    Example:
        >>> render_template(
        ...     '/usr/share/d9-tmux/templates/etc/tmux.conf.j2',
        ...     '/var/cache/d9-tmux/tmux.conf',
        ...     hue=210,
        ...     status_bg='#0000ff'
        ... )
    """
    with open(template_path) as f:
        template = Template(f.read())

    rendered = template.render(**variables)

    # Ensure parent directory exists
    os.makedirs(os.path.dirname(output_path), exist_ok=True)

    with open(output_path, 'w') as f:
        f.write(rendered)
