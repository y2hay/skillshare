---
name: infra
description: Quick homelab infrastructure status check
allowed-tools: ["Bash"]
---

# Infrastructure Status Check

Quickly check the status of the homelab infrastructure.

## Checks to perform

1. **Proxmox hosts connectivity:**
   ```bash
   ping -c 1 -W 2 10.10.0.100 && echo "balthazar: UP" || echo "balthazar: DOWN"
   ping -c 1 -W 2 10.10.0.200 && echo "caspar: UP" || echo "caspar: DOWN"
   ```

2. **List running LXC containers on balthazar:**
   ```bash
   ssh root@10.10.0.100 "pct list" 2>/dev/null || echo "Cannot reach balthazar"
   ```

3. **List running LXC containers on caspar:**
   ```bash
   ssh root@10.10.0.200 "pct list" 2>/dev/null || echo "Cannot reach caspar"
   ```

4. **DNS status (Pi-hole):**
   ```bash
   curl -s "http://10.10.0.53/admin/api.php?summary" | jq -r '"Pi-hole: \(.status) | Queries today: \(.dns_queries_today) | Blocked: \(.ads_blocked_today)"' 2>/dev/null || echo "Pi-hole: Cannot reach"
   ```

5. **Dockhand status:**
   ```bash
   curl -s -o /dev/null -w "%{http_code}" http://10.10.0.155:3006 2>/dev/null | grep -q 200 && echo "Dockhand: UP" || echo "Dockhand: DOWN or unreachable"
   ```

6. **Traefik status:**
   ```bash
   curl -s -o /dev/null -w "%{http_code}" http://10.10.0.155:8082 2>/dev/null | grep -q 200 && echo "Traefik: UP" || echo "Traefik: DOWN or unreachable"
   ```

7. ***arr services count:**
   ```bash
   ssh 10.10.0.155 "docker ps --format '{{.Names}}' | grep -cE 'sonarr|radarr|prowlarr|lidarr|jellyfin'" 2>/dev/null || echo "Cannot count arr services"
   ```

## Network topology reference

- **Router:** 10.10.0.1 (FreshTomato)
- **balthazar:** 10.10.0.100 (Proxmox)
- **caspar:** 10.10.0.200 (Proxmox)
- **Pi-hole:** 10.10.0.53 (DNS, LXC 253 on caspar)
- **Unbound:** 10.10.0.54 (Recursive DNS, LXC 200 on caspar)
- **Dockhand:** 10.10.0.155 (Container manager, LXC on balthazar)
- **Traefik:** 10.10.0.155:8082 (Reverse proxy dashboard)

## Related Commands

- `/arr` - Detailed *arr stack management
- `/traefik` - Traefik reverse proxy management
- `/dockhand` - Docker stack operations
- `/external` - External access status check
