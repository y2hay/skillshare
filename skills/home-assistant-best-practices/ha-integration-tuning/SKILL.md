---
name: ha-integration-tuning
description: >
  Direct .storage editing for HA integration config changes, API-based reload
  without restart, config modularization with !include, and integration-specific
  optimizations (Govee MQTT, Hue local push).
metadata:
  version: 1
---

# HA Integration Tuning

Techniques for modifying integration behavior by editing `.storage` files directly and reloading without a full HA restart.

## Prerequisites

- SSH root access to the HA host
- HA API long-lived access token (from `HASS_TOKEN` in `.env` or created in HA UI)
- Python3 on the HA host for JSON manipulation

## Integration Config Tuning via .storage

### Pattern: Edit → Reload → Verify

Integration config entries live in `/config/.storage/core.config_entries`. You can modify them directly, then reload the integration via the HA API.

### Step 1: Read Current Config

```bash
ssh root@<host> "python3 << 'PYEOF'
import json
with open('/config/.storage/core.config_entries') as f:
    data = json.load(f)
for e in data['data']['entries']:
    if e['domain'] == '<integration_domain>':
        print(json.dumps(e, indent=2))
PYEOF"
```

### Step 2: Edit and Write

```bash
ssh root@<host> "python3 << 'PYEOF'
import json
with open('/config/.storage/core.config_entries', 'r') as f:
    data = json.load(f)
for e in data['data']['entries']:
    if e['domain'] == '<integration_domain>':
        # Modify options or top-level fields
        e['options']['<key>'] = <value>
        # or e['<field>'] = <value>
        break
with open('/config/.storage/core.config_entries', 'w') as f:
    json.dump(data, f, indent=2)
print('Updated')
PYEOF"
```

### Step 3: Reload Without Restart

Use the HA REST API to reload just the config entry:

```bash
# Get the entry_id
ENTRY_ID=$(ssh root@<host> "python3 -c \"
import json
with open('/config/.storage/core.config_entries') as f:
    entries = json.load(f).get('data',{}).get('entries',[])
for e in entries:
    if e['domain']=='<integration_domain>':
        print(e['entry_id'])
        break
\"")

# Reload via API
curl -s -X POST \
  -H "Authorization: Bearer $HASS_TOKEN" \
  -H "Content-Type: application/json" \
  -d "{\"entry_id\": \"$ENTRY_ID\"}" \
  "https://<ha_url>/api/services/homeassistant/reload_config_entry"
```

Returns `[]` on success.

### Step 4: Verify

```bash
ssh root@<host> "ha core logs | grep -i '<integration_domain>' | tail -5"
```

## Integration-Specific Optimizations

### Govee (lasswellt/govee-homeassistant)

This custom component uses AWS IoT MQTT for device control. Key settings in `options`:

| Setting | Default | Optimized | Effect |
|---------|---------|-----------|--------|
| `enable_mqtt_control` | `false` | `true` | Switches from REST API to MQTT. Eliminates DNS timeout errors to `openapi.api.govee.com:443`. |
| `enable_scenes` | `true` | `false` | Disables scene entity creation (reduces entity noise) |
| `enable_diy_scenes` | `true` | `false` | Disables DIY scene entity creation |
| `poll_interval` | `60` | `300` | Reduces polling frequency when MQTT pushes state |

**Pitfall:** The `enable_mqtt_control` option may not appear in the config entry until explicitly set. Add it to `options` dict if missing.

**Verification:** Check `sensor.govee_integration_mqtt_status` entity — should show `connected`.

### Hue

| Setting | Default | Optimized | Effect |
|---------|---------|-----------|--------|
| `pref_disable_polling` | `false` | `true` | Switches from cloud polling to local SSE push. Faster response, no cloud dependency. |

Set at the top level of the config entry (not in `options`):
```python
e['pref_disable_polling'] = True
```

## Config Modularization with !include

### The Key Insight

When using `!include` in HA YAML, the included file's content is inserted **under** the domain key. Therefore, package files must contain **only the value**, not the domain key.

**Wrong** — package file includes the domain key:
```yaml
# packages/lights.yaml
light:
  - platform: group
    name: Ambience
```
Result: `light: { light: [ ... ] }` — nested, invalid.

**Correct** — package file contains only the value:
```yaml
# packages/lights.yaml
- platform: group
  name: Ambience
```
Result: `light: [ ... ]` — flat, valid.

### Directory Structure

```
/config/
  configuration.yaml        # Main file with !include directives
  packages/
    lights.yaml             # Light group definitions
    frontend.yaml           # Frontend themes + card resources
    adaptive_lighting.yaml  # Adaptive lighting config
    recorder.yaml           # Recorder/database settings
    dashboards.yaml         # Lovelace dashboard definitions
```

### Main configuration.yaml Pattern

```yaml
default_config:
enable_ha_mcp: true          # Required for MCP integrations
http:
  use_x_forwarded_for: true
  trusted_proxies:
    - 127.0.0.1
    - 172.30.33.0/24
    - 10.10.0.0/24
automation: !include automations.yaml
script: !include scripts.yaml
scene: !include scenes.yaml
light: !include packages/lights.yaml
frontend: !include packages/frontend.yaml
adaptive_lighting: !include packages/adaptive_lighting.yaml
```

### Entity Name Verification

After modularizing, always verify entity names against the git-committed version:

```bash
cd /config && git diff HEAD -- configuration.yaml
```

The live file may have stale/divergent names from AI agent edits. The git-committed version is the source of truth.

## card-mod Double-Load Fix

The warning `CARD-MOD: hui-card already patched by 4.2.1!` means card-mod is loaded twice. Causes:

1. Listed in `extra_module_url` in frontend config
2. AND loaded by HACS as a frontend resource, or bundled by another custom card

**Fix:** Ensure card-mod appears exactly once in `extra_module_url`. Check HACS frontend resources in `.storage/lovelace_resources` — if card-mod is registered there, remove it from `extra_module_url` (or vice versa).

## References

See `references/govee-hue-tuning.md` for session-specific Govee/Hue config entry dumps and error patterns.