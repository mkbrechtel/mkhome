# mkhome Development Guidelines

## Architecture Overview

This Ansible collection manages system and user configurations through a role-based architecture. Each role can be configured using feature flags that control which tasks are executed.

## Feature Flags

Roles are controlled by three feature flags:

- **`mkhome_install`**
  - Runs `tasks/install.yaml` in each role
  - Installs packages from `apt.txt` via apt
  - Requires elevated privileges (become: true)
  - Used by `system.yaml` playbook

- **`mkhome_configure_global`**
  - Runs `tasks/global.yaml` in each role
  - Configures system-wide settings in `/etc`
  - Sets up system services and alternatives
  - Requires elevated privileges
  - Used by `system.yaml` playbook and mkosi build process

- **`mkhome_configure_home`**
  - Runs `tasks/home.yaml` in each role
  - Sets up user-specific configurations
  - Does not require elevated privileges
  - Used by `home.yaml` playbook

## Role Structure

### Standard Roles

Each standard role follows this structure:

```
roles/role_name/
├── apt.txt             # Debian packages for this role (one per line, # comments allowed)
├── tasks/
│   ├── main.yaml       # Conditional imports based on feature flags
│   ├── install.yaml    # Package installation only (optional)
│   ├── global.yaml     # System-wide configuration (optional)
│   └── home.yaml       # User-specific configurations (optional)
├── defaults/
│   └── main.yaml       # Default variables
├── handlers/
│   └── main.yaml       # Event handlers (optional)
├── templates/
│   └── ...             # Regular templates
└── vars/
    └── main.yaml       # Role variables (optional)
```

### Meta Roles

Meta roles aggregate multiple standard roles through dependencies. They don't contain tasks themselves but serve as convenient bundles.

```
roles/meta_role_name/
├── meta/
│   └── main.yaml       # Role dependencies
└── tasks/
    └── main.yaml       # Empty or minimal (just comments)
```

Example `meta/main.yaml`:
```yaml
---
dependencies:
  - role: firefox
  - role: kitty
  - role: git
```

The `home` meta role includes all roles needed for a complete user environment. Use meta roles to:
- Create logical groupings of related functionality
- Simplify playbook definitions
- Maintain consistent role sets across environments

### Package Management with apt.txt

Each role should have an `apt.txt` file listing Debian packages to install, one per line. Comments starting with `#` are allowed.

Example `apt.txt`:
```
# Window manager packages
i3-wm
i3blocks
i3status
```

### tasks/main.yaml Pattern

Every role's main task file should follow this pattern:

```yaml
---
- import_tasks: install.yaml
  when: mkhome_install

- import_tasks: global.yaml
  when: mkhome_configure_global

- import_tasks: home.yaml
  when: mkhome_configure_home
```

Only include the imports for task files that exist. For example, a role that only configures user settings would only have the home.yaml import.

### Task File Purposes

- **install.yaml**:
  - Read and install packages from `apt.txt`
  - Package installation only

Example `install.yaml`:
```yaml
---
- name: Install debian packages
  apt:
    pkg: "{{ lookup('file', role_path + '/apt.txt') | regex_replace('#.*', '') | split('\n') | select('match', '^\\s*\\S+') | map('trim') | list }}"
```

- **global.yaml**:
  - Configure system-wide settings in `/etc`
  - Set up system services
  - Configure system-level alternatives
  - Create system users/groups

Example `global.yaml`:
```yaml
---
- name: Create system-wide config directory
  file:
    path: /etc/xdg/myapp
    state: directory
    mode: '0755'

- name: Install system-wide configuration
  template:
    src: myapp.conf.j2
    dest: /etc/xdg/myapp/myapp.conf
    mode: '0644'
```

- **home.yaml**:
  - Configure user dotfiles in `~/.config`
  - Set up user-specific settings
  - Create user directories
  - Install user-level configurations


## Adding a New Role

1. Create the role directory structure
2. Create `apt.txt` with required Debian packages (one per line, comments with `#`)
3. Add conditional imports in `tasks/main.yaml`
4. Implement appropriate task files based on what the role configures:
   - `install.yaml`: Read `apt.txt` and install packages
   - `global.yaml`: Configure system-wide settings in `/etc`
   - `home.yaml`: Configure user-specific settings
5. Add the role to the `home` meta role in `roles/home/meta/main.yaml`

**Note**: Packages from `apt.txt` files are automatically discovered by the `mkosi.configure` script during image builds.

## Playbook Examples

### home.yaml - User Configuration Only
```yaml
---
- name: Deploy home configuration for current user
  hosts: localhost
  become: false
  vars:
    mkhome_configure_home: true
  roles:
    - firefox
    - micro
```

### system.yaml - Full System Setup
```yaml
---
- name: Deploy system packages and configuration
  hosts: localhost
  become: true
  vars:
    mkhome_install: true
    mkhome_configure_global: true
  roles:
    - kitty
    - i3
```

### mkosi.postinst - System Image Configuration
The `mkosi.postinst` script is an executable Ansible playbook that configures the system image during the mkosi build process. It includes only roles that have `global.yaml` tasks that should be executed during image creation.

Example structure:
```yaml
#!/bin/bash -c "exec ansible-playbook \"$0\" \"$@\""
---
- name: Configure system image for mkosi build
  hosts: localhost
  become: false
  connection: community.general.chroot
  vars:
    mkhome_configure_global: true
  roles:
    - kitty
    - mkosi
    - x11
    - xfce
```

The shebang uses bash to execute ansible-playbook on the script itself, ignoring any arguments passed by mkosi.

## mkosi Integration

mkosi builds system images by running Ansible inside the build environment. Package discovery and system configuration are both automated:

### Build Process

1. **Package Discovery** (`mkosi.configure`):
   - Executed by mkosi before building the image
   - Scans all `roles/*/apt.txt` files
   - Injects discovered packages into mkosi's configuration
   - Packages are deduplicated and sorted

2. **System Configuration** (`mkosi.postinst`):
   - Executed after packages and trees are installed
   - Self-executing Ansible playbook script
   - Uses bash shebang to invoke ansible-playbook on itself
   - Ansible connects to the build environment via chroot connection
   - All roles listed in the playbook with `global.yaml` tasks configure system files in the image

### Configuration Files

- **mkosi.conf**: Base mkosi configuration
  - `ConfigureScripts=mkosi.configure` - Package discovery
  - `PostInstallationScripts=mkosi.postinst` - Ansible execution
  - `ToolsTreePackages=ansible` - Ansible in tools tree

- **mkosi.configure**: Python script that discovers packages from apt.txt files

- **mkosi.postinst**: Self-executing Ansible playbook that configures the system with mkhome_configure_global=true

This architecture ensures:
- Packages are automatically discovered from apt.txt files
- System configuration reuses the same Ansible roles as live systems
- No duplication between live system and image configuration
- Ansible runs inside mkosi's controlled environment
