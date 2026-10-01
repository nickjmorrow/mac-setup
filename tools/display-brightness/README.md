# display-brightness

Day/night brightness for the four external monitors. They run through the UGREEN DisplayLink dock, which
blocks DDC, so this uses BetterDisplay's software dimming (BetterDisplay must be running; it is a login item).

- `brightness.py day|night|toggle|up|down|auto|status`. Night levels per monitor are in `MONITORS`
  (set by Nicholas 2026-09-30); day is 100%. To change night levels, set them in BetterDisplay and copy
  `brightness.py status` into `MONITORS`.
- Automatic: launchd `com.nicholai.display-brightness` (symlinked plist here) runs `auto` every 5 minutes and
  at login. It applies the preset once per sunrise/sunset in Chicago, so a manual change holds until the next
  one. State `~/Library/Application Support/Roland/display-brightness.json`, log
  `~/Library/Logs/display-brightness.log`.
- Hotkeys (skhd, config in dotfiles `skhd/skhdrc`): ⌃⌥⌘B toggle day/night, ⌃⌥⌘↑ / ⌃⌥⌘↓ all monitors ±10%.
