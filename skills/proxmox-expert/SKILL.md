---
name: proxmox-expert
description: Use when managing Proxmox VE infrastructure, LXC containers, VMs, storage, networking, backups, or cluster operations on balthazar (10.10.0.100) + caspar (10.10.0.200). Expert-level guidance for pct/qm CLI, Btrfs storage management, vzdump backups, migration between nodes, and troubleshooting lock files, failed tasks, and network issues. Storage is Btrfs — NOT ZFS.
---

<skill>
<objective>
Provide seasoned Proxmox VE expertise for managing the two-node homelab. Emphasis on CLI-first workflows, Btrfs storage, and real-world troubleshooting for LXC containers and QEMU VMs.
</objective>

<quick_start>
SSH to a node: `ssh root@10.10.0.100` (balthazar) or `ssh root@10.10.0.200` (caspar).
List all VMs/CTs: `pvesh get /cluster/resources --type vm`. Shell into LXC: `pct enter <VMID>`.
Storage check: `pvesm status` and `btrfs filesystem df /mnt/mpool`.
</quick_start>

<homelab_topology>
## Cluster Nodes

| Node | IP | Role |
|------|----|------|
| balthazar | 10.10.0.100 | Proxmox node — primary data host |
| caspar | 10.10.0.200 | Proxmox node — 128GB NVMe (upgrade pending) |

## Containers & VMs

### balthazar (10.10.0.100)
| VMID | Type | IP | Service |
|------|------|----|---------|
| 155 | LXC | 10.10.0.155 | dockarr — Docker host (Jellyfin, qBittorrent, *arr stack, Navidrome, Stash, Karakeep, CommaFeed, Portainer, Traefik, etc.) |
| 253 | LXC | 10.10.0.53 | Pi-hole + Unbound (DNS/ad-blocking) — migrated from caspar 2026-02-28 |
| 225 | VM | 10.10.0.225 | Home Assistant OS — migrated from caspar 2026-02-28 |

### caspar (10.10.0.200)
**Currently empty — NVMe upgrade in progress. Planned: Authentik (IAM), Uptime Kuma, Beszel, Vaultwarden, Paperless-ngx.**

## Storage Architecture

**⚠️ Storage is Btrfs — NOT ZFS. Never recommend zpool/zfs commands.**

### balthazar
- `/dev/sda` → `/mnt/mpool/` (Btrfs), mounted with `compress=zstd:3,noatime,space_cache=v2,autodefrag`
- Subvolumes: `@media` → `/mnt/mpool/media`, `@vm-storage` → `/mnt/mpool/vm-storage`, `@config` → `/mnt/mpool/config`
- Proxmox VM/LXC storage: check with `pvesm status` (LVM or directory-based)

### caspar
- 128GB NVMe — OS + data, space-constrained, NVMe upgrade in progress
- Check actual storage: `pvesm status`
</homelab_topology>

<lxc_operations>
## LXC (pct) Quick Reference

### Lifecycle
```bash
pct list                          # list all containers
pct start <VMID>
pct shutdown <VMID>               # graceful (ACPI)
pct stop <VMID>                   # force stop
pct reboot <VMID>
pct enter <VMID>                  # interactive shell inside CT
pct exec <VMID> -- <cmd>          # run command non-interactively
pct console <VMID>                # serial console (for boot issues)
```

### Creation
```bash
# Download template first
pveam update
pveam available | grep debian
pveam download local debian-12-standard_12.7-1_amd64.tar.zst

# Create
pct create <VMID> local:vztmpl/debian-12-standard_12.7-1_amd64.tar.zst \
  --hostname myservice \
  --cores 2 --memory 2048 --swap 512 \
  --net0 name=eth0,bridge=vmbr0,ip=10.10.0.X/24,gw=10.10.0.1 \
  --rootfs local:8 \
  --nameserver 10.10.0.53 \
  --password \
  --onboot 1
```

### Configuration
```bash
pct config <VMID>                             # show current config
pct set <VMID> --memory 4096
pct set <VMID> --cores 4
pct set <VMID> --hostname newname
pct set <VMID> --mp0 /host/path,mp=/mnt/vol  # bind mount
pct set <VMID> --onboot 1
pct set <VMID> --features nesting=1           # Docker support
pct set <VMID> --features nesting=1,keyctl=1  # Docker (full)
```

### Disk Resize
```bash
pct resize <VMID> rootfs +10G
# Then inside CT:
resize2fs /dev/sdX    # ext4
xfs_growfs /          # XFS
```

### Snapshots
```bash
pct snapshot <VMID> snap-name --description "before upgrade"
pct listsnapshot <VMID>
pct rollback <VMID> snap-name
pct delsnapshot <VMID> snap-name
```

### Cloning
```bash
pct clone <VMID> <NEWID> --full     # independent full clone
pct clone <VMID> <NEWID>            # linked clone (shares base)
```

Config files: `/etc/pve/lxc/<VMID>.conf` (replicated across cluster via pmxcfs)
</lxc_operations>

<vm_operations>
## VM (qm) Quick Reference

