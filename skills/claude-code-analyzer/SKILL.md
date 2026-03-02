---
name: claude-code-analyzer
description: Analyzes Claude Code usage patterns and provides comprehensive recommendations. Runs usage analysis, discovers GitHub community resources, suggests CLAUDE.md improvements, and fetches latest docs on-demand. Use when user wants to optimize their Claude Code workflow, create configurations (agents/skills/commands), or set up project documentation.
---

<skill>
<objective>
Optimize Claude Code workflow through automated usage analysis, community resource discovery on GitHub, and intelligent generation of project-specific configurations.
</objective>

<quick_start>
Run `bash scripts/analyze.sh` to see tool usage and community suggestions. Run `bash scripts/analyze-claude-md.sh` to detect your tech stack and generate a CLAUDE.md tailored to your project.
</quick_start>

<success_criteria>
- Usage analysis correctly identifies frequently used tools and potential auto-allows
- GitHub discovery finds relevant community skills, agents, or commands
- Project analysis accurately detects the framework, package manager, and testing setup
- Generated configurations (CLAUDE.md, agents, skills) follow latest Anthropic best practices
</success_criteria>

<core_capabilities>
This skill provides a complete Claude Code optimization workflow:

**1. Usage Analysis** - Extracts patterns from Claude Code history
- Tool usage frequency
- Auto-allowed tools vs actual usage
- Model distribution
- Project activity levels

**2. GitHub Discovery** - Finds community resources automatically
- Skills matching your tools
- Agents for your workflows
- Slash commands for common operations
- CLAUDE.md examples from similar projects

**3. Project Analysis** - Detects tech stack and suggests documentation
- Package manager and scripts
- Framework and testing setup
- Docker, CI/CD, TypeScript configuration
- Project-specific CLAUDE.md sections

**4. On-Demand Documentation** - Fetches latest Claude Code docs
- Agents/subagents structure and configuration
- Skills architecture and bundled resources
- Slash commands with MCP integration
- CLAUDE.md best practices from Anthropic teams
- Settings and environment variables
</core_capabilities>

<process>
<step_1_run_usage_analysis>
Run the usage analysis script:
```bash
bash scripts/analyze.sh --current-project
```

This automatically:
- Extracts tool usage from JSONL files
- Checks auto-allowed tools configuration
- Analyzes model distribution
- **Searches GitHub for community resources** (always enabled)
</step_1_run_usage_analysis>

<step_2_run_project_analysis>
Detect project structure:
```bash
bash scripts/analyze-claude-md.sh
```

This detects:
- Package manager (npm, pnpm, yarn, cargo, go, python)
- Framework (Next.js, React, Django, FastAPI, etc.)
- Testing setup (Vitest, Jest, pytest, etc.)
- CI/CD, Docker, TypeScript, linting configuration
</step_2_run_project_analysis>

<step_3_interpret_combined_results>
Combine insights from both analyses:

**Usage patterns** show:
- Tools used frequently but requiring approval -> Add to auto-allows
- Auto-allowed tools never used -> Remove from config
- Repetitive bash commands -> Create slash commands
- Complex workflows -> Create dedicated agents
- Domain-specific tasks -> Build custom skills

**GitHub discovery** provides:
- Similar configurations from community
- Proven patterns for your tool usage
- Example agents/skills/commands to adapt

**Project analysis** reveals:
- Required CLAUDE.md sections
- Framework-specific conventions to document
- Testing and build commands to include
</step_3_interpret_combined_results>
</process>

<how_it_works>
<configuration_generation>
Based on recommendations, fetch latest docs and create:

**For frequently used tools** -> Update auto-allows:
- Fetch: https://docs.claude.com/en/docs/claude-code/settings
- Update: `~/.claude/settings.json`

**For repetitive commands** -> Create slash command:
- Fetch: https://docs.claude.com/en/docs/claude-code/slash-commands
- Create: `.claude/commands/NAME.md`

