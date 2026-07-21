---
name: proxmox
description: Use when managing Proxmox VE on the caspar node; triggers include "manage Proxmox", "Proxmox container", "Proxmox VM", "caspar node", and "snapshot VM". Covers containers, VMs, storage, backups, and snapshots.
---

# Proxmox Skill for pi — caspar Node Operations

You are managing a single Proxmox VE node. This node IS your entire domain.

## Node Identity

### LXC Containers

# Refer to _AGENTS.md_

| VMID | Name | Status | Notes |
| ---- | ---- | ------ | ----- |

### QEMU VMs

| VMID | Name | Status | Notes |
| ---- | ---- | ------ | ----- |

## Storage

## Available Tools

# Check storage

pvesm status

````

### Direct CLI (pct / qm)
```bash
pct list                          # List containers
pct enter <VMID>                  # Interactive shell
pct exec <VMID> -- <cmd>          # Run command
pct start/shutdown/stop <VMID>
pct config <VMID>
pct set <VMID> --cores 4 --memory 4096

qm list                           # List VMs
qm start/shutdown/stop <VMID>
qm config <VMID>
````

## Container Lifecycle

# Create with pct CLI

pct create <VMID> local:vztmpl/debian-\*\*.tar.zst \
 --hostname myservice \
 --cores 2 --memory 2048 --swap 512 \
 --net0 name=eth0,bridge=vmbr0,ip=10.10.0.X/24,gw=10.10.0.1 \
 --local-btrfs
--nameserver 10.10.0.253 \
 --password 666666

````

### Resource Adjustment
```bash
pct set <VMID> --cores 4
pct set <VMID> --memory 4096
pct resize <VMID> rootfs +10G
````

## Backup & Snapshots

### Snapshots (before risky changes)

````

