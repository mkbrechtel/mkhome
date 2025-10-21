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

***dd*-able** - the core philosophy: stream and copy filesystems with dd, pv, and friends

***D*ebian-based** - built on Debian's stable package ecosystem

**system*d* ecosystem** - mkosi, systemd-repart, systemd-homed, systemd-sysext, systemd-confext, etc.

***d*istribution** - a complete Linux distro, not just a collection of tools

***d*eclarative** - everything configured as code with mkosi and systemd-repart

***d*eployable** - easy deployment methods: disk images, incus images, OCI images, etc.

***d*isaster-recoverable** - with restic and borg backups, A/B partitions, and trivial rollback

***d*ev/**d**aily ***d*esktop** - for both development environments and daily desktop use

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

[^1]: n may vary
