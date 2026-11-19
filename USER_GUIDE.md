# Sampati v0.0.1 Alpha — User Guide

**The open-source compliance automation platform built for India's regulators.**

---

## Table of Contents

1. [Getting Started](#getting-started)
2. [Core Concepts](#core-concepts)
3. [Organisations & Entities](#organisations--entities)
4. [Frameworks & Country Packs](#frameworks--country-packs)
5. [Controls & Crosswalk](#controls--crosswalk)
6. [Connectors & Plugins](#connectors--plugins)
7. [Evidence & Ledger](#evidence--ledger)
8. [Control Tests & Automation](#control-tests--automation)
9. [Gap Assessment & Readiness](#gap-assessment--readiness)
10. [Manual Evidence & Requests](#manual-evidence--requests)
11. [India DPDP Pack](#india-dpdp-pack)
12. [Auditor Portal](#auditor-portal)
13. [Troubleshooting](#troubleshooting)

---

## Getting Started

### Quick Start (Docker)

```bash
cd sampati
cp .env.example .env
docker compose -f deploy/docker-compose.yml up -d

# Verify
docker compose -f deploy/docker-compose.yml ps
# All services: healthy
```

**Access:**
- API: http://localhost:8000
- API Docs: http://localhost:8000/docs
- Web App: http://localhost:3000 (run `cd apps/web && pnpm dev`)

### Quick Start (Native)

```bash
# Prerequisites: PostgreSQL 16+, Redis 7+, Python 3.12+, uv
sudo apt-get install postgresql-16 redis-server
pip install uv

# Create database
sudo -u postgres psql -c "CREATE DATABASE sampati;"
sudo -u postgres psql -c "CREATE USER sampati WITH PASSWORD 'sampati-dev'; GRANT ALL PRIVILEGES ON DATABASE sampati TO sampati;"

# Start
./scripts/dev-local.sh up
```

---

## Core Concepts

| Term | Definition |
|------|------------|
| **Organisation** | Top-level tenant (your company) |
| **Entity** | Legal entity or business unit within organisation |
| **Framework** | Compliance standard (SOC 2, ISO 27001, DPDP, etc.) |
| **Control** | A safeguard (e.g., "MFA enforced for all users") |
| **Evidence** | Proof a control works (collected automatically or manually) |
| **Control Test** | Automated CEL rule that evaluates evidence |
| **Crosswalk** | Mapping: one control → many framework requirements |
| **Country Pack** | Regulation-as-code (DPDP, CERT-In, RBI, SEBI, IRDAI) |
| **Plugin** | Connector, scanner, or pack (runs sandboxed) |
| **Evidence Ledger** | Tamper-evident hash chain of all evidence |

---

## Organisations & Entities

### Create Organisation
```bash
curl -X POST http://localhost:8000/api/v1/organisations \
  -H "Content-Type: application/json" \
  -d '{"name": "Acme Corp", "slug": "acme", "region": "IN"}'
```

### Create Entity
```bash
curl -X POST http://localhost:8000/api/v1/organisations/{org_id}/entities \
  -H "Content-Type: application/json" \
  -d '{"name": "Acme India", "type": "legal_entity"}'
```

### Switch Organisation (Web)
Use the organisation switcher in the top navigation bar.

---

## Frameworks & Country Packs

### Load a Framework
```bash
curl -X POST http://localhost:8000/api/v1/frameworks/load \
  -H "Content-Type: application/json" \
  -d '{"file_path": "frameworks/soc2.yaml"}'
```

### List Frameworks
```bash
curl http://localhost:8000/api/v1/frameworks
```

### India Country Packs (Pre-installed)
```bash
# DPDP (Data Protection)
curl -X POST http://localhost:8000/api/v1/frameworks/load \
  -d '{"file_path": "packs/india/dpdp/frameworks/dpdp.yaml"}'

# CERT-In (Cyber incidents)
curl -X POST http://localhost:8000/api/v1/frameworks/load \
  -d '{"file_path": "packs/india/cert-in/frameworks/cert-in.yaml"}'

# RBI, SEBI, IRDAI (coming in v0.1.0)
```

### Select Framework for Entity
```bash
curl -X POST http://localhost:8000/api/v1/frameworks/entities/{entity_id}/frameworks \
  -H "Content-Type: application/json" \
  -d '{"framework_id": "soc2", "framework_version_id": "..."}'
```

---

## Controls & Crosswalk

### View Controls for Entity
```bash
curl http://localhost:8000/api/v1/controls/entities/{entity_id}
```

### View Crosswalk (Control → Frameworks)
```bash
curl http://localhost:8000/api/v1/controls/{control_id}/mappings
```

### Update Control Status
```bash
curl -X PATCH http://localhost:8000/api/v1/controls/{control_id} \
  -H "Content-Type: application/json" \
  -d '{"status": "implemented", "owner_id": "user-id"}'
```

**Crosswalk Example:**
```
Control: CTRL-ACCESS-002 "MFA enforced"
  → SOC 2: CC6.1
  → ISO 27001: A.8.5
  → DPDP: Section 8(3)
```
One control implementation satisfies multiple frameworks.

---

## Connectors & Plugins

### Available Connectors (v0.0.1)
| Connector | Evidence Types |
|-----------|----------------|
| GitHub | Branch protection, PR reviews, signed commits, Dependabot, secret scanning, MFA |
| Google Workspace | User MFA, suspended users, admin privileges, Drive sharing, groups |

### Install Connector
```bash
# GitHub
curl -X POST http://localhost:8000/api/v1/plugins/install \
  -H "Content-Type: application/json" \
  -d '{
    "plugin_id": "github",
    "config": {
      "organization": "my-org",
      "token": "ghp_xxx",
      "include_private": true
    }
  }'

# Google Workspace
curl -X POST http://localhost:8000/api/v1/plugins/install \
  -d '{
    "plugin_id": "google-workspace",
    "config": {
      "customer_id": "C0xxxxx",
      "service_account_key": "...",
      "admin_email": "admin@company.com"
    }
  }'
```

### List Installed Plugins
```bash
curl http://localhost:8000/api/v1/plugins
```

### Trigger Collection
```bash
curl -X POST http://localhost:8000/api/v1/plugins/github/collect \
  -d '{"window_start": "2026-11-01T00:00:00Z", "window_end": "2026-11-19T00:00:00Z"}'
```

### Plugin Sandbox Security
- Runs in isolated containers
- Network allow-list enforced
- Read-only scopes only
- Signed manifests required
- Resource limits (CPU, memory, timeout)

---

## Evidence & Ledger

### View Evidence
```bash
curl http://localhost:8000/api/v1/evidence?limit=20&check=branch_protection_enabled
```

### Verify Ledger Integrity
```bash
curl http://localhost:8000/api/v1/evidence/verify
# Returns: {"valid": true, "errors": []}
```

### Get Latest Hash
```bash
curl http://localhost:8000/api/v1/evidence/latest-hash
# Returns: {"hash": "sha256:..."}
```

### Evidence Structure
```json
{
  "id": "uuid",
  "source_plugin": "github",
  "collector": "connector",
  "check": "branch_protection_enabled",
  "subject": "repo:acme/payments-api",
  "result": "pass",
  "collected_at": "2026-11-19T10:30:00Z",
  "valid_until": "2027-02-19T10:30:00Z",
  "data": {"branch": "main", "required_reviews": 2},
  "hash": "sha256:...",
  "prev_hash": "sha256:...",
  "linked_controls": ["CTRL-CODE-001"]
}
```

**Tamper Detection**: Any change breaks the SHA-256 hash chain. Auditors can verify independently.

---

## Control Tests & Automation

### Run Tests
```bash
curl -X POST http://localhost:8000/api/v1/controls/run-tests \
  -d '{"schedule": "daily"}'
```

### Starter Tests (10 included)
| Test ID | Control | Check |
|---------|---------|-------|
| TEST-MFA-001 | CTRL-ACCESS-002 | MFA for all active users |
| TEST-MFA-002 | CTRL-ACCESS-001 | MFA for admin access |
| TEST-ENCRYPTION-001 | CTRL-DATA-001 | Encryption at rest |
| TEST-ENCRYPTION-002 | CTRL-DATA-002 | TLS 1.2+ in transit |
| TEST-BRANCH-PROTECTION-001 | CTRL-CODE-001 | Branch protection |
| TEST-REQUIRED-REVIEWS-001 | CTRL-CODE-002 | PR reviews ≥2 |
| TEST-SECRET-SCANNING-001 | CTRL-CODE-005 | Secret scanning |
| TEST-DEPENDABOT-001 | CTRL-CODE-006 | Dependabot alerts |
| TEST-SUSPENDED-USERS-001 | CTRL-ACCESS-003 | No suspended users |
| TEST-ADMIN-COUNT-001 | CTRL-ACCESS-004 | Admin count ≤5 |

### Test Results
```json
{
  "test_id": "TEST-MFA-001",
  "result": "fail",
  "evidence_ids": ["uuid1", "uuid2"],
  "data_used": {"idp_user_mfa_status": [...]},
  "evaluated_at": "2026-11-19T10:30:00Z"
}
```

### On Failure
- Control marked as failing
- Task created for owner
- Notification sent
- Exception possible (max 30 days, requires approval)

---

## Gap Assessment & Readiness

### Run Scoping Questionnaire
Answer questions about company size, data types, sector, cloud usage.

### Get Gap Report
```bash
curl http://localhost:8000/api/v1/frameworks/entities/{entity_id}/gap-report
```

**Response:**
```json
{
  "framework_id": "soc2",
  "readiness_score": 72.5,
  "total_requirements": 64,
  "implemented": 38,
  "partial": 12,
  "not_started": 14,
  "gaps": [
    {
      "requirement_id": "CC6.4",
      "reference": "CC6.4",
      "title": "MFA for remote access",
      "status": "not_started",
      "mapped_controls": [{"control_id": "CTRL-ACCESS-002", "status": "fail"}],
      "gap_severity": "high"
    }
  ]
}
```

### Get Readiness Score
```bash
curl http://localhost:8000/api/v1/frameworks/entities/{entity_id}/readiness
```

---

## Manual Evidence & Requests

### Create Evidence Request
```bash
curl -X POST http://localhost:8000/api/v1/evidence-requests \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Board resolution for data processing",
    "description": "Upload signed board resolution authorizing data processing",
    "assignee_id": "user-uuid",
    "due_days": 14,
    "control_implementation_id": "ctrl-impl-uuid",
    "priority": "high"
  }'
```

### Submit Evidence (Assignee)
```bash
curl -X POST http://localhost:8000/api/v1/evidence-requests/{id}/submit \
  -d '{
    "evidence_type": "file",
    "file_key": "minio/object/key",
    "description": "Signed board resolution PDF"
  }'
```

### Review Evidence (Reviewer)
```bash
curl -X POST http://localhost:8000/api/v1/evidence-requests/{id}/review \
  -d '{"action": "approve", "comment": "Signature verified"}'
```

### List Requests
```bash
curl http://localhost:8000/api/v1/evidence-requests?status=pending&assignee_id=me
```

---

## India DPDP Pack

### Load DPDP Pack
```bash
curl -X POST http://localhost:8000/api/v1/frameworks/load \
  -d '{"file_path": "packs/india/dpdp/frameworks/dpdp.yaml"}'
```

### DPDP Controls Included
- Notice & Consent (CTRL-DPDP-NC-001 to 004)
- Data Quality (CTRL-DPDP-DQ-001 to 003)
- Security Safeguards (CTRL-DPDP-SEC-001 to 006)
- Breach Response (CTRL-DPDP-BR-001 to 004)
- Data Principal Rights
- Children's Data
- Cross-border Transfers
- Significant Data Fiduciary extras

### Breach Clock (Multi-regulator)
```bash
curl -X POST http://localhost:8000/api/v1/incidents \
  -d '{
    "type": "personal_data_breach",
    "affected_data": ["email", "phone", "aadhaar"],
    "regulators": ["dpdp", "cert-in"]
  }'
```

**Starts clocks automatically:**
- DPDP: 72 hours to Board + affected individuals
- CERT-In: 6 hours to CERT-In
- RBI/SEBI: Sector-specific (if applicable)

### Data Inventory & PII Scanner
```bash
# Run PII scanner (on-premise)
curl -X POST http://localhost:8000/api/v1/scanners/india-pii/scan \
  -d '{"targets": ["postgresql://...", "s3://bucket/"]}'
```

---

## Auditor Portal

### Create Audit Project
```bash
curl -X POST http://localhost:8000/api/v1/audit/projects \
  -d '{
    "name": "SOC 2 Type II 2026",
    "framework_id": "soc2",
    "period_start": "2026-01-01",
    "period_end": "2026-12-31",
    "auditor_emails": ["auditor@firm.com"]
  }'
```

### Grant Auditor Access
```bash
curl -X POST http://localhost:8000/api/v1/audit/projects/{id}/access \
  -d '{"auditor_email": "auditor@firm.com", "expires_days": 30}'
```

### Auditor Can
- View controls in scope with evidence trail
- Use sampling tools
- Request additional evidence (PBC list)
- Record findings/exceptions
- Export audit pack (controls, evidence index, test results)

---

## Troubleshooting

| Issue | Solution |
|-------|----------|
| `pg_isready` fails | Check PostgreSQL on 5432, user `sampati` exists |
| `redis-cli ping` fails | Check Redis on 6379 |
| MinIO health fails | Wait 30s; check `docker logs minio` |
| API 500 error | Check `docker compose logs api` |
| RLS blocks query | Set `X-Organisation-ID` header |
| Plugin install fails | Check network allowlist, token scopes |
| Evidence verify fails | Hash chain tampered — check `audit_logs` |
| Connector returns no data | Verify token scopes, org name |

---

## CLI Reference

### Evidence Ledger CLI
```bash
# Verify chain
sampati-ledger --org-id ORG_ID verify

# List records
sampati-ledger --org-id ORG_ID list --limit 20

# Show record
sampati-ledger --org-id ORG_ID show RECORD_ID

# Latest hash
sampati-ledger --org-id ORG_ID latest-hash
```

### Plugin CLI
```bash
# Scaffold new connector
sampati-plugin scaffold connector my-connector --name "My Connector"

# Validate manifest
sampati-plugin validate manifest.json

# Test plugin
sampati-plugin test ./my-connector
```

---

## Support

- **Documentation**: `docs/` folder
- **Issues**: GitHub Issues
- **Security**: security@vayux.systems
- **Design Partners**: partners@vayux.systems

---

**Sampati by VayuX** — Apache 2.0 licensed. Not legal advice.
