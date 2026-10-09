# Implement offline VPS posture auditor MVP

The repository previously had no executable auditor. Add a Python CLI that evaluates
sanitized evidence across ten VPS exposure and provider-control-plane checks, with
pass/fail/unknown/not_run, evidence references, severity and remediation. Missing,
stale and unsupported evidence remains visible; no network or provider calls run.

Includes a closed JSON Schema, safe bounded input/output handling, synthetic fixtures,
JSON/Markdown reports, design/security/lab documentation, hash-pinned build tooling,
reproducible wheel/source artifacts and CI with gitleaks and clean-install smoke tests.

Validation: 17 unit/integration test cases with per-rule subcases, all passing;
fresh wheel/source installs and installed CLI smoke; matching repeated artifact
checksums; docs/public-data checks and gitleaks without detected leaks.
Real provider, network, cloud-init/metadata, backup and recovery labs were not run.
First release must remain prerelease (v0.1.0a1); pass means supplied-evidence compliance,
not independently verified infrastructure security. No paid resources or real credentials used.
