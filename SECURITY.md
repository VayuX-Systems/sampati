# Security Policy

## Supported Versions

| Version | Supported          |
| ------- | ------------------ |
| 1.x.x   | :white_check_mark: |
| < 1.0   | :x:                |

## Reporting a Vulnerability

Please report security vulnerabilities to **security@vayux.systems**.

Do not open a public issue for security vulnerabilities.

We will acknowledge receipt within 48 hours and provide a status update within 7 days.

## Security Features

- Tenant isolation via PostgreSQL row-level security
- Encrypted secrets storage with per-tenant keys
- Metadata-first evidence design (no raw PII stored)
- Sandboxed, signed plugin runtime
- Comprehensive audit logging
- Regular dependency scanning and SBOM generation

## Responsible Disclosure

We follow responsible disclosure practices. Please give us reasonable time
to address the issue before public disclosure.
