---
name: using-superpowers
description: Use when starting any conversation - establishes how to find and use skills, requiring Skill tool invocation before ANY response including clarifying questions
version: 1
triggers: ["start", "init", "begin", "conversation", "task", "skills"]
---

<skill>
<objective>
Ensure that skills are invoked and followed for every relevant task to maintain discipline and follow project-specific best practices.
</objective>

<quick_start>
Invoke the Skill tool for any task with even a 1% chance of relevance. Do this BEFORE gathering context or responding to the user.
</quick_start>

<success_criteria>
- Skills are invoked BEFORE any response or action
- The AI announces which skill is being used and why
- All checklist items in a skill are tracked as todos
</success_criteria>

<EXTREMELY-IMPORTANT>
If you think there is even a 1% chance a skill might apply to what you are doing, you ABSOLUTELY MUST invoke the skill.

IF A SKILL APPLIES TO YOUR TASK, YOU DO NOT HAVE A CHOICE. YOU MUST USE IT.
</EXTREMELY-IMPORTANT>

<how_to_access_skills>
**In Claude Code:** Use the `Skill` tool. When you invoke a skill, its content is loaded and presented to you—follow it directly. Never use the Read tool on skill files.

**In Cursor / Windsurf:** Use `@Skills` in the composer or check the skills panel. Skills may need to be enabled per project in `.cursor/rules/` or `.windsurf/rules/`.

**In GitHub Copilot / VS Code:** Chat extensions load skills via `.github/copilot-instructions.md` or VS Code prompt files in `.vscode/` — apply the content manually.

**In OpenCode / Continue.dev:** Skills are loaded from the configured skills directory (`~/.config/skillshare/skills/`). Use `Read` tool to load the relevant SKILL.md, then follow it.

**Generic fallback:** If no native Skill tool exists, read the SKILL.md file directly with the Read tool and follow its instructions manually. Announce which skill is being used.
</how_to_access_skills>

<the_rule>
**Invoke relevant or requested skills BEFORE any response or action.** Even a 1% chance a skill might apply means that you should invoke the skill to check.

```dot
digraph skill_flow {
    "User message received" [shape=doublecircle];
    "Might any skill apply?" [shape=diamond];
    "Invoke Skill tool" [shape=box];
    "Announce: 'Using [skill] to [purpose]'" [shape=box];
    "Follow skill exactly" [shape=box];
    "Respond" [shape=doublecircle];

    "User message received" -> "Might any skill apply?";
    "Might any skill apply?" -> "Invoke Skill tool" [label="yes, even 1%"];
    "Might any skill apply?" -> "Respond" [label="definitely not"];
    "Invoke Skill tool" -> "Announce: 'Using [skill] to [purpose]'";
    "Announce: 'Using [skill] to [purpose]'" -> "Follow skill exactly";
    "Follow skill exactly" -> "Respond";
}
```
</the_rule>

<red_flags>
These thoughts mean STOP—you're rationalizing:
- "This is just a simple question" → Questions are tasks. Check for skills.
- "I need more context first" → Skill check comes BEFORE clarifying questions.
- "Let me explore the codebase first" → Skills tell you HOW to explore. Check first.
- "I can check git/files quickly" → Files lack conversation context. Check for skills.
- "Let me gather information first" → Skills tell you HOW to gather information.
- "This doesn't need a formal skill" → If a skill exists, use it.
- "I remember this skill" → Skills evolve. Read current version.
- "This doesn't count as a task" → Action = task. Check for skills.
- "The skill is overkill" → Simple things become complex. Use it.
- "I'll just do this one thing first" → Check BEFORE doing anything.
- "This feels productive" → Undisciplined action wastes time. Skills prevent this.
- "I know what that means" → Knowing the concept ≠ using the skill. Invoke it.
</red_flags>

<skill_priority>
1. **Process skills first** (brainstorming, debugging)
2. **Implementation skills second** (frontend-design, mcp-builder)
</skill_priority>

<skill_types>
**Rigid** (TDD, debugging): Follow exactly.
**Flexible** (patterns): Adapt principles to context.
</skill_types>

<user_instructions>
Instructions say WHAT, not HOW. "Add X" doesn't mean skip workflows.
</user_instructions>

</skill>
