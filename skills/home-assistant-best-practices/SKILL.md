---
name: home-assistant-best-practices
description: >
  HA automations, helpers, naming, and config auditing. Covers SSH/docker
  inspection, .storage JSON analysis, area assignment, naming conventions,
  template lighting, Lutron Pico remotes, and ongoing monitoring.
metadata:
  version: 1
triggers: ["HA best practices", "config audit", "entity naming", "area assignment", "HA automation patterns", "Lutron Pico", "template lights", "HA monitoring"]
---

# Home Assistant Best Practices

This skill covers HA configuration best practices, automation patterns, integration tuning, and ongoing monitoring. It is organized into three sub-skills:

## Sub-Skills

- **[ha-integration-tuning](./ha-integration-tuning/SKILL.md)** — Direct `.storage` editing for integration config changes, API-based reload without restart, config modularization with `!include`, Govee MQTT tuning, Hue local push, and card-mod fixes.
- **[ha-lighting-automation](./ha-lighting-automation/SKILL.md)** — Template-based dynamic light groups, Lutron Caseta Pico remote automations, and all-lights control patterns.
- **[ha-audit-and-monitoring](./ha-audit-and-monitoring/SKILL.md)** — SSH-based config audit, entity registry inspection, integration health checks, phased cleanup roadmap, and ongoing monitoring via Hermes agent profile + cron.

## Core Principles

- **Async-First**: All automation actions should be idempotent and non-blocking
- **Single Source of Truth**: Use `.storage` files for integration config, YAML for automations/helpers
- **Git-Backed**: `/config` should be a git repo with proper `.gitignore`
- **No Restart Required**: Prefer API-based reloads and `!include` modularization

## Decision Workflow

1. **New entity needed?** → Use helpers UI first (template sensor, switch, etc.), YAML only when UI can't express it
2. **Integration misbehaving?** → Check `.storage/core.config_entries` before uninstalling/reinstalling
3. **Config too large?** → Split with `!include` packages/ — restart only once
4. **Dashboard slow?** → Check card-mod duplication, Bubble Card conflicts, entity noise from Govee scenes
5. **Git divergence?** → The git-committed version is the source of truth, not the live file

## Common Anti-Patterns

| Anti-Pattern | Fix |
|---|---|
| Entity IDs with brand names or MAC fragments | Rename to `domain.area_function` |
| >80% entities unassigned to areas | Define areas and reassign |
| Hue cloud polling enabled | Set `pref_disable_polling: true` in config entry |
| Govee scene entities (30+ from 3 strips) | Set `enable_scenes: false`, `enable_diy_scenes: false` |
| card-mod loaded twice | Remove from `extra_module_url` or HACS resources |
| Single monolithic `configuration.yaml` | Split with `!include packages/` |
| `.gitignore` missing database/storage entries | Add `*.db`, `*.db-wal`, `*.db-shm`, `.storage/`, `secrets.yaml` |

## Extension: Config Audit & Health Check

Use this when auditing an existing HA instance — inspecting state, identifying stale entities, planning cleanup.

### Remote Audit Commands

```
ssh root@<host>
docker exec homeassistant cat /config/configuration.yaml
docker exec homeassistant python3 -c "import json; ..."
```

### .storage JSON Inspection Targets

| File | What to extract |
|------|-----------------|
| `core.config_entries` | Integration domain, title, version, source |
| `core.area_registry` | Area IDs and names |
| `core.entity_registry` | Domain counts, unassigned count, platform filter |
| `core.device_registry` | Device count per integration |

### Key Audit Checks

1. **Area coverage** — count unassigned entities. >80% unassigned = never set up.
2. **Naming convention** — entity IDs should be `domain.area_function`. No brand names or MAC fragments.
3. **Phantom entities in dashboards** — extract dashboard entity refs, verify against registry.
4. **Integration health** — Hue polling (`pref_disable_polling`), Govee scene noise (30+ scene lights from 3 physical strips), Adaptive Lighting.
5. **Git health** — check `.gitignore` covers `*.db`, `*.db-wal`, `*.db-shm`, `.storage/`, `secrets.yaml`.

### Phased Cleanup Roadmap

```
Phase 1: Define areas + audit naming
Phase 2: Rename entities domain.area_function + assign areas
Phase 3: Switch cloud integrations to LAN, disable entity noise
Phase 4: Split configuration.yaml, remove unused custom_components
Phase 5: Rebuild dashboards with single card framework
```

For detailed audit commands and monitoring setup, see the **[ha-audit-and-monitoring](./ha-audit-and-monitoring/SKILL.md)** sub-skill.