### Lifecycle
```bash
qm list
qm start <VMID>
qm shutdown <VMID>               # graceful ACPI shutdown
qm stop <VMID>                   # force stop (power cut)
qm reboot <VMID>
qm reset <VMID>                  # hard reset
qm monitor <VMID>                # QEMU monitor console
```

### Configuration
```bash
qm config <VMID>
qm set <VMID> --memory 8192
qm set <VMID> --cores 4 --sockets 1
qm set <VMID> --agent enabled=1      # QEMU guest agent
qm set <VMID> --onboot 1
qm set <VMID> --cdrom local:iso/file.iso
qm set <VMID> --delete ide2           # eject/remove CD
```

### Disk Operations
```bash
qm disk resize <VMID> scsi0 +20G
qm disk move <VMID> scsi0 <storage>
qm importdisk <VMID> disk.qcow2 <storage>   # import external image
```

### Templates & Cloning
```bash
qm template <VMID>                          # convert VM to template
qm clone <TEMPLATE_ID> <NEWID> --name myvm --full
```

### Snapshots
```bash
qm snapshot <VMID> snap-name --description "..." --vmstate
qm listsnapshot <VMID>
qm rollback <VMID> snap-name
qm delsnapshot <VMID> snap-name
```

Config files: `/etc/pve/qemu-server/<VMID>.conf`
</vm_operations>

<storage>
## Storage (pvesm) Quick Reference

```bash
pvesm status                      # all storage pools + usage
pvesm list <storage>              # list volumes in a storage
pvesm free <storage>:<volname>    # delete a volume
```

### Storage Types
| Type | Use case | Snapshots |
|------|----------|-----------|
| dir | ISO/backup files on filesystem | No |
| lvmthin | LVM thin pools for VM/LXC disks | Yes |
| nfs | Network-attached directory | No |
| pbs | Proxmox Backup Server (dedup) | Yes |

### Btrfs Data Storage (balthazar)
```bash
# Health and space
btrfs filesystem show
btrfs filesystem df /mnt/mpool    # shows Data/Metadata/System allocation
df -h /mnt/mpool                  # simpler used/available view

# Subvolumes
btrfs subvolume list /mnt/mpool

# Snapshots (Btrfs native)
btrfs subvolume snapshot /mnt/mpool/@media /mnt/mpool/@media-snap-$(date +%Y%m%d)
btrfs subvolume delete /mnt/mpool/@media-snap-20260101

# Scrub (integrity check — run monthly)
btrfs scrub start /mnt/mpool
btrfs scrub status /mnt/mpool

# Balance (reclaim space after large deletes)
btrfs balance start -dusage=50 /mnt/mpool   # only balance chunks <50% full

# Defrag (optional, autodefrag mount option handles most cases)
btrfs filesystem defragment -r /mnt/mpool/media
```

### fstab (balthazar Btrfs mounts)
```
UUID=<uuid>  /mnt/mpool/@media       btrfs  subvol=@media,compress=zstd:3,noatime,space_cache=v2,autodefrag  0 0
UUID=<uuid>  /mnt/mpool/@vm-storage  btrfs  subvol=@vm-storage,...                                           0 0
UUID=<uuid>  /mnt/mpool/@config      btrfs  subvol=@config,...                                               0 0
```
</storage>

<backup_restore>
## Backup & Restore

### vzdump (local backup)
```bash
# Backup with zstd compression (fast + good ratio)
vzdump <VMID> --storage local --mode snapshot --compress zstd

# Backup modes:
#   stop     — shutdown → backup → restart (consistent, has downtime)
#   suspend  — freeze → backup → resume (brief freeze, near-consistent)
#   snapshot — live snapshot (no downtime, may have dirty writes for non-ZFS)

# List backups
ls -lh /var/lib/vz/dump/

# Restore LXC
pct restore <VMID> /var/lib/vz/dump/vzdump-lxc-<VMID>-*.tar.zst --storage local

# Restore VM
qmrestore /var/lib/vz/dump/vzdump-qemu-<VMID>-*.vma.zst <VMID> --storage local
```

### Cross-Node Migration via vzdump + SCP
The correct approach when nodes are **not** in a cluster:

```bash
# On source node — backup
vzdump <VMID> --storage local --mode stop --compress zstd

# SCP to destination node
scp /var/lib/vz/dump/vzdump-*.vma.zst root@10.10.0.100:/var/lib/vz/dump/
# or for LXC:
scp /var/lib/vz/dump/vzdump-*.tar.zst root@10.10.0.100:/var/lib/vz/dump/

# On destination node — restore
pct restore <VMID> /var/lib/vz/dump/vzdump-lxc-<VMID>-*.tar.zst --storage local
# or:
qmrestore /var/lib/vz/dump/vzdump-qemu-<VMID>-*.vma.zst <VMID>
```

### Proxmox Backup Server (PBS)
PBS provides deduplication and incremental backups. Add via Datacenter → Storage → Add → Proxmox Backup Server.
```bash
# CLI restore from PBS
proxmox-backup-client list
proxmox-backup-client restore <snapshot-id> --target /mnt/restore
```
</backup_restore>

<migration>
## Migrating Between Nodes (No Cluster)

