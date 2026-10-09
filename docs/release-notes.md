# v0.1.0a1 — offline MVP prerelease candidate

Adds strict sanitized JSON evidence schema, ten offline posture rules, JSON/Markdown
reports, pass/fail/unknown/not_run semantics, freshness/policy gates and private
exclusive output creation. Synthetic safe/unsafe/missing fixtures and replayable
examples are included. Zero runtime dependencies, hash-pinned setuptools build,
wheel/source bundle with SHA256SUMS, synthetic unit/integration tests and CI.

Installation/run instructions are in [README](../README.md). Build/test instructions
are in [environment](environment.md); real validation protocol is in [lab](lab.md).
This document is prepared release content, not proof that a GitHub release exists.

## Validation limits
All local fixtures and test observations are synthetic. No real public ports/panels,
SSH, cloud firewall/IPv6, provider IAM/tokens/MFA, cloud-init/metadata, DNS/TLS,
backup or restore checks were performed. No provider adapters or network collectors.
Actual platform validation needs a separate authorized disposable lab. No paid resources
or real credentials used. Pass means only that supplied facts meet configured policy.
Local validation: 17 unittest cases (with per-rule subcases), fresh wheel installation
and source-bundle installation, identical repeated artifact checksums, documentation
links, targeted public-data checks and gitleaks 8.24.3 (no leaks found).
Remote CI and release publication must be confirmed from the actual run/release.
Only Python 3.12 on POSIX is locally validated; versions 3.13+ are not independently tested.
