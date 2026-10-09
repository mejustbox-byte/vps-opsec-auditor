# MVP implementation and validation plan

## This release candidate
1. Review scope/threats/ADR and fix input/report semantics.
2. Closed schema for sanitized evidence; ten deterministic posture rules.
3. Offline CLI, JSON/Markdown reports, freshness gate and safe filesystem behavior.
4. Synthetic safe/unsafe/missing fixtures and reproducible report examples.
5. Unit/integration tests: every rule positive/negative/missing/stale/unsupported,
   numeric boundaries, IPv6 gaps, invalid input, output safety, no network and fresh installation.
6. Hash-pinned build tool, deterministic artifacts, CI and public-data checks.
7. PR, merge and prerelease only when actual access/CI permits; do not claim blocked operations succeeded.

## Acceptance boundaries
No real platform validation has run. Offline rules evaluate owner-normalized facts;
this MVP does not independently inventory ports or derive effective firewall policy.
CI checks synthetic behavior, not infrastructure. No real credentials, paid resources,
network scans, provider provisioning or automated recovery operations.

## Follow-up gates
Select one provider and document its IAM/API semantics and unavailable capabilities.
Run a separately authorized disposable lab with negative cases for IPv6 bypass,
metadata isolation, excess token scopes, MFA gaps and failed restores.
Add offline import/adapter contracts and only then consider scoped read-only collectors.
Stable release requires recorded real lab outcomes, provenance/freshness review and
confirmation of install/CI on the supported environment. Expand supported OS/Python
versions only after actual validation. See [laboratory protocol](lab.md).
