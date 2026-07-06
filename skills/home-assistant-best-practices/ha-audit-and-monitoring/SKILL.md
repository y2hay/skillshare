---
name: ha-audit-and-monitoring
description: >
  SSH-based HA config audit, entity registry inspection, integration health
  checks, and ongoing monitoring via Hermes agent profile + cron. Covers HAOS,
  Docker, and core installations.
metadata:
  version: 1
---

# HA Audit & Monitoring

SSH-based methodology for auditing and continuously monitoring a Home Assistant instance.

## Prerequisites

- SSH root access to the HA host
- For HAOS: `ha` CLI available natively
- For Docker: `docker exec homeassistant` prefix on commands

## Phase 1: Full Assessment

### System Overview

```bash
ssh root@<host> "ha info"
ssh root@<host> "df -h && free -h && nproc && uptime"
ssh root@<host> "docker ps --format '{{.Names}} {{.Status}} {{.Image}}'"
```

### Configuration Structure

```bash
ssh root@<host> "cat /config/configuration.yaml"
ssh root@<host> "ls -la /config/"
ssh root@<host> "ls /config/packages/ 2>/dev/null || echo 'No packages dir'"
ssh root@<host> "ls /config/custom_components/"
ssh root@<host> "ls /config/www/"
```

### Entity Registry Analysis

Use Python heredocs to avoid SSH quoting issues:

```bash
ssh root@<host> "python3 << 'PYEOF'
import json
from collections import Counter

with open('/config/.storage/core.entity_registry') as f:
    data = json.load(f)
entities = data.get('data', {}).get('entities', [])

total = len(entities)
assigned = sum(1 for e in entities if e.get('area_id'))
disabled = sum(1 for e in entities if e.get('disabled_by'))
hidden = sum(1 for e in entities if e.get('hidden_by'))

print(f'Total entities: {total}')
print(f'Area-assigned: {assigned}')
print(f'Unassigned: {total - assigned}')
print(f'Disabled: {disabled}')
print(f'Hidden: {hidden}')

domains = Counter(e['entity_id'].split('.')[0] for e in entities)
for domain, count in domains.most_common(25):
    print(f'  {domain}: {count}')
PYEOF"
```

### Integration Health

```bash
ssh root@<host> "python3 << 'PYEOF'
import json
from collections import Counter

with open('/config/.storage/core.config_entries') as f:
    data = json.load(f)
entries = data.get('data', {}).get('entries', [])

print(f'Total integrations: {len(entries)}')
domains = Counter(e['domain'] for e in entries)
for domain, count in domains.most_common():
    disabled = sum(1 for e in entries if e['domain'] == domain and e.get('disabled_by'))
    print(f'  {domain}: {count}' + (' (DISABLED)' if disabled else ''))

# Check specific integrations
for e in entries:
    if e['domain'] in ('govee', 'hue'):
        print(f'\n--- {e["domain"]} ---')
        print(f'  Title: {e.get("title")}')
        print(f'  Source: {e.get("source")}')
        print(f'  Disabled: {e.get("disabled_by", "no")}')
        d = e.get('data', {})
        if e['domain'] == 'govee':
            print(f'  API Key set: {bool(d.get("api_key"))}')
            print(f'  LAN Discovery: {d.get("lan_discovery", "not set")}')
        if e['domain'] == 'hue':
            print(f'  Bridge IP: {d.get("host")}')
            print(f'  Polling disabled: {d.get("pref_disable_polling", "not set")}')
PYEOF"
```

### Area Registry

```bash
ssh root@<host> "python3 << 'PYEOF'
import json
with open('/config/.storage/core.area_registry') as f:
    data = json.load(f)
areas = data.get('data', {}).get('areas', [])
print(f'Total areas: {len(areas)}')
for a in areas:
    name = a.get('name', '?')
    aid = a.get('area_id', '?')[:12]
    print(f'  - {name} (id: {aid}...)')
PYEOF"
```

### Log Analysis

