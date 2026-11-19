# ADR 0002: Multi-Tenancy with Row-Level Security

## Context

Sampati is a multi-tenant SaaS and self-hosted platform. Every organisation (tenant) must be strictly isolated: no tenant can read, write, or even detect the existence of another tenant's data. This is a security requirement and a regulatory requirement for Indian data residency and sector-specific rules.

## Decision

Use **PostgreSQL row-level security (RLS)** as the primary isolation mechanism:

1. **Every tenant table includes `organisation_id`** (UUIDv7, not nullable)
2. **RLS policies** on all tenant tables restrict rows to `current_setting('app.current_organisation_id')`
3. **Application sets tenant context** in a single location: a request-scoped database session middleware
4. **Background jobs** explicitly carry and set their `organisation_id` before any database access
5. **Automated cross-tenant test suite** attempts reads, writes, searches, and file downloads across tenants and must find nothing

The RLS policy is defined in `deploy/init-rls.sql` and applied at database initialisation.

## Consequences

### Positive

- **Database-enforced**: isolation cannot be bypassed by application bugs
- **Performance**: RLS policies are evaluated at the storage layer, no application overhead
- **Simplicity**: no need for manual `WHERE organisation_id = ?` on every query
- **Auditable**: isolation is visible in the database schema

### Negative

- **All queries must go through the session middleware** - direct DB access bypasses RLS
- **Schema changes require RLS policy updates** - automated tests catch regressions
- **PostgreSQL-specific** - limits portability to other databases (accepted)

## Alternatives Considered

1. **Application-level filtering** (manual `WHERE` clauses)
   - Rejected: human error risk, impossible to audit completely
2. **Separate database per tenant**
   - Rejected: operational overhead, doesn't scale to thousands of tenants
3. **Separate schema per tenant**
   - Rejected: same operational issues, connection pooling complexity

## Implementation Notes

- `get_tenant_session()` in `apps/api/src/sampati_api/database.py` sets the context
- `TenantMiddleware` extracts `organisation_id` from auth token
- Cross-tenant test in `tests/test_cross_tenant.py` runs in CI
- Background workers use `get_tenant_session(organisation_id)` explicitly

## References

- SAMPATI-GRANTH.md sections 6.2, 8.1 (F1), 18.5, 19.2
- Security rules in AGENTS.md