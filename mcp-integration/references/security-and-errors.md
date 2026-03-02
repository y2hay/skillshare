# MCP Security and Error Handling

## Security Best Practices

### Use HTTPS/WSS
Always use secure connections for cloud services:
- ✅ `https://mcp.example.com/sse`
- ❌ `http://mcp.example.com/sse`

### Token Management
- ✅ Use environment variables for tokens: `Authorization: Bearer ${API_TOKEN}`
- ✅ Document required env vars in README
- ✅ Let OAuth handle authentication where available
- ❌ NEVER hardcode tokens in configuration
- ❌ NEVER commit tokens to git
- ❌ NEVER share tokens in documentation

### Permission Scoping
Pre-allow only necessary MCP tools in command frontmatter:
- ✅ `allowed-tools: ["mcp__plugin_api_server__read_data"]`
- ❌ `allowed-tools: ["mcp__plugin_api_server__*"]`

## Error Handling Patterns

### Connection Failures
Handle MCP server unavailability:
- Provide fallback behavior in commands
- Inform user of connection issues
- Check server URL and configuration

### Tool Call Errors
- Validate inputs BEFORE calling MCP tools
- Provide clear, user-friendly error messages
- Check rate limiting and quotas

### Configuration Errors
- Test server connectivity during development
- Validate JSON syntax
- Check required environment variables are set
