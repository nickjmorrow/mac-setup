# Mac setup manual

How Nicholas's Macs are set up, so a new one can be made to match, and the rules any coding agent follows on them. Agents read it together with two private files: the machines' private notes (`MACHINES.md`) and the manual of his personal agent (`AGENTS.md`), both in his private agent-harness repo.

Keep it current. This repo is public, so it holds only what helps set up a new Mac: anything that names an address, a hostname, a private repo or a secret, or that's only history, goes in the private `MACHINES.md`.

## The owner

- Owner: Nicholas Morrow (njmorrow95@gmail.com, has a GitHub account). Nicholas keeps full admin control; an agent does most setup and maintenance.
- Primary use: coding, development and hacking. Optimize setup decisions for that.

## Setting up a new Mac

1. Sign in to iCloud and the App Store. Clone this repo to `~/Projects/mac-setup` (the first `git` on a new Mac offers to install Apple's command line tools: accept, then clone again) and run `./setup.sh` in a terminal. It installs `Brewfile` (what every Mac gets), then `Brewfile.personal`.
2. It installs `bws` (Bitwarden Secrets Manager's CLI; pinned SHA-256, then Bitwarden's signature and Apple's notarization are checked) and asks for an access token, saved in the login Keychain with no app trusted (`-T ""`), so each read asks first: a read-only machine account's token as `bws-access-token-read` (what `pull` uses), plus, only on a Mac that pushes secrets, the read-write one as `bws-access-token`. Click Allow, not Always Allow. Run `./setup.sh` again: `secrets.py` pulls every secret into place, then it clones the personal repos listed in the private repo list and runs each one's `install.sh`.
3. Run `./macos.sh` for macOS preferences (the agent asks first; it changes system settings).
4. Do the settings below that no script covers. Re-run `./secrets.py pull` after cloning a project whose `.env` lives in Bitwarden.

## Setting up a work Mac

A Mac an employer owns gets his tools and shell, and nothing personal. The employer's IT rules win over anything here.

1. Finish the employer's own setup first (their account, device management, their sign-ins).
2. Clone this repo to `~/Projects/mac-setup` and run `./setup.sh --work`. It installs Homebrew, `Brewfile` and the dotfiles, and stops. Homebrew needs an admin account: without one the script skips Homebrew and the Brewfile, still links the dotfiles, and says so; ask IT for admin rights or to install Homebrew, then re-run. Don't install Homebrew in the home folder to get around it: it's unsupported, and it sidesteps a limit IT set. It skips `Brewfile.personal`, the secrets and the personal repos, and remembers the choice in `~/.config/mac-setup/profile`, so a later plain `./setup.sh` stays in work mode. The dotfiles' `link.sh` reads the same file and leaves out the app-icon background job.
3. `./macos.sh` (dark mode, tap to click, Dock, Chrome as default browser).
4. Git identity: his name with the work email, not the personal one (`git config --global user.email …`); default branch `main`. Make a new SSH key for the employer's Git host; never copy a key from another Mac.
5. Optional, for the home dock: the monitor-brightness job and hotkeys (`tools/display-brightness/README.md`, "On another Mac").

Never on a work Mac:

- The Bitwarden access token, `secrets.py pull`, or any personal secret, API key or `~/.zshrc.local` copied from another Mac.
- His personal repos, the personal agent's rules, memory and skills, or his notes.
- Tailscale on his own tailnet, his VPNs, Sync.com, torrents.
- The power and lock settings below (never sleeps, no auto-lock): leave what IT set.
- The employer's code, data or credentials going the other way: none of it on a personal Mac, in a personal repo or in Bitwarden.

A coding agent there reads this file for the folder, package and Ask-first rules (point `~/.claude/CLAUDE.md` at it), has no private files to read, and installs only software the employer allows.

## Settings no script covers

- FileVault on. Touch ID set up.
- Homebrew at `/opt/homebrew` (shellenv loaded in `~/.zprofile`). Non-login shells may need `eval "$(/opt/homebrew/bin/brew shellenv zsh)"`.
- Xcode (from the Brewfile) set as the active developer directory (`sudo xcode-select -s /Applications/Xcode.app`), license accepted, first launch done.
- Git identity set globally (Nicholas Morrow, njmorrow95@gmail.com — use this, not the GitHub noreply address); default branch `main`.
- Never sleeps on AC power (`pmset -c sleep 0`), so services keep running.
- Tailscale signed in with GitHub.
- **Monitor brightness by time of day:** the external monitors' software brightness (BetterDisplay, a login item; the dock blocks DDC) is set to day (100%) at sunrise and to his night levels at sunset by `tools/display-brightness` (launchd `com.nicholai.display-brightness`, log `~/Library/Logs/display-brightness.log`; see its README). Hotkeys via skhd (dotfiles `skhd/skhdrc`, needs Accessibility): ⌃⌥⌘B toggle, ⌃⌥⌘↑/↓ ±10%.

## Folders

| Folder | Purpose |
| --- | --- |
| `~/Downloads` | Inbox. Keep it near zero: triage items and propose where each goes. Never delete without asking. |
| `~/Projects` | All code. One folder per project, each a git repo. |
| `~/Sync` | Cloud-backed things Nicholas cares about, via Sync.com (end-to-end encrypted). Not for secrets. |
| `~/Documents` | TBD — don't organize or put things here until a convention is decided. |

## Packages

- The agent may install packages with Homebrew without asking.
- Every install or removal is reflected in the same change: in `Brewfile` when a work Mac should get it too (dev tools, editor, terminal, dock drivers), otherwise in `Brewfile.personal`. Edit it by hand, in the right section with a short comment: `brew bundle dump --force` would wipe its sections and comments (use `brew bundle dump --file=- ` only to spot what's missing).
- App Store apps go in `Brewfile.personal`, as `mas` lines.
- A formula from a third-party tap (`owner/tap/name`) also goes in `TRUSTED_FORMULAE` in `setup.sh`: Homebrew won't load it until it's trusted.
- Global npm packages can't be pinned in the Brewfile (`brew bundle` matches them by bare name); note the known-good version in a comment beside the line.

## Scripts

- `setup.sh` — idempotent bootstrap: Homebrew, adopt pre-installed apps, `brew bundle` for both Brewfiles, dotfiles, secrets, personal repos. `--work` stops after the shared Brewfile and dotfiles (see above). Run it in a real terminal (installers may ask for a password).
- `macos.sh` — macOS preferences (appearance, trackpad, Dock). Changes system settings, so the agent asks before running it.
- `secrets.py` — secrets live in Bitwarden Secrets Manager (project `personal-agent`), never in git or a synced folder. Each secret's key says where it goes: `env:NAME` becomes a line `export NAME='value'` in `~/.zshrc.local` (names must match `^[A-Z_][A-Z0-9_]*$`; values are stored raw and shell-quoted on write; an older value stored with its quotes, like `"abc"`, is unquoted on pull, and `push-env` stores it unquoted), `file:~/path` a file (mode 600). File destinations are an allowlist, checked on the resolved path (no `..`, no symlink leading elsewhere): `~/.config/**`, `~/.eight-sleep-mcp/**`, `~/.ssh/config`, and `.env` / `.env.*` directly inside a `~/Projects/<project>` folder. Anything else (shell rc files, `~/Library`, other `~/.ssh` files) is refused and reported, and `pull` exits 1; `push-file` refuses the same paths. `pull` writes them all (`--check` / `--dry-run` shows what would change and what's refused); `push-env` / `push-file` upload a change. Tokens come from the login Keychain (`pull` and `list` prefer `bws-access-token-read`, `push-*` use `bws-access-token`), so on a server Mac run it from the login session, not over SSH. Tests: `python3 -m unittest` (temp HOME and a fake `bws`; no network or Keychain). Files that apps rewrite on their own (refreshing login tokens) and SSH keys (one per Mac) stay local.
- `tools/display-brightness` — day/night monitor brightness (see its README; `setup.sh` doesn't install its launchd job or start skhd).
- `tools/set-env-secret NAME [ssh-host …]` — sets or rotates a shared env secret from the clipboard: Bitwarden (`env:NAME`), this Mac's `~/.zshrc.local` and each host's. The value never shows on screen.

## Shared API keys

API keys more than one project uses (`ANTHROPIC_API_KEY` and the like) are `env:` secrets, so every shell, project and agent on every Mac finds them in the environment. Projects read them from there; never copy a key into a project's `.env`, where it goes stale when the key is rotated. A launchd service doesn't load the shell, so its run script sources `~/.zshrc.local` before starting. To add or rotate a key, have him copy it and run `tools/set-env-secret`, then restart the services that use it.

## Dotfiles

Shell and tool config lives in [nickjmorrow/dotfiles](https://github.com/nickjmorrow/dotfiles), cloned to `~/Projects/dotfiles`. Its `link.sh` symlinks files into `~` (`~/.zshrc`, `~/.config/git/ignore`, VS Code settings, the Midnight Sun VS Code theme and iTerm2 profile) and installs oh-my-zsh.

- Keep it up to date: when shell or tool config changes, change it in the dotfiles repo, commit, and push. The agent may push the dotfiles repo without asking.
- **Theme:** Midnight Sun (navy + sunshine yellow) lives in `dotfiles/themes/midnight-sun`. Edit `palette.json`, run `build.py`; it feeds Logseq, iTerm2, VS Code, Linear and the iPhone home-screen icons (see its README; re-adding them on the phone is by hand). Terminal apps that support it use the ANSI palette, so they inherit iTerm's colors.
- **Never commit secrets there.** Tokens and machine-specific settings go in `~/.zshrc.local`, which isn't tracked (`secrets.py pull` writes it from Bitwarden).

## Ask first

The agent must ask Nicholas and wait for a clear yes before:

- **Deleting anything** — files, folders, uninstalling apps or packages, emptying the Trash, force-overwriting. (Git branches are the exception: the agent may delete them without asking, since 2026-09-28.)
- **Changing security or system settings** — FileVault, firewall, Gatekeeper, SIP, lock screen/password, sharing, privacy and security permissions, login/background items, computer name.
- **Running anything with `sudo`.**
- **Pushing to a remote or publishing anything** (except the dotfiles repo, above, this repo and his own personal repos listed in the private repo list: the agent may push any commit there without asking, force pushes included).
- **Moving anything into or out of `~/Sync`.** Adding or changing a secret in Bitwarden with `secrets.py push-*` is fine.

Free to do without asking: read-only checks, Homebrew installs (recorded in `Brewfile`), creating files in `~/Projects`, and edits and commits inside this repo.

When a rule is unclear, ask.
