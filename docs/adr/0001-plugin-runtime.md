# ADR 0001: Plugin Runtime Architecture

## Context

Sampati must support a plugin ecosystem for connectors, country packs, scanners, notifiers, and report templates. Plugins are third-party code that must not be able to compromise the core platform, access other plugins' credentials, or escape their declared permissions.

## Decision

Plugins run **out-of-process** in isolated containers with:

- **gRPC/HTTP protocol v1** for communication with the host
- **Network allow-list** from the manifest (`network_allowlist`)
- **Declared permission scopes** (read-only OAuth scopes, no wildcards)
- **No filesystem access** by default; explicit declaration required
- **Signed manifests** verified at install time
- **Unsigned plugins require explicit admin opt-in**
- **Resource limits** (CPU, memory, timeout) enforced by container runtime

The plugin host (in `packages/plugin-host`) manages the container lifecycle, validates permissions, and proxies RPC calls.

## Consequences

### Positive

- A broken or malicious plugin cannot crash the core or access its memory
- Credentials are encrypted per-tenant and never exposed to plugins
- Clear permission model visible to admins at install time
- Language-agnostic: plugins can be written in any language that speaks the protocol
- Supports hot-reload and independent scaling of plugins

### Negative

- Higher operational complexity than in-process plugins
- Added latency for each plugin call (mitigated by batching in `Collect`)
- Requires container runtime (Docker/containerd) on the host
- More complex debugging and observability

## Alternatives Considered

1. **In-process plugins** (shared memory, direct function calls)
   - Rejected: no isolation, any bug or exploit affects the whole platform
2. **WASM sandbox** (e.g., wasmtime)
   - Rejected: immature ecosystem for Python/Go plugins, limited syscall control
3. **Separate process with Unix sockets** (no containers)
   - Rejected: no network/filesystem isolation, harder resource limits

## Implementation Notes

- Protocol v1 defined in `sampati-sdk/spec/plugin-protocol/protocol.proto`
- Manifest schema in `sampati-sdk/spec/manifest.schema.json`
- Conformance tests in `sampati-sdk/conformance/`
- First-party plugins live in `sampati/plugins/` and are built with the SDK

## References

- SAMPATI-GRANTH.md sections 6.2, 8.8 (F9), 19.7
- Threat model: `docs/threat-model.md`