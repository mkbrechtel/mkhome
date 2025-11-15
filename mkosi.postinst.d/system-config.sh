#!/bin/bash
#
# mkosi postinst script for system configuration
# Runs after all packages and files are installed
#

set -e

echo "================================================"
echo "d9 System Configuration Post-Install"
echo "================================================"

# Update dconf databases
echo "Updating dconf databases..."
if [ -d "$BUILDROOT/etc/dconf/db" ]; then
    dconf update || true
fi

# Configure update-alternatives
echo "Configuring update-alternatives..."

# Set kitty as default terminal emulator
if [ -x "$BUILDROOT/usr/bin/kitty" ]; then
    update-alternatives --install /usr/bin/x-terminal-emulator x-terminal-emulator /usr/bin/kitty 50 || true
fi

# Set xfce4-session as default session manager
if [ -x "$BUILDROOT/usr/bin/xfce4-session" ]; then
    update-alternatives --install /usr/bin/x-session-manager x-session-manager /usr/bin/xfce4-session 50 || true
fi

echo "================================================"
echo "System configuration completed"
echo "================================================"
