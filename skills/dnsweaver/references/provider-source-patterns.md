# dnsweaver Provider and Source Patterns

## Provider Implementation Pattern

Use `docs/contributing/adding-provider.md` and current provider implementations as the primary reference.

### Files

Create or modify files under `providers/<provider>/`:

```text
providers/<provider>/
├── config.go
├── config_test.go
├── client.go
├── client_test.go
├── provider.go
├── provider_test.go
└── factory.go or Factory() in provider.go/config.go as existing pattern warrants
```

### Interface

Implement `pkg/provider.Provider`:

```go
type Provider interface {
    Name() string
    Type() string
    Ping(ctx context.Context) error
    Capabilities() Capabilities
    List(ctx context.Context) ([]Record, error)
    Create(ctx context.Context, record Record) error
    Delete(ctx context.Context, record Record) error
}
```

Optional interfaces:

- `provider.Updater` for safe native in-place update support.
- `provider.Closer` for providers that hold resources that must close at shutdown.

### Capabilities

Return accurate `provider.Capabilities`:

- `SupportsOwnershipTXT`: false for providers that cannot create TXT ownership records.
- `SupportsNativeUpdate`: true only when `Updater` is implemented correctly.
- `SupportedRecordTypes`: include only supported record types.

Supported record type constants include `A`, `AAAA`, `CNAME`, `TXT`, `SRV`, and `HTTPS`.

### Ownership

Default ownership uses TXT records:

```text
_dnsweaver.app.example.com TXT "heritage=dnsweaver"
_dnsweaver.app.example.com TXT "heritage=dnsweaver,instance=<id>"
```

Use helpers in `pkg/provider`:

- `MakeOwnershipValue(instanceID, metadata)`
- `ParseOwnershipValue(value)`
- `MatchesOwnership(value, ourInstanceID)`
- `IsDnsweaverOwned(value)`

Provider-specific exceptions:

- OPNsense and pfSense host overrides do not support TXT; ownership is tracked with `dnsweaver:{instance}` markers in description fields.
- File-backed providers can have limitations around updates and ownership metadata.

### Registration

Register provider factories in `cmd/dnsweaver/setup.go` inside `registerProviderFactories`.

Also update:

- `docs/providers/<provider>.md`
- `docs/configuration/environment.md`
- `docs/providers/index.md`
- `README.md` provider table if support changes
- `CHANGELOG.md` under `[Unreleased]`
- `mkdocs.yml` when adding a new page

### Tests

Prefer:

- Table-driven config validation tests.
- `httptest.NewServer` for HTTP clients.
- Mock provider records for create/update/delete/list behavior.
- Compile-time interface checks: `var _ provider.Provider = (*Provider)(nil)`.
- Error context with `%w` and actionable messages.

## Source Implementation Pattern

Use current `pkg/source/source.go`, `sources/*`, and `cmd/dnsweaver/setup.go` as truth. Some older docs may describe an obsolete `internal/sources` layout; current implementations live in top-level `sources/*`.

### Interface

Implement `pkg/source.Source`:

```go
type Source interface {
    Name() string
    Extract(ctx context.Context, w workload.Workload) ([]Hostname, error)
    Discover(ctx context.Context) ([]Hostname, error)
    SupportsDiscovery() bool
    SupportedPlatforms() []workload.Platform
}
```

### Behavior Rules

- `Extract` parses labels, annotations, pre-extracted hostnames, or workload metadata.
- `Discover` parses configured files or returns `nil, nil` when file discovery is not configured.
- `SupportsDiscovery` returns true only when file paths/static discovery are configured.
- `SupportedPlatforms` scopes the source to Docker/Kubernetes/static/etc.; an empty slice means all platforms.
- Return an empty slice for no hostnames.
- Return errors only for malformed configured data or unreadable configured inputs.
- Keep sources stateless and concurrency-safe.

### Registration

Register sources in `cmd/dnsweaver/setup.go` inside `registerSources`.

Current behavior:

- Listed `DNSWEAVER_SOURCES` are registered explicitly.
- Kubernetes source auto-registers when Kubernetes platform is enabled.
- Proxmox source auto-registers when Proxmox config/platform is enabled.
- Incus source auto-registers when Incus config is enabled.

### Source-Specific Config

Update `internal/config` for new config fields. Add environment reference entries under `docs/configuration/environment.md`. Preserve the design principle from `pkg/source/source.go`: presence implies intent for file discovery; do not add redundant enable flags unless truly required.

### Docs and Tests

Add or update:

- `docs/sources/<source>.md`
- `docs/sources/index.md`
- `docs/configuration/environment.md`
- `mkdocs.yml`
- `CHANGELOG.md`

Test parsers with edge cases: multiple host rules, malformed rules, empty labels, mixed platforms, duplicate hostnames, exclusions if relevant, and file discovery glob behavior.
