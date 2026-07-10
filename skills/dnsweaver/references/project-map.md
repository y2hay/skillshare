# dnsweaver Project Map

## Repository Identity

- Local git root: `/home/xcx/repos/dnsweaver/dnsweaver`
- Parent directory `/home/xcx/repos/dnsweaver` is not the git repository.
- Remote: `https://github.com/maxfield-allison/dnsweaver`
- Branch observed: `main`
- Module: `github.com/maxfield-allison/dnsweaver`
- Go directive observed: `go 1.26.5`
- Current recent commits observed:
  - `0c50a09 feat(providers): add pfSense provider (pfSense-pkg-RESTAPI) (#129)`
  - `e1c4084 docs: enrich architecture diagram + add lifecycle and matching diagrams (#128)`
  - `7fcc5eb chore(release): finalize CHANGELOG for v2.4.0 (#127)`
  - `334d25f fix(docker): bounded startup connection retry (#125) (#126)`
  - `75372d2 fix(docker): support root-owned sockets via DNSWEAVER_DOCKER_GID + socket proxy (#123)`

## Product Summary

dnsweaver automatically manages DNS records for homelab workloads. It watches Docker/Swarm, Kubernetes, Proxmox VE, Incus, and reverse-proxy static config sources, extracts hostnames, matches them to DNS provider instances, and creates/updates/deletes DNS records. It supports split-horizon DNS and multiple provider instances simultaneously.

## Core Flow

```text
Sources/platforms
  Docker/Swarm labels, K8s resources, Proxmox VMs/LXCs, Incus instances, static files
    ↓
Workload normalization (`pkg/workload`)
    ↓
Hostname extraction (`pkg/source`, `sources/*`)
    ↓
Domain matching (`internal/matcher`, provider instance domains/exclusions)
    ↓
Reconciliation (`internal/reconciler`)
    ↓
Provider actions (`pkg/provider`, `providers/*`)
```

## Directory Overview

- `cmd/dnsweaver/` — CLI flags, configuration entry, logging setup, registry setup, source/provider registration, runtime wiring.
- `internal/config/` — configuration load/validation for env vars and YAML.
- `internal/docker/` — Docker client, event handling, workload adapter.
- `internal/kubernetes/` — Kubernetes clients/watchers and resource conversion.
- `internal/proxmox/` — Proxmox API client and IP resolution.
- `internal/incus/` — Incus client and IP resolution.
- `internal/health/` — health/readiness HTTP server.
- `internal/matcher/` — domain glob/regex matching.
- `internal/metrics/` — Prometheus metrics.
- `internal/reconciler/` — diffing, ownership, create/update/delete, orphan cleanup.
- `internal/testutil/` — shared mocks and assertions.
- `internal/watcher/` — event/listing orchestration.
- `pkg/dnsupdate/` — RFC 2136 DNS update client.
- `pkg/httputil/` — HTTP/TLS helper utilities.
- `pkg/provider/` — provider interfaces, records, capabilities, registry, manager, ownership helpers.
- `pkg/source/` — source interface, hostname types, registry, file discovery watcher.
- `pkg/sshutil/` — SSH/SFTP utilities for file-backed providers.
- `pkg/workload/` — platform-neutral workload abstraction.
- `providers/*` — concrete provider implementations.
- `sources/*` — concrete source implementations.
- `deploy/helm/dnsweaver/` — Helm chart.
- `deploy/kubernetes/` and `deploy/kustomize/` — Kubernetes manifests.
- `docs/` — MkDocs documentation.

## Supported Providers

- Technitium
- Cloudflare
- OVHcloud
- RFC 2136
- PowerDNS
- Pi-hole
- AdGuard Home
- OPNsense
- pfSense
- dnsmasq
- Webhook

## Supported Sources

- `traefik` — Docker/Swarm labels and static file discovery.
- `dnsweaver` — native dnsweaver labels.
- `caddy` — caddy-docker-proxy labels and files.
- `nginx-proxy` — `VIRTUAL_HOST` labels/config.
- `kubernetes` — Ingress, Traefik IngressRoute, HTTPRoute, optionally Service.
- `proxmox` — Proxmox VMs/LXCs via API.
- `incus` — Incus system containers/VMs via socket or HTTPS.

## Important Docs

- `README.md` — overview, supported providers, quick starts, split-horizon examples.
- `docs/getting-started.md` — first deployment and verification.
- `docs/configuration/environment.md` — complete env var reference.
- `docs/config.example.yml` — YAML configuration format and examples.
- `docs/contributing/architecture.md` — system overview and package boundaries.
- `docs/contributing/development.md` — dev setup and testing patterns.
- `docs/contributing/adding-provider.md` — provider implementation guide.
- `docs/contributing/adding-source.md` — source implementation guide; verify against current `pkg/source` and `sources/*` because some prose may lag current tree layout.
- `docs/observability.md` — health, metrics, logging.
- `CHANGELOG.md` — release history and recent behavior changes.

## Development Commands

From `/home/xcx/repos/dnsweaver/dnsweaver`:

```bash
make build          # build binary
make test           # go test -v -race ./...
make test-short     # go test -v -short ./...
make test-cover     # coverage report
make lint           # golangci-lint run ./...
make fmt            # go fmt ./...
make vet            # go vet ./...
make docker-build   # build container image
make security       # vuln + secrets
make tools          # install golangci-lint and govulncheck
```

CI additionally runs gofmt, go vet, golangci-lint, race tests with coverage, build, and govulncheck. The local shell observed during ingestion did not have `go` on PATH, so validation may require fixing PATH/toolchain first.
