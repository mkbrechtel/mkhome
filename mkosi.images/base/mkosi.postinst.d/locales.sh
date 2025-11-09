#!/bin/bash
set -e

# Generate German locales
echo "de_DE.UTF-8 UTF-8" > "$BUILDROOT/etc/locale.gen"
chroot "$BUILDROOT" locale-gen
