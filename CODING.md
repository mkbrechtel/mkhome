# mkhome Development Guidelines

## Architecture Overview

This Ansible collection manages system and user configurations through a role-based architecture. Each role can operate in different modes depending on the deployment context.

## mkhome_mode Settings

The `mkhome_mode` variable determines how roles behave:

- **`home`**: Configure user's home directory only
  - Runs `tasks/home.yaml` in each role
  - Sets up user-specific configurations
  - Does not require elevated privileges
  - Used by `home.yaml` playbook

- **`system`**: Install system packages and configure system-wide settings
  - Runs `tasks/system.yaml` in each role
  - Installs packages via apt
  - Configures system-wide settings
  - Requires elevated privileges (become: true)
  - Used by `system.yaml` playbook
  - Also installs mkosi package for image building

- **`mkosi`**: Configure for mkosi image build
  - Runs `tasks/mkosi.yaml` in each role
  - Templates mkosi configuration fragments into `image/` directory
  - Adds packages to mkosi package lists
  - Creates system-wide configurations for the image
  - Used by `mkosi.yaml` playbook

## Role Structure

Each role follows this standard structure:

```
roles/role_name/
├── tasks/
│   ├── main.yaml       # Conditional imports based on mkhome_mode
│   ├── home.yaml       # User-specific configurations (optional)
│   ├── system.yaml     # System packages and configs (optional)
│   └── mkosi.yaml      # mkosi image configurations (optional)
├── defaults/
│   └── main.yaml       # Default variables
├── handlers/
│   └── main.yaml       # Event handlers (optional)
├── templates/
│   ├── ...             # Regular templates
│   └── mkosi/          # mkosi-specific templates (optional)
└── vars/
    └── main.yaml       # Role variables (optional)
```

### tasks/main.yaml Pattern

Every role's main task file should follow this pattern:

```yaml
---
- import_tasks: system.yaml
  when: mkhome_mode == 'system'
  
- import_tasks: home.yaml  
  when: mkhome_mode == 'home'

- import_tasks: mkosi.yaml
  when: mkhome_mode == 'mkosi'
```

Only include the imports for task files that exist. For example, a role that only configures user settings would only have the home.yaml import.

### Task File Purposes

- **system.yaml**: 
  - Install packages from package managers
  - Configure system-wide settings in `/etc`
  - Set up system services
  - Create system users/groups

- **home.yaml**:
  - Configure user dotfiles in `~/.config`
  - Set up user-specific settings
  - Create user directories
  - Install user-level configurations

- **mkosi.yaml**:
  - Template mkosi configuration drop-ins
  - Add packages to `image/mkosi.packages.d/`
  - Configure image-specific settings
  - Ensure consistent base image configuration

## Adding a New Role

1. Create the role directory structure
2. Add conditional imports in `tasks/main.yaml`
3. Implement appropriate task files based on what the role configures
4. For mkosi support, create `tasks/mkosi.yaml` and `templates/mkosi/` directory
5. Add the role to relevant playbooks (`home.yaml`, `system.yaml`, `mkosi.yaml`)

## mkosi Integration

The mkosi mode enables building consistent system images. When running in mkosi mode:

1. The `mkosi` role sets up the base configuration in `image/`
2. Each included role adds its packages and configurations via drop-in files
3. The resulting image contains all system-level configurations but no user-specific settings

Example mkosi task file:

```yaml
---
- name: Create mkosi drop-in directory for packages
  file:
    path: "{{ playbook_dir }}/image/mkosi.packages.d"
    state: directory
    mode: '0755'

- name: Add role packages to mkosi image
  template:
    src: mkosi/10-rolename.conf.j2
    dest: "{{ playbook_dir }}/image/mkosi.packages.d/10-rolename.conf"
    mode: '0644'
```

## Best Practices

1. Keep role tasks focused and single-purpose
2. Use defaults for configurable values
3. Document role variables in defaults/main.yaml
4. Test roles in all applicable modes
5. Use consistent naming conventions for mkosi drop-in files