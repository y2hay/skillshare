---
name: dms-wallpaper-cycling
description: Diagnose and fix Dank Material Shell wallpaper stuck while matugen colors cycle
category: devops
version: 1
triggers: ["wallpaper stuck", "colors cycle", "DMS wallpaper", "matugen"]
---

<skill>
<quick_start>
When DMS wallpaper image stops changing but matugen color cycling continues (every 5m), the two mechanisms have drifted apart. Check `wallpaperCyclingEnabled` in DMS settings and toggle it on — no restart needed.
</quick_start>

<setup>
No external credentials or dependencies required. All diagnostics use local file inspection and journalctl on the niri/DMS host.

Required tools:
- `journalctl` (systemd-journal)
- `niri msg` (niri compositor)
- `grep` / basic shell
</setup>

<objective>
Diagnose and resolve the root cause when DMS wallpaper cycling stalls while matugen color extraction continues working.
</objective>

<success_criteria>
- Wallpaper image changes on every 5-minute cycle tick
- `grep wallpaperCycling ~/.config/DankMaterialShell/settings.json` returns `true`
- Journal logs show both `Processing theme` (matugen) and wallpaper cycling events
- No manual intervention needed after settings change — DMS auto-reloads
</success_criteria>

## Architecture

DMS on niri has TWO independent cycling mechanisms:

1. **Go backend matugen cycle** — Picks random images, extracts colors, applies to apps. Active when `currentThemeName: dynamic`.
2. **QML WallpaperCyclingService** — Actually sets the on-screen wallpaper image via `SessionData.setWallpaper()`. Controlled by `wallpaperCyclingEnabled` (default: false).

The Go backend feeds images to matugen but does NOT update `SessionData.wallpaperPath` — that's the wallpaper cycle's job.

## Diagnosis

1. Check if wallpaper cycling is enabled:
   ```bash
   grep -E "wallpaperCycling" ~/.config/DankMaterialShell/settings.json
   ```

2. Check journal for matugen cycling (working) vs wallpaper updates (missing):
   ```bash
   journalctl --user -u dms --since "1 hour ago" | grep -iE "Processing theme|setWallpaper|cycling"
   ```

3. Verify niri background layer is alive:
   ```bash
   niri msg outputs 2>/dev/null | grep -A5 "Background layer"
   ```

## Fix

Add to `~/.config/DankMaterialShell/settings.json`:
```json
"wallpaperCyclingEnabled": true,
"wallpaperCyclingMode": "interval",
"wallpaperCyclingInterval": 300
```

DMS watches the config file — no restart needed. The next 5-minute tick will fire wallpaper cycling.

## Pitfalls

- `wallpaperShufflerPlugin` is a legacy GNOME extension plugin — NOT used by the niri quickshell implementation. Don't try to enable it.
- `wallpaperCarousel` is a UI feature (thumbnail browser), not background cycling.
- The WallpaperCyclingService uses `find` to enumerate images in the wallpaper directory's parent folder, then cycles sequentially through the sorted list.

<error_handling>
- If `settings.json` is missing, DMS uses defaults — create it with the settings above
- If journal shows no DMS entries, DMS may not be running: `systemctl --user status dms`
- If `niri msg` fails, you're not running under niri — run diagnostics from the niri session
- If wallpaper still doesn't cycle after setting `wallpaperCyclingEnabled: true`, restart DMS: `systemctl --user restart dms`
</error_handling>
</skill>
