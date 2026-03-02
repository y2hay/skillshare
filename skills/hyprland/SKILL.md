---
name: hyprland
description: "Comprehensive Hyprland Wayland compositor configuration skill. Use when users need help with: (1) Creating or modifying Hyprland config files, (2) Setting up keybindings, window rules, monitors, or animations, (3) Troubleshooting Hyprland configuration issues, (4) Searching for valid config variables and values, (5) Understanding Hyprland syntax and structure, (6) Setting up multi-monitor configurations, (7) Configuring input devices, decorations, or layouts, or (8) Any other Hyprland-related configuration tasks."
---

<skill>
<objective>
Provide comprehensive support for configuring and troubleshooting Hyprland, a dynamic tiling Wayland compositor, using official documentation and best practices.
</objective>

<quick_start>
Use `scripts/search_hyprland_docs.py` to find configuration variables. Load `references/config_reference.md` for syntax and `references/examples.md` for patterns. Apply changes to `~/.config/hypr/hyprland.conf`.
</quick_start>

<success_criteria>
- Configuration changes follow correct Hyprland syntax and conventions
- `hyprctl reload` or `hyprctl keyword` commands are used to validate and apply settings
- High DPI and NVIDIA-specific configurations are applied correctly when relevant
- Multi-monitor setups are logically arranged and functional
</success_criteria>

<documentation_search>
Use the search script to find configuration variables, keybindings, and documentation:
```bash
python3 scripts/search_hyprland_docs.py "QUERY"
```
The script searches local markdown documentation in `references/docs/` (synced from wiki.hypr.land).
</documentation_search>

<documentation_index>
| Section | File |
|---------|------|
| Variables | `references/docs/variables.md` |
| Keywords | `references/docs/keywords.md` |
| Binds | `references/docs/binds.md` |
| Animations | `references/docs/animations.md` |
| Dispatchers | `references/docs/dispatchers.md` |
| Window Rules | `references/docs/window-rules.md` |
| Monitors | `references/docs/monitors.md` |
</documentation_index>

<output_guidelines>
1. **Always include comments** explaining sections and non-obvious settings
2. **Use proper syntax** - verify with references before providing
3. **Provide complete sections** - don't leave partial configurations
4. **Explain what you've done** - help the user understand the config
5. **Use variables** (e.g., `$mainMod = SUPER`) for consistency
</output_guidelines>

<resources>
<reference_index>
- **references/config_reference.md**: Complete syntax guide and variable reference
- **references/examples.md**: Practical working configurations for common use cases
- **references/workflows-and-tasks.md**: Detailed configuration and troubleshooting workflows
- **references/patterns-and-considerations.md**: Multi-monitor, gaming, and hardware-specific patterns
</reference_index>

<scripts_index>
- **scripts/search_hyprland_docs.py**: Fast offline search of Hyprland documentation
</scripts_index>
</resources>
</skill>
