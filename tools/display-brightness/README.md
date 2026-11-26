# display-brightness

Day/night brightness for the four external monitors. They run through the UGREEN DisplayLink dock, which
blocks DDC, so this uses BetterDisplay's software dimming (BetterDisplay must be running; it is a login item).

- `brightness.py day|night|toggle|up|down|auto|status`. Night levels per monitor are in `MONITORS`
  (set by Nicholas 2026-09-30); day is 100%. To change night levels, set them in BetterDisplay and copy
  `brightness.py status` into `MONITORS`.
- Automatic: launchd `com.nicholai.display-brightness` (symlinked plist here) runs `auto` every minute and at
  login. It applies the preset once per sunrise/sunset in Chicago, and again when the monitors are plugged in
  (so plugging in after sunset dims them), so a manual change holds until the next one. It starts
  BetterDisplay if it isn't running. State `~/Library/Application Support/Roland/display-brightness.json`, log
  `~/Library/Logs/display-brightness.log`.
- On another Mac: `setup.sh` doesn't install this. The plist names this Mac's home folder, so write a copy with the
  right one, load it, and start skhd (which then needs Accessibility in System Settings):
  `sed "s|/Users/nicholasmorrow|$HOME|g" com.nicholai.display-brightness.plist > ~/Library/LaunchAgents/com.nicholai.display-brightness.plist`,
  `launchctl bootstrap gui/$UID ~/Library/LaunchAgents/com.nicholai.display-brightness.plist`, `skhd --start-service`.
  Not yet tried on a second Mac: if BetterDisplay gives the monitors different IDs there, `brightness.py status`
  shows them and `MONITORS` needs those too.
- Hotkeys (skhd, config in dotfiles `skhd/skhdrc`): ⌃⌥⌘B toggle day/night, ⌃⌥⌘↑ / ⌃⌥⌘↓ all monitors ±10%.
