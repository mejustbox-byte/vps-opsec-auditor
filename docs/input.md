# Input v1 and interpretation

The authoritative [schema](../schemas/input-v1.schema.json) is bundled in the installed
package. Start from [safe.json](../fixtures/safe.json) or [missing.json](../fixtures/missing.json).
Never paste a raw provider export or token into this public repository.

Required root fields: schema_version=1, synthetic boolean, safe target_alias,
policy (all five positive integer limits), checks (zero to ten supported IDs).
Policy: max_age_hours, min_tls_days, min_retention_days, max_rpo_minutes,
max_rto_minutes. These are owner-selected goals; examples are not universal policy.
Each present check requires state, source, evidence_id, collected_at and facts.

- state: observed / unsupported / not_run / error. Non-observed states require empty facts.
- source: synthetic / operator / provider_export / lab. A synthetic document must
  use only synthetic sources; a non-synthetic document cannot use synthetic sources.
- evidence_id and target_alias: 1–64 ASCII alphanumeric/underscore/hyphen characters,
  starting with alphanumeric. Use aliases, never secrets, IPs or account identifiers.
- collected_at: timezone-aware ISO timestamp with T and seconds, optional fractional
  seconds (up to six digits), Z or ±HH:MM offset. Future/stale timestamps are unknown.
- facts: only the explicitly typed booleans and integer metrics in the schema.
  Unknown fields, coercions such as "false", duplicate JSON keys and non-finite numbers fail.
  JSON file maximum 1 MiB; input must be a regular file.

Missing required facts produce unknown unless a known unsafe fact already produces fail.
Missing check = not_run; unsupported/error = unknown. An explicit disabled IPv6
assertion excludes IPv6 deny-policy evaluation; omitted IPv6 capability is unknown.
No rule treats missing evidence as pass. See [exact rule matrix](checks.md).

`--at` fixes replay time for tests; it must not be used to conceal stale real evidence.
Severity is potential impact if unsafe; a passing critical-severity rule is not a
critical finding. Confidence is synthetic or supplied_evidence, never independent verification.
Output includes only typed facts, evidence IDs, source/state/timestamps and explanations.
Even aliases can contain sensitive identifiers: operator review is still mandatory.

Real use: privately normalize authorized owner observations to this schema, set
synthetic=false and accurate source/time, store input outside checkout, run CLI with
actual clock and --fail-on incomplete, review coverage and corroborate findings.
This is an evidence assessment, not a direct provider/network test.
