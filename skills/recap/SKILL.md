---
name: recap
description: Daily or period recap via `oma-recap`. Resolves a date or window from natural language, invokes `oma recap --json`, delegates theme analysis and Markdown formatting to the skill, and reports a TL;DR plus saved path.
disable-model-invocation: true
version: 1
triggers: ["/recap", "recap", "daily recap", "what did I do", "weekly recap"]
---

# MANDATORY RULES: VIOLATION IS FORBIDDEN

- **Response language follows `language` setting in `.agents/oma-config.yaml` if configured.**
- **NEVER skip steps.** Execute from Step 1 in order.
- **Never modify `.agents/`.** SSOT protection applies.
- **Follow the host-LLM contract** — theme analysis, grouping rules, and Markdown output format are owned by the skill (see Step 4 for the inline fallback spec if `oma-recap` skill is unavailable). This workflow resolves intent, runs the CLI, and reports.
- **Never auto-translate technical terms** in the saved recap (project names, tool names, CLI flags).

---

> **Vendor note:** This workflow executes inline (no subagent spawning). All vendors invoke `oma recap` directly.

---

## Step 1: Detect Mode & Resolve Window

Inspect the user's request and resolve **at most three** arguments. Default mode is `daily` with today as the target date.

| Mode | Triggers | CLI flag |
|------|----------|----------|
| `daily` | No date, "today", "오늘", "yesterday", "어제", specific date ("4월 10일", "2026-04-10") | `--date YYYY-MM-DD` (or omitted for today) |
| `period` | "this week", "지난 7일", "last month", "past 2 weeks", "이번달" | `--window Nd` |

Only extract a tool filter when the user **explicitly names** one or more tools (e.g., "코덱스만", "claude only", "qwen과 codex"). Supported values: `grok, claude, codex, qwen, cursor, antigravity`. Otherwise omit `--tool`.

Resolution rules (delegate ambiguous cases to the skill):
- Relative day references → `--date YYYY-MM-DD`
- Relative weekday references → calculate the date
- Period phrases → `--window Nd` (1w=7d, 1mo=30d)
- No date specified → today (omit flags)

If the user supplies multiple conflicting signals (e.g., "지난주 어제"), pick the more specific one and state the assumption in Step 5.

---

## Step 2: Preflight

1. Confirm `oma` is available: `command -v oma` (or `bun run oma --help` if running from source).
2. If `oma` is missing:
   - Fall back to the Claude-history-only `jq` path documented in the inline fallback Step 4 §2.
   - Note the limited coverage in the Step 5 report.
3. If neither source is available, exit with a message stating the requested range and the missing inputs. Do NOT fabricate a recap.
4. **Ensure output directory exists**:
   ```bash
   mkdir -p .agents/results/recap
   ```

---

## Step 3A: Daily Recap

// turbo
Use one of:

```bash
# Today
oma recap --json

# Specific date
oma recap --date 2026-05-11 --json

# Specific date with explicit tool filter
oma recap --date 2026-05-11 --tool claude,codex --json
```

---

## Step 3B: Period Recap

// turbo
Use one of:

```bash
# Past N days
oma recap --window 7d --json
oma recap --window 30d --json

# Period with explicit tool filter
oma recap --window 7d --tool codex --json
```

The CLI emits a normalized history JSON. **Do not interpret the rows here** — Step 4 delegates that to the skill.

---

## Step 4: Synthesize & Save

If the `oma-recap` skill exists (`.agents/skills/oma-recap/SKILL.md`), delegate to it per its spec.

**Otherwise, use the inline fallback below.**

### Step 4 (inline fallback) — Theme Analysis and Grouping

Group the JSON history rows by **time-adjacent clusters** (≤15 minutes between entries = same session). Within each cluster, identify the dominant theme.

**Grouping rules:**
- Adjacent entries within 15 minutes → same theme group (title from first substantive entry)
- Entries spaced >15 minutes apart → new theme group
- Cross-tool entries within the same 15-minute window → merge into one group
- Any group accounting for <10% of total entries → "Miscellaneous" bucket (unless it's the only group)
- **Daily template** (single date): organize by time blocks (morning/afternoon/evening), list the theme group under each block
- **Multi-day template** (period): organize by project/domain, not by day; list what was accomplished per project across the window

### Step 4.2 — Output Format

**Daily recap format:**
```markdown
# Recap: YYYY-MM-DD (DayName)

## Morning (~HH:MM–HH:MM)
- **{Theme}** — {key accomplishment} ({tool})
- **{Theme}** — {key accomplishment} ({tool})

## Afternoon (~HH:MM–HH:MM)
...
```

**Multi-day recap format:**
```markdown
# Recap: YYYY-MM-DD ~ YYYY-MM-DD ({N} days)

## {Project/Domain}
- **{Theme}** — {key accomplishment} ({tool}, {date})
...

## Summary
- Total sessions: {N}
- Tools used: {list}
- Key outcomes: {bullet list}
```

### Step 4.3 — Save Results

Write to `.agents/results/recap/{date}.md` (daily) or `.agents/results/recap/{start}~{end}.md` (period).

```bash
cat > .agents/results/recap/{filename} << 'RECAP_EOF'
{formatted recap content}
RECAP_EOF
```

### Step 4.4 — jq Fallback (No `oma` CLI)

If `oma` is not installed, read `~/.claude/history.jsonl` directly and synthesize a recap from Claude-only history:

```bash
cat ~/.claude/history.jsonl | jq -r '
  select(.ts >= $start and .ts <= $end) |
  "\(.ts) | \(.tool // "chat") | \(.summary // .input[0:80])"
' | head -50
```

Note limited coverage: Claude history only, no other tools.

---

## Step 5: Report

Display **only**:

```markdown
> **TL;DR**
> - {accomplishment 1}
> - {accomplishment 2}
> - {accomplishment 3}

Saved to: `.agents/results/recap/{date}.md`
```

Append a single-line coverage note **only if** any of the following apply:
- Fallback (jq) path was used → "Coverage: Claude history only (oma CLI not installed)"
- History was sparse → "Coverage: limited history for the requested range"
- An assumption was made about an ambiguous date → "Assumed: {assumption}"

---

## Failure Handling

| Situation | Recovery |
|-----------|----------|
| `oma` not on PATH | Use the `jq` fallback from SKILL.md §2; note limited coverage. |
| No `~/.claude/history.jsonl` and no `oma` | Exit with missing-source message; do not invent data. |
| Range resolves to zero records | Emit minimal TL;DR with "no activity recorded" and the save path. |
| Ambiguous date input | Pick the more specific signal; declare the assumption in Step 5. |
| Save path collision | Skill overwrites by design; no special handling here. |

---

## Quick Reference

| Command | Effect |
|---------|--------|
| `/recap` | Today's recap |
| `/recap yesterday` | Yesterday's recap |
| `/recap 2026-04-10` | Specific date |
| `/recap this week` | `--window 7d` |
| `/recap last month` | `--window 30d` |
| `/recap last week claude only` | `--window 7d --tool claude` |

---

## References

- Skill spec (if exists): `.agents/skills/oma-recap/SKILL.md`
- Inline fallback: Step 4 above (theme analysis, grouping, output format)
- Output directory: `.agents/results/recap/`
- Language config: `.agents/oma-config.yaml`
- Claude fallback history: `~/.claude/history.jsonl`
- Related: `oma retro` (Git commit retrospective — different scope)
