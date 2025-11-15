# d9 Development Guidelines

## Architecture Overview

d9 is a pure mkosi-based Debian system with declarative configuration. All package management and system configuration is handled through mkosi configuration files and build scripts.

## Directory Structure

```
d9/
├── mkosi.conf                    # Main mkosi configuration
├── mkosi.build                   # Template rendering build script
├── mkosi.conf.d/                 # Package configuration (one file per role)
│   ├── firefox.conf             # Firefox packages
│   ├── kitty.conf               # Kitty terminal packages
│   ├── xfce.conf                # Xfce desktop packages
│   └── ...                      # One conf file per logical role
├── mkosi.postinst.d/            # Post-install scripts
│   ├── system-config.sh         # System configuration (alternatives, dconf)
│   └── locales.sh               # Locale generation
├── mkosi.repart/                # Partition definitions
│   ├── 00-esp.conf              # EFI System Partition
│   └── 20-root.conf             # Root partition (EROFS)
├── mkosi.images/                # Image definitions
│   ├── base/                    # Base system image
│   ├── initrd/                  # Initramfs image
│   └── rescue/                  # Rescue system image
├── mkosi.files/                 # Static file overlays
│   ├── etc/                     # System configuration files
│   │   ├── xdg/                # XDG base directory configs
│   │   ├── lightdm/            # Display manager config
│   │   ├── dconf/              # dconf databases
│   │   └── systemd/            # systemd configuration
│   ├── opt/                     # Optional software
│   │   └── backgrounds/        # Desktop backgrounds
│   └── usr/                     # User utilities
│       ├── local/bin/          # Local scripts
│       └── share/              # Shared data
├── src/                         # Source files for build
│   ├── d9.yaml                  # Central configuration file
│   └── templates/               # Jinja2 templates
│       ├── kitty.conf.j2
│       ├── lightdm.conf.j2
│       ├── xfce4-panel.xml.j2
│       └── ...
└── roles/                       # [DEPRECATED] Old Ansible roles
```

## Configuration Management

### Package Management

Packages are declaratively defined in `mkosi.conf.d/*.conf` files. Each file corresponds to a logical role or component:

**Example**: `mkosi.conf.d/firefox.conf`
```ini
[Content]
Packages=firefox-esr firefox-esr-l10n-de webext-ublock-origin-firefox
```

All packages are automatically installed by mkosi during the image build process.

### Configuration Files

Configuration is managed through two mechanisms:

#### 1. Static Files

Static configuration files are placed in `mkosi.files/` and copied verbatim during the build:

```
mkosi.files/etc/pam.d/lightdm          → /etc/pam.d/lightdm
mkosi.files/etc/dconf/profile/user     → /etc/dconf/profile/user
mkosi.files/usr/local/bin/in2qr        → /usr/local/bin/in2qr
```

#### 2. Template Rendering

Dynamic configuration files use Jinja2 templates that are rendered during the build using `mkosi.build`:

**Configuration**: `src/d9.yaml`
```yaml
kitty:
  font_family: "Hack"
  font_size: 12
```

**Template**: `src/templates/kitty.conf.j2`
```jinja2
font_family {{font_family}}
font_size {{font_size}}
```

**Rendered output**: `mkosi.files/etc/xdg/kitty/kitty.conf`
```
font_family Hack
font_size 12
```

The `mkosi.build` script automatically renders all templates before the mkosi build starts.

### Build Process

The build process follows these steps:

1. **Template Rendering** (`mkosi.build`):
   - Loads configuration from `src/d9.yaml`
   - Renders all Jinja2 templates from `src/templates/`
   - Outputs rendered files to `mkosi.files/etc/`

2. **mkosi Build**:
   - Installs all packages from `mkosi.conf.d/*.conf` files
   - Copies files from `mkosi.files/` to the image
   - Executes `mkosi.postinst.d/` scripts

3. **Post-Install** (`mkosi.postinst.d/system-config.sh`):
   - Updates dconf databases
   - Configures update-alternatives
   - Enables systemd services (via presets)

## Adding New Functionality

### Adding a New Component

To add a new component or application:

1. **Create package configuration** in `mkosi.conf.d/`:
   ```bash
   # mkosi.conf.d/myapp.conf
   [Content]
   Packages=myapp myapp-plugins
   ```

2. **Add static configuration files** (if any):
   ```bash
   mkosi.files/etc/myapp/myapp.conf
   ```

3. **Or create a template** (if dynamic):
   ```bash
   # src/templates/myapp.conf.j2
   setting={{my_setting}}
   ```

4. **Add configuration variables** to `src/d9.yaml`:
   ```yaml
   myapp:
     my_setting: "value"
   ```

5. **Update mkosi.build** to render your template:
   ```python
   ("myapp.conf.j2", "etc/myapp/myapp.conf", "myapp"),
   ```

### Modifying Configuration

To change system configuration:

1. Edit `src/d9.yaml` to change values
2. Run `./mkosi.build` to re-render templates
3. Rebuild the image with `mkosi`

### Customization

Users can customize their system by:

1. Forking the repository
2. Editing `src/d9.yaml` with their preferences
3. Adding/removing packages in `mkosi.conf.d/`
4. Adding custom scripts to `mkosi.files/usr/local/bin/`
5. Building with `mkosi`

## System Integration

### Systemd Services

Services are enabled via systemd presets in:
```
mkosi.files/etc/systemd/system-preset/90-d9.preset
```

Example:
```
enable lightdm.service
enable bluetooth.service
```

### Update-alternatives

Alternative selections are configured in `mkosi.postinst.d/system-config.sh`:

```bash
update-alternatives --install /usr/bin/x-terminal-emulator x-terminal-emulator /usr/bin/kitty 50
```

## Migration from Ansible-based mkhome

For users migrating from the old Ansible-based system:

1. The new system uses pure mkosi configuration
2. All configuration is now system-wide in `/etc`
3. Run `clean-mkhome-after-d9-migration` to remove old user configs
4. The old `roles/`, Ansible playbooks, and `apt.txt` files are deprecated

## Build Requirements

- mkosi (latest version)
- python3-jinja2 (for template rendering)
- python3-yaml (for configuration parsing)

## Building the Image

```bash
# Render templates
./mkosi.build

# Build the image
mkosi

# Test in a VM
mkosi qemu
```

## Key Differences from Ansible Approach

| Aspect | Old (Ansible) | New (Pure mkosi) |
|--------|--------------|------------------|
| Package management | `roles/*/apt.txt` discovered dynamically | `mkosi.conf.d/*.conf` declarative |
| Configuration | Ansible tasks with `global.yaml` and `home.yaml` | Static files + Jinja2 templates |
| Template engine | Ansible Jinja2 + filters | Pure Jinja2 |
| Build system | `mkosi.configure` + `mkosi.postinst.d/ansible.yaml` | `mkosi.build` + shell postinst |
| Configuration location | Split between `/etc` and `~/.config` | All in `/etc` (system-wide) |
| User customization | Ansible variables + home playbook | Fork and edit `src/d9.yaml` |

## Philosophy

- **Declarative**: Everything is configuration, not code
- **Pure mkosi**: No external config management tools
- **Global configuration**: System-wide settings in `/etc`
- **Reproducible**: Same config = same image
- **Simple**: Python + Jinja2 + mkosi, nothing more
