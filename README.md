# vps-opsec-auditor

Read-only **offline** VPS exposure and provider-control-plane evidence auditor.
Version **0.1.0a1** is a prerelease candidate: real provider and network laboratory
validation has **not** been performed. No scanner, API client or remediation is included.
A `pass` evaluates supplied evidence; it does not certify real infrastructure.

## Install (Python 3.12+, POSIX)

For a downloaded release wheel and SHA256SUMS in the same directory:

```sh
sha256sum -c SHA256SUMS
python3 -m venv .venv
.venv/bin/python -m pip install --no-index --no-deps vps_opsec_auditor-0.1.0a1-py3-none-any.whl
.venv/bin/vps-opsec-auditor --version
```

If only the wheel was downloaded, verify its matching SHA256SUMS line instead;
the full check also expects the source archive. Checksums detect corruption, not
publisher identity. Obtain artifacts/checksums through a trusted release channel.
The executable is installed inside the virtual environment; activation is optional.

From this checkout (no runtime dependencies), `bash scripts/setup_environment.sh`
performs installation and validation without a saved virtual environment. For installation only:

```sh
python3 -m venv .venv
.venv/bin/python -m pip install --require-hashes -r requirements-build.txt
.venv/bin/python -m pip install --no-build-isolation --no-deps .
```

## Run synthetic examples

```sh
.venv/bin/vps-opsec-auditor fixtures/safe.json --at 2026-10-09T01:00:00Z --format json
.venv/bin/vps-opsec-auditor fixtures/unsafe.json --at 2026-10-09T01:00:00Z --format markdown
.venv/bin/vps-opsec-auditor fixtures/missing.json --at 2026-10-09T01:00:00Z --fail-on incomplete
```

The third command intentionally exits **1** because no checks ran. Fixtures are
frozen synthetic examples; without `--at` they eventually become stale (`unknown`).
Real audits should use the actual evaluation clock and separately stored private,
sanitized evidence. No credentials or target IPs are required or accepted.
`--output /private/new-report.json` creates a new file with mode 0600 and refuses
existing paths. Do not store real input/report files in this public checkout.

Statuses: **pass**, **fail**, **unknown** (missing/stale/unsupported/error evidence),
**not_run** (no collection). Default valid-report exit code is 0;
`--fail-on fail` exits 1 for failures, `--fail-on incomplete` also fails for gaps.
Invalid input/clock/filesystem usage exits 2 without exposing input contents.

Ten rules cover public ports/panels, SSH, firewall/IPv6, IAM/tokens, MFA/recovery,
cloud-init/metadata, DNS, TLS, backups and measured recovery objectives.
The schema accepts sanitized typed facts, aliases and evidence references, not
raw provider exports, credentials or IP addresses. See [input guide](docs/input.md),
[design and MVP plan](docs/README.md), [laboratory protocol](docs/lab.md),
[security boundaries](SECURITY.md) and [release notes](docs/release-notes.md).

## Develop and validate

```sh
PYTHONPATH=src python3 -m unittest discover -s tests -v
python3 scripts/check_docs.py
python3 scripts/check_public_data.py
.venv/bin/python scripts/build_release.py
```

Unit/integration tests are offline and synthetic. Build tooling is hash-pinned;
wheel/source bundle checksums are written to `dist/SHA256SUMS`. CI executes the
same tests and a fresh wheel installation smoke test without provider secrets.
License: MIT.
