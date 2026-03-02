## Integration Templates

### Standard Integration Structure
```
homeassistant/components/my_integration/
├── __init__.py          # Entry point with async_setup_entry
├── manifest.json        # Integration metadata and dependencies
├── const.py            # Domain and constants
├── config_flow.py      # UI configuration flow
├── coordinator.py      # Data update coordinator (if needed)
├── entity.py          # Base entity class (if shared patterns)
├── sensor.py          # Sensor platform
├── strings.json        # User-facing text and translations
├── services.yaml       # Service definitions (if applicable)
└── quality_scale.yaml  # Quality scale rule status
```

An integration can have platforms as needed (e.g., `sensor.py`, `switch.py`, etc.). The following platforms have extra guidelines:
- **Diagnostics**: [`platform-diagnostics.md`](platform-diagnostics.md) for diagnostic data collection
- **Repairs**: [`platform-repairs.md`](platform-repairs.md) for user-actionable repair issues

### Minimal Integration Checklist
- [ ] `manifest.json` with required fields (domain, name, codeowners, etc.)
- [ ] `__init__.py` with `async_setup_entry` and `async_unload_entry`
- [ ] `config_flow.py` with UI configuration support
- [ ] `const.py` with `DOMAIN` constant
- [ ] `strings.json` with at least config flow text
- [ ] Platform files (`sensor.py`, etc.) as needed
- [ ] `quality_scale.yaml` with rule status tracking

## Integration Quality Scale

Home Assistant uses an Integration Quality Scale to ensure code quality and consistency. The quality level determines which rules apply:

### Quality Scale Levels
- **Bronze**: Basic requirements (ALL Bronze rules are mandatory)
- **Silver**: Enhanced functionality
- **Gold**: Advanced features
- **Platinum**: Highest quality standards

### Quality Scale Progression
- **Bronze → Silver**: Add entity unavailability, parallel updates, auth flows
- **Silver → Gold**: Add device management, diagnostics, translations
- **Gold → Platinum**: Add strict typing, async dependencies, websession injection

### How Rules Apply
1. **Check `manifest.json`**: Look for `"quality_scale"` key to determine integration level
2. **Bronze Rules**: Always required for any integration with quality scale
3. **Higher Tier Rules**: Only apply if integration targets that tier or higher
4. **Rule Status**: Check `quality_scale.yaml` in integration folder for:
   - `done`: Rule implemented
   - `exempt`: Rule doesn't apply (with reason in comment)
   - `todo`: Rule needs implementation

### Example `quality_scale.yaml` Structure
```yaml
rules:
  # Bronze (mandatory)
  config-flow: done
  entity-unique-id: done
  action-setup:
    status: exempt
    comment: Integration does not register custom actions.

  # Silver (if targeting Silver+)
  entity-unavailable: done
  parallel-updates: done

  # Gold (if targeting Gold+)
  devices: done
  diagnostics: done

  # Platinum (if targeting Platinum)
  strict-typing: done
```

**When Reviewing/Creating Code**: Always check the integration's quality scale level and exemption status before applying rules.

