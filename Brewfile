# What every one of Nicholas's Macs gets, a work laptop included: dev tools, editor, terminal, dock drivers.
# Personal Macs also get Brewfile.personal. Install with ./setup.sh (./setup.sh --work skips the personal file).

# ── CLI ──────────────────────────────────────────────────────────────
brew "gh"                  # GitHub CLI
brew "git-filter-repo"     # rewrite git history
brew "gitleaks"            # scan for secrets before publishing a repo
brew "trufflehog"          # find and verify leaked credentials
brew "fzf"
brew "ripgrep"
brew "the_silver_searcher"
brew "vim"
brew "watchman"
brew "deno"
brew "bun"                 # JS runtime + package manager
brew "node"                # default Node; stable path for global npm tools
brew "pnpm"
brew "defaultbrowser"      # set default browser (used by macos.sh)
brew "uv"                  # Python (replaces pyenv/poetry/conda)
brew "awscli"
brew "tokei"               # count lines of code by language
brew "tmux"
# skhd moved from koekeishiya's tap to asmvik's. Homebrew loads a third-party formula only once it's trusted;
# setup.sh trusts the ones named in these files (TRUSTED_FORMULAE there: keep the two in step).
tap "asmvik/formulae"
brew "asmvik/formulae/skhd"   # global hotkeys (config in dotfiles skhd/skhdrc)

# ── Apps ─────────────────────────────────────────────────────────────
cask "claude"
cask "claude-code"         # CLI agent
cask "google-chrome"
cask "firefox"
cask "rectangle"           # window snapping; scriptable via rectangle:// URLs
cask "visual-studio-code"
cask "iterm2"
cask "github"              # GitHub Desktop

# ── Hardware ─────────────────────────────────────────────────────────
cask "elgato-control-center"   # stream lights
cask "displaylink"             # DisplayLink driver for the UGREEN UG69PD10 dock (4 screens)
cask "instantview"             # Silicon Motion USB display dock
cask "betterdisplay"           # software dimming per monitor (the dock blocks DDC brightness)

# ── Fonts ────────────────────────────────────────────────────────────
cask "font-fira-code-nerd-font"
cask "font-ubuntu-mono-nerd-font"
cask "font-noto-color-emoji"

# ── Global npm ───────────────────────────────────────────────────────
# brew bundle can't pin npm versions: it matches entries to `npm ls -g` by bare name, so a "name@1.2.3" entry
# always reads as missing (`brew bundle check` fails, every run reinstalls) and `cleanup` would remove the
# package. It does install with --ignore-scripts and a minimum release age. Versions known good are noted here;
# to pin by hand: `npm install -g --ignore-scripts name@version`.
npm "corepack"

# ── VS Code extensions ───────────────────────────────────────────────
vscode "ahmadawais.shades-of-purple"
vscode "alefragnani.project-manager"
vscode "alexandernanberg.horizon-theme-vscode"
vscode "anthropic.claude-code"
vscode "astro-build.astro-vscode"
vscode "atomiks.moonlight"
vscode "chakrounanas.turbo-console-log"
vscode "cmstead.js-codeformer"
vscode "dbaeumer.vscode-eslint"
vscode "dkundel.vscode-new-file"
vscode "docker.docker"
vscode "dotjoshjohnson.xml"
vscode "eamodio.gitlens"
vscode "esbenp.prettier-vscode"
vscode "forgng.theme-cotton-candy"
vscode "formulahendry.auto-rename-tag"
vscode "github.vscode-github-actions"
vscode "github.vscode-pull-request-github"
vscode "jonkwheeler.styled-components-snippets"
vscode "kisstkondoros.vscode-gutter-preview"
vscode "ms-azuretools.vscode-containers"
vscode "ms-playwright.playwright"
vscode "ms-python.black-formatter"
vscode "ms-python.debugpy"
vscode "ms-python.python"
vscode "ms-python.vscode-pylance"
vscode "ms-python.vscode-python-envs"
vscode "ms-vscode-remote.remote-containers"
vscode "ms-vscode.live-server"
vscode "ms-vscode.vscode-typescript-next"
vscode "msjsdiag.vscode-react-native"
vscode "patbenatar.advanced-new-file"
vscode "rvest.vs-code-prettier-eslint"
vscode "sleistner.vscode-fileutils"
vscode "streetsidesoftware.code-spell-checker"
vscode "wayou.vscode-todo-highlight"
vscode "wmaurer.change-case"
