# Threat Model — Sampati by VayuX

**Version:** 0.1.0-dev | **Updated:** 2026-11-19 | **Classification:** Internal

---

## 1. System Overview

Sampati is an open-source compliance automation platform that:
- Collects evidence from external systems via connectors
- Evaluates controls continuously against evidence
- Stores evidence in a tamper-evident ledger
- Provides auditor portals and trust centres
- Runs plugins (connectors, scanners, packs) in a sandboxed runtime

### Trust Boundaries

```
┌─────────────────────────────────────────────────────────────┐
│                    INTERNET / EXTERNAL                      │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐       │
│  │  Connectors  │  │  Auditors    │  │  Customers   │       │
│  │ (GitHub,     │  │ (read-only)  │  │ (trust       │       │
│  │  AWS, etc.)  │  │              │  │  centre)     │       │
│  └──────┬───────┘  └──────┬───────┘  └──────┬───────┘       │
└─────────┼─────────────────┼─────────────────┼────────────────┘
          │                 │                 │
          ▼                 ▼                 ▼
┌─────────────────────────────────────────────────────────────┐
│                      SAMPATI PLATFORM                        │
│  ┌─────────────┐  ┌──────────────┐  ┌──────────────────┐   │
│  │   API       │  │  Plugin Host │  │  Evidence Ledger │   │
│  │ (FastAPI)   │  │  (containers)│  │  (PostgreSQL +   │   │
│  └──────┬──────┘  └──────┬───────┘  │   hash chain)    │   │
│         │                │          └────────┬─────────┘   │
│         ▼                ▼                   ▼             │
│  ┌─────────────────────────────────────────────────────┐  │
│  │              PostgreSQL (RLS per tenant)            │  │
│  └─────────────────────────────────────────────────────┘  │
│  ┌─────────────────────────────────────────────────────┐  │
│  │            Redis (jobs, cache, sessions)            │  │
│  └─────────────────────────────────────────────────────┘  │
│  ┌─────────────────────────────────────────────────────┐  │
│  │        MinIO / S3 (encrypted evidence files)        │  │
│  └─────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────┘
          │
          ▼
┌─────────────────────────────────────────────────────────────┐
│                    CUSTOMER ENVIRONMENT                      │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐       │
│  │ Device Agent │  │ On-premise   │  │  PII Scanner │       │
│  │ (laptops)    │  │ Collector    │  │  (local)     │       │
│  └──────────────┘  └──────────────┘  └──────────────┘       │
└─────────────────────────────────────────────────────────────┘
```

---

## 2. Assets

| Asset | Description | Sensitivity | Location |
|-------|-------------|-------------|----------|
| Connector credentials | OAuth tokens, API keys for external systems | **Critical** | Encrypted in PostgreSQL (per-tenant keys) |
| Evidence records | Control test results, metadata | **High** | PostgreSQL (RLS) + hash chain |
| Evidence files | Exports, logs, documents | **High** | MinIO (encrypted at rest, per-tenant keys) |
| PII scan findings | Locations of Aadhaar, PAN, etc. | **High** | PostgreSQL (RLS), never raw values |
| Audit logs | All write operations | **High** | PostgreSQL (append-only) |
| User sessions / MFA | Authentication state | **Medium** | Redis (encrypted) |
| Plugin manifests | Third-party plugin definitions | **Medium** | PostgreSQL |
| Regulatory pack content | Controls, deadlines, templates | **Low** | PostgreSQL (public) |
| Platform secrets | JWT signing key, encryption keys | **Critical** | Environment / HSM |

---

## 3. Threat Actors

| Actor | Motivation | Capability |
|-------|------------|------------|
| External attacker | Data theft, ransomware, disruption | Network access, phishing, vulnerability exploits |
| Malicious plugin author | Credential theft, data exfiltration | Code execution in sandbox |
| Compromised connector | Supply chain attack | Network access to external APIs |
| Insider (platform admin) | Data access, sabotage | Full platform access |
| Rogue tenant | Cross-tenant data access | Valid authentication |
| Auditor (malicious) | Over-collection of evidence | Read-only portal access |

---

## 4. Threat Analysis (STRIDE)

### Spoofing

| Threat | Mitigation |
|--------|------------|
| Attacker impersonates a tenant | JWT/OIDC with short expiry, MFA mandatory, session binding to IP/fingerprint |
| Attacker impersonates a connector | mTLS for connector callbacks, signed webhooks with HMAC |
| Malicious plugin spoofs another plugin | Plugin signing, manifest verification, isolated containers |

### Tampering

| Threat | Mitigation |
|--------|------------|
| Modify evidence records | Append-only ledger with SHA-256 hash chain, verification CLI |
| Modify audit logs | Append-only audit table, no UPDATE/DELETE policies |
| Modify plugin behaviour at runtime | Immutable container images, signed manifests, no runtime code loading |
| SQL injection | Parameterised queries only, ORM (SQLAlchemy), no raw SQL |
| Modify connector responses | Connector health checks, recorded-response tests, schema validation |

