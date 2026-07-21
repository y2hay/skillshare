---
name: daily-project-manager
description: Use when the user wants day-to-day project management, daily planning, reminders, standups, check-ins, focus sessions, follow-up tracking, or says phrases like "keep me on track", "I be forgetting", "daily plan", "what should I do today", "check in later", "end of day review", "standup", or "project manager". Coordinates Pi todos, pi-scheduler reminders, pi-daily reports, planning-with-files, and Honcho memory.
version: 1.0.0
---

# Daily Project Manager

## Objective

Keep xcx oriented day to day by converting vague intent into a small active plan, scheduled check-ins, visible todos, and durable follow-ups.

## Quick start

When this skill triggers:

1. Establish the mode: morning plan, check-in, focus block, reminder, end-of-day review, or weekly reset.
2. Create or update Pi todos for the current work.
3. For recurring or later prompts, use `pi-scheduler` commands/tools when available.
4. For work summaries, use `pi-daily` when available.
5. Persist durable decisions, recurring preferences, and long-lived follow-ups to Honcho.
6. Keep the user’s working set small: one active task, two or three next actions, explicit blockers.

## Modes

### Morning plan

Use when the user asks what to do today, starts the day, or says they need to stay on track.

Do this:

- Ask for, infer, or review the top outcomes for today.
- Limit the plan to three outcomes maximum.
- Convert outcomes into a todo list with exactly one `in_progress` task.
- Identify appointments, blockers, dependencies, and context needed.
- Offer check-ins via scheduler:
  - midday drift check
  - end-of-day review
  - custom reminder if the user names one

Suggested prompt:

```text
What are the top 1-3 outcomes that would make today successful?
```

If the user does not know, propose outcomes from current repo state, recent context, or Honcho memory, then ask for confirmation.

### Check-in / drift correction

Use when a scheduled prompt fires or the user says they got distracted.

Do this:

- Summarize the current active task and intended outcome.
- Ask: continue, switch, defer, or close?
- Update todo statuses immediately.
- If work drifted, capture the new item without letting it hijack the current one unless the user chooses to switch.

Suggested response shape:

```md
Current lane: <active task>
Next concrete action: <one action>
Blocker: <none or blocker>
Choose: continue / switch / defer / close
```

### Focus block

Use when the user wants to work for a set time or stop bouncing between tasks.

Do this:

- Define one focus objective.
- Set a timer/check-in with `/remind` or scheduler.
- Refuse scope creep during the block unless urgent.
- At the end, ask what changed and update todos.

Useful commands:

```text
/remind in 45m review focus block progress
/loop 30m check current focus and blockers
/schedule list
```

### End-of-day review

Use near the end of day or when the user asks what got done.

Do this:

- Run or suggest `/daily --save` for session-based report generation.
- Review open todos.
- Mark completed items, identify blocked/deferred items, and write tomorrow’s first action.
- Persist durable project state or preferences to Honcho.

Useful commands:

```text
/daily
/daily --project current
/daily --save
```

### Weekly reset

Use when the user wants a broader reset.

Do this:

- Review current projects and stale todos.
- Choose active projects, parked projects, and explicit next actions.
- Prune or defer old tasks.
- Persist the active project list and weekly priorities to Honcho.

## Scheduler integration

`pi-scheduler` provides:

```text
/loop 5m check if CI is green
/loop check deployment every 2h
/remind in 45m follow up on release PR
/schedule list
/schedule
/unschedule <id>
```

Rules:

- Use reminders only when they help; do not spam.
- Prefer one midday and one end-of-day check-in for daily tracking.
- Tell the user scheduler tasks only run while Pi is open and idle.
- If natural language scheduling is ambiguous, ask one clarifying question.

Suggested daily reminders:

```text
/loop 4h do a project-manager drift check: active task, blocker, next action
/remind in 8h run end-of-day review: completed, blocked, tomorrow's first action
```

## Daily report integration

`pi-daily` provides:

```text
/daily
/daily YYYY-MM-DD
/daily --project current
/daily --save
/daily --day-start 05:00
```

Rules:

- Use `/daily --save` when the user wants an artifact.
- Use `/daily --project current` when reviewing one project.
- Treat reports as raw material, not the final plan; convert follow-ups into todos.

## Todo discipline

Use Pi todo tracking for any day plan or multi-step effort.

Rules:

- Exactly one task should be `in_progress`.
- Mark tasks completed immediately when truly done.
- Keep the active task small enough to finish in one sitting.
- If a blocker appears, create a blocker task or mark dependency explicitly.
- Do not leave vague tasks like “work on project”; rewrite as concrete next actions.

Good task examples:

- `Audit Proxmox backup docs`
- `Write daily review summary`
- `Verify pi-scheduler reminders`

Bad task examples:

- `Do stuff`
- `Fix everything`
- `Research`

## Honcho memory

Persist only durable information:

- recurring daily/weekly preferences
- active project commitments
- stable decisions
- long-lived blockers
- important follow-up promises

Do not persist transient “I am currently typing” style state.

## Response style

Be concise and directive. The user wants help remembering and staying on track, not a lecture.

Default structure:

```md
Now: <one thing>
Next: <one concrete action>
Later: <1-3 queued items>
Reminder: <scheduled or suggested>
```

## Escalation

If the user has too many active projects, stop and force prioritization:

```text
We need to pick the lane. Which one is today’s priority: A, B, or C?
```

If a task requires implementation, use the appropriate implementation/planning skills after the daily plan is stable.
