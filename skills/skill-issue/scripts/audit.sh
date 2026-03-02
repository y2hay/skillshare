#!/usr/bin/env bash
# skill-issue audit wrapper
# Runs the Node.js audit script with sensible defaults.
#
# Usage:
#   bash audit.sh                          # Scan ./skills + ./memory
#   SKILL_DIRS="./skills,/other" bash audit.sh   # Custom paths
#
# For Clawdbot users, auto-detects system + workspace skill dirs:
#   bash audit.sh --clawdbot

set -euo pipefail
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"

if [[ "${1:-}" == "--clawdbot" ]]; then
  # Auto-detect Clawdbot paths
  CLAWDBOT_SYSTEM="/opt/homebrew/lib/node_modules/clawdbot/skills"
  CLAWDBOT_WORKSPACE="${HOME}/clawd/skills"
  DIRS=""
  [[ -d "$CLAWDBOT_SYSTEM" ]] && DIRS="$CLAWDBOT_SYSTEM"
  [[ -d "$CLAWDBOT_WORKSPACE" ]] && DIRS="${DIRS:+$DIRS,}$CLAWDBOT_WORKSPACE"
  export SKILL_DIRS="${DIRS:-./skills}"
  export MEMORY_DIR="${HOME}/clawd/memory"
fi

exec node "$SCRIPT_DIR/audit.mjs"
