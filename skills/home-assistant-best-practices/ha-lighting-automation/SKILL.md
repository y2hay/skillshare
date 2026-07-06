---

name: ha-lighting-automation
description: |
  Use when building Home Assistant lighting automations; triggers include "Home Assistant lights", "Pico remote automation", "dynamic light group", and "all lights automation". Covers template-based dynamic light groups and Lutron Caseta Pico remotes.
metadata:
  version: 1

---

# HA Lighting Automation

Patterns for dynamic light control and Lutron Pico remote automations in Home Assistant.

## Template Lights — Dynamic All-Lights Entity

For a single entity that controls every light (current and future), use the `template` light platform:

```yaml
- platform: template
  lights:
    all_lights:
      friendly_name: "All Lights"
      turn_on:
        - action: light.turn_on
          data:
            entity_id: >-
              {{ states.light | map(attribute='entity_id') | list }}
      turn_off:
        - action: light.turn_off
          data:
            entity_id: >-
              {{ states.light | map(attribute='entity_id') | list }}
      set_level:
        - action: light.turn_on
          data:
            entity_id: >-
              {{ states.light | map(attribute='entity_id') | list }}
            brightness: "{{ brightness }}"
```

**Key details:**
- Uses `>-` (folded block scalar with strip) to avoid YAML parsing issues with Jinja2 templates
- `set_level` receives `brightness` as a built-in variable from the template light framework
- The `entity_id` template dynamically resolves all entities in the `light` domain at runtime
- **Caveat:** Template lights require a **full HA restart** to load — `reload_core_config` won't create them

### Inline Template in Automations (no restart needed)

Instead of creating a template light entity, use an inline template in the automation itself:

```yaml
actions:
  - action: light.turn_on
    target:
      entity_id: "{{ states.light | map(attribute='entity_id') | list }}"
```

This dynamically resolves all lights at runtime. New lights are included automatically.

## Lutron Caseta Pico Remote Automations

### Device Trigger Pattern

Pico remotes use device-based triggers with `type: press` and `subtype` for each button:

```yaml
- alias: "Pico On — All lights"
  mode: single
  triggers:
  - platform: device
    domain: lutron_caseta
    device_id: "<device_id>"
    type: press
    subtype: true
  actions:
  - action: light.turn_on
    target:
      entity_id: light.all_lights
```

### Button Mapping

| Pico Button | `subtype` value |
|---|---|
| On | `true` |
| Raise | `raise` |
| Stop | `stop` |
| Lower | `lower` |
| Off | `off` |

### Finding Device IDs

```bash
ssh root@<host> "python3 << 'PYEOF'
import json
with open('/config/.storage/core.device_registry') as f:
    data = json.load(f)
for d in data['data']['devices']:
    name = d.get('name', '') or ''
    if 'Pico' in name:
        print(f'Name: {name}  ID: {d[\"id\"]}')
PYEOF"
```

### Full 5-Button Automation Set

```yaml
# On → Turn on all lights
- alias: "Pico On"
  triggers:
    - platform: device
      domain: lutron_caseta
      device_id: "<id>"
      type: press
      subtype: true
  actions:
    - action: light.turn_on
      target:
        entity_id: light.all_lights

# Raise → Brightness +15%
- alias: "Pico Raise"
  triggers:
    - platform: device
      domain: lutron_caseta
      device_id: "<id>"
      type: press
      subtype: raise
  actions:
    - action: light.turn_on
      target:
        entity_id: light.all_lights
      data:
        brightness_step_pct: 15

# Stop → Resync adaptive lighting
- alias: "Pico Stop"
  triggers:
    - platform: device
      domain: lutron_caseta
      device_id: "<id>"
      type: press
      subtype: stop
  actions:
    - action: adaptive_lighting.apply
      data:
        entity_id: switch.adaptive_lighting_circadian

# Lower → Brightness -15%
- alias: "Pico Lower"
  triggers:
    - platform: device
      domain: lutron_caseta
      device_id: "<id>"
      type: press
      subtype: lower
  actions:
    - action: light.turn_on
      target:
        entity_id: light.all_lights
      data:
        brightness_step_pct: -15

# Off → Turn off all lights
- alias: "Pico Off"
  triggers:
    - platform: device
      domain: lutron_caseta
      device_id: "<id>"
      type: press
      subtype: 'off'
  actions:
    - action: light.turn_off
      target:
        entity_id: light.all_lights
```

### Duplicating for Multiple Remotes

Copy the 5 automations, change the `device_id` and alias names. Each Pico has its own device ID in the device registry.

## Writing Complex Files to HA VM

When heredoc escaping fails (nested quotes, Jinja2 templates with single quotes), use a two-step approach:

1. Write the file locally with `write_file` tool
2. Copy it to the HA VM via `scp`:

```bash
scp /tmp/<file> root@<ha_ip>:/config/packages/<file>
```

This avoids shell escaping issues with complex YAML containing Jinja2 templates.

## Communication: Git Operations

When performing git operations on the HA config repo, **do not use git jargon without explanation**. The user does not speak git. Translate every operation:

| Instead of | Say |
|---|---|
| "Committed to main" | "Saved everything — you can go back to this state later" |
| "Working tree clean" | "All files match what's saved — nothing pending" |
| "Staged changes" | "Picked which files to save" |
| "SHA abc1234" | Don't use — say "the last save" |