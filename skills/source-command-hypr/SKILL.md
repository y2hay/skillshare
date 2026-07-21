---

name: "source-command-hypr"
description: |
  Use when managing Hyprland compositor commands; triggers include "Hyprland command", "hyprctl", "move window", "monitor config", and "Hyprland keybinds".
version: 1
triggers: ["hyprland", "hyprctl", "compositor", "window manager"]

---
<skill>
<objective>
Provide quick access to Hyprland compositor commands and configuration locations for window management, monitor setup, keybinding, and troubleshooting.
</objective>

<success_criteria>
- Commands execute correctly via hyprctl and return expected output
- Configuration files are correctly referenced and editable
- Troubleshooting steps resolve common compositor issues
</success_criteria>

<process>
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
</process>
</skill>
