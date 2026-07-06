---
name: arr
description: *arr stack status and management (Sonarr, Radarr, Prowlarr, Lidarr)
allowed-tools: ["Bash"]
---

# *arr Stack Management

Manage the media automation stack on Dockhand LXC (10.10.0.155).

## Quick Status

```bash
ssh 10.10.0.155 "docker ps --format 'table {{.Names}}\t{{.Status}}\t{{.Ports}}' | grep -E 'sonarr|radarr|prowlarr|lidarr|whisparr|jellyfin|qbittorrent'"
```

## Service Health Checks

API keys are stored in `~/CREDENTIALS.md` - reference them there.

| Service | Port | API Check |
|---------|------|-----------|
| Sonarr | 8989 | `curl -s http://10.10.0.155:8989/api/v3/health -H "X-Api-Key: <SONARR_API_KEY>"` |
| Radarr | 7878 | `curl -s http://10.10.0.155:7878/api/v3/health -H "X-Api-Key: <RADARR_API_KEY>"` |
| Prowlarr | 9696 | `curl -s http://10.10.0.155:9696/api/v1/health` |
| Lidarr | 8686 | `curl -s http://10.10.0.155:8686/api/v1/health -H "X-Api-Key: <LIDARR_API_KEY>"` |

See `~/CREDENTIALS.md` for API keys.

## Common Operations

- **Restart all arr services:** `ssh 10.10.0.155 "cd /opt/stacks/arr && docker compose restart sonarr radarr prowlarr lidarr"`
- **View logs:** `ssh 10.10.0.155 "cd /opt/stacks/arr && docker compose logs -f --tail 50 sonarr"`
- **Check downloads:** `ssh 10.10.0.155 "docker exec qbittorrent qbt torrent list"`
- **Restart qBittorrent:** `ssh 10.10.0.155 "cd /opt/stacks/arr && docker compose restart qbittorrent"`

## Stack Location

- **Compose file:** `/opt/stacks/arr/compose.yaml`
- **Data volumes:** `/opt/stacks/arr/*/config`
- **Media mount:** `/mnt/media` (from balthazar NFS)

## External Access

| Subdomain | Service | Internal Port |
|-----------|---------|---------------|
| shows.y2hay.com | Sonarr | 8989 |
| flicks.y2hay.com | Radarr | 7878 |
| hits.y2hay.com | Jellyfin | 8096 |
| ask.y2hay.com | Jellyseerr | 5055 |

## Troubleshooting

- **Container won't start:** Check `docker logs <container>` for errors
- **API not responding:** Verify container is healthy with `docker ps`
- **Media not showing:** Check NFS mount status on Dockge LXC
- **Downloads stuck:** Verify qBittorrent connectivity and tracker status
