---
name: "source-command-hypr"
description: "Hyprland compositor helper commands"
---

# source-command-hypr

Use this skill when the user asks to run the migrated source command `hypr`.

## Command Template

# Hyprland Helper

Common Hyprland operations and quick access to configuration.

## Quick commands

| Command | Description |
|---------|-------------|
| `hyprctl reload` | Reload configuration |
| `hyprctl clients` | List all windows |
| `hyprctl activewindow` | Current focused window info |
| `hyprctl binds` | Show all keybindings |
| `hyprctl devices` | List input devices |
| `hyprctl monitors` | Show monitor configuration |
| `hyprctl version` | Hyprland version info |

## Configuration locations

- **Main config:** `~/.config/hypr/hyprland.conf`
- **Keybinds:** `~/.config/hypr/conf.d/keybinds.conf`
- **Monitors:** `~/.config/hypr/conf.d/monitors.conf`
- **Autostart:** `~/.config/hypr/conf.d/autostart.conf`
- **Animations:** `~/.config/hypr/conf.d/animations.conf`
- **Quickshell config:** `/etc/xdg/quickshell/`

## Troubleshooting

- **Hyprland logs:** `journalctl --user -u hyprland`
- **Quickshell issues:** Run `/qs` to rebuild after Qt updates
- **Check keybind conflicts:** `hyprctl binds | grep -i <key>`
