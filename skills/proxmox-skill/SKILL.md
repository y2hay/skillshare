---
name: proxmox-skill
description: Operate a Proxmox VE environment by reading connection details from the local `.env` file and using the bundled helper script to inspect nodes, QEMU VMs, and LXC containers, start existing guests, allocate a new VM or container ID, create a new VM shell, clone from a template, or create a new LXC container from a local Proxmox template.
version: 1
triggers: ["proxmox", "create VM", "list nodes", "clone template", "LXC"]
allowed-tools: [terminal, python]
---

# Proxmox Guest Control

## Overview

Use this skill from the directory that contains `.env`.

Prefer the bundled helper script over ad-hoc curl snippets. The script reads `IP`, `USR`, and `PWD` from the local `.env`, normalizes usernames that omit a realm, authenticates against the Proxmox REST API, and handles the cookie plus CSRF token needed for write operations.

## Setup

Before using this skill for the first time, copy the environment template and fill in your Proxmox credentials:

```bash
cp .env.example .env
```

Then edit `.env` with your Proxmox host IP, username, and password:
```
IP=proxmox-host-or-ip
USR=root@pam
PWD=replace-me
PORT=8006
VERIFY_SSL=false
```

**Security note**: The `.env` file is gitignored by default. Never commit it or share its contents.

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

## Quick Start

Run all commands from this skill root so the helper can find `.env` automatically.

Inspect nodes:

```bash
uv run ./scripts/proxmox_vm.py nodes
```

Inspect the next free VM ID:

```bash
uv run ./scripts/proxmox_vm.py nextid
```

Inspect VMs on a node:

```bash
uv run ./scripts/proxmox_vm.py list-vms --node pve
```

Inspect LXC containers on a node:

```bash
uv run ./scripts/proxmox_vm.py list-cts --node pve
```

Inspect all nodes at once:

```bash
uv run ./scripts/proxmox_vm.py list-vms
```

## Start an Existing VM

Use this flow when the VM already exists and only needs to be powered on.

1. Find the target node and VM ID.

```bash
uv run ./scripts/proxmox_vm.py list-vms --node pve
```

2. Start the VM and wait for the task to finish when confirmation is needed.

```bash
uv run ./scripts/proxmox_vm.py start --node pve --vmid 120 --wait
```

3. Re-check the VM list for a second confirmation pass.

```bash
uv run ./scripts/proxmox_vm.py list-vms --node pve
```

## Create a Blank VM

Use this flow when a new VM shell is needed with explicit CPU, memory, network, and optional disk settings.

1. Get a free VM ID.

```bash
uv run ./scripts/proxmox_vm.py nextid
```

2. Create the VM shell.

```bash
uv run ./scripts/proxmox_vm.py create \
  --node pve \
  --vmid 220 \
  --name app-220 \
  --memory 4096 \
  --cores 4 \
  --bridge vmbr0 \
  --storage local-lvm \
  --disk-gb 32 \
  --wait
```

3. Add any Proxmox-specific arguments with repeated `--param key=value`.
   - Use this for options that are not covered by the first-class flags.
   - Example: `--param tags=lab --param ciuser=ubuntu`

4. Start the new VM if the shell should be booted immediately.

```bash
uv run ./scripts/proxmox_vm.py start --node pve --vmid 220 --wait
```

## Clone from a Template

Use this flow when a template VM already exists on the target cluster.

1. Inspect the source template and the destination node.

```bash
uv run ./scripts/proxmox_vm.py list-vms --node pve
```

2. Clone it to a new VM ID.

```bash
uv run ./scripts/proxmox_vm.py clone \
  --node pve \
  --source-vmid 9000 \
  --newid 221 \
  --name app-221 \
  --full \
  --wait
```

3. Boot the cloned VM when needed.

```bash
uv run ./scripts/proxmox_vm.py start --node pve --vmid 221 --wait
```

## Create an LXC Container

Use this flow when a lightweight container is wanted rather than a full VM.

1. Inspect the available Proxmox templates and confirm the target node.
   - Read [references/api-notes.md](./references/api-notes.md) for the known template patterns in this environment.
   - Prefer a `local:vztmpl/...` template that already exists on the node.

2. Get a free ID.

```bash
uv run ./scripts/proxmox_vm.py nextid
```

3. Create the container from a template and optionally boot it immediately.

```bash
uv run ./scripts/proxmox_vm.py create-ct \
  --node pve \
  --vmid 230 \
  --hostname agent-230 \
  --ostemplate local:vztmpl/ubuntu-24.04-standard_24.04-2_amd64.tar.zst \
  --storage local-lvm \
  --memory 512 \
  --swap 512 \
  --cores 1 \
  --disk-gb 8 \
  --bridge vmbr0 \
  --ip dhcp \
  --wait \
  --start-after-create
```

4. If the container was created without `--start-after-create`, boot it with:

```bash
uv run ./scripts/proxmox_vm.py start-ct --node pve --vmid 230 --wait
```

5. Re-check the container list when a visible state confirmation is needed.

```bash
uv run ./scripts/proxmox_vm.py list-cts --node pve
```

## Verification

- Use `--wait` on `start`, `create`, `clone`, `start-ct`, and `create-ct` when the task result is needed instead of only the queued task ID.
- Re-run `list-vms` after a mutation when a visible state check is wanted.
- Re-run `list-cts` after container mutations when a visible state check is wanted.
- Read [references/api-notes.md](./references/api-notes.md) when the exact API assumptions or command patterns behind the helper are needed.

## Avoid

- Do not duplicate credentials from `.env` into logs, markdown, or chat output.
- Do not guess the node name, bridge, storage, or free VM ID.
- Do not guess the template volid for `create-ct`.
- Do not call `create` without checking whether a `clone` was actually intended.
