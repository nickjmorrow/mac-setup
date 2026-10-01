# mac-setup

How I set up my Macs. If a Mac dies or I buy a new one, this gets it back to the same state: the same apps, settings, dotfiles and secrets, with an AI agent doing most of the work.

## On a new Mac

1. Sign in to iCloud and the App Store.
2. `git clone https://github.com/nickjmorrow/mac-setup ~/Projects/mac-setup && cd ~/Projects/mac-setup && ./setup.sh`
3. Add a Bitwarden Secrets Manager access token when it asks (a read-only machine account's, stored so the Keychain asks before each use), and run `./setup.sh` again. It pulls the secrets into place and clones the rest.
4. `./macos.sh`, then the settings in [AGENTS.md](AGENTS.md#settings-no-script-covers) that no script covers.

## What's here

| | |
| --- | --- |
| `setup.sh` | Idempotent bootstrap: Homebrew, the `Brewfile`, [dotfiles](https://github.com/nickjmorrow/dotfiles), secrets, and my personal repos (each wires itself in with its own `install.sh`). |
| `Brewfile` | Every app, CLI tool, App Store app, font and VS Code extension. |
| `macos.sh` | macOS preferences (dark mode, tap to click, Dock). |
| `secrets.py` | Secrets live in Bitwarden Secrets Manager, never in git. This pulls each one into its usual place (`env:` keys into `~/.zshrc.local`, `file:` keys into files), so a dead Mac loses nothing. Names are checked, values shell-quoted, and files go only to an allowlist of places (`~/.config`, `~/.ssh/config`, project `.env` files...). Tests: `python3 -m unittest`. |
| `tools/display-brightness` | Day/night brightness for monitors on a dock that blocks DDC (through BetterDisplay). |
| `AGENTS.md` | The manual coding agents read on these Macs: settings no script covers, folder conventions, and what it must ask before doing. |

Machine-specific details (hostnames, addresses, what runs where) and the changelog live in a private companion file.
