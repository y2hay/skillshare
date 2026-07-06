---

name: workspace-dispatch
description: |
  Use when decomposing a mission into worker tasks and chaining execution; triggers include "dispatch workspace task", "spawn worker per task", "decompose mission", "chain tasks", and "single-agent mission".
version: 1
triggers: ["dispatch", "orchestrate", "parallel tasks", "mission", "decompose"]

---

# Workspace Dispatch (Single Agent)

You are an autonomous mission orchestrator. Decompose work into tasks, spawn one worker per task, verify output, chain to the next — no user intervention needed.

## Platform Assumptions

This skill uses **Claude Code's proprietary `sessions_spawn()` API** for parallel worker dispatch. It does NOT work with other platforms (OpenCode, Cursor, Copilot, etc.) unless they provide an equivalent subagent spawning mechanism.

| Platform | Compatibility | Notes |
|----------|--------------|-------|
| **Claude Code** | ✅ Full | Uses `sessions_spawn()` + `sessions_yield()` |
| **OpenCode** | ❌ No | No subagent spawning API — use `oma agent:spawn` or orchestrate sequentially |
| **Cursor** | ❌ No | No subagent spawning API — orchestrate manually |
| **GitHub Copilot** | ❌ No | No subagent spawning API — orchestrate manually |
| **Continue.dev** | ❌ No | No subagent spawning API — orchestrate manually |

For non-Claude runtimes, decompose tasks and execute them sequentially yourself instead, or use `oma agent:spawn` where available.

## Success Criteria

Before dispatching any task, ensure:

1. **Mission is fully decomposed** into 2–6 concrete, ordered tasks
2. **Every task has machine-checkable exit criteria** (file existence, compilation, grep pattern)
3. **Dependencies between tasks are explicit** — if task B needs task A's output, A must complete before B
4. **No task exceeds the scope of a single worker session** (600s timeout, no long-running processes)
5. **All tasks can fail independently** — a failed dependent task should not block unrelated work

## Flow

1. **Decompose** the goal into 2-6 tasks with machine-checkable exit criteria
2. **For each task**: spawn a worker → wait → verify exit criteria → approve or retry
3. **Report** summary when all tasks complete

## Decomposition Rules

- **Max 6 tasks** — keep it focused
- **Every task needs exit criteria** verifiable with shell commands:
  - `test -f /path` — file exists
  - `npx tsc --noEmit` — compiles
  - `grep -q "keyword" /path` — contains expected content
  - `wc -c < /path | awk '$1 > 100'` — file has real content
- **No vague criteria** — must be machine-checkable
- **Include working directory** (`cwd`) for each task
- **Each task is independent** — worker gets full context, no shared state between workers

## Task Types

| Type | Worker Does | Verify With |
|------|-----------|-------------|
| coding | Write code, create files | file exists, tsc passes |
| research | Search, read, synthesize | output file exists with content |
| review | Read code, check behavior | reviewer outputs PASS verdict |

## Dispatch Loop

```
For each task (in dependency order):
  1. Spawn worker:
     sessions_spawn(
       task: <worker prompt>,
       label: "worker-<task-slug>",
       mode: "run",
       runTimeoutSeconds: 600
     )
  2. sessions_yield() — wait for worker
  3. Verify exit criteria via exec commands
  4. If ALL pass → mark complete, next task
  5. If ANY fail → retry (max 3) with error context, then fail + skip dependents
```

## Worker Prompt

Give each worker everything it needs in one prompt:

```
## Mission: {goal}
## Your Task: {task.title}
{task.description}

Working directory: {cwd}

## Exit Criteria (you MUST satisfy ALL):
- {criterion_1}
- {criterion_2}

## Rules
- Do NOT start servers or long-running processes
- Do NOT modify files outside your working directory
- Verify your own work before finishing — run the exit criteria commands yourself
- Commit only if the mission explicitly allows commits; otherwise leave changes uncommitted and report them
```

On retry, append:
```
## ⚠️ Previous attempt failed (attempt {n}/3)
Error: {what went wrong}
Fix this specific issue.
```

## Completion

When all tasks done, output:

```
✅ Mission complete: {goal}

Tasks:
- ✅ {title} — verified
- ✅ {title} — verified

Output: {project_path}
Duration: {elapsed}
```

## Failure Handling

| Failure | Action |
|---------|--------|
| Worker timeout | Retry with simpler scope |
| Exit criteria fail | Retry with specific error |
| 3 retries exhausted | Mark failed, skip dependents, continue |

## Rules

- One worker per task, default model, no critic
- Workers self-verify (exit criteria are the quality gate)
- Don't hardcode model names — use whatever's available
- Don't hold state in memory — be ready for context loss
- Don't start servers in tasks
