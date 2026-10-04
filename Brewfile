# Everything installed on Nicholas's Macs. Install with ./setup.sh (or `brew bundle`).

# ── CLI ──────────────────────────────────────────────────────────────
brew "gh"                  # GitHub CLI
brew "git-filter-repo"     # rewrite git history
brew "gitleaks"            # scan for secrets before publishing a repo
brew "mas"                 # App Store installs below
brew "fzf"
brew "ripgrep"
brew "the_silver_searcher"
brew "vim"
brew "ffmpeg"
brew "yt-dlp"
brew "watchman"
brew "cocoapods"
brew "deno"
brew "bun"                 # JS runtime + package manager (CodeCrafters TypeScript challenges)
brew "node"                # default Node; stable path for global npm tools
brew "defaultbrowser"      # set default browser (used by macos.sh)
brew "uv"                  # Python + runs the Logseq MCP server (replaces pyenv/poetry/conda)
brew "awscli"
tap "keith/formulae"
brew "keith/formulae/reminders-cli"   # Apple Reminders CLI (life-mcp)
brew "xcodegen"            # generates Xcode projects (life-mcp's HomeKit helper app)
brew "llama.cpp"            # local LLMs: llama-server, llama-bench (~/Projects/local-llm)
brew "opencode"             # coding agent for the local model (config in dotfiles)
brew "koekeishiya/formulae/skhd"   # global hotkeys (config in dotfiles skhd/skhdrc)
brew "geckodriver"          # WebDriver for Firefox (Selenium scripts)
brew "resvg"                # SVG → PNG for Midnight Sun app icons
brew "tokei"                # count lines of code by language (research: codebase history)
brew "tmux"                 # terminal multiplexer (drives a Claude Code session headlessly to screenshot mods)

# ── Apps ─────────────────────────────────────────────────────────────
cask "claude"
cask "claude-code"         # CLI agent
cask "opencode-desktop"   # coding agent app for the local model (~/Projects/local-llm)
cask "sync"                # Sync.com → ~/Sync
cask "google-chrome"
cask "brave-browser"
cask "firefox"
cask "linear"
cask "logseq"
cask "signal"
cask "discord"
cask "zoom"
cask "spotify"
cask "vlc"
cask "anki"
cask "figma"
cask "expressvpn"
# qBittorrent (BitTorrent) is installed by hand from qbittorrent.org: Homebrew disabled its cask on 2026-09-01 (fails Gatekeeper). After copying it to /Applications: xattr -dr com.apple.quarantine /Applications/qbittorrent.app
cask "rectangle"           # window snapping; scriptable via rectangle:// URLs (replaces Magnet)

# ── Dev ──────────────────────────────────────────────────────────────
cask "visual-studio-code"
cask "iterm2"
cask "github"              # GitHub Desktop
cask "orbstack"            # Docker and Linux VMs
cask "ngrok"
cask "tailscale-app"       # tailnet + Funnel
cask "raspberry-pi-imager"

# ── Hardware ─────────────────────────────────────────────────────────
cask "elgato-control-center"   # stream lights
cask "displaylink"             # DisplayLink driver for the UGREEN UG69PD10 dock (4 screens)
cask "instantview"             # Silicon Motion USB display dock
cask "betterdisplay"           # software dimming per monitor (the dock blocks DDC brightness)

# ── Fonts ────────────────────────────────────────────────────────────
cask "font-fira-code-nerd-font"
cask "font-ubuntu-mono-nerd-font"
cask "font-noto-color-emoji"

# ── App Store (sign in to the App Store app first) ───────────────────
mas "Bitwarden", id: 1352778147
mas "Fantastical", id: 975937182
mas "Magnet", id: 441258766
mas "Slack", id: 803453959
mas "Kindle", id: 302584613
mas "Streaks", id: 963034692
mas "RadarScope", id: 288419283
mas "Health Auto Export", id: 1115567069
mas "Family Tools", id: 1541899076
mas "GIPHY Capture", id: 668208984
mas "MindNode", id: 6446116532
mas "Keynote", id: 361285480
mas "Numbers", id: 361304891
mas "Pages", id: 361309726
mas "GarageBand", id: 682658836
mas "iMovie", id: 408981434
mas "Xcode", id: 497799835  # ~15 GB

# ── Global npm ───────────────────────────────────────────────────────
# brew bundle can't pin npm versions: it matches entries to `npm ls -g` by bare name, so a "name@1.2.3" entry
# always reads as missing (`brew bundle check` fails, every run reinstalls) and `cleanup` would remove the
# package. It does install with --ignore-scripts and a minimum release age. Versions known good are noted here;
# to pin by hand: `npm install -g --ignore-scripts name@version`.
npm "corepack"
npm "eight-sleep-mcp-unofficial"   # Eight Sleep MCP server (life-mcp); known good: 0.2.13

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
vscode "ms-python.black-formatter"
vscode "ms-azuretools.vscode-containers"
vscode "ms-playwright.playwright"
vscode "ms-python.debugpy"
vscode "ms-python.python"
vscode "ms-python.vscode-pylance"
vscode "ms-python.vscode-python-envs"
vscode "ms-vscode.live-server"
vscode "ms-vscode.vscode-typescript-next"
vscode "msjsdiag.vscode-react-native"
vscode "patbenatar.advanced-new-file"
vscode "rvest.vs-code-prettier-eslint"
vscode "sleistner.vscode-fileutils"
vscode "streetsidesoftware.code-spell-checker"
vscode "vscodevim.vim"
vscode "wayou.vscode-todo-highlight"
vscode "wmaurer.change-case"
