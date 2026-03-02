---
name: skill-issue
description: "Audit and review all installed agent skills. Run on-demand or via cron to get a health report: skill inventory, usage tracking, version checks, dependency health, and actionable recommendations (keep, update, review, remove). Use when asked to review skills, check for skill updates, find unused skills, or audit the skill ecosystem."
---

<skill>
<objective>
Audit installed agent skills to produce health reports, track usage, verify dependencies, and provide actionable recommendations for ecosystem maintenance.
</objective>

<quick_start>
Run `node scripts/audit.mjs` to scan for skills. Specify custom locations via `SKILL_DIRS` and `MEMORY_DIR` environment variables if needed.
</quick_start>

<success_criteria>
- All installed skills are correctly inventoried with version information
- Skill usage is accurately tracked from memory/log files over the specified period
- Dependency health (binaries and env vars) is verified for each skill
- Actionable recommendations (keep, update, review, remove) are generated based on health and usage
</success_criteria>

<process>
1. **Inventory**: Find every subdirectory containing a `SKILL.md` with valid YAML metadata.
2. **Usage Tracking**: Scan recent memory files for skill name mentions within the `AUDIT_DAYS` window.
3. **Health Check**: Verify required binaries and environment variables.
4. **Version Check**: Query the ClawdHub registry (if available) for updates.
5. **Report Generation**: Produce a markdown summary with categorized recommendations.
</process>

<setup>
<environment_variables>
| Variable | Default | Description |
|----------|---------|-------------|
| `SKILL_DIRS` | `./skills` | Comma-separated skill directories to scan |
| `MEMORY_DIR` | `./memory` | Dated markdown logs for usage tracking |
| `AUDIT_DAYS` | `7` | Days back to scan for usage |
</environment_variables>
</setup>

<safety>
- **Read-only**: The auditor never modifies, installs, or removes skill files.
- **Advisory**: All recommendations (update/remove) must be executed manually by the user.
</safety>

<resources>
<scripts_index>
- **scripts/audit.mjs**: Primary Node.js auditing script.
- **scripts/audit.sh**: Bash wrapper for easier execution.
</scripts_index>
</resources>
</skill>
