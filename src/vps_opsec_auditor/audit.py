"""Deterministic rules over sanitized evidence; never opens a network connection."""
from datetime import datetime, timezone, timedelta
from . import __version__
from .validation import timestamp

# (title, severity, remediation, expected boolean facts)
RULES = {
    'NET-01': ('Public ports and panels', 'high', 'Restrict administrative exposure and remove unexpected ports.', {'public_admin_panel': False}),
    'SSH-01': ('SSH authentication and algorithms', 'high', 'Disable password/root login and retire weak SSH algorithms.', {'password_auth': False, 'root_login': False, 'weak_algorithms': False}),
    'FW-01': ('Cloud firewall and IPv6', 'critical', 'Attach a default-deny firewall to both address families and restrict admin ingress.', {'attached': True, 'default_deny_v4': True, 'world_open_admin': False}),
    'IAM-01': ('Provider IAM and API tokens', 'critical', 'Use least privilege, expiring individual tokens and a rotation policy.', {'least_privilege': True, 'tokens_expire': True, 'rotation_policy': True, 'shared_tokens': False}),
    'MFA-01': ('Provider MFA and recovery', 'critical', 'Enable MFA for every administrator and isolate recovery channels.', {'all_admins_mfa': True, 'recovery_isolated': True}),
    'META-01': ('Cloud-init and metadata', 'high', 'Remove secrets from user-data and restrict metadata access inside the guest.', {'user_data_contains_secrets': False, 'metadata_protected': True}),
    'DNS-01': ('DNS ownership and inventory', 'high', 'Reconcile DNS records with inventory and remove dangling references.', {'records_match_inventory': True, 'dangling_records': False}),
    'TLS-01': ('TLS identity and lifetime', 'high', 'Correct the certificate identity/chain, renew it and disable weak protocols.', {'identity_valid': True, 'chain_valid': True, 'weak_protocols': False}),
    'BAK-01': ('Backup protection', 'critical', 'Schedule encrypted, isolated, immutable backups with sufficient retention.', {'scheduled': True, 'encrypted': True, 'isolated': True, 'immutable': True}),
    'REC-01': ('Restore and recovery objectives', 'critical', 'Test restoration in an isolated disposable lab and meet the agreed RPO/RTO.', {'restore_tested': True, 'restore_success': True}),
}


def evaluate(check_id, facts, policy):
    expected = dict(RULES[check_id][3])
    # An IPv6-disabled claim must be explicit. Unknown IPv6 capability is not safe.
    if check_id == 'FW-01':
        if facts.get('ipv6_enabled') is True:
            expected['default_deny_v6'] = True
        elif 'ipv6_enabled' not in facts:
            expected['ipv6_enabled'] = None
    missing = [key for key in expected if key not in facts]
    failures = [key for key, desired in expected.items()
                if key in facts and desired is not None and facts[key] != desired]
    numeric = {
        'NET-01': ('unexpected_ports', 0, 'max'),
        'TLS-01': ('days_remaining', policy['min_tls_days'], 'min'),
        'BAK-01': ('retention_days', policy['min_retention_days'], 'min'),
    }
    comparisons = [numeric[check_id]] if check_id in numeric else []
    if check_id == 'REC-01':
        comparisons = [('rpo_minutes', policy['max_rpo_minutes'], 'max'),
                       ('rto_minutes', policy['max_rto_minutes'], 'max')]
    for key, limit, direction in comparisons:
        if key not in facts:
            missing.append(key)
        elif (direction == 'max' and facts[key] > limit) or (direction == 'min' and facts[key] < limit):
            failures.append(key)
    # A known unsafe fact remains a failure even when another fact is missing.
    if failures:
        return 'fail', 'Unsafe evidence: ' + ', '.join(sorted(failures)) + ('. Also incomplete.' if missing else '.')
    if missing:
        return 'unknown', 'Missing facts: ' + ', '.join(sorted(missing))
    return 'pass', 'Supplied evidence meets this rule and configured policy; not an infrastructure guarantee.'


def audit(data, now=None):
    now = now or datetime.now(timezone.utc)
    findings = []
    for check_id, (title, severity, remediation, _) in RULES.items():
        item = data['checks'].get(check_id)
        evidence = None
        if item is None:
            status, reason = 'not_run', 'No evidence supplied.'
        else:
            evidence = {key: item[key] for key in ('source', 'evidence_id', 'collected_at', 'state')}
            if item['state'] == 'not_run':
                status, reason = 'not_run', 'Evidence collection was not run.'
            elif item['state'] in ('unsupported', 'error'):
                status, reason = 'unknown', 'Evidence collection unavailable: ' + item['state']
            else:
                age = now - timestamp(item['collected_at'])
                if age < timedelta(0):
                    status, reason = 'unknown', 'Evidence timestamp is in the future.'
                elif age > timedelta(hours=data['policy']['max_age_hours']):
                    status, reason = 'unknown', 'Evidence is stale for configured max_age_hours.'
                else:
                    status, reason = evaluate(check_id, item['facts'], data['policy'])
                    # Only typed, sanitized facts can reach the report.
                    evidence['facts'] = item['facts']
        findings.append({'check_id': check_id, 'title': title, 'status': status,
                         'severity': severity, 'confidence': 'synthetic' if data['synthetic'] else 'supplied_evidence',
                         'reason': reason, 'evidence': evidence, 'remediation': remediation})
    summary = {status: sum(f['status'] == status for f in findings)
               for status in ('pass', 'fail', 'unknown', 'not_run')}
    return {'schema_version': 1, 'auditor_version': __version__, 'mode': 'offline',
            'synthetic': data['synthetic'], 'target_alias': data['target_alias'],
            'evaluated_at': now.isoformat(), 'policy': data['policy'], 'summary': summary,
            'limitations': ['No network or provider API checks were performed.',
                            'Evidence is supplied, not independently verified.',
                            'A pass applies only to this rule, evidence and configured policy.'],
            'findings': findings}


def markdown(report):
    lines = ['# VPS security posture report', '',
             f"Target: `{report['target_alias']}`", f"Mode: offline; synthetic: {str(report['synthetic']).lower()}",
             f"Evaluated at: {report['evaluated_at']}", '',
             'Summary: ' + ', '.join(f'{k}={v}' for k, v in report['summary'].items()), '',
             'Evidence is supplied, not independently verified. No network/provider checks performed.', '']
    for finding in report['findings']:
        lines.extend([f"## {finding['check_id']} — {finding['title']}", '',
                      f"Status: **{finding['status']}**; severity: {finding['severity']}; confidence: {finding['confidence']}",
                      finding['reason']])
        evidence = finding['evidence']
        if evidence:
            lines.append(f"Evidence: `{evidence['evidence_id']}`; source: {evidence['source']}; collected: {evidence['collected_at']}")
            if 'facts' in evidence:
                lines.append('Facts: ' + ', '.join(f'{k}={v}' for k, v in sorted(evidence['facts'].items())))
        lines.extend(['Recommendation: ' + finding['remediation'], ''])
    return '\n'.join(lines).rstrip()
