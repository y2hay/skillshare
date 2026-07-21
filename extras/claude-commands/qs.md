---
name: qs
description: Rebuild quickshell after Qt updates (fixes Qt version mismatches)
allowed-tools: ["Bash"]
---

# Quickshell Rebuild

Rebuild quickshell when Qt version mismatches occur after system updates.

## What to do

Run the quickshell recovery script:
```bash
~/scripts/rebuild-quickshell.sh
```

This script:
1. First tries to rebuild from cached paru source (fastest)
2. Falls back to fresh AUR clone if cache fails
3. Provides manual fallback instructions if AUR build fails

## When this is needed

- After `pacman -Syu` updates Qt packages
- When quickshell fails to launch with Qt version errors
- When you see errors like "Qt version mismatch" or "cannot load library"
