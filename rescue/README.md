# mkrescue

mkrescue is a custom rescue system tailored to my needs based on mkosi and Debian.

## features
Not much yet, currently we have a basic live system with working secure boot, no BIOS boot yet even. The idea is to have all tools i usually need during rescue operation right at hand.

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
