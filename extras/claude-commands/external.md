---
name: external
description: External access status for all *.y2hay.com services
allowed-tools: ["Bash"]
---

# External Access Status

Quick check of all externally accessible services via y2hay.com subdomains.

## Quick Health Check

```bash
echo "=== External Access Status ===" && \
for domain in shows flicks hits ask dash; do
  code=$(curl -s -o /dev/null -w "%{http_code}" --connect-timeout 5 "https://${domain}.y2hay.com" 2>/dev/null)
  if [ "$code" = "200" ] || [ "$code" = "302" ] || [ "$code" = "401" ]; then
    echo "✅ ${domain}.y2hay.com: $code"
  else
    echo "❌ ${domain}.y2hay.com: $code"
  fi
done
```

## Service Mapping

| Subdomain | Service | Backend | Expected Response |
|-----------|---------|---------|-------------------|
| shows.y2hay.com | Sonarr | 10.10.0.155:8989 | 200/302 |
| flicks.y2hay.com | Radarr | 10.10.0.155:7878 | 200/302 |
| hits.y2hay.com | Jellyfin | 10.10.0.155:8096 | 200/302 |
| ask.y2hay.com | Jellyseerr | 10.10.0.155:5055 | 200/302 |
| dash.y2hay.com | Glance | 10.10.0.155:8080 | 200 |

## DNS Resolution Check

```bash
echo "=== DNS Resolution ===" && \
for domain in shows flicks hits ask dash; do
  ip=$(dig +short ${domain}.y2hay.com 2>/dev/null | tail -1)
  echo "${domain}.y2hay.com -> ${ip:-FAILED}"
done
```

## Cloudflare DDNS Status

The Cloudflare DDNS container keeps DNS records updated with dynamic WAN IP.

```bash
# Check DDNS container status
ssh 10.10.0.155 "docker ps --filter name=cloudflare-ddns --format '{{.Status}}'"

# View recent DDNS logs
ssh 10.10.0.155 "docker logs cloudflare-ddns --tail 20 2>&1"
```

## Certificate Expiration Check

```bash
echo "=== Certificate Expiry ===" && \
for domain in shows flicks hits ask dash; do
  expiry=$(echo | openssl s_client -servername ${domain}.y2hay.com -connect ${domain}.y2hay.com:443 2>/dev/null | openssl x509 -noout -enddate 2>/dev/null | cut -d= -f2)
  echo "${domain}.y2hay.com: ${expiry:-CHECK FAILED}"
done
```

## Full Diagnostic

Run all checks:
```bash
echo "=== Full External Access Diagnostic ===" && \
echo "" && \
echo "1. HTTP Status:" && \
for domain in shows flicks hits ask dash; do
  code=$(curl -s -o /dev/null -w "%{http_code}" --connect-timeout 5 "https://${domain}.y2hay.com" 2>/dev/null)
  echo "   ${domain}.y2hay.com: $code"
done && \
echo "" && \
echo "2. DNS Resolution:" && \
for domain in shows flicks hits ask dash; do
  ip=$(dig +short ${domain}.y2hay.com 2>/dev/null | tail -1)
  echo "   ${domain}.y2hay.com -> ${ip:-FAILED}"
done && \
echo "" && \
echo "3. Traefik Status:" && \
traefik_status=$(curl -s -o /dev/null -w "%{http_code}" http://10.10.0.155:8082 2>/dev/null)
echo "   Dashboard (internal): $traefik_status" && \
echo "" && \
echo "4. DDNS Container:" && \
ssh 10.10.0.155 "docker ps --filter name=cloudflare-ddns --format '   Status: {{.Status}}'" 2>/dev/null || echo "   Cannot reach Dockhand LXC"
```

## Troubleshooting

### All services down
1. Check if Traefik is running: `ssh 10.10.0.155 "docker ps | grep traefik"`
2. Check WAN connectivity from router
3. Verify Cloudflare DNS records point to correct IP

### Single service down
1. Check if backend container is running
2. Verify Traefik labels in compose.yaml
3. Check service-specific logs

### Certificate errors
1. Check acme.json permissions (must be 600)
2. Verify Cloudflare API token is valid
3. Check Traefik logs for ACME errors

### DNS not resolving
1. Check Cloudflare DDNS container logs
2. Verify DNS records in Cloudflare dashboard
3. Check if WAN IP has changed
