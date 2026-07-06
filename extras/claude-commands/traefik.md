---
name: traefik
description: Traefik reverse proxy and SSL certificate management
allowed-tools: ["Bash", "Read"]
---

# Traefik Management

Manage external access via Traefik reverse proxy on Dockhand LXC (10.10.0.155).

## Dashboard

- **Internal:** http://10.10.0.155:8082

## Check Certificate Status

```bash
ssh 10.10.0.155 "cat /opt/stacks/arr/traefik/acme.json | jq '.letsencrypt.Certificates[] | {domain: .domain.main, expiry: .certificate | @base64d | openssl x509 -noout -enddate}'" 2>/dev/null || echo "Certificate check failed - verify acme.json exists"
```

## Quick Certificate Expiry Check

```bash
ssh 10.10.0.155 "cat /opt/stacks/arr/traefik/acme.json | jq -r '.letsencrypt.Certificates[].domain.main'" 2>/dev/null
```

## Route Health

| Subdomain | Backend | Check |
|-----------|---------|-------|
| shows.y2hay.com | Sonarr:8989 | `curl -s -o /dev/null -w "%{http_code}" https://shows.y2hay.com` |
| flicks.y2hay.com | Radarr:7878 | `curl -s -o /dev/null -w "%{http_code}" https://flicks.y2hay.com` |
| hits.y2hay.com | Jellyfin:8096 | `curl -s -o /dev/null -w "%{http_code}" https://hits.y2hay.com` |
| ask.y2hay.com | Jellyseerr:5055 | `curl -s -o /dev/null -w "%{http_code}" https://ask.y2hay.com` |
| dash.y2hay.com | Glance | `curl -s -o /dev/null -w "%{http_code}" https://dash.y2hay.com` |

## Test All Routes

```bash
for domain in shows flicks hits ask dash; do
  code=$(curl -s -o /dev/null -w "%{http_code}" "https://${domain}.y2hay.com" 2>/dev/null)
  echo "${domain}.y2hay.com: $code"
done
```

## Configuration Files

- **Traefik config:** `/opt/stacks/arr/traefik/traefik.yml`
- **Dynamic config:** `/opt/stacks/arr/traefik/dynamic/`
- **Certificates:** `/opt/stacks/arr/traefik/acme.json` (chmod 600)
- **Labels:** In compose.yaml service definitions

## Cloudflare DNS-01 Challenge

Traefik uses Cloudflare DNS-01 for Let's Encrypt certificates:
- **API Token:** Stored in docker compose environment
- **Wildcard support:** Can issue *.y2hay.com certificates

## Troubleshooting

### Cert renewal issues
1. Check Cloudflare DNS API token validity
2. Verify acme.json permissions: `chmod 600 /opt/stacks/arr/traefik/acme.json`
3. Check Traefik logs: `ssh 10.10.0.155 "cd /opt/stacks/arr && docker compose logs traefik --tail 100"`

### Route not working
1. Verify Docker network connectivity between Traefik and backend service
2. Check service labels in compose.yaml
3. Verify backend service is running

### 502 Bad Gateway
1. Backend service is not running - check `docker ps`
2. Wrong internal port in Traefik labels
3. Network isolation - services must be on same Docker network

### 404 Not Found
1. Missing or incorrect Host rule in Traefik labels
2. Service not registered with Traefik

## Restart Traefik

```bash
ssh 10.10.0.155 "cd /opt/stacks/arr && docker compose restart traefik"
```
