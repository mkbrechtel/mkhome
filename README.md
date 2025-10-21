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

with mkosi you can create awesome customized desktop images.

with systemd-repart you can create disk and disk image partitions declaratively.

with systemd-homed your home directory lives on a LUKS-encrypted image or storage medium.

with systemd-sysext and systemd-confext you can layer extensions and configs.

with pv you can see how quickly a file transfer progresses.

with restic and borg you can do incremental stream backups and restores.

## reproducibility

an interesting research question is if we can make the images fully reproducible:
- make them be based only on reproducibly built Debian packages
- make the build of the images also reproducible so we can build the same images based on the same sources in an 1:1 way

## origin

based on [my](https://mkbrechtel.dev) personal home directory and desktop setup i developed over a long time.

## status

works for me. might work for you. no promises.

## environment
You need mkosi installed. I currently develop in Debian Trixie. Install with:
```bash
apt-get install mkosi
```

## build
You can build with mkosi:
```bash
mkosi
```

## test
Run the test VM with:
```bash
mkosi vm
```

## issues
If you have an issue, please make a pull request with the issue in a markdown file inside the `issues/` folder.

## license
LGPL-2.1+, see [LICENSE file](./LICENSE)

## footnotes

[^1]: n may vary
