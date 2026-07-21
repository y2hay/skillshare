---
name: proxmox
triggers: ["Proxmox", "Proxmox VE", "PVE", "caspar node", "melchior node", "Proxmox container", "Proxmox VM", "snapshot VM", "Proxmox storage", "pvecm", "pct", "qm", "Proxmox backup", "Proxmox cluster", "LXC container", "Proxmox guest"]
description: "Use when managing Proxmox VE nodes in the xcx homelab. Branches: user mentions a specific node (\"caspar\" or \"melchior\"), asks to manage a guest (VM or LXC), says \"snapshot\", \"backup\", \"storage\", \"pct\", \"qm\", \"pvecm\", or \"cluster\". Covers guest lifecycle, storage operations, backup/restore, cluster management, API vs SSH access, and the snapshot-before-change safety protocol. Does NOT cover gaming VMs (use gaming-vm) or generic Docker orchestration inside guests. Use pi-proxmox plugin tools (proxmox_*) as primary access method over SSH direct CLI."
metadata:
  version: 2
  source: combined from PROXMOX-AGENTS.md, pi-proxmox plugin, and current skill
---

# Proxmox — caspar + melchior Node Operations

Managing two Proxmox VE nodes in the xcx homelab.

## Leading words

- **node** — a Proxmox VE host: caspar (primary) or melchior (secondary/standalone). Every operation targets one node.
- **guest** — any managed workload: both VMs (QEMU/KVM) and containers (LXC). One word for the same lifecycle regardless of type.
- **snapshot** — the pre-change safety net. Always take one before modifying guest config, OS packages, or service config.

## Step 1 — Orient

Before touching anything, establish which node and which guest the task targets.

### Node identity

| Node | IP | Role | RAM | Storage | Cluster |
|------|----|------|-----|---------|---------|
| **caspar** | 10.10.0.200 | Primary Proxmox host | 16 GB | 475 GB NVMe (Btrfs) | Clustered (standalone) |
| **melchior** | 10.10.0.150 | Secondary Proxmox host | 38 GB | 2× NVMe (ext4/LVM) | Standalone (not clustered with caspar) |

**caspar** runs the bulk of infrastructure: Docker host dockarr (Traefik, *arr), Proxmox Backup Server, Pi-hole/Technitium DNS, Home Assistant OS, music stack. Btrfs-based storage.

**melchior** runs compute-heavy workloads: Ollama LLM (16 GB allocated), Jellyfin media, Frigate NVR, Authentik SSO, Honcho/Termix. Ext4 + LVM — **not Btrfs**. Not cluster-joined; manage via SSH or local shell when API is unavailable (SSL cert issue from ramiel).

**Completion criterion**: you know which node to operate on and which type of guest to target.

### Guest inventory — caspar

| Guest | VMID | Type | IP | Role |
|-------|------|------|----|------|
| dockarr | 155 | LXC | 10.10.0.155 | Docker: Traefik, *arr, 25+ services, public ingress |
| pbs | 230 | LXC | 10.10.0.230 | Proxmox Backup Server |
| tunerr | 244 | LXC | 10.10.0.244 | Music: Lidarr, Navidrome |
| technitium | 253 | LXC | 10.10.0.253 | Secondary DNS |
| pihole.bak | 254 | LXC | 10.10.0.53 | Primary DNS, Pi-hole |
| haos17.1 | 227 | VM | 10.10.0.225 | Home Assistant OS |
| proxmox-gateway | — | LXC | (TBD) | Gateway — inspect before touching |

### Guest inventory — melchior

| Guest | VMID | Type | IP | Role | Spec |
|-------|------|------|----|------|------|
| technitiumdns2 | 153 | LXC | 10.10.0.153 | DNS test instance | 1C/512 MB — **stopped** |
| ollama | 205 | LXC | 10.10.0.205 | Ollama + Open WebUI | 8C/16 GB, 40 GB root + 64 GB data bind |
| semaphore | 206 | LXC | 10.10.0.206 | Ansible Semaphore | 2C/2 GB |
| authentik | 211 | LXC | 10.10.0.211 | SSO authentication | 2C/8 GB, 16 GB root + data mount |
| jellyfin | 213 | LXC | 10.10.0.202 | Media streaming | 4C/3 GB, `/dev/dri/card1` passthrough |
| sencho | 215 | LXC | 10.10.0.215 | Admin tools, Honcho, Termix, FreshRSS | 4C/8 GB, 32 GB root + 64 GB Docker; `/dev/dri/card1` |
| frigate.lan | 224 | LXC | 10.10.0.224 | NVR / Frigate | 8C/4 GB, `/dev/dri/renderD128` + `card1` |

**Completion criterion**: the target node and guest are identified, and the guest's current status and role are clear.

## Step 2 — Snapshot (safety net)

Before changing guest config, OS packages, service config, or storage on any running production guest:

```bash
pct snapshot <VMID> pre-change-$(date +%Y%m%d-%H%M) --description "Before agent change"
```

For VMs:
```bash
qm snapshot <VMID> pre-change-$(date +%Y%m%d-%H%M) --description "Before agent change"
```

