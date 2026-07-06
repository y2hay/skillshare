---
name: home-assistant-best-practices
description: >
  HA automations, helpers, naming, and config auditing. Covers SSH/docker
  inspection, .storage JSON analysis, area assignment, naming conventions.
  Extends the shared skill with config-audit.md.
metadata:
  version: 1
---

# Home Assistant Best Practices (Profile Extension)

This profile-level copy provides a `references/config-audit.md` file not in the shared skill. Refer to the shared `home-assistant-best-practices/skill/SKILL.md` for the full anti-patterns table, decision workflow, and core reference files.

## Extension: Config Audit & Health Check

File: `references/config-audit.md`

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
