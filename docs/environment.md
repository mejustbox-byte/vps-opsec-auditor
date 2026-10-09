# Development environment and CI

Managed runtime is running/connected. The initial checkout was clean on branch work
at main commit 1b5005ea6b899b9ae2cdba4443e504de4d234a10, with only README tracked.
Prepared docs/fixtures/scripts were untracked and preserved/updated for implementation.
/workspace/onboarding does not exist. No AGENTS.md was found in the workspace.

## Required workflow
Python 3.12+, POSIX, git. Runtime has no third-party dependencies and no services.
Create .venv; install `requirements-build.txt` with --require-hashes; install project
with --no-build-isolation --no-deps. Tests use unittest with PYTHONPATH=src.
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
