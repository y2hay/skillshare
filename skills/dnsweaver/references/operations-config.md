# dnsweaver Operations and Configuration Notes

## Configuration Sources

Configuration priority:

1. Environment variables with `DNSWEAVER_` prefix.
2. YAML file selected by `DNSWEAVER_CONFIG` or `--config`.
3. Defaults.

`docs/config.example.yml` demonstrates the YAML format with env var interpolation. Environment variables override YAML.

## Global Settings

Important env vars:

- `DNSWEAVER_INSTANCES` — comma-separated provider instance names. Deprecated alias: `DNSWEAVER_PROVIDERS`.
- `DNSWEAVER_PLATFORM` — `docker`, `kubernetes`, `both`, `none`, or `standalone`.
- `DNSWEAVER_SOURCES` — `traefik,caddy,nginx-proxy,dnsweaver,kubernetes,proxmox,incus`; default observed docs say `traefik`.
- `DNSWEAVER_INSTANCE_ID` — unique id for multi-instance coordination.
- `DNSWEAVER_DRY_RUN` — preview changes without modifying DNS.
- `DNSWEAVER_CLEANUP_ORPHANS` — delete records for removed workloads.
- `DNSWEAVER_CLEANUP_ON_STOP` — delete Docker records when containers stop.
- `DNSWEAVER_OWNERSHIP_TRACKING` — use ownership markers.
- `DNSWEAVER_ADOPT_EXISTING` — adopt existing records by creating ownership TXT.
- `DNSWEAVER_RECONCILE_INTERVAL` — default `60s`.
- `DNSWEAVER_HEALTH_PORT` — default `8080`.

## Provider Instance Settings

For instance `internal-dns`, use env prefix `DNSWEAVER_INTERNAL_DNS_`.

Common fields:

- `TYPE`
- `RECORD_TYPE`
- `TARGET`
- `DOMAINS`
- `DOMAINS_REGEX`
- `EXCLUDE_DOMAINS`
- `EXCLUDE_DOMAINS_REGEX`
- `ENTRYPOINTS`
- `TTL`
- `MODE`

Modes include `managed`, `authoritative`, and `additive`.

## Secrets

Use `_FILE` suffix for sensitive fields where supported, such as tokens, API keys, auth tokens, passwords, TSIG secrets, and SSH passwords. Prefer Docker secrets or Kubernetes Secrets in production.

Examples:

```bash
DNSWEAVER_INTERNAL_TOKEN_FILE=/run/secrets/technitium_token
DNSWEAVER_PROXMOX_TOKEN_SECRET_FILE=/etc/dnsweaver/pve-token
```

## TLS

Unified per-provider TLS keys:

- `DNSWEAVER_<NAME>_TLS_CA_FILE`
- `DNSWEAVER_<NAME>_TLS_CERT_FILE`
- `DNSWEAVER_<NAME>_TLS_KEY_FILE`
- `DNSWEAVER_<NAME>_TLS_SERVER_NAME`
- `DNSWEAVER_<NAME>_TLS_MIN_VERSION` (`1.2` default or `1.3`)
- `DNSWEAVER_<NAME>_TLS_SKIP_VERIFY`

Proxmox uses:

- `DNSWEAVER_PROXMOX_TLS_CA_FILE`
- `DNSWEAVER_PROXMOX_TLS_CERT_FILE`
- `DNSWEAVER_PROXMOX_TLS_KEY_FILE`
- `DNSWEAVER_PROXMOX_TLS_SERVER_NAME`
- `DNSWEAVER_PROXMOX_TLS_MIN_VERSION`
- `DNSWEAVER_PROXMOX_TLS_SKIP_VERIFY`

Deprecated aliases still exist for compatibility but should not be introduced in new docs/config.

### TLS File Permission Gotcha

The official container drops privileges to uid/gid `1000`. A root-owned `0600` key mounted into the container will fail with permission denied even if the container starts as root, because the long-running process is not root.

Safe fixes:

- `chown 1000:1000 key.pem && chmod 0600 key.pem`
- `chgrp 1000 key.pem && chmod 0640 key.pem`
- Use Docker/Kubernetes secrets.

Never recommend world-readable private keys.

## Docker Operations

Prefer socket proxy for security:

```yaml
environment:
  - DNSWEAVER_DOCKER_HOST=tcp://socket-proxy:2375
```

Socket-related settings:

- `DNSWEAVER_DOCKER_HOST` — default `unix:///var/run/docker.sock`.
- `DNSWEAVER_DOCKER_MODE` — `auto`, `swarm`, or `standalone`.
- `DNSWEAVER_DOCKER_CONNECT_TIMEOUT` — default `30s`; set `0` for strict fail-fast.
- `DNSWEAVER_DOCKER_GID` — explicit supplemental group for socket access; `0` is an escape hatch for root-owned sockets such as Synology and logs a warning.

## Kubernetes Operations

Helm defaults observed:

- `config.platform: kubernetes`
- `replicaCount: 1`
- run as uid/gid `1000`, non-root, read-only root filesystem, drop all capabilities.
- service port `8080`.
- liveness path `/health`, readiness path `/ready`.
- resource requests `10m` CPU and `32Mi` memory; limits `100m` CPU and `128Mi` memory.
- RBAC can watch Ingress, IngressRoute, HTTPRoute, and optionally Service.

## Standalone Mode

Set `DNSWEAVER_PLATFORM=none` or `standalone` to avoid creating Docker/Kubernetes clients. Configure at least one non-container source: Proxmox, Incus, or static file discovery. This is useful for running as a bare binary on a host, VM, or LXC.

## xcx Homelab Deployment Hints

Use the ritsuko-rebuild source of truth for live IPs, credentials key names, and topology before applying changes: `~/repos/ritsuko-rebuild/AGENTS.md`, `HOSTS/<host>.md`, `SERVICES/<service>.md`, `NETWORK.md`, and `CREDENTIALS-INDEX.md`.

Likely dnsweaver homelab fit:

- Internal DNS providers: Pi-hole at `10.10.0.53`, Technitium at `10.10.0.253`, Technitium fallback at `10.10.0.153`.
- Proxmox sources: `caspar` at `10.10.0.200` and `melchior` at `10.10.0.150`; verify current node names and token credential keys in ritsuko-rebuild before writing config.
- Docker/Traefik workload source: `dockarr` at `10.10.0.155` is the Docker/Traefik host; use a socket proxy when deploying dnsweaver near Docker.
- Public/split-horizon provider: Cloudflare Tunnel/Traefik services run from dockarr; use Cloudflare CNAME targets only after checking the service docs and credential index.
- Good first production mode for Proxmox-only DNS: run dnsweaver with `DNSWEAVER_PLATFORM=none`, `DNSWEAVER_SOURCES=proxmox`, one or more `DNSWEAVER_PROXMOX_*` source configs, and an internal Technitium/Pi-hole provider instance.

Do not invent credential names or API token values. Look up key names in `CREDENTIALS-INDEX.md` and ask the user for any missing secret material.

## Observability

- Structured logging uses `slog`, JSON by default; text format is available.
- Health and readiness endpoints run on the configured health port.
- Prometheus metrics are served from the same server.
- Build info metrics include dnsweaver version and Go runtime version.

## Validation Notes on ramiel

Go was installed with `paru -S --needed --noconfirm go` during skill setup. Confirm with `go version` before validation if PATH changes. After installation, `go test ./...` passed from `/home/xcx/repos/dnsweaver/dnsweaver`.
