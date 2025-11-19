we went the pure-mkosi path. this has limitations though. i thought a lot on how to go about this, the new way is the debian pure blend way. this enables us to define our package dependencies in debian meta packages and apply the configuration through debconf. we can use each mkosi config file with Packages= directives as the base of such a metapackage. but let's first setup a basic debian package build system in our repo

## Design: Debian Pure Blend Build System

### Overview

The build system will transform our mkosi-based configuration into proper Debian metapackages. Each mkosi.conf.d/*.conf becomes a metapackage with:
- Package dependencies from the conf file
- Configuration management via debconf + templates
- Ansible-style file organization (templates/ and files/ directories)

### Directory Structure

```
d9/                              # This repo
├── tasks/
│   ├── editor                   # Task file (RFC822 format)
│   ├── desktop-xfce
│   ├── network
│   └── base
├── files/
│   ├── editor/
│   │   └── etc/
│   │       └── vim/
│   │           └── vimrc.local
│   └── desktop-xfce/
│       └── etc/
│           ├── lightdm/
│           │   └── lightdm.conf
│           └── systemd/
│               └── system-preset/
│                   └── 90-d9-desktop.preset
├── templates/
│   └── desktop-xfce/
│       └── etc/
│           └── xdg/
│               └── xfce4/
│                   └── xfconf/
│                       └── xfce-perchannel-xml/
│                           └── xfce4-panel.xml.j2
├── config.yaml                  # Central configuration (feeds templates)
├── debian/                      # Standard Debian packaging
│   ├── control
│   ├── rules
│   └── ...
├── mkosi.conf                   # mkosi config (uses local repo)
└── README.md
```

Structure follows Debian Pure Blends conventions:
- `tasks/` - task files in RFC822 format (like debian/control)
- `files/` - static configs organized by task name
- `templates/` - Jinja2 templates organized by task name

### Task Structure
 
Each task consists of three components:

#### 1. Task File (RFC822 format)

```
Task: Editor
Description: Text editors for d9
 A comprehensive collection of text editors including nano, micro,
 neovim, and vim with GTK support.

Depends: nano

Depends: micro

Depends: neovim
```

Task files use RFC822 format (like debian/control):
- `Task:` - task name (becomes metapackage d9-editor)
- `Description:` - short and long description
- `Depends:` - packages to install
- `Recommends:` - recommended packages
- `Suggests:` - optional packages

Additional fields supported:
- `X-Begin-Category:` / `X-End-Category:` - group related packages
- `Why:` - explain package inclusion
- `Homepage:`, `License:`, `Pkg-Description:` - for prospective packages

#### 2. Static Files (optional)

```
files/editor/
└── etc/
    └── vim/
        └── vimrc.local
```

Files in `files/<task-name>/` are copied verbatim to their target locations.

#### 3. Templates (optional)

```
templates/desktop-xfce/
└── etc/
    └── xdg/
        └── xfce4/
            └── xfconf/
                └── xfce-perchannel-xml/
                    └── xfce4-panel.xml.j2
```

Templates in `templates/<task-name>/` are rendered using debconf values during package installation. This allows users to configure the system during package installation using standard Debian configuration tools.

### Build System

The build system will:
- Read task definitions from `tasks/`
- Generate `debian/control` from task files (using blends-dev or custom tool)
- Package static files from `files/<task-name>/`
- Package templates from `templates/<task-name>/` to be rendered during installation via debconf
- Generate .deb metapackages (d9-editor, d9-desktop-xfce, etc.)
- Create a local APT repository

Implementation details to be determined.

### Configuration System: Python Scripts + debconf + UCF

Instead of shell scripts, use Python for all configuration management:

#### debian/config (Python)

```python
#!/usr/bin/python3
"""debconf configuration script for d9-desktop-xfce."""

from debconf import Debconf

db = Debconf()

# Ask questions
db.input('medium', 'd9-desktop-xfce/panel-position')
db.input('low', 'd9-desktop-xfce/enable-compositing')
db.go()
```

#### debian/postinst (Python)

```python
#!/usr/bin/python3
"""Post-installation script for d9-desktop-xfce."""

import sys
import os
from pathlib import Path
from jinja2 import Template
from debconf import Debconf

def render_template(template_path, output_path, **variables):
    """Render Jinja2 template with variables."""
    with open(template_path) as f:
        template = Template(f.read())

    rendered = template.render(**variables)

    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    with open(output_path, 'w') as f:
        f.write(rendered)

def ucf_install(source, destination, package):
    """Install file using UCF."""
    os.system(f'ucf --debconf-ok "{source}" "{destination}"')
    os.system(f'ucfr "{package}" "{destination}"')

def main():
    if len(sys.argv) < 2:
        sys.exit(0)

    action = sys.argv[1]

    if action != 'configure':
        return

    # Get debconf values
    db = Debconf()
    panel_position = db.get('d9-desktop-xfce/panel-position')
    enable_compositing = db.get('d9-desktop-xfce/enable-compositing')

    # Render templates
    render_template(
        '/usr/share/d9-desktop-xfce/templates/xfce4-panel.xml.j2',
        '/var/cache/d9-desktop-xfce/xfce4-panel.xml',
        panel_position=panel_position,
        enable_compositing=enable_compositing
    )

    # Install with UCF
    ucf_install(
        '/var/cache/d9-desktop-xfce/xfce4-panel.xml',
        '/etc/xdg/xfce4/xfconf/xfce-perchannel-xml/xfce4-panel.xml',
        'd9-desktop-xfce'
    )

if __name__ == '__main__':
    main()
```

#### Benefits

✅ **Pure Python**: No shell scripting, easier to read and maintain
✅ **Jinja2 built-in**: Template rendering directly in postinst
✅ **debconf-python**: Native Python bindings for debconf
✅ **UCF integration**: Call ucf from Python
✅ **Debian Policy Compliant**: UCF prevents conffile conflicts
✅ **Reconfigurable**: `dpkg-reconfigure` works automatically

### Integration with mkosi

Once built, packages will be available via local APT repository for mkosi to consume.

### Migration Path

1. Create `tasks/` directory
2. Convert existing mkosi.images/*/mkosi.conf.d/*.conf to RFC822 task files
3. Organize files/ and templates/ by task name
4. Implement build system (blends-dev or custom)
5. Test .deb generation
6. Integrate with mkosi via local APT repository

### Advantages

✅ **Standard Debian Pure Blends format**: Uses established RFC822 task file format
✅ **Compatible with blends-dev**: Can use standard Debian tooling
✅ **Upstream potential**: Follows Debian guidelines for potential upstreaming
✅ **Dependency management**: Proper Depends/Recommends/Suggests
✅ **User configuration**: Debconf integration for installation choices and template rendering
✅ **Reconfigurable**: Users can change settings with `dpkg-reconfigure`
✅ **Preseedable**: Non-interactive installation with preseed files
✅ **Upgradability**: Standard `apt upgrade` workflow
✅ **Modularity**: Users can install specific metapackages
✅ **Documentation**: Why/Remark/Comment fields explain package choices
✅ **Categories**: Organize packages into logical groups

### Example: Shell Task with tmux Configuration

**tasks/shell:**
```
Task: Shell
Description: Shell environment for d9
 Essential shell tools and terminal multiplexer with
 user-configurable color schemes.

Depends: bash

Depends: tmux

Depends: zsh

Recommends: fzf

Recommends: ripgrep
```

**templates/shell/etc/tmux.conf.j2:**
```
# tmux configuration
set -g default-terminal "screen-256color"

# Status bar colors (configurable via debconf)
set -g status-style bg={{tmux_status_bg}},fg={{tmux_status_fg}}

# Active window colors
setw -g window-status-current-style bg={{tmux_active_bg}},fg={{tmux_active_fg}}

# Pane border colors
set -g pane-border-style fg={{tmux_border_color}}
set -g pane-active-border-style fg={{tmux_active_border_color}}
```

**debian/templates:**
```
Template: d9-shell/tmux-status-bg
Type: select
Choices: black, red, green, yellow, blue, magenta, cyan, white
Default: blue
Description: tmux status bar background color
 Choose the background color for the tmux status bar.

Template: d9-shell/tmux-status-fg
Type: select
Choices: black, red, green, yellow, blue, magenta, cyan, white
Default: white
Description: tmux status bar foreground color
 Choose the text color for the tmux status bar.

Template: d9-shell/tmux-active-bg
Type: select
Choices: black, red, green, yellow, blue, magenta, cyan, white
Default: green
Description: tmux active window background color
 Choose the background color for the active window in tmux.
```

**debian/postinst (Python):**
```python
#!/usr/bin/python3
import sys
import os
from jinja2 import Template
from debconf import Debconf

def render_template(template_path, output_path, **variables):
    with open(template_path) as f:
        template = Template(f.read())

    rendered = template.render(**variables)

    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    with open(output_path, 'w') as f:
        f.write(rendered)

def ucf_install(source, destination, package):
    os.system(f'ucf --debconf-ok "{source}" "{destination}"')
    os.system(f'ucfr "{package}" "{destination}"')

if len(sys.argv) > 1 and sys.argv[1] == 'configure':
    db = Debconf()

    # Get tmux color preferences
    tmux_status_bg = db.get('d9-shell/tmux-status-bg')
    tmux_status_fg = db.get('d9-shell/tmux-status-fg')
    tmux_active_bg = db.get('d9-shell/tmux-active-bg')

    # Render tmux config
    render_template(
        '/usr/share/d9-shell/templates/tmux.conf.j2',
        '/var/cache/d9-shell/tmux.conf',
        tmux_status_bg=tmux_status_bg,
        tmux_status_fg=tmux_status_fg,
        tmux_active_bg=tmux_active_bg,
        tmux_active_fg='white',
        tmux_border_color='blue',
        tmux_active_border_color='green'
    )

    # Install with UCF
    ucf_install(
        '/var/cache/d9-shell/tmux.conf',
        '/etc/tmux.conf',
        'd9-shell'
    )
```

The metapackage d9-shell will be generated from this task. When users install it, they'll be asked about their preferred tmux colors.

### Next Steps

1. Create `tasks/` directory in d9 repo
2. Create first task file (base) as proof of concept
3. Set up files/ and templates/ directories
4. Implement build system (evaluate blends-dev vs custom)
5. Test .deb generation and installation
