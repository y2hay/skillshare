# 🔍 skill-issue

An agent skill that audits all your other agent skills. HR department for AI agents.

**Find the skill issues before they find you.**

> **Name:** [Josh Puckett](https://x.com/joshpuckett) — who immediately knew it had to be called `/skill-issue`
>
> **Concept:** [Benji Taylor](https://x.com/benjitaylor) — "I need a skill that reviews all the other skills, figures out which ones are performing, and fires the rest."

## What It Does

- **Inventories** every installed skill across your project
- **Tracks usage** by scanning recent logs for skill mentions
- **Checks health** — verifies required binaries and environment variables
- **Recommends action** — keep, update, review, or remove

## Quick Start

```bash
git clone https://github.com/krispuckett/skill-issue.git
cd skill-issue

# Point it at your skills directory
SKILL_DIRS="../my-project/skills" node scripts/audit.mjs
```

That's it. Any directory containing subdirectories with `SKILL.md` files will be scanned.

## Usage

### Ask Your Agent
> "Run a skill audit"
> "Check my skills for issues"
> "Do I have a skill issue?"

### CLI
```bash
# Scan default ./skills directory
node scripts/audit.mjs

# Scan multiple directories
SKILL_DIRS="./skills,./other-skills" node scripts/audit.mjs

# Scan with usage tracking from your logs
SKILL_DIRS="./skills" MEMORY_DIR="./logs" node scripts/audit.mjs
```

## Configuration

| Variable | Default | Description |
|----------|---------|-------------|
| `SKILL_DIRS` | `./skills` | Comma-separated directories to scan |
| `MEMORY_DIR` | `./memory` | Directory with dated markdown logs (`YYYY-MM-DD.md`) for usage tracking |
| `AUDIT_DAYS` | `7` | How far back to scan for usage |
| `SKIP_HUB` | `false` | Set to `1` to skip ClawdHub version checks |

## What It Scans

The auditor looks for subdirectories containing a `SKILL.md` with YAML frontmatter:

```
skills/
├── my-skill/
│   └── SKILL.md
├── another-skill/
│   └── SKILL.md
```

### SKILL.md Format

```yaml
---
name: my-skill
description: "What this skill does"
metadata: {"requires":{"bins":["curl","jq"],"env":["API_KEY"]}}
---
```

If `requires.bins` lists CLI tools, the audit checks they're installed. If `requires.env` lists env vars, it checks they're set.

## Sample Output

```
# 🔍 Skill Audit Report

## Summary
- Total skills: 12
- ✅ Keep: 5       (active + healthy)
- 🔎 Review: 4    (unused — maybe remove?)
- 🗑️ Remove: 3    (broken dependencies)

## Detailed Report
| # | Skill       | Bins     | Usage (7d) | Health | Rec       |
|---|-------------|----------|------------|--------|-----------|
| 1 | 🌤️ weather  | curl     | 📊 5       | ✅     | ✅ keep   |
| 2 | 🗣️ voice    | sag      | —          | ❌ sag | 🗑️ remove |
| 3 | 📧 email    | himalaya | 📊 8       | ✅     | ✅ keep   |

## ⚠️ Skills Needing Attention
- **voice** — 🗑️ Missing: `sag` not found. Install or remove.
```

## How It Works

1. Scans `SKILL_DIRS` for subdirectories with `SKILL.md`
2. Parses YAML frontmatter for metadata
3. Runs `which` on each required binary
4. Checks `process.env` for required variables
5. Scans dated `.md` files in `MEMORY_DIR` for skill name mentions
6. Outputs a markdown report with per-skill recommendations

**Read-only.** Never modifies, installs, or removes anything.

## Requirements

- Node.js 18+

## License

MIT — see [LICENSE](LICENSE)