### Repudiation

| Threat | Mitigation |
|--------|------------|
| Admin denies making a change | Comprehensive audit log (who, what, when, before, after, request_id) |
| Tenant denies evidence validity | Hash chain + optional trusted timestamping |
| Plugin author denies malicious code | Signed manifests, reproducible builds, SBOM |

### Information Disclosure

| Threat | Mitigation |
|--------|------------|
| Cross-tenant data access | PostgreSQL RLS on every table, automated cross-tenant test suite in CI |
| Connector credentials leaked | Encrypted at rest (per-tenant keys), never returned by API, audit on access |
| PII in evidence data | Metadata-first design: store hashes/counts, never raw values; PII scanner sends only metadata |
| Log injection | Structured JSON logging, no user input in log format strings |
| Error messages leak stack traces | Global error handler returns generic messages, details only in server logs |

### Denial of Service

| Threat | Mitigation |
|--------|------------|
| Connector API rate limits | Built-in rate limiting, exponential backoff, circuit breaker |
| Plugin resource exhaustion | Container CPU/memory limits, execution timeouts, network allow-list |
| Evidence flood | Batch processing, pagination, backpressure in job queue |
| Database connection exhaustion | Connection pooling, query timeouts, read replicas for heavy queries |

### Elevation of Privilege

| Threat | Mitigation |
|--------|------------|
| Tenant escalates to platform admin | RBAC with strict roles (section 19.3), no privilege escalation paths |
| Plugin escapes container | gVisor/firecracker, no host mounts, read-only rootfs, dropped capabilities |
| SQL injection to admin functions | Parameterised queries, least-privilege DB users |
| SSRF via webhook URLs | Allow-list validation, no internal metadata endpoints reachable |

---

## 5. Key Security Controls

| Control | Implementation |
|---------|----------------|
| **Tenant isolation** | PostgreSQL RLS + session middleware (ADR 0002) |
| **Credential protection** | Per-tenant envelope encryption, keys in HSM/key service |
| **Plugin sandbox** | Container runtime, network allow-list, signed manifests (ADR 0001) |
| **Evidence integrity** | Append-only ledger, SHA-256 hash chain (ADR 0003) |
| **Authentication** | OIDC (Google/Microsoft), TOTP/WebAuthn MFA, scoped API tokens |
| **Authorisation** | RBAC with 6 built-in roles, custom roles, time-boxed auditor access |
| **Audit logging** | Every write → append-only log with before/after values |
| **Secrets management** | Environment variables / Vault, never in code or logs |
| **Supply chain** | Signed container images, SBOM, dependency scanning, licence scan |
| **Vulnerability management** | Weekly automated dependency updates, CodeQL, truffleHog |
| **Incident response** | Security policy, responsible disclosure, penetration test pre-GA |

---

## 6. Data Flow: Evidence Collection

```
1. Connector (plugin)          2. Plugin Host                3. API / Worker
   ┌─────────────┐              ┌─────────────┐              ┌─────────────┐
   │ Authenticate │───────────▶│ Validate    │───────────▶│ Schedule    │
   │ with token   │  gRPC      │ permissions │  gRPC      │ collection  │
   └─────────────┘              └─────────────┘              └──────┬──────┘
                                                                    │
4. External System                                            ▼
   ┌─────────────┐              ┌─────────────┐         ┌─────────────┐
   │ Return data │───────────▶│ Normalise   │────────▶│ Store in    │
   │ (read-only) │  HTTPS      │ to evidence │  gRPC   │ ledger +    │
   └─────────────┘              │ record      │         │ object store│
                                └─────────────┘         └──────┬──────┘
                                                                   │
5. Rules Engine                                              ▼
   ┌─────────────┐              ┌─────────────┐         ┌─────────────┐
   │ Evaluate    │◀────────────│ Fetch       │◀───────│ Control     │
   │ CEL condition│  evidence  │ evidence    │  SQL    │ test runs   │
   └─────────────┘              └─────────────┘         └─────────────┘
```

---

## 7. Open Questions / Future Work

1. **Trusted timestamping** — integrate with a TSA for external anchoring of hash chain
2. **Hardware security module** — move tenant encryption keys to HSM / cloud KMS
3. **Plugin attestation** — remote attestation for plugin containers (TPM-based)
4. **Zero-trust network** — mTLS for all inter-service communication
5. **Data loss prevention** — DLP scanning on evidence files before storage
6. **Formal verification** — TLA+ model for RLS and hash chain logic

---

## 8. Review Log

| Date | Reviewer | Changes |
|------|----------|---------|
| 2026-11-19 | PragneshKumar S. Singh | Initial version for Stage 0 |

---

*This threat model must be updated whenever the architecture changes (ADR process).*
*Next review: end of Stage 1.*