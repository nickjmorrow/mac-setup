#!/usr/bin/env zsh
# Bring one of Nicholas's Macs up to spec (see MANUAL.md). Safe to re-run.
# Run it in a real terminal: some installers ask for your password.
set -euo pipefail
HERE="${0:A:h}"

step() { print -P "\n%F{cyan}==>%f %B$1%b" }

step "Homebrew"
if [[ ! -x /opt/homebrew/bin/brew ]]; then
  /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
fi
eval "$(/opt/homebrew/bin/brew shellenv zsh)"

step "Adopt apps installed outside Homebrew"
# brew bundle fails on an app that already exists but isn't brew-managed.
typeset -A preinstalled=(google-chrome "Google Chrome" claude "Claude")
for cask app in ${(kv)preinstalled}; do
  if [[ -d "/Applications/$app.app" ]] && ! brew list --cask "$cask" &>/dev/null; then
    brew install --cask --adopt "$cask"
  fi
done

step "Brewfile"
if ! mas list &>/dev/null; then
  print "Not signed in to the App Store — App Store apps may fail. Sign in via the App Store app and re-run."
fi
brew bundle --file="$HERE/Brewfile"

step "Dotfiles"
if [[ ! -d ~/Projects/dotfiles ]]; then
  git clone https://github.com/nickjmorrow/dotfiles.git ~/Projects/dotfiles
fi
~/Projects/dotfiles/link.sh

step "Secrets"
# They live in ~/Sync/secrets (Sync.com); link-secrets.sh links them into place. Needs Sync.com signed in and synced.
if [[ -d ~/Sync/secrets ]]; then
  "$HERE/link-secrets.sh"
else
  print "~/Sync/secrets isn't here yet: sign in to Sync.com, let it finish syncing, then run $HERE/link-secrets.sh"
fi

step "Personal repos"
# ~/Sync/secrets/repos.txt (private) lists "<git url> <folder>" per line. Each is cloned if missing,
# and its install.sh, if it has one, wires it into this Mac.
if [[ -f ~/Sync/secrets/repos.txt ]]; then
  while read -r url dir; do
    [[ -z $url || $url == \#* ]] && continue
    dir=${dir/#\~/$HOME}
    [[ -d $dir ]] || git clone "$url" "$dir"
    [[ -x $dir/install.sh ]] && "$dir/install.sh"
  done < ~/Sync/secrets/repos.txt
else
  print "~/Sync/secrets/repos.txt isn't here yet: finish syncing ~/Sync, then re-run."
fi

step "Done"
print "Done. Sign in to the App Store and Sync.com first if those steps complained, then re-run."
