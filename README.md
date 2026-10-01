# mac-setup

How I set up my Macs. If a Mac dies or I buy a new one, this gets it back to the same state: the same apps, settings, dotfiles and secrets, with an AI agent doing most of the work.

## On a new Mac

1. Sign in to iCloud and the App Store.
2. `git clone https://github.com/nickjmorrow/mac-setup ~/Projects/mac-setup && cd ~/Projects/mac-setup && ./setup.sh`
3. Sign in to Sync.com, let `~/Sync` finish syncing, and run `./setup.sh` again. It links the secrets back into place and clones the rest.
4. `./macos.sh`, then the settings in [AGENTS.md](AGENTS.md#settings-no-script-covers) that no script covers.

## What's here

| | |
| --- | --- |
| `setup.sh` | Idempotent bootstrap: Homebrew, the `Brewfile`, [dotfiles](https://github.com/nickjmorrow/dotfiles), secrets, and my personal repos (each wires itself in with its own `install.sh`). |
| `Brewfile` | Every app, CLI tool, App Store app, font and VS Code extension. |
| `macos.sh` | macOS preferences (dark mode, tap to click, Dock). |
| `link-secrets.sh` | Secrets live in Sync.com (end-to-end encrypted), never in git. This links each one from there into its usual place, so a dead Mac loses nothing. The list of files is private too. |
| `tools/display-brightness` | Day/night brightness for monitors on a dock that blocks DDC (through BetterDisplay). |
| `AGENTS.md` | The manual coding agents read on these Macs: settings no script covers, folder conventions, and what it must ask before doing. |

Machine-specific details (hostnames, addresses, what runs where) and the changelog live in a private companion file next to the secrets.
