#!/usr/bin/env zsh
# Bring one of Nicholas's Macs up to spec (see AGENTS.md). Safe to re-run.
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
# They live in Bitwarden Secrets Manager; secrets.py pulls them into place. Needs bws (installed here: a pinned
# SHA-256, then Bitwarden's Developer ID signature and Apple notarization) and an access token in the login Keychain.
BWS_VERSION=2.1.0
BWS_ZIP_SHA256=9cb1c1c6e6164d83b2e339883ba02b4cbb37188ce9a484b1ce8249443163e066  # bws-aarch64-apple-darwin-2.1.0.zip
BWS_REQUIREMENT='anchor apple generic and certificate leaf[subject.OU] = "LTZ2PFU5D6"'  # Bitwarden Inc's team ID
bws_ok() {
  codesign --verify --strict -R="$BWS_REQUIREMENT" "$1" 2>/dev/null && spctl -a -t install "$1" 2>/dev/null
}
if [[ ! -x ~/.local/bin/bws ]]; then
  tmp=$(mktemp -d)
  zip=bws-aarch64-apple-darwin-$BWS_VERSION.zip
  curl -fsSL -o "$tmp/$zip" "https://github.com/bitwarden/sdk-sm/releases/download/bws-v$BWS_VERSION/$zip" \
    || { print "Couldn't download bws; stopping"; exit 1 }
  print "$BWS_ZIP_SHA256  $tmp/$zip" | shasum -a 256 -c - >/dev/null \
    || { print "bws download doesn't match the pinned SHA-256; stopping"; exit 1 }
  unzip -oq "$tmp/$zip" bws -d "$tmp"
  bws_ok "$tmp/bws" || { print "bws isn't signed by Bitwarden and notarized by Apple; stopping"; exit 1 }
  mkdir -p ~/.local/bin && install -m 755 "$tmp/bws" ~/.local/bin/bws && rm -rf "$tmp"
fi
bws_ok ~/.local/bin/bws || { print "~/.local/bin/bws isn't Bitwarden's signed build; delete it and re-run"; exit 1 }
# pull prefers a read-only machine account's token (bws-access-token-read); push-* need bws-access-token.
# Checking that an item exists doesn't read its secret, so this doesn't prompt.
if security find-generic-password -a "$USER" -s bws-access-token-read >/dev/null 2>&1 \
   || security find-generic-password -a "$USER" -s bws-access-token >/dev/null 2>&1; then
  "$HERE/secrets.py" pull
else
  print "No Bitwarden access token yet. Add a read-only machine account's token (Bitwarden → Secrets Manager →"
  print "machine account with Can read on the project → access token); the Keychain will ask before each use:"
  print '  security add-generic-password -U -a "$USER" -s bws-access-token-read -T "" -w'
  print "(and, only on a Mac you push secrets from, the read-write one as -s bws-access-token), then re-run ./setup.sh."
fi

step "Personal repos"
# ~/.config/mac-setup/repos.txt (a Bitwarden secret file) lists "<git url> <folder>" per line. Each is cloned
# if missing, and its install.sh, if it has one, wires it into this Mac.
REPOS=~/.config/mac-setup/repos.txt
if [[ -f $REPOS ]]; then
  while read -r url dir; do
    [[ -z $url || $url == \#* ]] && continue
    dir=${dir/#\~/$HOME}
    [[ -d $dir ]] || git clone "$url" "$dir"
    [[ -x $dir/install.sh ]] && "$dir/install.sh"
  done < $REPOS
  "$HERE/secrets.py" pull >/dev/null  # again: files for projects that were just cloned
else
  print "$REPOS isn't here yet (it comes from Bitwarden with the secrets); re-run once the Secrets step works."
fi

step "Done"
print "Done. If a step complained (App Store sign-in, Bitwarden token), fix it and re-run."