```bash
# HAOS
ssh root@<host> "ha core logs | grep -i -E 'error|critical|traceback' | tail -30"
ssh root@<host> "ha core logs | grep -i -E 'warning' | tail -20"

# Docker
ssh root@<host> "journalctl -u homeassistant --since '24 hours ago' --no-pager | grep -i -E 'error|critical|traceback|fail' | tail -30"
```

### Config Validation

```bash
ssh root@<host> "ha core check"
```

### Dashboard Inspection

```bash
ssh root@<host> "cat /config/ui-lovelace-*.yaml"
```

### Git Health

```bash
ssh root@<host> "cd /config && git log --oneline -10 && echo '---' && cat /config/.gitignore"
```

## Key Audit Checks

1. **Area coverage** — count unassigned entities. >80% unassigned = areas never populated.
2. **Naming convention** — entity IDs should be `domain.area_function`. No brand names or MAC fragments.
3. **Integration health** — Hue polling (`pref_disable_polling`), Govee LAN vs cloud (`lan_discovery`), scene noise.
4. **card-mod duplication** — check `configuration.yaml` for duplicate `card-mod.js` resource URLs.
5. **Bubble Card conflicts** — check logs for `CustomElementRegistry` errors (`ha-selector-bc_object`).
6. **Modular structure** — single `configuration.yaml` vs `packages/` or `includes/` split.
7. **Git hygiene** — check `.gitignore` covers `*.db`, `*.db-wal`, `*.db-shm`, `.storage/`, `secrets.yaml`.

## Phased Cleanup Roadmap

```
Phase 1: Define areas + audit naming
Phase 2: Rename entities domain.area_function + assign areas
Phase 3: Switch cloud integrations to LAN, disable entity noise
Phase 4: Split configuration.yaml, remove unused custom_components
Phase 5: Rebuild dashboards with single card framework
```

## Phase 2: Ongoing Monitoring (Martha Agent Pattern)

For continuous HA monitoring, deploy a dedicated Hermes agent profile:

### Profile Setup

```bash
mkdir -p ~/.hermes/profiles/<name>/{skills,plugins,cron,memories,sessions}
```

Profile config at `~/.hermes/profiles/<name>/config.yaml`:
```yaml
agent:
  name: <name>
  role: Home Assistant Operations & Improvement Agent
gateway:
  enabled: true
  platforms:
    telegram:
      enabled: true
    homeassistant:
      enabled: true
      host: <ha_ip>
toolsets:
  enabled: [terminal, file, web, homeassistant]
state:
  file: /home/xcx/<name>_state.json
```

### State File

`~/<name>_state.json`:
```json
{
  "agent": "<name>",
  "last_log_timestamp": null,
  "last_monitor_run": null,
  "backlog": [],
  "backlog_approved": false,
  "monitoring_stats": { "total_runs": 0, "errors_found": 0, "critical_alerts_sent": 0 },
  "ha_vm": { "host": "<ha_ip>", "ssh_user": "root" }
}
```

### Monitor Script Pattern

`~/.hermes/scripts/<name>-monitor.sh`:
- SSH into HA VM and check `ha core logs` for new ERROR/WARNING since last timestamp
- Verify integration health (Hue bridge, Govee LAN/cloud)
- Poll system metrics (CPU, RAM, disk)
- Run `ha core check` for config validity
- Update state file with run timestamp
- **Output only when issues found** — silent on clean runs

### Cron Job

```bash
hermes cron create \
  --name "<name>-monitor" \
  --schedule "every 4h" \
  --profile "<name>" \
  --prompt "Run the monitor script and report findings. Silent on clean runs."
```

### Backlog Protocol

1. Present ranked task list from Phase 1 assessment
2. User replies with modifications ("Swap 1 and 3", "Approve all")
3. Commit approved backlog to state file
4. Work one item at a time: plan → user confirms → apply → verify → update state

## Guardrails

- Never restart HA without explicit user confirmation
- Never delete entities without backing up and logging the deleted config
- Present diffs before making config changes
- Silent monitoring — only report when issues found
- Critical issues bypass 4h cycle and alert immediately
- Work through backlog one item at a time with user approval