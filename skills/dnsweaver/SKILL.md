---
name: dnsweaver
triggers: ["dnsweaver", "DNS record", "DNS provider", "hostname source", "dnsweaver provider", "dnsweaver source"]
description: This skill should be used when the user asks to "work on dnsweaver", "modify dnsweaver", "add a dnsweaver provider", "add a dnsweaver source", "debug dnsweaver config", "deploy dnsweaver", "update dnsweaver docs", or mentions the local ~/repos/dnsweaver project. Provides repository-specific architecture, workflows, extension patterns, and operational guidance for dnsweaver.
version: 0.1.0
---

# dnsweaver Repository Skill

## Purpose

Work effectively in the local dnsweaver repository: a Go-based DNS record lifecycle manager for homelab workloads. Use this skill to inspect, modify, test, document, or deploy dnsweaver without rediscovering its architecture and conventions.

## Start Here

1. Resolve the repository root as `/home/xcx/repos/dnsweaver/dnsweaver`. The parent `/home/xcx/repos/dnsweaver` is not the git root.
2. Check `git status --short` before editing.
3. Prefer branch-per-task work from `main` for code/doc changes unless the user explicitly asks to commit directly on `main`.
4. Read the task-relevant documentation before changing code:
   - `README.md` for product scope and supported platforms/providers.
   - `docs/contributing/architecture.md` for package boundaries and data flow.
   - `docs/contributing/development.md` for development commands and style.
   - `docs/contributing/adding-provider.md` when adding or changing DNS providers.
   - `docs/contributing/adding-source.md` when adding or changing hostname sources.
   - `docs/configuration/environment.md` for env var behavior.
5. Ask one focused clarifying question when the target provider, source, deployment mode, domain pattern, or validation scope is ambiguous. Prefer recommended defaults when the request is clear.

## Mental Model

dnsweaver is “external-dns for the homelab.” It watches workload/source state, extracts desired hostnames, matches hostnames to provider instances by domain patterns, and reconciles DNS records in one or more providers. Split-horizon DNS is a first-class use case: the same hostname labels can create internal records in Technitium/Pi-hole/AdGuard and external records in Cloudflare/OVH/RFC2136/etc.

Core flow:

```text
Platform/source event
  → workload normalization
  → source hostname extraction/discovery
  → matcher applies provider domains/exclusions
  → reconciler diffs desired vs provider actual state
  → provider Create/Update/Delete
  → ownership metadata protects manual records
```

## Key Package Boundaries

- `cmd/dnsweaver/`: CLI flags, config loading, logging, registries, signal handling, runtime wiring.
- `internal/config/`: env/YAML loading, defaults, validation, provider/source instance configuration.
- `internal/docker/`, `internal/kubernetes/`, `internal/proxmox/`, `internal/incus/`: platform/API clients and workload listers/watchers.
- `internal/reconciler/`: diff/apply engine, orphan cleanup, ownership behavior, reconciliation results.
- `internal/watcher/`: event orchestration from listers/sources into reconciler.
- `pkg/provider/`: public provider interface, record types, capabilities, ownership helpers, registry/manager.
- `pkg/source/`: public source interface, hostname metadata, source registry, file watcher.
- `pkg/workload/`: platform-neutral workload model.
- `providers/*`: DNS provider implementations.
- `sources/*`: hostname extraction implementations.
- `docs/`: MkDocs documentation; update docs alongside behavior changes.
- `deploy/`: Helm, Kubernetes, and Kustomize manifests.

## Supported Extension Points

### Providers

Current providers include Technitium, Cloudflare, OVHcloud, RFC 2136, PowerDNS, Pi-hole, AdGuard Home, OPNsense, pfSense, dnsmasq, and Webhook.

To add or modify a provider:

1. Work in `providers/<provider>/`.
2. Keep API transport details in `client.go` and config parsing/validation in `config.go`.
3. Implement `pkg/provider.Provider`: `Name`, `Type`, `Ping`, `Capabilities`, `List`, `Create`, `Delete`.
4. Implement `provider.Updater` only if the backend has safe native updates; otherwise allow delete+create fallback.
5. Return accurate `Capabilities`, especially ownership TXT support and supported record types.
6. Expose `Factory()` and register it in `cmd/dnsweaver/setup.go` via `registerProviderFactories`.
7. Add config/client/provider tests plus docs and changelog updates.

