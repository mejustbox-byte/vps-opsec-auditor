# Architecture — implemented offline MVP

Regular bounded JSON file → strict schema validation → freshness/capability gate →
pure rule evaluation → JSON or readable Markdown. No network or shell execution.

- `validation.py`: bundled input-v1 schema with closed objects, bounded integers,
  exact booleans, safe aliases, timezone-aware timestamps, source enums and no raw exports.
  Implements only the subset used by this bundled schema, not arbitrary JSON Schema.
  Rejects duplicate keys, NaN/Infinity, invalid/deep JSON, oversized input and unknown fields.
- `audit.py`: deterministic evaluation across ten stable rule IDs. Policy thresholds
  are supplied by the owner; no universal RPO/RTO goals are assumed. Evidence timestamps
  are evaluated against the clock (or explicit replay time). Future/stale evidence
  produces unknown. Unsupported/error evidence produces unknown; absent/not_run
  collection produces not_run. Known unsafe facts dominate missing facts.
- `cli.py`: POSIX regular-file reads bounded to 1 MiB; FIFOs/devices rejected without
  waiting. Safe errors do not echo evidence, paths or parser excerpts. New output
  files are exclusive and mode 0600; existing paths/symlinks are not overwritten.
- Reporter: version, target alias, synthetic label, evaluation timestamp, policy,
  summary and per-rule severity/confidence/reason/evidence/remediation. Only constrained
  facts and references can reach output. No untrusted free-text rendering.

The `load(bytes)` API returns validated data; `audit(validated_data, now)` evaluates
it. Library callers must validate first and supply a timezone-aware clock if overriding.
Schema_version 1 is fixed; unknown versions fail closed. A source tag is an assertion,
not cryptographic evidence provenance. All results explicitly disclaim independent verification.
Read-only means no infrastructure mutation; an explicitly requested local report is written.

Future collectors/adapters are outside this release. They need owner-approved scope,
read-only API allowlists, endpoint/DNS/redirect validation, budgets, redaction and lab
validation before integration. Restore remains an owner action; auditor reads its evidence.