### Backups
```bash
vzdump <VMID> --storage local --mode snapshot --compress zstd
````

### Restore

```bash
# LXC
pct restore <VMID> /var/lib/vz/dump/vzdump-lxc-<VMID>-*.tar.zst --storage local
# VM
qmrestore /var/lib/vz/dump/vzdump-qemu-<VMID>-*.vma.zst <VMID>
```

## Troubleshooting

### Container won't start

```bash
pct unlock <VMID>           # Remove stale lock
pct config <VMID>           # Check config
pct console <VMID>          # Watch boot
```

### Disk space

```bash
df -h                        # Filesystem overview
pvesm status                 # Storage pools
du -sh /var/lib/vz/dump/* | sort -rh  # Old backups
journalctl --vacuum-size=200M
```

### Web UI unavailable

```bash
systemctl restart pveproxy pvedaemon
```

### Service health checks

````

## Monthly Maintenance

```bash
apt update && apt upgrade
pveam update
btrfs scrub start / && btrfs scrub status /
ls -lh /var/lib/vz/dump/          # Review old backups
````

## Critical Rules

1. **Always snapshot before config changes**

## Ansible Automation (community.proxmox)

When automating Proxmox with Ansible, prefer the `community.proxmox` collection over raw CLI commands. Native modules are idempotent by design and handle edge cases that shell commands miss.

### Module Selection

| Operation     | Use Module                          | NOT CLI       |
| ------------- | ----------------------------------- | ------------- |
| Create VM     | `community.proxmox.proxmox_kvm`     | `qm create`   |
| Clone VM      | `community.proxmox.proxmox_kvm`     | `qm clone`    |
| Manage users  | `community.proxmox.proxmox_user`    | `pveum user`  |
| Manage groups | `community.proxmox.proxmox_group`   | `pveum group` |
| Manage pools  | `community.proxmox.proxmox_pool`    | `pveum pool`  |
| Manage ACLs   | `community.proxmox.proxmox_acl`     | `pveum acl`   |
| Storage       | `community.proxmox.proxmox_storage` | `pvesm`       |

Some operations lack native modules — use CLI with idempotency guards:

| Operation      | Requires CLI         | Reason           |
| -------------- | -------------------- | ---------------- |
| Cluster create | `pvecm create`       | No module exists |
| Cluster join   | `pvecm add`          | No module exists |
| CEPH init      | `pveceph init`       | Complex workflow |
| CEPH OSD       | `pveceph osd create` | Complex workflow |

### Installation

```bash
ansible-galaxy collection install community.proxmox
```

### API Token Authentication

caspar already has `root@pam!pi-agent`. Standard playbook pattern:

```yaml
proxmox_api_host: "10.10.0.200"
proxmox_api_user: "root@pam"
proxmox_token_id: "pi-agent"
proxmox_token_secret: "{{ lookup('env', 'PROXMOX_TOKEN_SECRET') }}"

- name: Create VM from template
  community.proxmox.proxmox_kvm:
    api_host: "{{ proxmox_api_host }}"
    api_user: "{{ proxmox_api_user }}"
    api_token_id: "{{ proxmox_token_id }}"
    api_token_secret: "{{ proxmox_token_secret }}"
    node: caspar
    vmid: "{{ vm_id }}"
    name: "{{ vm_name }}"
    clone: "{{ template_name }}"
    full: true
    storage: local-btrfs
    memory: "{{ vm_memory | default(4096) }}"
    cores: "{{ vm_cores | default(2) }}"
    state: present
  delegate_to: localhost
```

### Idempotency for CLI Fallbacks

When a native module doesn't exist, add pre-checks and proper `changed_when`/`failed_when`:

```yaml
# API token creation (no native module)
- name: Create API token
  ansible.builtin.command: >
    pveum user token add {{ username }}@pam {{ token_name }}
    --privsep 0
  register: token_result
  changed_when: "'already exists' not in token_result.stderr"
  failed_when:
    - token_result.rc != 0
    - "'already exists' not in token_result.stderr"
  no_log: true

# Read-only cluster check (safe no-op)
- name: Get cluster status
  ansible.builtin.command: pvecm status
  register: cluster_status
  changed_when: false
  failed_when: false

# Conditional cluster create
- name: Create cluster on primary
  ansible.builtin.command: pvecm create {{ cluster_name }}
  when: cluster_status.rc != 0
  register: cluster_create
  changed_when: cluster_create.rc == 0
```

### Network Configuration

Use `community.general.interfaces_file` for persistent network changes:

```yaml
- name: Configure VLAN-aware bridge
  community.general.interfaces_file:
    iface: vmbr1
    option: bridge-vlan-aware
    value: "yes"
    backup: true
    state: present
  notify: reload network
```

### Anti-Patterns

**Using CLI when a module exists:**

```yaml
# BAD
- name: Create user
  ansible.builtin.command: pveum user add terraform@pve

# GOOD
- name: Create user
  community.proxmox.proxmox_user:
    api_host: "{{ proxmox_api_host }}"
    api_user: "root@pam"
    api_password: "{{ password }}"
    userid: "terraform@pve"
    state: present
```

**Missing idempotency on destructive CLI:**

```yaml
# BAD — fails on second run
- name: Create cluster
  ansible.builtin.command: pvecm create MyCluster

# GOOD — guarded by pre-check
- name: Check cluster status
  ansible.builtin.command: pvecm status
  register: cluster_check
  changed_when: false
  failed_when: false

- name: Create cluster
  ansible.builtin.command: pvecm create MyCluster
  when: cluster_check.rc != 0
```

**API calls from managed node instead of control host:**

```yaml
# BAD — calls Proxmox API from itself
- name: Create VM
  community.proxmox.proxmox_kvm:
    api_host: "{{ inventory_hostname }}"

# GOOD — delegate to the host running Ansible
- name: Create VM
  community.proxmox.proxmox_kvm:
    api_host: "{{ proxmox_api_host }}"
  delegate_to: localhost
```
