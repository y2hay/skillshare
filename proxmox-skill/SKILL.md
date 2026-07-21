---
name: proxmox-skill
description: Operate a Proxmox VE environment from this skill folder by reading connection details from the local `.env` file and using the bundled helper script to inspect nodes, QEMU VMs, and LXC containers, start existing guests, allocate a new VM or container ID, create a new VM shell, clone from a template, or create a new LXC container from a local Proxmox template. Use when Codex needs to work against this specific Proxmox host instead of only describing the API.
---

# Proxmox Guest Control

## Overview

Use this skill from the directory that contains `.env`.

Prefer the bundled helper script over ad-hoc curl snippets. The script reads `IP`, `USR`, and `PWD` from the local `.env`, normalizes usernames that omit a realm, authenticates against the Proxmox REST API, and handles the cookie plus CSRF token needed for write operations.

## Safety Rules

1. Read `.env` from disk instead of sourcing it into the shell.
   - This repo stores the password under `PWD=...`, which collides with common shell environment usage.
   - Let `scripts/proxmox_vm.py` load the file directly.

2. Normalize the Proxmox username before calling the API.
   - If `USR` already contains a realm such as `root@pam`, use it as-is.
   - If it does not contain `@`, treat it as `@pam` by default.

3. Inspect before mutating.
   - Start with `nodes`, `nextid`, or `list-vms` before `start`, `create`, or `clone`.
   - Confirm the target node name, the VM ID, and the bridge or storage name before writing anything.

4. Prefer `clone` when a template already exists.
   - Use `create` for a blank VM shell.
   - Use `clone` for faster provisioning from a prepared template.

5. Use `--verify-ssl` only when the Proxmox certificate chain is already trusted on this machine.
   - The helper defaults to the common self-signed Proxmox setup.

