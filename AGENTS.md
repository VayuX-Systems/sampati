# AGENTS.md: rules for AI coding agents working on Sampati

Project: Sampati by VayuX, an open-source compliance automation platform.
Source of truth: docs/SAMPATI-GRANTH.md. Read sections 17, 18, 19, 21 and 23 before any task.

## Always
- Work on one checklist item at a time. Write the plan in the PR description.
- Write tests from the acceptance criteria first, then the code.
- Run lint, type checks, tests, secret scan and licence scan before opening a PR.
- Keep PRs small (under about 400 changed lines). One feature slice per PR.
- Record every real design choice as an ADR in docs/adr/.
- Tick the feature checklist and update docs and the changelog in the same PR.

## Never
- Never commit secrets, real customer data or real personal data (use synthetic data).
- Never copy code, framework text or data from other projects.
- Never add a dependency with a GPL or AGPL licence.
- Never put Enterprise code in the Community repo or the reverse dependency direction.
- Never hard-code legal text, deadlines or regulator rules; they live in pack data.
- Never weaken tenant isolation, authentication or audit logging to make a test pass.
- Never name VayuX internal tools in public files.

## Stop and ask a human when
- A requirement is unclear, missing or contradictory.
- A change touches authentication, tenant isolation, secrets, the plugin sandbox or the evidence ledger design.
- A change alters a public API, a spec schema or a licence.
- Anything involves legal or regulatory wording, money, or real customer data.

## Style
- Python: type hints everywhere, ruff, mypy strict, pytest.
- TypeScript: strict mode, ESLint.
- Go: golangci-lint.
- Every source file starts with an SPDX licence identifier for its repo.
