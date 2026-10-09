"""Детерминированные правила по обезличенным свидетельствам; сеть не используется."""
from datetime import datetime, timezone, timedelta
from . import __version__
from .validation import timestamp

# (название, риск, рекомендация, ожидаемые логические факты)
RULES = {
    'NET-01': ('Публичные порты и панели', 'high', 'Ограничьте административный доступ и закройте неожиданные порты.', {'public_admin_panel': False}),
    'SSH-01': ('Вход и алгоритмы SSH', 'high', 'Отключите вход по паролю и root, исключите слабые алгоритмы SSH.', {'password_auth': False, 'root_login': False, 'weak_algorithms': False}),
    'FW-01': ('Облачный firewall и IPv6', 'critical', 'Привяжите firewall с запретом по умолчанию для обеих адресных семей и ограничьте административный входящий трафик.', {'attached': True, 'default_deny_v4': True, 'world_open_admin': False}),
    'IAM-01': ('IAM провайдера и токены API', 'critical', 'Используйте минимальные права, индивидуальные токены со сроком действия и политику ротации.', {'least_privilege': True, 'tokens_expire': True, 'rotation_policy': True, 'shared_tokens': False}),
    'MFA-01': ('MFA провайдера и восстановление доступа', 'critical', 'Включите MFA для каждого администратора и изолируйте каналы восстановления.', {'all_admins_mfa': True, 'recovery_isolated': True}),
    'META-01': ('Cloud-init и metadata', 'high', 'Удалите секреты из user-data и ограничьте доступ к metadata внутри гостевой системы.', {'user_data_contains_secrets': False, 'metadata_protected': True}),
    'DNS-01': ('Владение DNS и инвентаризация', 'high', 'Сверьте записи DNS с инвентаризацией и удалите ссылки на отсутствующие ресурсы.', {'records_match_inventory': True, 'dangling_records': False}),
    'TLS-01': ('Идентичность и срок действия TLS', 'high', 'Исправьте идентичность и цепочку сертификата, обновите его и отключите слабые протоколы.', {'identity_valid': True, 'chain_valid': True, 'weak_protocols': False}),
    'BAK-01': ('Защита резервных копий', 'critical', 'Настройте расписание зашифрованных, изолированных и неизменяемых копий с достаточным сроком хранения.', {'scheduled': True, 'encrypted': True, 'isolated': True, 'immutable': True}),
    'REC-01': ('Восстановление и его цели', 'critical', 'Проверьте восстановление на изолированном одноразовом стенде и достигните согласованных RPO/RTO.', {'restore_tested': True, 'restore_success': True}),
}


def evaluate(check_id, facts, policy):
    expected = dict(RULES[check_id][3])
    # Отключение IPv6 должно быть заявлено явно; неизвестность не означает безопасность.
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
    # Известный небезопасный факт даёт fail даже при отсутствии других фактов.
    if failures:
        return 'fail', 'Небезопасные факты: ' + ', '.join(sorted(failures)) + ('. Также отсутствует часть данных.' if missing else '.')
    if missing:
        return 'unknown', 'Отсутствуют факты: ' + ', '.join(sorted(missing))
    return 'pass', 'Переданные данные соответствуют правилу и порогам; это не гарантия безопасности инфраструктуры.'


def audit(data, now=None):
    now = now or datetime.now(timezone.utc)
    findings = []
    for check_id, (title, severity, remediation, _) in RULES.items():
        item = data['checks'].get(check_id)
        evidence = None
        if item is None:
            status, reason = 'not_run', 'Свидетельства не переданы.'
        else:
            evidence = {key: item[key] for key in ('source', 'evidence_id', 'collected_at', 'state')}
            if item['state'] == 'not_run':
                status, reason = 'not_run', 'Сбор свидетельств не выполнялся.'
            elif item['state'] in ('unsupported', 'error'):
                status, reason = 'unknown', 'Сбор свидетельств недоступен: ' + item['state']
            else:
                age = now - timestamp(item['collected_at'])
                if age < timedelta(0):
                    status, reason = 'unknown', 'Время свидетельства находится в будущем.'
                elif age > timedelta(hours=data['policy']['max_age_hours']):
                    status, reason = 'unknown', 'Свидетельство устарело относительно max_age_hours.'
                else:
                    status, reason = evaluate(check_id, item['facts'], data['policy'])
                    # В отчёт попадают только типизированные обезличенные факты.
                    evidence['facts'] = item['facts']
        findings.append({'check_id': check_id, 'title': title, 'status': status,
                         'severity': severity, 'confidence': 'synthetic' if data['synthetic'] else 'supplied_evidence',
                         'reason': reason, 'evidence': evidence, 'remediation': remediation})
    summary = {status: sum(f['status'] == status for f in findings)
               for status in ('pass', 'fail', 'unknown', 'not_run')}
    return {'schema_version': 1, 'auditor_version': __version__, 'mode': 'offline',
            'synthetic': data['synthetic'], 'target_alias': data['target_alias'],
            'evaluated_at': now.isoformat(), 'policy': data['policy'], 'summary': summary,
            'limitations': ['Проверки сети и API провайдера не выполнялись.',
                            'Свидетельства переданы извне и независимо не проверены.',
                            'Статус pass относится только к этому правилу, свидетельству и заданным порогам.'],
            'findings': findings}


def markdown(report):
    lines = ['# Отчёт о состоянии безопасности VPS', '',
             f"Цель: `{report['target_alias']}`", f"Режим: offline; Синтетические данные: {str(report['synthetic']).lower()}",
             f"Время оценки: {report['evaluated_at']}", '',
             'Сводка: ' + ', '.join(f'{k}={v}' for k, v in report['summary'].items()), '',
             'Свидетельства переданы извне и независимо не проверены. Проверки сети и провайдера не выполнялись.', '']
    for finding in report['findings']:
        lines.extend([f"## {finding['check_id']} — {finding['title']}", '',
                      f"Статус: **{finding['status']}**; severity (риск): {finding['severity']}; confidence (достоверность): {finding['confidence']}",
                      finding['reason']])
        evidence = finding['evidence']
        if evidence:
            lines.append(f"Свидетельство: `{evidence['evidence_id']}`; источник: {evidence['source']}; собрано: {evidence['collected_at']}")
            if 'facts' in evidence:
                lines.append('Факты: ' + ', '.join(f'{k}={v}' for k, v in sorted(evidence['facts'].items())))
        lines.extend(['Рекомендация: ' + finding['remediation'], ''])
    return '\n'.join(lines).rstrip()
