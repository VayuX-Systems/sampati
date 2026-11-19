# Sampati v0.0.1 Alpha — Design Partner Demo Script

**Duration**: 45-60 minutes  
**Audience**: Design partners (startup, regulated entity, CA/CS firm)  
**Goal**: Demonstrate end-to-end compliance automation from framework selection to gap report

---

## Demo Environment

- **URL**: http://localhost:8000/docs (API) / http://localhost:3000 (Web)
- **Org**: "Demo Corp" (pre-created)
- **Data**: Synthetic evidence pre-loaded for GitHub + Google Workspace

---

## Demo Flow (45 min)

### 1. Introduction (5 min)
- **Problem**: Manual compliance with spreadsheets, screenshots, consultant calls
- **Solution**: Sampati = continuous compliance automation + India-first country packs
- **Architecture**: API + Web + Plugins (sandboxed) + Evidence Ledger (tamper-evident)

### 2. Quick Setup (5 min)
**Live**: Create organisation → Create entity → Select frameworks

```bash
# 1. Create organisation
curl -X POST localhost:8000/api/v1/organisations \
  -H "Content-Type: application/json" \
  -d '{"name": "Demo Corp", "slug": "demo", "region": "IN"}'

# 2. Create entity
curl -X POST localhost:8000/api/v1/organisations/{org_id}/entities \
  -H "Content-Type: application/json" \
  -d '{"name": "Demo Corp India", "type": "legal_entity"}'

# 3. Select frameworks (SOC 2 + ISO 27001 + DPDP)
curl -X POST localhost:8000/api/v1/frameworks/entities/{entity_id}/frameworks \
  -H "Content-Type: application/json" \
  -d '{"framework_id": "soc2", "framework_version_id": "..."}'
```

**Web UI**: Show organisation switcher, entity tree, framework selection

### 3. Connector Configuration (5 min)
**Live**: Install GitHub + Google Workspace connectors

```bash
# GitHub
curl -X POST localhost:8000/api/v1/plugins/install \
  -H "Content-Type: application/json" \
  -d '{
    "plugin_id": "github",
    "config": {"organization": "demo-org", "token": "ghp_demo..."}
  }'

# Google Workspace
curl -X POST localhost:8000/api/v1/plugins/install \
  -H "Content-Type: application/json" \
  -d '{
    "plugin_id": "google-workspace",
    "config": {"customer_id": "C0xxxxx", "service_account_key": "...", "admin_email": "admin@demo.com"}
  }'
```

**Show**: Plugin list, permission prompts, sandbox info

### 4. Evidence Collection (10 min)
**Live**: Trigger collection → View evidence → Verify ledger

```bash
# Trigger collection (normally scheduled)
curl -X POST localhost:8000/api/v1/plugins/github/collect \
  -H "Content-Type: application/json" \
  -d '{"window_start": "2026-11-01T00:00:00Z", "window_end": "2026-11-19T00:00:00Z"}'

# View collected evidence
curl localhost:8000/api/v1/evidence?limit=20

# Verify ledger integrity
curl localhost:8000/api/v1/evidence/verify
```

**Show**: Evidence list with hash chain, tamper detection demo

### 5. Control Tests & Gap Assessment (10 min)
**Live**: Run tests → View gap report

```bash
# Run control tests
curl -X POST localhost:8000/api/v1/controls/run-tests \
  -H "Content-Type: application/json" \
  -d '{"schedule": "daily"}'

# Get gap assessment
curl localhost:8000/api/v1/frameworks/entities/{entity_id}/gap-report

# Get readiness score
curl localhost:8000/api/v1/frameworks/entities/{entity_id}/readiness
```

**Show**: 
- Test results (PASS/FAIL) with evidence links
- Gap report with prioritized remediation
- Readiness score per framework

### 6. Manual Evidence & Requests (5 min)
**Live**: Create evidence request → Submit → Review

```bash
# Create request
curl -X POST localhost:8000/api/v1/evidence-requests \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Board resolution for data processing",
    "description": "Upload signed board resolution",
    "assignee_id": "user-id",
    "due_days": 14,
    "control_implementation_id": "ctrl-impl-id"
  }'

# Submit evidence (as assignee)
curl -X POST localhost:8000/api/v1/evidence-requests/{id}/submit \
  -H "Content-Type: application/json" \
  -d '{"evidence_type": "file", "file_key": "minio-key", "description": "Signed PDF"}'

# Review (as reviewer)
curl -X POST localhost:8000/api/v1/evidence-requests/{id}/review \
  -H "Content-Type: application/json" \
  -d '{"action": "approve", "comment": "Verified signature"}'
```

### 7. DPDP India Pack Preview (5 min)
**Show**: DPDP framework, breach clock, data inventory

```bash
# Load DPDP pack
curl -X POST localhost:8000/api/v1/frameworks/load \
  -H "Content-Type: application/json" \
  -d '{"file_path": "packs/india/dpdp/frameworks/dpdp.yaml"}'

# Breach clock demo
curl -X POST localhost:8000/api/v1/incidents \
  -H "Content-Type: application/json" \
  -d '{
    "type": "personal_data_breach",
    "affected_data": ["email", "phone"],
    "regulators": ["dpdp", "cert-in"]
  }'

# Show: Multi-clock (DPDP 72hr, CERT-In 6hr)
```

---

## Key Talking Points

| Feature | Differentiator |
|---------|----------------|
| **Evidence Ledger** | SHA-256 hash chain — tamper-evident, auditor-verifiable |
| **Crosswalk** | One control → multiple frameworks (SOC 2 + ISO + DPDP) |
| **Plugin Sandbox** | Containers, network allow-list, signed manifests |
| **India Packs** | DPDP, CERT-In, RBI, SEBI — regulation-as-code |
| **Crosswalk** | Implement once, comply many |
| **Metadata-first** | No raw PII stored, only evidence metadata + hashes |

---

## Feedback Capture

After demo, ask design partner:

1. **Workflow**: Does the framework→controls→evidence flow match your process?
2. **Connectors**: Which tools do you need next? (Jira, Slack, AWS, Azure, Zoho, Tally, etc.)
3. **DPDP Pack**: Are the controls, breach clock, data inventory sufficient?
4. **Gap Report**: Is the prioritized gap list actionable?
5. **Manual Evidence**: Is the request→submit→review flow usable?
6. **Auditor Portal**: What would your auditor need to see?

---

## Next Steps for Design Partner

1. **Week 1**: Install in your environment, configure connectors
2. **Week 2**: Run real gap assessment for one framework
3. **Week 3**: Test manual evidence workflow with your team
4. **Week 4**: Provide structured feedback (template provided)

---

## Support During Pilot

- **Slack**: #sampati-design-partners
- **Email**: partners@vayux.systems
- **Weekly**: 30-min check-in calls
- **Issues**: GitHub Issues with "design-partner" label

---

**Thank you!** Your feedback shapes the product for India's compliance teams.
