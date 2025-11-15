# Pure mkosi Migration

## Status: ✅ COMPLETED

Get rid of the ansible and apt.txt. We go full on pure mkosi.

## Completed Tasks

### 1. ✅ Package Configuration Migration
Put the package configuration into mkosi config files in mkosi.conf.d/. The new config files have the same name as the old roles.

**Implementation:**
- Created 39 new package configuration files in `mkosi.conf.d/`
- Each file follows the naming pattern: `mkosi.conf.d/{role_name}.conf`
- All packages from `roles/*/apt.txt` files have been migrated
- Format: `[Content]\nPackages=pkg1 pkg2 pkg3`

**Examples:**
- `mkosi.conf.d/firefox.conf` - Firefox browser packages
- `mkosi.conf.d/kitty.conf` - Kitty terminal packages
- `mkosi.conf.d/xfce.conf` - Xfce desktop environment packages

### 2. ✅ Global Configuration Files
All config files go into /etc and are globally configured.

**Implementation:**
- **Static files** migrated to `mkosi.files/etc/`:
  - dconf profile configuration
  - LightDM PAM configuration
  - Background images → `/opt/backgrounds/`
  - System scripts → `/usr/local/bin/`
  - Xfce desktop configurations
  - Zoom updater desktop file

- **Template-based files** created with Jinja2:
  - `src/templates/*.j2` - Jinja2 templates for dynamic configs
  - `mkosi.build` - Python script to render templates
  - `src/d9.yaml` - Central configuration file with all variables

**Template System:**
- Kitty terminal configuration
- LightDM display manager configuration
- X11 touchpad configuration
- Xfce panel and window manager configuration
- Zoom update scripts and sudoers

### 3. ✅ Migration Cleanup Script
Create a clean-mkhome-after-d9-migration script in /usr/local/bin/ that gets installed automatically that cleans up all previously home directory configured config files that are now handled globally.

**Implementation:**
- Created: `mkosi.files/usr/local/bin/clean-mkhome-after-d9-migration`
- Removes old user-specific configurations from `~/.config/`
- Interactive script with confirmation prompt
- Cleans up:
  - Kitty configs
  - Xfce configs
  - dconf databases
  - X11 configs
  - Ansible markers

### 4. ✅ Jinja2 Template Rendering
For templates with config options, install python jinja apt package in the buildroot environment and create a build script that renders them all from a central d9.yaml in the src directory.

**Implementation:**
- Created `src/d9.yaml` - Central configuration file with all settings
- Created `mkosi.build` - Python script for template rendering
- Added `mkosi.conf.d/build-deps.conf` with `python3-jinja2` and `python3-yaml`
- Renders 8 templates during build process
- All templates use standard Jinja2 (no Ansible-specific filters)

**Build Process:**
1. `mkosi.build` reads `src/d9.yaml`
2. Renders all templates from `src/templates/`
3. Outputs to `mkosi.files/etc/`
4. mkosi copies files during image build

### 5. ✅ System Integration
Created supporting infrastructure for pure mkosi build.

**New Files:**
- `mkosi.postinst.d/system-config.sh` - System configuration (dconf, alternatives)
- `mkosi.files/etc/systemd/system-preset/90-d9.preset` - Service presets
- Disabled old Ansible infrastructure:
  - `mkosi.postinst.d/ansible.yaml.disabled`
  - `mkosi.configure.disabled`

### 6. ✅ Documentation
Updated all documentation to reflect the new architecture.

**Updated Files:**
- `CODING.md` - Completely rewritten with pure mkosi architecture
- `README.md` - Updated with new build process and configuration info
- Both documents now clearly mark old Ansible approach as deprecated

## Architecture Changes

### Before (Ansible-based)
```
Ansible roles/ → apt.txt discovery → dynamic package installation
Ansible playbooks → Jinja2 templates → /etc and ~/.config
mkosi.configure → Python package discovery
mkosi.postinst.d/ansible.yaml → Ansible in chroot
```

### After (Pure mkosi)
```
mkosi.conf.d/*.conf → declarative packages
src/d9.yaml + src/templates/ → mkosi.build → mkosi.files/etc/
mkosi.postinst.d/system-config.sh → simple shell script
```

## Benefits

1. **Simpler**: No Ansible dependency, just Python + Jinja2 + mkosi
2. **Faster**: No Ansible overhead during build
3. **Clearer**: All configuration in one place (`src/d9.yaml`)
4. **Pure mkosi**: Uses mkosi's native mechanisms throughout
5. **Global config**: All settings in `/etc`, no per-user complexity
6. **Declarative**: Everything is configuration files, not tasks

## Migration Path for Users

1. Pull latest changes
2. Install build dependencies: `apt-get install python3-jinja2 python3-yaml`
3. Run `./mkosi.build` to render templates
4. Build image with `mkosi`
5. After first boot, run `clean-mkhome-after-d9-migration` to clean old configs

## Files Kept (for reference)

The old `roles/` directory is kept but deprecated. It may be removed in a future version once the migration is fully validated.

## Technical Details

**Package Configuration Files Created:** 39
**Static Files Migrated:** 8
**Templates Created:** 8
**Scripts Created:** 3 (mkosi.build, system-config.sh, clean-mkhome-after-d9-migration)
**Configuration Files:** 1 (src/d9.yaml)
**Documentation Updates:** 2 (CODING.md, README.md)

## Testing

To test the migration:

```bash
# Render templates
./mkosi.build

# Build image
mkosi

# Test in VM
mkosi qemu
```

Expected output from mkosi.build:
```
============================================================
d9 Template Rendering Build Script
============================================================
Loading configuration from /home/mkbrechtel/d9/src/d9.yaml...
Setting up Jinja2 environment...
Rendering templates...
[8 templates rendered successfully]
============================================================
Build completed successfully!
============================================================
```

## Next Steps

Potential future improvements:
- Remove old `roles/` directory after validation period
- Add more configuration options to `src/d9.yaml`
- Consider mkosi profiles for different use cases
- Investigate reproducible builds
