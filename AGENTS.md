# Mac setup manual

How Nicholas's Macs are set up, so a new one can be made to match, and the rules any coding agent follows on them. Agents read it together with two private files kept in Sync: `~/Sync/secrets/AGENTS.local.md` (what's specific to his machines, plus the changelog) and the manual of his personal agent system.

Keep it current. This repo is public, so it holds only what helps set up a new Mac: anything that names an address, a hostname, a private repo or a secret, or that's only history, goes in `AGENTS.local.md`.

## The owner

- Owner: Nicholas Morrow (njmorrow95@gmail.com, has a GitHub account). Nicholas keeps full admin control; an agent does most setup and maintenance.
- Primary use: coding, development and hacking. Optimize setup decisions for that.

## Setting up a new Mac

1. Sign in to iCloud and the App Store. Clone this repo to `~/Projects/mac-setup` and run `./setup.sh` in a terminal.
2. It installs Sync.com along with everything else. Sign in to Sync.com, wait for `~/Sync` to finish syncing, then run `./setup.sh` again: it links the secrets back into place, clones the personal repos in `~/Sync/secrets/repos.txt` and runs each one's `install.sh`.
3. Run `./macos.sh` for macOS preferences (the agent asks first; it changes system settings).
4. Do the settings below that no script covers. Re-run `./link-secrets.sh` after cloning projects whose `.env` files it manages.

## Settings no script covers

- FileVault on. Touch ID set up.
- Homebrew at `/opt/homebrew` (shellenv loaded in `~/.zprofile`). Non-login shells may need `eval "$(/opt/homebrew/bin/brew shellenv zsh)"`.
- Xcode (from the Brewfile) set as the active developer directory (`sudo xcode-select -s /Applications/Xcode.app`), license accepted, first launch done.
- Git identity set globally (Nicholas Morrow, njmorrow95@gmail.com — use this, not the GitHub noreply address); default branch `main`.
- Never sleeps on AC power (`pmset -c sleep 0`), so services keep running.
- Tailscale signed in with GitHub.
- Logseq is a login item with its API server set to auto start.
- **Monitor brightness by time of day:** the external monitors' software brightness (BetterDisplay, a login item; the dock blocks DDC) is set to day (100%) at sunrise and to his night levels at sunset by `tools/display-brightness` (launchd `com.nicholai.display-brightness`, log `~/Library/Logs/display-brightness.log`; see its README). Hotkeys via skhd (dotfiles `skhd/skhdrc`, needs Accessibility): ⌃⌥⌘B toggle, ⌃⌥⌘↑/↓ ±10%.

## Folders

| Folder | Purpose |
| --- | --- |
| `~/Downloads` | Inbox. Keep it near zero: triage items and propose where each goes. Never delete without asking. |
| `~/Projects` | All code. One folder per project, each a git repo. |
| `~/Sync` | Cloud-backed things Nicholas cares about, via Sync.com (end-to-end encrypted). `~/Sync/secrets` holds the private files this repo needs (see `link-secrets.sh`). |
| `~/Documents` | TBD — don't organize or put things here until a convention is decided. |

## Packages

- The agent may install packages with Homebrew without asking.
- Every install or removal is reflected in `Brewfile` in the same change. Edit it by hand, in the right section with a short comment: `brew bundle dump --force` would wipe its sections and comments (use `brew bundle dump --file=- ` only to spot what's missing).
- App Store apps go in the Brewfile too, as `mas` lines.

## Scripts

- `setup.sh` — idempotent bootstrap: Homebrew, adopt pre-installed apps, `brew bundle`. Run it in a real terminal (installers may ask for a password).
- `macos.sh` — macOS preferences (appearance, trackpad, Dock). Changes system settings, so the agent asks before running it.
- `link-secrets.sh` — secrets live in `~/Sync/secrets` (Sync.com, end-to-end encrypted). It links or copies each file listed in the private `~/Sync/secrets/manifest.tsv` into its usual place (`~/.zshrc.local`, app logins, projects' `.env` files, the SSH key), so tools read the usual paths and every change lands in Sync. A new secret file gets a line in the manifest. Never keep secrets anywhere else.
- `tools/display-brightness` — day/night monitor brightness (see its README).

## Dotfiles

Shell and tool config lives in [nickjmorrow/dotfiles](https://github.com/nickjmorrow/dotfiles), cloned to `~/Projects/dotfiles`. Its `link.sh` symlinks files into `~` (`~/.zshrc`, `~/.config/git/ignore`, VS Code settings, the Midnight Sun VS Code theme and iTerm2 profile) and installs oh-my-zsh.

- Keep it up to date: when shell or tool config changes, change it in the dotfiles repo, commit, and push. The agent may push the dotfiles repo without asking.
- **Theme:** Midnight Sun (navy + sunshine yellow) lives in `dotfiles/themes/midnight-sun`. Edit `palette.json`, run `build.py`; it feeds Logseq, iTerm2, VS Code and Linear. Terminal apps that support it use the ANSI palette, so they inherit iTerm's colors.
- **Never commit secrets there.** Tokens and machine-specific settings go in `~/.zshrc.local`, which isn't tracked (it's a link into `~/Sync/secrets`).

## Ask first

The agent must ask Nicholas and wait for a clear yes before:

- **Deleting anything** — files, folders, uninstalling apps or packages, emptying the Trash, force-overwriting. (Git branches are the exception: the agent may delete them without asking, since 2026-09-28.)
- **Changing security or system settings** — FileVault, firewall, Gatekeeper, SIP, lock screen/password, sharing, privacy and security permissions, login/background items, computer name.
- **Running anything with `sudo`.**
- **Pushing to a remote or publishing anything** (except the dotfiles repo, above, this repo and his own personal repos listed in `~/Sync/secrets/repos.txt`: the agent may push any commit there without asking, force pushes included).
- **Moving anything into or out of `~/Sync`** (except a new secret file into `~/Sync/secrets` through `link-secrets.sh`).

Free to do without asking: read-only checks, Homebrew installs (recorded in `Brewfile`), creating files in `~/Projects`, and edits and commits inside this repo.

When a rule is unclear, ask.
