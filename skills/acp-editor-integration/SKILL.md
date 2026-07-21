---

name: acp-editor-integration
description: |
  Use when setting up Hermes Agent as an ACP server for VS Code, Zed, or JetBrains; triggers include "set up ACP", "Hermes ACP server", "VS Code ACP", "Zed ACP", and "JetBrains ACP". Covers dependency install, extension configuration, verification, and common pitfalls.
tools:
  - terminal
  - uv
  - hermes
  - code
preconditions:
  - Hermes Agent installed from source (or hermes-acp binary on PATH)
  - Python venv for Hermes Agent exists
  - uv available on PATH
steps:
- Install ACP Python dependency
  - Run `uv pip install agent-client-protocol==0.9.0` from the project root
  - This avoids PEP 668 issues on Arch Linux
  - Version pin must match pyproject.toml extras `[acp]`
- Verify the ACP server works
  - hermes acp --check confirms imports and deps
  - timeout 3 hermes acp confirms the server starts, loads .env, and accepts connections
- Install the VS Code extension
  - formulahendry.acp-client is the official/recommended ACP Client
  - Hermes Agent appears in its built-in agent list — no manual config needed
- (Optional) Install browser tools for browser_navigate etc.
  - hermes acp --setup-browser installs Node.js 22 LTS + agent-browser + Chromium
  - Idempotent, ~400 MB download
pitfalls:
  - "On Arch Linux, bare `pip install` hits PEP 668 externally-managed-environment. Use `uv pip install` instead."
  - "The `hermes-agent` skill is a bundled skill and cannot be edited. ACP setup steps belong here instead."
  - "`hermes-acp` binary may exist in the venv before the `acp` Python package is installed (it's a thin wrapper). Always run `hermes acp --check` to confirm the full dependency is present."
  - "The `PermissionError` on `_add_reader` during `timeout 3 hermes acp` is harmless — it's the timeout killing stdin. The important lines are `Loaded env from ...` and `ACP client connected`."
verification:
  - hermes acp --check prints "Hermes ACP check OK"
  - timeout 3 hermes acp 2>&1 shows "Starting hermes-agent ACP adapter" and "ACP client connected"
  - VS Code ACP Client panel shows Hermes Agent in the agent list
examples:
  - "Set up ACP so I can use Hermes in VS Code"
  - "Install ACP dependencies for editor integration"
  - "Connect Hermes to the ACP Client VS Code extension"

---

# ACP Editor Integration

Set up Hermes Agent as an ACP (Agent Client Protocol) server for VS Code, Zed, and JetBrains editors.

## What ACP Exposes in Editor Mode

When running as an ACP server, Hermes uses a curated `hermes-acp` toolset:
- File tools: `read_file`, `write_file`, `patch`, `search_files`
- Terminal: `terminal`, `process`
- Web/browser: `web_search`, `web_extract`, `browser_*`
- `memory`, `todo`, `session_search`, `skills`
- `execute_code`, `delegate_task`, `vision`

It excludes messaging delivery, cronjob management, and other tools that don't fit editor UX.

## Installation

### 1. Install the ACP Python dependency

```bash
cd ~/.hermes/hermes-agent
uv pip install agent-client-protocol==0.9.0
```

The version pin matches `pyproject.toml` extras `[acp]`.

### 2. Verify

```bash
hermes acp --check
# Expected: "Hermes ACP check OK"

timeout 3 hermes acp 2>&1
# Expected: "Starting hermes-agent ACP adapter" + "ACP client connected"
# Ignore PermissionError spam — that's just timeout killing stdin.
```

### 3. Install the VS Code Extension

```bash
code --install-extension formulahendry.acp-client
```

Hermes Agent is in the extension's **built-in agent list** — no manual config needed.

## Using It

1. Launch VS Code
2. Click the **ACP icon** in the Activity Bar
3. Select **Hermes Agent** from the agent list
4. Click **Connect** and start chatting

### Custom Agent Config

If the built-in list doesn't include Hermes, add to VS Code `settings.json`:

```json
"acp.agents": {
  "Hermes Agent": {
    "command": "hermes",
    "args": ["acp"]
  }
}
```

## Optional: Browser Tools

```bash
hermes acp --setup-browser         # interactive (~400 MB download)
hermes acp --setup-browser --yes   # non-interactive
```

Installs Node.js 22 LTS + agent-browser + Playwright Chromium into `~/.hermes/node/`. Idempotent.

## Zed

Use the built-in agent discovery in the Agent Panel, or add manually to `settings.json`:

```json
"agent_servers": {
  "hermes-agent": {
    "type": "custom",
    "command": "hermes",
    "args": ["acp"]
  }
}
```

## JetBrains

Point an ACP-compatible plugin at `hermes acp`.

## ACP CLI Reference

```
hermes acp                  Start ACP server (stdio JSON-RPC)
hermes acp --check          Verify deps + imports
hermes acp --version        Print Hermes version
hermes acp --setup          Interactive provider/model setup
hermes acp --setup-browser  Install browser tools
```

## Troubleshooting

| Symptom | Fix |
|---------|-----|
| `ModuleNotFoundError: No module named 'acp'` | `uv pip install agent-client-protocol==0.9.0` |
| `hermes-acp` binary exists but fails | Install the Python package (wrapper is present, dep is missing) |
| `pip install` fails with PEP 668 error | Use `uv pip install` instead |
| ACP Client doesn't list Hermes | Update extension or add manual `acp.agents` config |
| Server starts but VS Code doesn't connect | Ensure `hermes` is on VS Code's PATH, or use full path in config |
