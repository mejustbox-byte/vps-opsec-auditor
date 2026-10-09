# VPS security posture report

Target: `disposable-example`
Mode: offline; synthetic: true
Evaluated at: 2026-10-09T01:00:00+00:00

Summary: pass=0, fail=10, unknown=0, not_run=0

Evidence is supplied, not independently verified. No network/provider checks performed.

## NET-01 — Public ports and panels

Status: **fail**; severity: high; confidence: synthetic
Unsafe evidence: public_admin_panel, unexpected_ports.
Evidence: `net-01`; source: synthetic; collected: 2026-10-09T00:00:00Z
Facts: public_admin_panel=True, unexpected_ports=10
Recommendation: Restrict administrative exposure and remove unexpected ports.

## SSH-01 — SSH authentication and algorithms

Status: **fail**; severity: high; confidence: synthetic
Unsafe evidence: password_auth, root_login, weak_algorithms.
Evidence: `ssh-01`; source: synthetic; collected: 2026-10-09T00:00:00Z
Facts: password_auth=True, root_login=True, weak_algorithms=True
Recommendation: Disable password/root login and retire weak SSH algorithms.

## FW-01 — Cloud firewall and IPv6

Status: **fail**; severity: critical; confidence: synthetic
Unsafe evidence: attached, default_deny_v4, default_deny_v6, world_open_admin.
Evidence: `fw-01`; source: synthetic; collected: 2026-10-09T00:00:00Z
Facts: attached=False, default_deny_v4=False, default_deny_v6=False, ipv6_enabled=True, world_open_admin=True
Recommendation: Attach a default-deny firewall to both address families and restrict admin ingress.

## IAM-01 — Provider IAM and API tokens

Status: **fail**; severity: critical; confidence: synthetic
Unsafe evidence: least_privilege, rotation_policy, shared_tokens, tokens_expire.
Evidence: `iam-01`; source: synthetic; collected: 2026-10-09T00:00:00Z
Facts: least_privilege=False, rotation_policy=False, shared_tokens=True, tokens_expire=False
Recommendation: Use least privilege, expiring individual tokens and a rotation policy.

## MFA-01 — Provider MFA and recovery

Status: **fail**; severity: critical; confidence: synthetic
Unsafe evidence: all_admins_mfa, recovery_isolated.
Evidence: `mfa-01`; source: synthetic; collected: 2026-10-09T00:00:00Z
Facts: all_admins_mfa=False, recovery_isolated=False
Recommendation: Enable MFA for every administrator and isolate recovery channels.

## META-01 — Cloud-init and metadata

Status: **fail**; severity: high; confidence: synthetic
Unsafe evidence: metadata_protected, user_data_contains_secrets.
Evidence: `meta-01`; source: synthetic; collected: 2026-10-09T00:00:00Z
Facts: metadata_protected=False, user_data_contains_secrets=True
Recommendation: Remove secrets from user-data and restrict metadata access inside the guest.

## DNS-01 — DNS ownership and inventory

Status: **fail**; severity: high; confidence: synthetic
Unsafe evidence: dangling_records, records_match_inventory.
Evidence: `dns-01`; source: synthetic; collected: 2026-10-09T00:00:00Z
Facts: dangling_records=True, records_match_inventory=False
Recommendation: Reconcile DNS records with inventory and remove dangling references.

## TLS-01 — TLS identity and lifetime

Status: **fail**; severity: high; confidence: synthetic
Unsafe evidence: chain_valid, days_remaining, identity_valid, weak_protocols.
Evidence: `tls-01`; source: synthetic; collected: 2026-10-09T00:00:00Z
Facts: chain_valid=False, days_remaining=0, identity_valid=False, weak_protocols=True
Recommendation: Correct the certificate identity/chain, renew it and disable weak protocols.

## BAK-01 — Backup protection

Status: **fail**; severity: critical; confidence: synthetic
Unsafe evidence: encrypted, immutable, isolated, retention_days, scheduled.
Evidence: `bak-01`; source: synthetic; collected: 2026-10-09T00:00:00Z
Facts: encrypted=False, immutable=False, isolated=False, retention_days=0, scheduled=False
Recommendation: Schedule encrypted, isolated, immutable backups with sufficient retention.

## REC-01 — Restore and recovery objectives

Status: **fail**; severity: critical; confidence: synthetic
Unsafe evidence: restore_success, restore_tested, rpo_minutes, rto_minutes.
Evidence: `rec-01`; source: synthetic; collected: 2026-10-09T00:00:00Z
Facts: restore_success=False, restore_tested=False, rpo_minutes=1000, rto_minutes=1000
Recommendation: Test restoration in an isolated disposable lab and meet the agreed RPO/RTO.
