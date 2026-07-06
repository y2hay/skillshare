---
name: dms-wallpaper-cycling
description: Diagnose and fix Dank Material Shell wallpaper stuck while matugen colors cycle
category: devops
---

# DMS Wallpaper Cycling Fix

When DMS wallpaper image stops changing but matugen color cycling continues (every 5m), the two mechanisms have drifted apart.

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