**For complex workflows** -> Create agent:
- Fetch: https://docs.claude.com/en/docs/claude-code/sub-agents
- Create: `.claude/agents/NAME.md`

**For reusable domain knowledge** -> Build skill:
- Fetch: https://docs.claude.com/en/docs/agents-and-tools/agent-skills/overview
- Create: `.claude/skills/NAME/SKILL.md`

**For project context** -> Write CLAUDE.md:
- Fetch: https://www.anthropic.com/engineering/claude-code-best-practices
- Create: `.claude/CLAUDE.md`
</configuration_generation>

<example_complete_optimization_session>
**User**: "Help me optimize my Claude Code setup"

**Claude executes**:

1. **Analyze usage patterns**
   ```bash
   bash scripts/analyze.sh --current-project
   ```
   Finds: Bash tool used 150 times, Read 80 times, Write 45 times
   Auto-allows: None configured
   GitHub: Discovers community skills for TypeScript testing

2. **Analyze project structure**
   ```bash
   bash scripts/analyze-claude-md.sh
   ```
   Detects: Next.js project with Vitest, npm scripts: dev, build, test, lint
   Missing: CLAUDE.md doesn't exist

3. **Make recommendations**
   "I analyzed your Claude Code usage. Here's what I recommend:
   
   **Auto-Allows**: You use Bash (150x), Read (80x), and Write (45x) constantly. Let me add them to auto-allows.
   
   **Slash Command**: You run tests frequently. I'll create /test command.
   
   **CLAUDE.md**: Your Next.js project needs documentation. I'll create one with your npm scripts and testing setup.
   
   **Community Resource**: I found a TypeScript testing skill on GitHub that matches your workflow."

4. **Fetch docs and update configs**
   (Updating settings.json, creating test.md, creating CLAUDE.md)
</example_complete_optimization_session>
</how_it_works>

<when_to_use>
- User asks to "analyze my workflow"
- Optimizing Claude Code setup
- Finding unused auto-allows
- Discovering community resources
- Understanding usage patterns
- Creating CLAUDE.md or setting up new project
</when_to_use>

<resources>
<critical_documentation_urls>
| Type | URL |
|------|-----|
| Agents | https://docs.claude.com/en/docs/claude-code/sub-agents |
| Skills | https://docs.claude.com/en/docs/agents-and-tools/agent-skills/overview |
| Slash Commands | https://docs.claude.com/en/docs/claude-code/slash-commands |
| Settings | https://docs.claude.com/en/docs/claude-code/settings |
| CLAUDE.md | https://www.anthropic.com/engineering/claude-code-best-practices |
</critical_documentation_urls>

<technical_reference>
**Agents** (.md files with YAML frontmatter):
- Required: name, description
- Optional: tools (comma-separated), model (sonnet/opus/haiku/inherit)
- Location: `.claude/agents/` (project) or `~/.claude/agents/` (user)

**Skills** (directory with SKILL.md):
- Structure: `skill-name/SKILL.md`
- Bundled resources: scripts/, references/, assets/
- Location: `.claude/skills/`

**Slash Commands** (.md files):
- Required: name (with / prefix)
- Arguments: $ARGUMENTS, $1, $2
- Location: `.claude/commands/`

**CLAUDE.md** (project documentation):
- Hierarchical: user-level -> parent -> project -> nested
- Location: `.claude/CLAUDE.md`
</technical_reference>

<requirements>
- `jq` (install: `brew install jq` or `apt install jq`)
- Claude Code projects at `~/.claude/projects`
- Optional: `gh` CLI for direct GitHub search
</requirements>
</resources>

<why_this_approach_works>
**Comprehensive**: Combines usage analysis + community discovery + project detection
**Current**: Fetches latest docs on-demand, never stale
**Actionable**: Provides specific, implementable recommendations
**Automated**: GitHub discovery runs automatically, no flags needed
**Integrated**: All tools work together for complete workflow optimization
</why_this_approach_works>
</skill>
