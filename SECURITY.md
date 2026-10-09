# Security boundaries

This CLI never connects to networks or provider APIs and never changes infrastructure.
It evaluates supplied sanitized evidence. A pass is not a security certification.
Real provider validation is unperformed in the first prerelease candidate.
Do not put real tokens, credentials, IPs, raw exports or reports in public git/issues/CI.
Store private evidence outside this checkout and review aliases before sharing.

Input has a closed schema and 1 MiB limit; unknown fields/types, duplicate JSON keys,
NaN and invalid timestamps are rejected. Errors do not echo input values. Output
files are new/exclusive and mode 0600. Standard output may be logged by your shell/CI;
use an appropriate private output location for non-synthetic reports.
Only POSIX/Python 3.12 is currently validated. No support for Windows file protections.
Read-only is an infrastructure property, not a promise of zero local writes.

Report security problems without secrets or identifiable infrastructure. There is
no configured private reporting channel in this initial repository; do not disclose
sensitive vulnerability evidence publicly. Contact the repository owner through an
available private channel before sharing private details.
