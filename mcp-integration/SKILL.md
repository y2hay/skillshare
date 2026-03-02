---
name: MCP Integration
description: This skill should be used when the user asks to "add MCP server", "integrate MCP", "configure MCP in plugin", "use .mcp.json", "set up Model Context Protocol", "connect external service", mentions "${CLAUDE_PLUGIN_ROOT} with MCP", or discusses MCP server types (SSE, stdio, HTTP, WebSocket). Provides comprehensive guidance for integrating Model Context Protocol servers into Claude Code plugins for external tool and service integration.
version: 0.1.0
---

<skill>
<objective>
Provide comprehensive guidance for integrating Model Context Protocol (MCP) servers into Claude Code plugins to expose external service capabilities as tools.
</objective>

<quick_start>
Configure MCP servers in `.mcp.json` or `plugin.json`. Use `${CLAUDE_PLUGIN_ROOT}` for portable paths. Reference tools as `mcp__plugin_NAME_SERVER__TOOL`.
</quick_start>

<success_criteria>
- MCP server appears in `/mcp` output with correct tools
- Authentication (OAuth or tokens) works correctly
- Tools are successfully invoked from commands or agents
- Portable paths using ${CLAUDE_PLUGIN_ROOT} are used
</success_criteria>

<how_it_works>
<configuration_methods>
Plugins can bundle MCP servers in two ways:

**Method 1: Dedicated .mcp.json (Recommended)**
Create `.mcp.json` at plugin root with server definitions.

**Method 2: Inline in plugin.json**
Add `mcpServers` field to `plugin.json`.
</configuration_methods>

<server_types_summary>
- **stdio**: Local processes (npx, python, custom scripts). Communicates via stdin/stdout.
- **SSE**: Hosted services (Asana, GitHub). Supports automatic OAuth.
- **HTTP**: REST APIs with token/header authentication.
- **WebSocket**: Real-time bidirectional streaming.
</server_types_summary>

<environment_variables>
- `${CLAUDE_PLUGIN_ROOT}`: Plugin directory (always use for portability).
- `${ENV_VAR}`: Expansion of user environment variables.
</environment_variables>
</how_it_works>

<tool_naming>
**Format:** `mcp__plugin_PLUGIN-NAME_SERVER-NAME__TOOL-NAME`

Pre-allow specific tools in command frontmatter:
```markdown
---
allowed-tools: ["mcp__plugin_asana_asana__asana_create_task"]
---
```
</tool_naming>

<process>
<implementation_workflow>
1. Choose MCP server type (stdio, SSE, HTTP, ws)
2. Create `.mcp.json` at plugin root with configuration
3. Use `${CLAUDE_PLUGIN_ROOT}` for all file references
4. Document required environment variables in README
5. Test locally with `/mcp` command
6. Pre-allow MCP tools in relevant commands
7. Handle authentication and error cases
</implementation_workflow>
</process>

<resources>
<reference_index>
- **references/server-types.md**: Deep dive on stdio, SSE, HTTP, and WS
- **references/authentication.md**: OAuth, tokens, and custom headers
- **references/tool-usage.md**: Using MCP tools in commands and agents
- **references/security-and-errors.md**: Best practices and error patterns
- **references/testing-and-debugging.md**: Local testing and `/mcp` usage
</reference_index>

<examples_index>
- **examples/stdio-server.json**: Local process example
- **examples/sse-server.json**: Cloud service with OAuth
- **examples/http-server.json**: REST API with tokens
</examples_index>
</resources>
</skill>
