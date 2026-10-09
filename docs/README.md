# GITHUB-OPSEC: VPS — design and MVP

The implemented MVP is an offline evidence auditor. Focus: external VPS exposure
and provider control plane; guest Linux hardening belongs to a separate project.
Real provider checks remain unverified until an authorized disposable lab exists.

1. [Requirements](requirements.md)
2. [Threat model](threat-model.md)
3. [Architecture](architecture.md)
4. [Check matrix](checks.md)
5. [Disposable laboratory](lab.md)
6. [Stack ADR](adr/0001-stack.md)
7. [Environment and CI](environment.md)
8. [MVP plan](mvp.md)
9. [Input contract](input.md)
10. [Release notes](release-notes.md)
11. [Prepared PR description](pull-request.md)

[Safe synthetic evidence](../fixtures/safe.json), [unsafe evidence](../fixtures/unsafe.json),
[missing evidence](../fixtures/missing.json), [JSON Schema](../schemas/input-v1.schema.json)
and [readable example report](../examples/unsafe-report.md) are public synthetic data.
The older [synthetic report sketch](../fixtures/synthetic-audit.json) is historical
pre-implementation documentation; it is not valid CLI input.
