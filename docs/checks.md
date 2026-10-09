# Implemented rule matrix

All results concern supplied evidence. Real provider/lab validation is **not performed**.
Every row has synthetic pass/fail/missing/stale/unsupported/error tests. Missing metrics
or booleans are unknown; an observed unsafe fact is fail even when another fact is missing.

| ID / requirement | Pass predicate over fresh observed facts | Severity | Evidence limitation |
| --- | --- | --- | --- |
| NET-01 / R01 | unexpected_ports=0; public_admin_panel=false | high | Port inventory/panel classification supplied by owner; no scan |
| SSH-01 / R02 | password_auth=false; root_login=false; weak_algorithms=false | high | Auth policy cannot be inferred from banner alone |
| FW-01 / R03 | attached=true; default_deny_v4=true; world_open_admin=false; explicit ipv6_enabled and default_deny_v6=true when enabled | critical | Owner must normalize effective rules/attachments; no raw rule engine |
| IAM-01 / R04 | least_privilege=true; tokens_expire=true; rotation_policy=true; shared_tokens=false | critical | Aggregated inventory claims; no secrets or API scope verification |
| MFA-01 / R04 | all_admins_mfa=true; recovery_isolated=true | critical | API or owner attestation; unsupported source yields unknown |
| META-01 / R05 | user_data_contains_secrets=false; metadata_protected=true | high | Requires authorized internal evidence, never an external inference |
| DNS-01 / R06 | records_match_inventory=true; dangling_records=false | high | Owner supplies record reconciliation; no DNS takeover |
| TLS-01 / R06 | identity_valid=true; chain_valid=true; weak_protocols=false; days_remaining >= min_tls_days | high | Owner records trust store/SNI/clock; no handshake |
| BAK-01 / R07 | scheduled=true; encrypted=true; isolated=true; immutable=true; retention_days >= min_retention_days | critical | Backup existence does not prove recoverability |
| REC-01 / R07 | restore_tested=true; restore_success=true; rpo_minutes <= max_rpo_minutes; rto_minutes <= max_rto_minutes | critical | Owner-run disposable restore evidence required |

Severity describes the risk evaluated, not the number of known vulnerabilities.
Whole-rule pass needs every applicable predicate and fresh evidence. The firewall
rule accepts explicitly disabled IPv6, but cannot prove that assertion is accurate.
Retain timestamp/source/evidence_id privately and corroborate before operational action.
