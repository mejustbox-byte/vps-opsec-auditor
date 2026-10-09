# ADR-0001: offline-first Python CLI

Status: accepted for MVP under the user's implementation authorization. Date: 2026-10-09.

## Decision and rationale
Python 3.12+, POSIX CLI; zero third-party runtime dependencies. Standard library
JSON/typing/time handling and unittest support strict offline rules and synthetic tests.
The bundled closed JSON Schema is enforced by a deliberately small validator for
its used keywords. The schema and installed copy must match (tested).
Setuptools 80.9.0 builds the wheel; its wheel hash is pinned in requirements-build.txt.
The public source bundle is deterministic, and wheel timestamps use a fixed build epoch.
No database, web server, provider SDK, daemon or VPS guest agent.

## Alternatives / trade-offs
Go provides a portable binary and compile-time types but more fixture iteration work.
TypeScript adds a Node/runtime dependency ecosystem without a current CLI benefit.
Python reduces offline complexity; the small validator must evolve with the schema.
A full schema library is preferable if the contract grows beyond the tested subset.
CLI POSIX filesystem protections are intentionally required; Windows is not validated.
Provider SDK selection is deferred until a provider-specific disposable lab exists.
Revisit for portable binaries, broad concurrency, complex schemas or adapter requirements.
