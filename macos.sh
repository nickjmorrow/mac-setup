#!/usr/bin/env zsh
# Roland's macOS preferences (from Edgar). Safe to re-run.
# These change system settings, so an agent runs this only with Nicholas's OK.
set -euo pipefail

# Appearance: dark mode (takes full effect at next login; flip it now in Control Center if you like)
defaults write -g AppleInterfaceStyle Dark

# Trackpad: tap to click (natural scrolling is the macOS default)
defaults write com.apple.AppleMultitouchTrackpad Clicking -bool true
defaults write com.apple.driver.AppleBluetoothMultitouch.trackpad Clicking -bool true
defaults -currentHost write NSGlobalDomain com.apple.mouse.tapBehavior -int 1

# Default browser: Chrome (macOS asks to confirm)
defaultbrowser chrome

# Dock: auto-hide, icon size 71
defaults write com.apple.dock autohide -bool true
defaults write com.apple.dock tilesize -int 71
killall Dock

print "Done. Dark mode and tap-to-click fully apply after you log out and back in."