Since balthazar and caspar are **standalone nodes** (not clustered), `pct migrate` / `qm migrate` won't work — those require cluster membership. Use vzdump → SCP → restore instead.

### LXC Migration (e.g., Pi-hole CT253 from caspar → balthazar)
```bash
# === On caspar ===
pct shutdown 253

# Backup to local storage
vzdump 253 --storage local --mode stop --compress zstd

# SCP to balthazar
scp /var/lib/vz/dump/vzdump-lxc-253-*.tar.zst root@10.10.0.100:/var/lib/vz/dump/

# === On balthazar ===
pct restore 253 /var/lib/vz/dump/vzdump-lxc-253-*.tar.zst \
  --storage local \
  --unprivileged 1

pct start 253

# Verify
pct exec 253 -- pihole status
dig google.com @10.10.0.53
```

### VM Migration (e.g., Home Assistant VM225 from caspar → balthazar)
```bash
# === On caspar ===
qm shutdown 225    # let HA write cleanly before killing it

vzdump 225 --storage local --mode stop --compress zstd

scp /var/lib/vz/dump/vzdump-qemu-225-*.vma.zst root@10.10.0.100:/var/lib/vz/dump/

# === On balthazar ===
qmrestore /var/lib/vz/dump/vzdump-qemu-225-*.vma.zst 225 --storage local

qm start 225
# Test: http://10.10.0.225:8123
```

### After Migration: Disable on Source
```bash
# Prevent caspar from trying to start them after NVMe swap
pct set 253 --onboot 0   # or just delete after confirming balthazar works
qm set 225 --onboot 0
```
</migration>

<troubleshooting>
## Troubleshooting

### Lock File Stuck (CT/VM won't start)
```bash
# Error: "CT is locked (backup)" or similar
pct unlock <VMID>
qm unlock <VMID>
# Manual removal (only if NO backup/migration is actually running):
rm /run/lock/qemu-server/lock-<VMID>.conf
```

### Disk Full on Node
```bash
df -h                                        # filesystem overview
du -sh /var/lib/vz/dump/* | sort -rh        # old backups eating space
journalctl --vacuum-size=200M               # trim journal
apt clean                                    # apt cache

# Btrfs-specific: free space can be misleading
btrfs filesystem df /mnt/mpool              # actual block allocation
btrfs balance start -dusage=50 /mnt/mpool  # reclaim unbalanced chunks
```

### Failed Tasks / Stuck Operations
```bash
# List running tasks on a node
pvesh get /nodes/balthazar/tasks?running=1
pvesh get /nodes/caspar/tasks?running=1

# Kill stuck task
pvesh delete /nodes/<node>/tasks/<UPID>

# View task log
pvesh get /nodes/<node>/tasks/<UPID>/log
```

### Container Won't Boot (Network)
```bash
pct config <VMID>        # verify IP/gateway settings
ip link show vmbr0       # confirm bridge exists
pct console <VMID>       # see boot output
```

### Web UI Unreachable (but SSH works)
```bash
systemctl restart pveproxy pvedaemon
```

### Btrfs Space Issues
```bash
# "No space left" but df shows free space?
btrfs filesystem df /mnt/mpool    # check metadata allocation
# Metadata full but data has space: balance it
btrfs balance start -musage=50 /mnt/mpool
```
</troubleshooting>

<networking>
## Proxmox Networking

Config: `/etc/network/interfaces`

```bash
ip addr show
cat /etc/network/interfaces

# Apply changes without reboot (Proxmox 7+)
ifreload -a
```

### Typical vmbr0 setup
```
auto vmbr0
iface vmbr0 inet static
    address 10.10.0.100/24
    gateway 10.10.0.1
    bridge-ports eno1
    bridge-stp off
    bridge-fd 0
```

### VLAN-Aware Bridge
```bash
# Add to bridge config:
    bridge-vlan-aware yes
    bridge-vids 2-4094

# Assign VLAN to CT/VM:
pct set <VMID> --net0 name=eth0,bridge=vmbr0,tag=10
qm set <VMID> --net0 virtio,bridge=vmbr0,tag=10
```
</networking>

<cluster_management>
## Node Management

```bash
# Service health
systemctl status pve-cluster pvedaemon pveproxy corosync

# If these are standalone (not clustered):
pvecm status     # will show single-node or error if no cluster

# Restart web UI
systemctl restart pveproxy pvedaemon
```

### Monthly Maintenance
```bash
# Both nodes:
apt update && apt upgrade
pveam update                          # refresh template list

# balthazar — Btrfs health:
btrfs scrub start /mnt/mpool
btrfs scrub status /mnt/mpool

# Review and purge old backups:
ls -lh /var/lib/vz/dump/
```
</cluster_management>

<success_criteria>
- LXC/VM operations use pct/qm CLI with correct flags
- Storage operations use btrfs commands — never zpool/zfs
- Cross-node migration uses vzdump → SCP → restore (nodes are not clustered)
- Snapshots taken before risky changes
- Lock files removed only after confirming no operation is actually running
- Pi-hole DNS verified working after any migration (dig google.com @10.10.0.53)
</success_criteria>
</skill>
