# Sampati by VayuX

The Community Edition of **Sampati by VayuX**: an open-source compliance automation platform built for India's regulators.

Approved positioning: **The open-source compliance automation platform built for India's regulators.**

Sampati turns controls, evidence, policies, risks, vendors, and regulatory packs into an auditable programme. It is not a certification body, law firm, SIEM, or substitute for operating security controls.

## Repository map

- `apps/` — API, worker, web app, trust centre
- `packages/` — domain, rules engine, evidence ledger, plugin host, extension points, UI kit
- `agent/` — device agent (planned)
- `collector/` — on-premise collector and PII scanner runtime (planned)
- `plugins/` — first-party connectors, scanners, notifiers
- `packs/` — country packs
- `deploy/` — Docker Compose, Helm, air-gapped deployment
- `docs/` — user, developer, security, and architecture documentation

## Quick start

Prerequisites: Docker and Docker Compose.

```bash
./scripts/dev.sh up
```

Services:

- API: http://localhost:8000
- API documentation: http://localhost:8000/docs
- MinIO console: http://localhost:9001
- Mailcatcher: http://localhost:1080

Stop the environment:

```bash
./scripts/dev.sh down
```

## Development

Read `AGENTS.md` and `docs/SAMPATI-GRANTH.md` before making changes. Work on one checklist task at a time. Use synthetic data only. Never commit secrets or raw personal data.

The three repositories have a strict dependency direction:

`sampati-sdk` → `sampati` → `sampati-enterprise`

## Licence

The Community Edition is licensed under Apache-2.0. The Sampati and VayuX names and logos are trademarks of VayuX Systems LLP; see `TRADEMARKS.md`.

## Contact

PragneshKumar S. Singh, Co-Founder & CTO, VayuX Systems LLP
