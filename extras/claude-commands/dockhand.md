---
name: dockhand
description: Docker stack operations on Dockhand LXC (10.10.0.155)
allowed-tools: ["Bash"]
---

# Dockhand Stack Operations

Direct access to Dockhand LXC (10.10.0.155) for Docker stack management.

## Connection

- **Web UI:** http://10.10.0.155:3006
- **SSH:** `ssh 10.10.0.155` or `ssh root@10.10.0.155`

## Stack Locations

| Stack | Path | Description |
|-------|------|-------------|
| arr | `/opt/stacks/arr` | Media automation (*arr services, Jellyfin, qBittorrent, Traefik) |
| cloudflare-ddns | `/opt/stacks/cloudflare-ddns` | Dynamic DNS updates to Cloudflare |

## Common Stack Commands

All commands assume SSH to 10.10.0.155 first.

### Stack Management

```bash
# List all stacks
ssh 10.10.0.155 "ls -la /opt/stacks/"

# View stack status
ssh 10.10.0.155 "cd /opt/stacks/arr && docker compose ps"

# Start stack
ssh 10.10.0.155 "cd /opt/stacks/arr && docker compose up -d"

# Stop stack
ssh 10.10.0.155 "cd /opt/stacks/arr && docker compose down"

# Restart stack
ssh 10.10.0.155 "cd /opt/stacks/arr && docker compose restart"

# Pull latest images
ssh 10.10.0.155 "cd /opt/stacks/arr && docker compose pull"

# Update stack (pull + recreate)
ssh 10.10.0.155 "cd /opt/stacks/arr && docker compose pull && docker compose up -d"
```

### Container Operations

```bash
# View all running containers
ssh 10.10.0.155 "docker ps --format 'table {{.Names}}\t{{.Status}}\t{{.Ports}}'"

# View logs for specific service
ssh 10.10.0.155 "cd /opt/stacks/arr && docker compose logs -f --tail 50 <service>"

# Restart specific service
ssh 10.10.0.155 "cd /opt/stacks/arr && docker compose restart <service>"

# Shell into container
ssh 10.10.0.155 "docker exec -it <container> /bin/bash"
# or for alpine-based:
ssh 10.10.0.155 "docker exec -it <container> /bin/sh"
```

### Maintenance

```bash
# Prune unused images
ssh 10.10.0.155 "docker image prune -f"

# Prune everything unused (careful!)
ssh 10.10.0.155 "docker system prune -f"

# Check disk usage
ssh 10.10.0.155 "docker system df"

# View container resource usage
ssh 10.10.0.155 "docker stats --no-stream"
```

## Services in arr Stack

| Service | Internal Port | External Access |
|---------|---------------|-----------------|
| jellyfin | 8096 | hits.y2hay.com |
| sonarr | 8989 | shows.y2hay.com |
| radarr | 7878 | flicks.y2hay.com |
| lidarr | 8686 | - |
| prowlarr | 9696 | - |
| whisparr | 6969 | - |
| qbittorrent | 8080 | - |
| jellyseerr | 5055 | ask.y2hay.com |
| traefik | 80, 443, 8082 | Reverse proxy |
| flaresolverr | 8191 | - |
| recyclarr | - | Config sync |

## Troubleshooting

### Container keeps restarting
```bash
ssh 10.10.0.155 "docker logs <container> --tail 100"
```

### Out of disk space
```bash
ssh 10.10.0.155 "df -h && docker system df"
```

### Network issues between containers
```bash
ssh 10.10.0.155 "docker network ls && docker network inspect arr_default"
```
