---
name: skill-issue
description: "Audit and review all installed agent skills. Run on-demand or via cron to get a health report: skill inventory, usage tracking, version checks, dependency health, and actionable recommendations (keep, update, review, remove). Use when asked to review skills, check for skill updates, find unused skills, or audit the skill ecosystem."
version: 1
triggers: ["skill audit", "review skills", "check skills", "unused skills", "skill health"]
---

# Skill Issue — Skill Auditor

Audit all installed skills and produce a markdown report with recommendations.

## Quick Start

```bash
# Basic — scans ./skills and ./memory
node scripts/audit.mjs

# Custom directories
SKILL_DIRS="./skills,/path/to/more/skills" MEMORY_DIR="./memory" node scripts/audit.mjs

# Save report
node scripts/audit.mjs > /tmp/skill-audit-report.md
```

## Environment Variables

| Variable | Default | Description |
|----------|---------|-------------|
| `SKILL_DIRS` | `./skills` | Comma-separated skill directories to scan |
| `MEMORY_DIR` | `./memory` | Dated markdown logs for usage tracking |
| `AUDIT_DAYS` | `7` | Days back to scan for usage |

## What It Checks

1. **Inventory** — Finds every subdirectory containing a `SKILL.md` with YAML frontmatter
2. **Usage** — Scans recent memory/log files for skill name mentions
3. **Health** — Verifies required binaries (`requires.bins`) and env vars (`requires.env`)
4. **Versions** — Checks ClawdHub registry if `clawdhub` CLI is available
5. **Recommendations** — keep (active+healthy), update (outdated), review (unused), remove (broken deps)

## Process

Follow these steps when running a skill audit:

1. **Run audit** — Execute `node scripts/audit.mjs` (or `SKILL_DIRS="./skills" MEMORY_DIR="./memory" node scripts/audit.mjs` for custom paths) to scan all skill directories, check usage logs, and validate dependencies.

2. **Interpret results** — Review the generated report for:
   - **Inventory**: Which skills are installed, their versions, and frontmatter health
   - **Usage**: Which skills are actively used vs. dormant (based on memory/log references within `AUDIT_DAYS`)
   - **Health**: Missing binaries (`requires.bins`) or environment variables (`requires.env`)
   - **Versions**: Outdated skills with available updates from the registry

3. **Take action** — Based on recommendations:
   - **keep**: Active + healthy — no action needed
   - **update**: Outdated — update the skill definition
   - **review**: Unused — decide whether to archive or remove
   - **remove**: Broken dependencies — investigate and remove if unrecoverable

> **Alternative entry point**: `bash scripts/audit.sh` provides a shell wrapper around the same audit logic for quick runs without Node.js setup.

## Safety

- **Read-only** — Never modifies, installs, or removes anything
- **Advisory only** — Recommendations require manual action
