# Hyprland Workflows and Common Tasks

## Configuration Workflow

### 1. Understanding the Request
Determine what the user needs:
- **New configuration**: Start from scratch or use minimal template
- **Modification**: Edit existing config (ask user to provide current config)
- **Troubleshooting**: Identify syntax errors or config issues
- **Feature addition**: Add specific functionality (keybinds, rules, etc.)
- **Optimization**: Improve performance or aesthetics

### 2. Gathering Context
Ask clarifying questions when needed:
- Monitor setup (resolution, refresh rate, arrangement)
- Preferred keybinding modifier (SUPER, ALT, CTRL)
- Desired layout (dwindle, master)
- Aesthetic preferences (gaps, rounding, animations)
- Hardware specifics (NVIDIA GPU, laptop, touchpad)

### 3. Loading References
Always load the appropriate reference files:
- `references/config_reference.md`: For understanding syntax, all available variables, and their options
- `references/examples.md`: For complete working configurations and common patterns

### 4. Searching Documentation
If the references don't contain the needed information:
```bash
python3 scripts/search_hyprland_docs.py "<query>"
```

### 5. Creating Configuration
- **Location**: `~/.config/hypr/hyprland.conf`
- **Principles**: Use variables ($mainMod), comment sections clearly, group related settings, use `source` for modularity.

## Common Tasks

### Creating a New Configuration
1. Load `references/examples.md` and find the "Complete Minimal Configuration"
2. Customize based on user's needs
3. Add monitor setup if multi-monitor
4. Configure keybindings with user's preferred modifier
5. Add autostart applications

### Adding Keybindings
1. Check `references/config_reference.md` for bind syntax
2. Use `$mainMod` variable for consistency
3. Common bind types: `bind` (normal), `bindm` (mouse), `binde` (repeat), `bindr` (release), `bindl` (locked).

### Configuring Window Rules
1. Check `references/config_reference.md` for windowrule syntax
2. Use `windowrulev2` for modern syntax
3. Test rules with: `hyprctl clients` (lists window classes)

### Troubleshooting
- **Syntax errors**: Check for missing commas, brackets, or quotes
- **Wrong variable names**: Search documentation to verify
- **Monitor not detected**: Try `hyprctl monitors`
- **Keybinds not working**: Ensure no conflicts, check modifier keys
- **Performance issues**: Reduce blur passes, disable animations, check `misc.vfr`

**Debugging commands**:
```bash
hyprctl monitors
hyprctl clients
hyprctl reload
hyprctl getoption general:border_size
hyprctl keyword general:border_size 3
```