**Completion criterion**: snapshot exists and is listed in `pct snapshot list <VMID>` or `qm snapshot list <VMID>`.

## Step 3 — Execute the change

### Choose your access method

| Scenario | Access method | Tool |
|----------|---------------|------|
| Inspect/list/status from ramiel | Pi Proxmox API tools | `proxmox_node_list`, `proxmox_vm_list`, `proxmox_lxc_list`, etc. |
| Create/modify guest from ramiel | Pi Proxmox API tools | `proxmox_lxc_create`, `proxmox_vm_create`, `proxmox_vm_clone` |
| Snapshot/backup from ramiel | Pi Proxmox API tools | `proxmox_vm_snapshot`, `proxmox_lxc_snapshot`, `proxmox_backup_create` |
| SSH into node for direct CLI | SSH to node | `ssh root@10.10.0.200` (caspar) or `ssh root@10.10.0.150` (melchior) |
| Execute inside LXC | SSH to node + pct | `ssh root@<node> pct exec <VMID> -- <cmd>` |
| Execute inside VM (with agent) | Pi QEMU Guest Agent | `proxmox_vm_agent_exec` (if QEMU agent is running) |

### API tools available (via pi-proxmox plugin)

The `proxmox_*` toolset covers 142 operations. Key groupings:

| Area | Key tools |
|------|-----------|
| **VM lifecycle** | `proxmox_vm_list`, `proxmox_vm_start/stop/shutdown/reset/reboot`, `proxmox_vm_create/delete/clone/migrate`, `proxmox_vm_update_config`, `proxmox_vm_resize_disk`, `proxmox_vm_move_disk` |
| **LXC lifecycle** | `proxmox_lxc_list`, `proxmox_lxc_start/stop/shutdown/reboot`, `proxmox_lxc_create/delete`, `proxmox_lxc_update_config`, `proxmox_lxc_resize` |
| **Snapshots** | `proxmox_vm_snapshot/snapshot_list/snapshot_rollback/snapshot_delete`, `proxmox_lxc_snapshot/snapshot_list/snapshot_rollback/snapshot_delete` |
| **Storage** | `proxmox_storage_list/content/create/detail/delete/scan/upload/remove_volume` |
| **Cluster** | `proxmox_cluster_status/resources/options`, `proxmox_node_list/status/config/services/journal` |
| **Backup** | `proxmox_backup_list/create/delete` |
| **Firewall** | `proxmox_firewall_rules/rule_add/rules_delete/options/aliases/ipset_*` |
| **Access** | `proxmox_user_*/group_*/role_*/acl_*/token_*/domain_list` |
| **HA** | `proxmox_ha_status/resources_*/groups_*/group_create/group_delete` |
| **Universal** | `proxmox_api_call` (any API path), `proxmox_api_upload_file` (multipart upload) |

### CLI commands on-node (when SSH'd in)

```bash
# Status
pct list                         # All containers
qm list                          # All VMs
pvesm status                     # Storage pools
pvecm status || true             # Cluster status (melchior won't have this)
pvesh get /cluster/resources     # All cluster resources

# LXC operations
pct config <VMID>                # Current config
pct enter <VMID>                 # Interactive shell
pct exec <VMID> -- <cmd>         # Run command
pct start/shutdown/stop <VMID>   # Lifecycle
pct set <VMID> --cores 4 --memory 4096  # Adjust resources
pct resize <VMID> rootfs +10G   # Grow rootfs

# VM operations
qm config <VMID>                 # Current config
qm start/shutdown/stop <VMID>    # Lifecycle

# Logs
pvefirewall log                  # Firewall logs
journalctl -u pveproxy           # Web UI logs
journalctl -u pvedaemon          # API daemon logs
```

### LXC create pattern

```bash
pct create <VMID> local:vztmpl/debian-*.tar.zst \
  --hostname <name> \
  --cores 2 --memory 2048 --swap 512 \
  --net0 name=eth0,bridge=vmbr0,ip=10.10.0.X/24,gw=10.10.0.1 \
  --nameserver 10.10.0.253 \
  --password <temp-pw> \
  --start 1
```

On melchior, storage is typically `local-lvm` (LVM-thin) rather than Btrfs — adjust `--storage` accordingly. Check with `pvesm status` before creating.

**Completion criterion**: the change is applied, the guest reports the expected new state, and the snapshot from Step 2 is confirmed unneeded (or the guest is rolled back).

## Step 4 — Verify + document

1. Confirm the guest is healthy:
   ```bash
   pct status <VMID>       # running/stopped
   pct exec <VMID> -- systemctl is-system-running
   ```
2. If the change is durable (new guest, new storage, new DNS entry, config moved):
   - Update `HOSTS/<node>.md` in ritsuko-rebuild (new guest entries)
   - Update `NETWORK.md` if IP/MAC/DNS changed
   - Update `STACKS.md` if Docker placement changed
   - Update `SERVICES/<service>.md` if a new service was added
   - Add entry to `CHANGELOG.md`
3. Clean up the snapshot if everything is verified working:
   ```bash
   pct snapshot delete <VMID> pre-change-<timestamp>
   ```
   (Keep the snapshot if risk of rollback within the session — always clean up before session end.)