### Sources

Current sources include `traefik`, `dnsweaver`, `caddy`, `nginx-proxy`, `kubernetes`, `proxmox`, and `incus`.

To add or modify a source:

1. Work in `sources/<source>/`.
2. Implement `pkg/source.Source`: `Name`, `Extract`, `Discover`, `SupportsDiscovery`, `SupportedPlatforms`.
3. Return an empty slice when no hostnames are present; reserve errors for malformed or unreadable configured inputs.
4. Register source construction in `cmd/dnsweaver/setup.go` via `registerSources`.
5. Update `internal/config` if new env/YAML settings are required.
6. Add source docs under `docs/sources/`, update env reference and `mkdocs.yml` when navigation changes.

## Configuration Rules

- Environment variables use `DNSWEAVER_` prefix.
- `DNSWEAVER_CONFIG` or `--config` enables YAML configuration; environment variables override YAML values.
- `DNSWEAVER_INSTANCES` declares provider instance names; dashes normalize to underscores for env var prefixes.
- `DNSWEAVER_PLATFORM` supports `docker`, `kubernetes`, `both`, and `none`/`standalone`.
- `DNSWEAVER_SOURCES` can include `traefik,caddy,nginx-proxy,dnsweaver,kubernetes,proxmox,incus`.
- Sensitive fields support `_FILE` suffix for Docker/Kubernetes secrets.
- Unified TLS keys use `TLS_CA_FILE`, `TLS_CERT_FILE`, `TLS_KEY_FILE`, `TLS_SERVER_NAME`, `TLS_MIN_VERSION`, and `TLS_SKIP_VERIFY` per provider instance; Proxmox uses `DNSWEAVER_PROXMOX_TLS_*`.

## Ownership and Safety Rules

- Default ownership uses TXT records named `_dnsweaver.<hostname>` with value `heritage=dnsweaver` and optional `instance=<id>`.
- Never delete manual/operator records unless they are clearly owned by the current dnsweaver instance or the requested migration explicitly adopts them.
- Some providers cannot create TXT records. OPNsense and pfSense track ownership in host override description fields; dnsmasq/file-backed flows have provider-specific limits.
- Preserve multi-instance semantics when changing matching or cleanup logic.

## Development and Validation

Preferred commands from repo root:

```bash
make fmt
make vet
make test-short
make test
make lint
make build
```

CI gates include `gofmt`, `go vet ./...`, `golangci-lint`, `go test -race -coverprofile=coverage.out ./...`, `go build ./...`, and `govulncheck` with documented Docker SDK suppressions.

If `go` is not on PATH in the current shell, report that validation is blocked rather than pretending tests passed. Go was installed on ramiel via `paru -S --needed go` during skill setup; re-check `go version` if validation unexpectedly fails.

## Operational Gotchas

- The official container drops privileges to uid/gid `1000`; mounted TLS cert/key files must be readable by that identity or delivered as Docker/Kubernetes secrets.
- Prefer a Docker socket proxy over direct socket mounting. `DNSWEAVER_DOCKER_GID=0` is an explicit escape hatch for root-owned sockets such as Synology.
- Health/metrics server defaults to port `8080`; docs and chart values may refer to `/health`, `/ready`, and `/metrics`.
- Kubernetes Helm chart defaults to platform `kubernetes`, runAsNonRoot uid/gid `1000`, read-only root filesystem, low resource requests, and optional ServiceMonitor.

## Documentation Discipline

When behavior changes, update all affected surfaces in the same change:

- Code and tests.
- `docs/configuration/environment.md` for env/config changes.
- Provider or source page under `docs/providers/` or `docs/sources/`.
- `README.md` if support tables or quick-start examples change.
- `CHANGELOG.md` under `[Unreleased]`.
- `mkdocs.yml` when adding a new documentation page.

## Additional References

Load these references as needed:

- `references/project-map.md` — concise project inventory, architecture map, and commands.
- `references/provider-source-patterns.md` — provider/source implementation checklists.
- `references/operations-config.md` — deployment, configuration, TLS, Docker socket, and health notes.
