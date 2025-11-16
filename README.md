# d9

i have too many computers. i want my OS to be copyable.

this is a Debian-based system built with mkosi and systemd tooling that you can literally dd from one machine to another.

## why?

because i'm tired of:
- reinstalling the same packages on every machine
- keeping dotfiles in sync
- remembering which machine has what setup
- spending weekends setting up new hardware

## what is d9?

the name stands for 9[^1] d's that define the project:

_**dd**-able_ - the core philosophy: stream and copy filesystems with dd, pv, and friends

_**D**ebian-based_ - built on Debian's stable package ecosystem

_system**d** ecosystem utilizing_ - mkosi, systemd-repart, systemd-homed, systemd-sysext, systemd-confext, etc.

_**d**istribution_ - a complete Linux distro, not just a collection of tools

_**d**eclarative_ - everything configured as code with mkosi and systemd-repart

_**d**eployable_ - easy deployment methods: disk images, incus images, OCI images, etc.

_**d**isaster-recoverable_ - with restic and borg backups, A/B partitions, and trivial rollback

_dev/daily **d**esktop_ - for both development environments and daily desktop use

## profiles

we support multiple roles for different use cases:

### base
a base tree every other build is based upon

### bootable
makes the image bootable

### rescue
rescue system with recovery tools

### forensics
tools to help with system recovery and debugging

### desktop
desktop distribution for normie users and power users alike

## how it works

**Pure mkosi architecture** - everything is configured declaratively through mkosi configuration files

**Jinja2 templating** - configuration files are rendered from templates using a central d9.yaml config

**Static file overlays** - mkosi.files/ directory contains all system configuration in /etc

**Declarative packages** - mkosi.conf.d/ contains one file per component defining required packages

**systemd-repart** - disk and partition layout defined declaratively

**systemd-homed** - home directories on LUKS-encrypted images (optional)

**systemd-sysext/confext** - layer extensions and configs (future)

**restic and borg** - incremental stream backups and restores

## reproducibility

an interesting research question is if we can make the images fully reproducible:
- make them be based only on reproducibly built Debian packages
- make the build of the images also reproducible so we can build the same images based on the same sources in an 1:1 way

## non-issues

*image size*: i need a full operating system that comes with everything i might possibly need. the goal is to ship a system where you do not need to install anything else.

if you are concerned about this, you can use other distributions.

## origin

based on [my](https://mkbrechtel.dev) personal home directory and desktop setup i developed over a long time.

## status

works for me. might work for you. no promises.

## requirements

- mkosi (latest version recommended)
- python3-jinja2 (for template rendering)
- python3-yaml (for configuration parsing)

Install on Debian Trixie:
```bash
apt-get install mkosi python3-jinja2 python3-yaml
```

## build

Build the image in two steps:

```bash
# 1. Render configuration templates
./mkosi.build

# 2. Build the image
mkosi
```

Or combine both:
```bash
./mkosi.build && mkosi
```

## test

Run the test VM with:
```bash
mkosi qemu
```

## configuration

All system configuration is centralized in `src/d9.yaml`. Edit this file to customize:

- Display manager settings (autologin, background image)
- Desktop environment preferences (Xfce panel, compositing)
- Terminal settings (Kitty font, size)
- Application defaults

After editing, re-run `./mkosi.build` to regenerate configuration files.

## migration from ansible-based mkhome

If you're migrating from the previous Ansible-based system:

1. The system now uses pure mkosi configuration
2. All configs are system-wide in `/etc` (no more per-user configs)
3. Old `roles/` directory and Ansible playbooks are deprecated
4. Run `clean-mkhome-after-d9-migration` script to clean up old user configs

## issues
If you have an issue, please make a pull request with the issue in a markdown file inside the `issues/` folder.

## license
LGPL-2.1+, see [LICENSE file](./LICENSE)

## footnotes

[^1]: n may vary