**Completion criterion**: the guest passes its health check, and all documentation changes are committed and pushed.

## Storage reference

### caspar

Btrfs-oriented — use `pvesm status` to confirm:

```bash
pvesm status
df -h /var/lib/vz        # Primary Btrfs pool
btrfs scrub status /     # Btrfs health
```

Common storage IDs: `local` (Btrfs), `local-lvm` (LVM-thin on NVMe).

### melchior

Ext4 + LVM — **no Btrfs, no ZFS** (unless live inspection proves otherwise):

```bash
pvesm status              # List pools
lsblk -f                  # Filesystem layout
pvdisplay / vgdisplay     # LVM status
df -h                     # Free space
```

Common storage IDs: `local` (directory), `local-lvm` (LVM-thin).

**Safety rule**: Never use `zfs` or `btrfs` commands on melchior unless live inspection proves the pool exists and the user approves.

## Backup reference

### On-demand backup

```bash
vzdump <VMID> --storage local --mode snapshot --compress zstd
```

### Scheduled backups

```bash
# List existing jobs
proxmox_backup_list

# Create a daily backup job for a guest
proxmox_backup_create id="daily-<name>" node=caspar storage=local schedule="0 2 * * *" vmid=<VMID>
```

### Restore

```bash
# LXC
pct restore <VMID> /var/lib/vz/dump/vzdump-lxc-<VMID>-*.tar.zst --storage local

# VM
qmrestore /var/lib/vz/dump/vzdump-qemu-<VMID>-*.vma.zst <VMID>
```

## Common troubleshooting

### Container won't start

```bash
pct unlock <VMID>           # Remove stale lock file
pct config <VMID>           # Inspect config for errors
pct console <VMID>          # Watch boot log
journalctl -u pvecontainer  # Systemd container service log
```

### Disk space

```bash
df -h                         # Overview
pvesm status                  # Storage pool usage
du -sh /var/lib/vz/dump/* | sort -rh  # Find large backups
journalctl --vacuum-size=200M # Trim logs
```

### Web UI / API unavailable

```bash
systemctl restart pveproxy pvedaemon
systemctl status pveproxy     # Check for cert errors or port conflicts
journalctl -u pveproxy --since "-10m"
```

### melchior API unreachable from ramiel

The Proxmox API on melchior (10.10.0.150:8006) has a known SSL cert issue — API calls fail. Workaround:

```bash
# SSH directly
ssh root@10.10.0.150 <command>

# Or through a bash heredoc for multi-line commands
ssh root@10.10.0.150 bash << 'EOF'
qm list
pct list
pvesm status
EOF
```

## Ansible automation patterns

When automating Proxmox with Ansible, prefer the `community.proxmox` collection over raw CLI commands. Native modules are idempotent by design.

### Module selection

| Operation | Use module | Not CLI |
|-----------|------------|---------|
| Create VM | `community.proxmox.proxmox_kvm` | `qm create` |
| Clone VM | `community.proxmox.proxmox_kvm` (clone:) | `qm clone` |
| Users/groups/ACLs | `proxmox_user`, `proxmox_group`, `proxmox_acl` | `pveum *` |
| Storage | `community.proxmox.proxmox_storage` | `pvesm` |

### API token auth

caspar has `root@pam!pi-agent` configured. Standard playbook:

```yaml
- name: Create VM from template
  community.proxmox.proxmox_kvm:
    api_host: "10.10.0.200"
    api_user: "root@pam"
    api_token_id: "pi-agent"
    api_token_secret: "{{ lookup('env', 'PROXMOX_TOKEN_SECRET') }}"
    node: caspar
    vmid: "{{ vm_id }}"
    name: "{{ vm_name }}"
    clone: "{{ template_name }}"
    full: true
    storage: local
  delegate_to: localhost
```

## Safety rules

1. **Always snapshot before config changes** — guest config, OS packages, service config, or storage. See Step 2.

2. **Never run without explicit approval**: guest deletion, disk deletion, backup deletion, `rm -rf`, `wipefs`, `mkfs` outside a bounded temp path, credential rotation, DNS/ingress/auth/backup service changes, firewall or public exposure changes, bulk host package upgrades, node reboot/power-off.

3. **Storage**: caspar = Btrfs, melchior = ext4/LVM. Do not use ZFS or Btrfs commands on melchior unless live inspection proves otherwise.

4. **CLI guard**: always wrap on-node commands from a fish shell in `bash -c '...'` or use heredocs. Fish does not handle inline SSH commands the same way bash does.

5. **Documentation update contract**: every durable change updates the relevant file in ritsuko-rebuild (HOSTS, NETWORK, STACKS, SERVICES, CHANGELOG) and stamps a `last-verified` date. See PROXMOX-AGENTS.md for the full protocol.

## Monthly maintenance

```bash
apt update && apt upgrade -y          # Host packages
pveam update                          # LXC template list
btrfs scrub start / && btrfs scrub status /   # caspar only — Btrfs health
ls -lh /var/lib/vz/dump/              # Review old backups
journalctl --vacuum-size=200M         # Trim system logs
```
