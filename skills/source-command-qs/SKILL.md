---
name: "source-command-qs"
description: "Rebuild quickshell after Qt updates to fix version mismatches and launch failures."
version: 1
triggers: ["quickshell", "rebuild qs", "qt mismatch", "rebuild quickshell"]
---

# source-command-qs

Use this skill when the user asks to run the migrated source command `qs`.

## Command Template

# Quickshell Rebuild

Rebuild quickshell when Qt version mismatches occur after system updates.

## What to do

### Option 1: Run the recovery script (recommended)
```bash
~/scripts/rebuild-quickshell.sh
```
This script:
1. First tries to rebuild from cached paru source (fastest)
2. Falls back to fresh AUR clone if cache fails
3. Provides manual fallback instructions if AUR build fails

### Option 2: Manual rebuild (fallback if script unavailable)
```bash
# Remove broken build and reinstall from AUR
paru -R quickshell
paru -S quickshell
```

### Option 3: Manual rebuild from source cache
```bash
# Rebuild from the PKGBUILD cache without re-fetching
cd ~/.cache/paru/clone/quickshell
makepkg -si --clean
```

## When this is needed

- After `pacman -Syu` updates Qt packages
- When quickshell fails to launch with Qt version errors
- When you see errors like "Qt version mismatch" or "cannot load library"

## Safety

> **⚠️ Important warnings before rebuilding:**

- **Qt rebuild time**: Rebuilding quickshell from source can take **10–30 minutes** depending on your system. Plan accordingly.
- **Hyprland process interruption**: Quickshell is your Hyprland shell/panel. If it fails to rebuild or the new build has issues, your panel/shell may be unavailable until you restart Hyprland or roll back.
- **Backup config**: Before rebuilding, backup your quickshell config:
  ```bash
  cp -r ~/.config/quickshell ~/.config/quickshell.bak
  ```
- **Rollback**: If the new build has issues, restart Hyprland (Super+Shift+M) or use `hyprctl reload` to restore previous session state.
