---
name: catalog-projects
description: Analyzes Claude Code project session files (.jsonl) and creates descriptive symbolic links in ~/documents/projects/ following the naming convention from CLAUDE.md. Use this skill when the user wants to organize, catalog, or create human-readable references to their Claude Code project history. This skill reads conversation content to generate meaningful names and maintains project organization.
---

# Catalog Projects Skill

This skill analyzes Claude Code project files and creates human-readable symbolic links for easy access and organization.

## What This Skill Does

1. **Discovers Project Files**: Finds all .jsonl project files in ~/.claude/projects/
2. **Analyzes Content**: Reads the first significant user messages and assistant responses to understand what each project was about
3. **Generates Descriptive Names**: Creates kebab-case names following the convention in ~/CLAUDE.md
4. **Creates Symlinks**: Places symbolic links in ~/documents/projects/ pointing to the original UUID-named files
5. **Maintains Index**: Optionally creates a catalog file documenting all projects

## Process

### Step 1: Find All Project Files

Search for all .jsonl files in:
- ~/.claude/projects/-home-xcx/
- ~/.claude/projects/-/
- Any other workspace directories

### Step 2: Analyze Each Project - THOROUGH APPROACH

**CRITICAL: USER MESSAGES ARE OFTEN VAGUE - READ ASSISTANT RESPONSES TO UNDERSTAND ACTUAL WORK**

For each .jsonl file:

1. **Read sufficient content** (100-300 lines) to understand the session
2. **Parse BOTH user AND assistant messages**:
   - User messages might be: "help me fix this", "can you help", "please do X"
   - **ASSISTANT responses reveal what was actually done**: "I'll sync your clipboard in Hyprland", "I'll configure SSH to 10.10.0.110"

3. **Extract meaningful information from assistant responses**:
   - Look at assistant's FIRST substantive response explaining what they'll do
   - Check tool_use blocks for:
     - File paths being modified (reveals technology/component)
     - Bash commands being run (reveals tools/systems)
     - Edit/Write operations (reveals what's being configured)
   - Read assistant's summary/completion messages

4. **Identify key elements** (prioritize assistant's descriptions):
   - **Primary technology**: Hyprland, Docker, Ansible, SSH, clipboard, wallpaper, etc.
   - **Specific component**: monitor config, clipboard sync, SSH connection, GPU drivers
   - **Action performed**: setup, configure, debug, fix, sync, install, rebuild
   - **Purpose/outcome**: What problem was solved or what was accomplished

5. **Skip files that are**:
   - Nearly empty (< 500 bytes)
   - Only contain "/exit" or meta commands
   - Agent subprocess files (agent-*.jsonl)

### Step 3: Generate Descriptive Name - BE SPECIFIC

**Name Generation Strategy:**
1. Start with PRIMARY TECHNOLOGY/SYSTEM (from assistant's work, not user's vague request)
2. Add SPECIFIC COMPONENT/FEATURE if applicable
3. Add ACTION/PURPOSE to clarify what was done

**Format**: `[technology]-[component]-[action/purpose]`

**Excellent examples** (specific, technology + purpose):
- hyprland-clipboard-sync (not "help-what-copy")
- ssh-connection-debugging (not "help-figure-cant")
- nvidia-gpu-driver-setup (not "video-card-would")
- firefox-bookmarks-toolbar (not "need-bookmarks-toolbar")
- quickshell-rebuild-after-qt-update
- adguard-docker-deployment
- goldwarden-bitwarden-integration
- home-assistant-obsidian-sync

**Bad examples to NEVER use:**
- help-me-do (starts with user's request phrasing)
- please-through-logs (meaningless fragment)
- need-you-to (vague user plea)
- can-you-help (useless)
- what-does-installmethod (question fragment)
- update-yourself (too vague)
- request-configuration (generic)
- work-session-1 (no information)
- misc (useless)

### Step 4: Create Symlink

```bash
ln -s ~/.claude/projects/[workspace]/[uuid].jsonl ~/documents/projects/[descriptive-name].jsonl
```

**Important:**
- Check if symlink already exists before creating
- If name collision occurs, append a differentiator (e.g., "-v2", "-part2", or date)
- Never rename or move the original UUID files

### Step 5: Generate Report

Create a summary showing:
- Total project files found
- Number analyzed
- Number of symlinks created
- Number skipped (and why)
- List of all new symlinks in format: `descriptive-name.jsonl -> workspace/uuid.jsonl`

## Usage Examples

**User might say:**
- "Catalog my projects"
- "Organize my Claude sessions"
- "Create readable names for my project history"
- "I want to see what projects I've worked on"

**When invoked:**
1. Use Bash to find all .jsonl files
2. Use Read or Bash (cat/head) to examine file contents
3. Parse JSON to extract meaningful conversation data
4. Generate names based on content analysis
5. Create symlinks using `ln -s`
6. Report results to user

## Best Practices

- **Batch processing**: Process all projects in one run for efficiency
- **Conflict handling**: If a descriptive name already exists, examine the existing symlink's target and differentiate appropriately
- **Minimal reading**: Only read enough of each file to understand the topic (first 50-100 lines usually sufficient)
- **Preserve originals**: Never modify the actual .jsonl files in ~/.claude/projects/
- **Clear reporting**: Show the user what was created so they can find projects easily

## Edge Cases

1. **Very short sessions**: Skip or name as "quick-[topic]" if identifiable
2. **Multi-topic sessions**: Use the primary or most significant topic
3. **Continuation sessions**: Add "-continued" or "-part-2" suffix
4. **Generic conversations**: If truly generic, use "general-discussion-[date]"
5. **Agent files**: Skip agent subprocess files (agent-*.jsonl) as they're not primary sessions

## Output Format

Present results as a clean list:

```
Created 47 project symlinks in ~/documents/projects/

New symlinks:
  hyprland-monitor-setup.jsonl -> -home-xcx/abc123.jsonl
  adguard-docker-config.jsonl -> -home-xcx/def456.jsonl
  [... etc ...]

Skipped 23 files:
  - 15 agent subprocess files
  - 5 minimal/exit-only sessions
  - 3 duplicate topics (already cataloged)
```

## Maintenance

This skill can be run periodically to catalog new projects. It should:
- Detect existing symlinks and skip re-creating them
- Only process new/uncataloged projects
- Update the index if maintained

## Integration with CLAUDE.md

This skill follows the Project File Naming Convention defined in ~/CLAUDE.md. Always adhere to those guidelines when generating names.
