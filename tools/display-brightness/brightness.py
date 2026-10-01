#!/usr/bin/python3
"""Day/night brightness for the external monitors, through BetterDisplay's software dimming.

The dock blocks DDC, so BetterDisplay must be running. Usage:
  brightness.py day | night      apply a preset now
  brightness.py toggle           switch between them
  brightness.py up | down        all monitors ±10%
  brightness.py auto             apply the preset for the time of day, only when sunrise/sunset
                                 has passed since the last run (so manual changes stick until then)
  brightness.py status
"""
from __future__ import annotations

import json
import math
import subprocess
import sys
from datetime import date, datetime, timedelta, timezone
from pathlib import Path

BD = "/Applications/BetterDisplay.app/Contents/MacOS/BetterDisplay"
STATE = Path.home() / "Library/Application Support/Roland/display-brightness.json"

# Chicago. Night = from sunset to sunrise.
LAT, LON = 41.88, -87.63

# Software brightness (0–1) per monitor, by BetterDisplay UUID. Night levels set by Nicholas 2026-09-30.
MONITORS = {
    "101256C3-F527-4A72-BAC4-937FDECF4DDF": ("Sceptre Z27", 0.449),
    "9D0882DB-974B-4BAD-90BE-AC881AA58DDB": ("C27M2020", 0.30),
    "C2CF7685-49EC-46D0-9782-5EF7B7D4261D": ("KB272HL H 1", 0.174),
    "32C850D5-F8AC-4729-AC4C-594998D5B738": ("KB272HL H 2", 0.096),
}
DAY = 1.0
STEP = 0.10


def bd(*args: str) -> str:
    r = subprocess.run([BD, *args], capture_output=True, text=True, timeout=15)
    return r.stdout.strip()


def get(uuid: str) -> float | None:
    try:
        return float(bd("get", f"-UUID={uuid}", "-softwareBrightness"))
    except ValueError:
        return None  # monitor unplugged or BetterDisplay not running


def put(uuid: str, value: float) -> None:
    bd("set", f"-UUID={uuid}", f"-softwareBrightness={max(0.0, min(1.0, value)):.3f}")


def apply(mode: str) -> None:
    for uuid, (_, night) in MONITORS.items():
        put(uuid, DAY if mode == "day" else night)
    save({**load(), "mode": mode})


def sun_times(day: date) -> tuple[datetime, datetime]:
    """Sunrise and sunset (UTC) for LAT/LON, NOAA approximation (good to a couple of minutes)."""
    n = day.timetuple().tm_yday
    g = 2 * math.pi / 365 * (n - 1)
    eqtime = 229.18 * (0.000075 + 0.001868 * math.cos(g) - 0.032077 * math.sin(g)
                       - 0.014615 * math.cos(2 * g) - 0.040849 * math.sin(2 * g))
    decl = (0.006918 - 0.399912 * math.cos(g) + 0.070257 * math.sin(g) - 0.006758 * math.cos(2 * g)
            + 0.000907 * math.sin(2 * g) - 0.002697 * math.cos(3 * g) + 0.00148 * math.sin(3 * g))
    lat = math.radians(LAT)
    ha = math.degrees(math.acos(math.cos(math.radians(90.833)) / (math.cos(lat) * math.cos(decl))
                                - math.tan(lat) * math.tan(decl)))
    midnight = datetime(day.year, day.month, day.day, tzinfo=timezone.utc)
    rise = midnight + timedelta(minutes=720 - 4 * (LON + ha) - eqtime)
    sset = midnight + timedelta(minutes=720 - 4 * (LON - ha) - eqtime)
    return rise, sset


def period_now() -> tuple[str, str]:
    """('day'|'night', an id for the current day/night period)."""
    now = datetime.now(timezone.utc)
    today = datetime.now().date()
    rise, sset = sun_times(today)
    if now < rise:
        return "night", f"{today - timedelta(days=1)}-night"
    if now < sset:
        return "day", f"{today}-day"
    return "night", f"{today}-night"


def load() -> dict:
    try:
        return json.loads(STATE.read_text())
    except (OSError, ValueError):
        return {}


def save(state: dict) -> None:
    STATE.parent.mkdir(parents=True, exist_ok=True)
    STATE.write_text(json.dumps(state))


def main(cmd: str) -> None:
    if cmd in ("day", "night"):
        apply(cmd)
    elif cmd == "toggle":
        apply("night" if load().get("mode") == "day" else "day")
    elif cmd in ("up", "down"):
        for uuid in MONITORS:
            cur = get(uuid)
            if cur is not None:
                put(uuid, cur + (STEP if cmd == "up" else -STEP))
    elif cmd == "auto":
        mode, period = period_now()
        state = load()
        if state.get("period") != period:
            # Only act once per period, and only if the monitors are there to take it.
            if any(get(u) is not None for u in MONITORS):
                apply(mode)
                save({**load(), "period": period})
                print(f"{datetime.now():%F %T} {period}: applied {mode}", flush=True)
    elif cmd == "status":
        rise, sset = sun_times(datetime.now().date())
        print(f"now: {period_now()[0]}  sunrise {rise.astimezone():%H:%M}  sunset {sset.astimezone():%H:%M}")
        print(f"last preset: {load().get('mode')}")
        for uuid, (name, night) in MONITORS.items():
            print(f"  {name}: {get(uuid)}  (night {night})")
    else:
        sys.exit(__doc__)


if __name__ == "__main__":
    main(sys.argv[1] if len(sys.argv) > 1 else "")
