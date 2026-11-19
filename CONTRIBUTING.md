# Contributing to Sampati

Thank you for your interest in contributing to Sampati! This document outlines the contribution process.

## Getting Started

1. Fork the repository
2. Create a branch: `git checkout -b feat/your-feature-name`
3. Make your changes
4. Run tests and checks locally: `./scripts/check.sh`
5. Submit a pull request

## Commit Convention

We use [Conventional Commits](https://www.conventionalcommits.org/):

- `feat:` — new feature
- `fix:` — bug fix
- `docs:` — documentation only
- `test:` — adding tests
- `refactor:` — code change that neither fixes a bug nor adds a feature
- `chore:` — maintenance tasks
- `security:` — security-related changes

All commits must be signed off with `git commit -s` (DCO).

## Pull Request Requirements

- All CI checks must pass
- At least one human review (two for security-critical areas)
- Tests for new functionality
- Documentation updates
- ADR for any design decision

## Licensing

All contributions to the Community Edition are licensed under Apache-2.0.
By contributing, you agree that your contributions will be licensed under Apache-2.0
and that you have the right to license them as such (DCO sign-off).

## Code of Conduct

Please read our [Code of Conduct](CODE_OF_CONDUCT.md).

## Security

Please read our [Security Policy](SECURITY.md) for reporting vulnerabilities.

## Development Environment

See [DEVELOPMENT.md](docs/DEVELOPMENT.md) for setup instructions.
