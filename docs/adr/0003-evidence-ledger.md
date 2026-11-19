# ADR 0003: Evidence Ledger with Hash Chain

## Context

Evidence is the core artefact auditors examine. It must be tamper-evident: any modification, deletion, or reordering of evidence records must be detectable. The ledger must also support verification by auditors without requiring them to trust the platform operator.

## Decision

Implement an **append-only evidence ledger with a SHA-256 hash chain**:

1. **Each evidence record** contains:
   - All evidence fields (source, result, data, timestamps)
   - `hash`: SHA-256 of the canonical JSON representation + previous hash
   - `prev_hash`: hash of the previous record in the chain
   - `linked_controls`: list of control IDs this evidence supports

2. **Hash computation**: deterministic JSON (sorted keys, no whitespace) + previous hash

3. **Append-only**: records are never modified or deleted. Corrections are new records.

4. **Verification**: anyone with the full ledger can recompute the chain and detect tampering

5. **Optional trusted timestamping**: future enhancement for external anchoring

The ledger lives in `packages/ledger/` with `EvidenceLedger` and `LedgerRecord` classes.

## Consequences

### Positive

- **Tamper-evident**: any change breaks the chain
- **Auditor-verifiable**: auditors can independently verify integrity
- **Simple**: no blockchain, no external dependencies
- **Performant**: O(1) append, O(n) verification

### Negative

- **No deletion**: GDPR right to erasure requires careful handling (store only metadata, not raw PII)
- **Chain grows unbounded**: periodic snapshots/checkpoints needed for large deployments
- **Single chain per organisation**: cross-org verification not supported (by design)

## Alternatives Considered

1. **Database audit tables** (trigger-based)
   - Rejected: admin can bypass triggers, not independently verifiable
2. **Merkle tree** (periodic roots)
   - Rejected: adds complexity, hash chain is sufficient for linear history
3. **Blockchain / DLT**
   - Rejected: overkill, operational burden, no regulatory requirement

## Implementation Notes

- `EvidenceRecord` schema in `sampati-sdk/spec/evidence.schema.json`
- `packages/ledger/models.py` has `compute_hash()` and `verify_chain()`
- Metadata-first design: `data` field never contains raw PII (section 6.3, 18.6)
- Large files go to encrypted object storage; ledger stores only metadata + hash

## References

- SAMPATI-GRANTH.md sections 6.3, 8.10 (F11), 18.5, 18.6, 19.5
- Privacy rules in AGENTS.md