# Development environment and CI

Managed runtime is running/connected. The initial checkout was clean on branch work
at main commit 1b5005ea6b899b9ae2cdba4443e504de4d234a10, with only README tracked.
Prepared docs/fixtures/scripts were untracked and preserved/updated for implementation.
No AGENTS.md was found in the workspace.

## Required workflow
Python 3.12+, POSIX, git. Runtime has no third-party dependencies and no services.
Run `bash scripts/setup_environment.sh` from the checkout. It creates .venv,
installs `requirements-build.txt` with --require-hashes, installs the project with
--no-build-isolation --no-deps, then runs tests/docs/public-data/installed CLI smoke.
It works without a saved virtual environment and is repeatable. No shell activation required. Tests use unittest with PYTHONPATH=src.
Check docs/public data; build via `scripts/build_release.py`; install resulting wheel
into a separate clean venv with --no-index --no-deps and run a synthetic audit.
No provider tokens, cloud resources or new audit destinations are needed.

## CI and release evidence
CI runs pinned checkout/setup-python, pinned build dependencies, docs/public-data
checks, unit/integration tests, wheel/source build, checksum-pinned gitleaks scan, clean installation and synthetic
smoke test. Contents permission is read; no provider secrets or report artifacts.
Remote CI/PR/release status must be reported from actual GitHub outcomes, not inferred
from local tests. First release is prerelease while real platform checks are unperformed.
API access and Git proxy authorization are separate capabilities; a working ls-remote
is not proof of PR/merge/release permission. Publication blockers are recorded in the
final execution report, not disguised as completed release work.

## Reusable cloud startup
Use the existing isolated checkout; no worktree unless explicitly requested. Inspect
status and docs before work. Preserve credentials/proxy/CA configuration. Rerun tests
and installed CLI smoke after restoring a snapshot. Prior docs-only scope is superseded
by the current user's explicit implementation/commit/push/PR/merge/release authorization.
Public data remains synthetic; no paid resources, real credentials or arbitrary scans.

## Managed environment draft
install_script: `set -euo pipefail; cd /workspace/vps-opsec-auditor; bash scripts/setup_environment.sh`.
start_skill: inspect this checkout, run the setup script if .venv is absent, then tests
and installed CLI smoke as documented above; no services or credentials required.
The prior docs-only instructions are replaced. No onboarding directory is used.
API domains api.github.com/uploads.github.com may be added to the existing package-manager
preset through the draft. No credentials are added or revealed. Saving is not runtime
application or environment publication. Git push works independently of API authorization.
GitHub API access subsequently became available through the normal gh CLI.
PR #1 and commit d8ddb6a were verified through gh; push run 37923541901 and PR run
37923547213 both completed successfully. Later commits require their own CI verification.

## Release publication through Actions
`.github/workflows/release.yml` is manually dispatched from main for the existing
v0.1.0a1 draft (ID 407850186), with immutable source commit
069c2e93fc85fb45bc997f95e00730cef036a1c3. The tag is never moved or recreated.
A read-only job checks tag/commit ancestry, runs tests/secret scan, builds twice,
checks reproducibility and tests the installed wheel. A separate job has only
contents:write and uses the standard job GITHUB_TOKEN to upload assets to the existing
draft. It checks tag identity, downloads and compares all assets/checksums before
publishing prerelease, then verifies published state. It does not create another release.
No user credentials or provider operations are involved. Unexpected existing assets,
identity mismatches or differing files stop publication. The workflow is specific to
this first release; a future version needs a reviewed update to its fixed constants.
