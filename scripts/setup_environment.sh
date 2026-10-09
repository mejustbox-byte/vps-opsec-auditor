#!/usr/bin/env bash
# Recreate the development environment from source; no saved venv is required.
set -euo pipefail
cd "$(dirname "${BASH_SOURCE[0]}")/.."
python3 -c 'import os, sys; assert os.name == "posix" and sys.version_info >= (3, 12), "Python 3.12+ on POSIX required"'
python3 -m venv .venv
.venv/bin/python -m pip install --require-hashes -r requirements-build.txt
.venv/bin/python -m pip install --no-build-isolation --no-deps .
.venv/bin/python -m pip check
PYTHONPATH=src .venv/bin/python -m unittest discover -s tests -v
.venv/bin/python scripts/check_docs.py
.venv/bin/python scripts/check_public_data.py
.venv/bin/vps-opsec-auditor fixtures/safe.json --at 2026-10-09T01:00:00Z --format json --fail-on incomplete |
  .venv/bin/python -c 'import json, sys; r=json.load(sys.stdin); assert r["synthetic"] and r["summary"] == {"pass": 10, "fail": 0, "unknown": 0, "not_run": 0}; print("PASS: installed CLI smoke")'
