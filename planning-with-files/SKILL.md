---
name: planning-with-files
description: Transforms workflow to use Manus-style persistent markdown files for planning, progress tracking, and knowledge storage. Use when starting complex tasks, multi-step projects, research tasks, or when the user mentions planning, organizing work, tracking progress, or wants structured output.
---

<skill>
<objective>
Adopt a persistent, file-based "working memory" workflow (like Manus) to manage complex, multi-step tasks through disciplined planning, research storage, and progress tracking.
</objective>

<quick_start>
Before starting any complex task, create `task_plan.md` with goals and phases. Update it after every action. Use `notes.md` for research findings. Read the plan before making major decisions.
</quick_start>

<success_criteria>
- A `task_plan.md` file exists and is updated regularly with progress and status
- Research findings are stored in `notes.md` instead of bloating the conversation context
- Large deliverables are created as separate files
- Error logs are maintained in the plan file for future reference
</success_criteria>

<the_3_file_pattern>
| File | Purpose | When to Update |
|------|---------|----------------|
| `task_plan.md` | Track phases and progress | After each phase |
| `notes.md` | Store findings and research | During research |
| `[deliverable].md` | Final output | At completion |
</the_3_file_pattern>

<core_workflow>
1. **Initialize**: Create `task_plan.md` with goal and phases.
2. **Research**: Save findings to `notes.md`; update `task_plan.md`.
3. **Execute**: Read `notes.md`, create deliverable, update `task_plan.md`.
4. **Deliver**: Deliver final output and finalize plan.
</core_workflow>

<critical_rules>
1. **ALWAYS Create Plan First**: Never start complex tasks without `task_plan.md`.
2. **Read Before Decide**: Refresh goals in attention window by reading the plan.
3. **Update After Act**: Mark phases [x] and log errors immediately.
4. **Store, Don't Stuff**: Move large outputs to files, keep only paths in context.
</critical_rules>

<when_to_use>
- Multi-step tasks (3+ steps)
- Research-intensive projects
- Building or creating new repositories/features
- Tasks spanning multiple tool calls
</when_to_use>

<resources>
<reference_index>
- **reference.md**: Attention manipulation, error recovery, and context optimization.
- **examples.md**: Real-world task examples and complex workflow patterns.
</reference_index>

<templates>
- Use the templates in `SKILL.md` (legacy) or `examples.md` for `task_plan.md` and `notes.md`.
</templates>
</resources>
</skill>
