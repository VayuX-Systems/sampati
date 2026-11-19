# Sampati by VayuX — Quick Start Guide

Get the **v0.0.1 Alpha** running in under 15 minutes.

## Prerequisites

- **Docker** 24+ and **Docker Compose** v2
- **OR** native: PostgreSQL 16+, Redis 7+, Python 3.12+, uv (`pip install uv`)

---

## Option 1: Docker Compose (Recommended)

```bash
cd sampati

# 1. Copy environment template
cp .env.example .env

# 2. Start all services
docker compose -f deploy/docker-compose.yml up -d

# 3. Verify health
docker compose -f deploy/docker-compose.yml ps
# All services should show "healthy"

# 4. Access services
# API:        http://localhost:8000
# API Docs:   http://localhost:8000/docs
# Web App:    http://localhost:3000 (after `cd apps/web && pnpm dev`)
# MinIO:      http://localhost:9001 (sampati / sampati-dev)
# MailHog:    http://localhost:8025
```

### Stop / Reset

```bash
# Stop
docker compose -f deploy/docker-compose.yml down

# Full reset (destroys data!)
docker compose -f deploy/docker-compose.yml down -v
```

---

## Option 2: Native (No Containers)

```bash
# 1. Install dependencies
sudo apt-get install -y postgresql-16 redis-server
pip install uv

# 2. Create database
sudo -u postgres psql -c "CREATE DATABASE sampati;"
sudo -u postgres psql -c "CREATE USER sampati WITH PASSWORD 'sampati-dev'; GRANT ALL PRIVILEGES ON DATABASE sampati TO sampati;"

# 3. Start Redis
sudo systemctl start redis-server

# 4. Run everything
./scripts/dev-local.sh up
```

---

## First Steps

### 1. Create Organisation

```bash
curl -X POST http://localhost:8000/api/v1/organisations \
  -H "Content-Type: application/json" \
  -d '{"name": "Acme Corp", "slug": "acme", "region": "IN"}'
```

### 2. Load Frameworks

```bash
# SOC 2 and ISO 27001 are pre-loaded
# Load DPDP pack (India)
curl -X POST http://localhost:8000/api/v1/frameworks/load \
  -H "Content-Type: application/json" \
  -d '{"file_path": "packs/india/dpdp/frameworks/dpdp.yaml"}'
```

### 3. Select Framework for Entity

```bash
curl -X POST http://localhost:8000/api/v1/frameworks/entities/{entity_id}/frameworks \
  -H "Content-Type: application/json" \
  -d '{"framework_id": "soc2", "framework_version_id": "..."}'
```

### 4. Configure Connectors

```bash
# Install GitHub connector
curl -X POST http://localhost:8000/api/v1/plugins/install \
  -H "Content-Type: application/json" \
  -d '{
    "plugin_id": "github",
    "config": {
      "organization": "my-org",
      "token": "ghp_xxx"
    }
  }'
```

### 5. Run Gap Assessment

```bash
# Answer scoping questionnaire, then:
curl http://localhost:8000/api/v1/frameworks/entities/{entity_id}/gap-assessment
```

---

## Architecture Overview

```
┌─────────────┐     ┌─────────────┐     ┌─────────────┐
│   Web App   │────▶│    API      │────▶│ PostgreSQL  │
│  (Next.js)  │     │  (FastAPI)  │     │   + RLS     │
└─────────────┘     └──────┬──────┘     └─────────────┘
                           │
                    ┌──────▼──────┐
                    │   Redis     │
                    │  (Queue)    │
                    └──────┬──────┘
                           │
              ┌────────────┼────────────┐
              ▼            ▼            ▼
        ┌──────────┐ ┌──────────┐ ┌──────────┐
        │ MinIO    │ │ Worker   │ │ Plugins  │
        │ (Evidence)│ │ (APScheduler)│ (GitHub, │
        └──────────┘ └──────────┘ │  Google) │
                                  └──────────┘
```

---

## Key Concepts

| Concept | Description |
|---------|-------------|
| **Organisation** | Top-level tenant (company) |
| **Entity** | Legal entity or business unit within organisation |
| **Framework** | Compliance standard (SOC 2, ISO 27001, DPDP, etc.) |
| **Control** | A safeguard (e.g., "MFA enforced") |
| **Evidence** | Proof a control works (collected by connectors) |
| **Control Test** | Automated CEL rule that evaluates evidence |
| **Plugin** | Connector, scanner, or pack (runs sandboxed) |
| **Country Pack** | Regulation-as-code (DPDP, CERT-In, RBI, etc.) |

---

## Troubleshooting

| Issue | Solution |
|-------|----------|
| `pg_isready` fails | Check PostgreSQL is running on 5432 |
| `redis-cli ping` fails | Check Redis is running on 6379 |
| MinIO health fails | Wait longer; MinIO takes ~30s to start |
| API returns 500 | Check `docker compose logs api` |
| RLS blocks queries | Ensure `X-Organisation-ID` header is set |

---

## Next Steps

- Read `docs/SAMPATI-GRANTH.md` for full product specification
- Check `AGENTS.md` for AI agent development rules
- Explore `packs/india/` for DPDP/CERT-In packs
- Build your own connector with `sampati-plugin scaffold connector my-connector`

---

## Support

- **Issues**: GitHub Issues
- **Security**: security@vayux.systems
- **Docs**: `docs/` folder

---

**Sampati by VayuX** — The open-source compliance automation platform built for India's regulators.
