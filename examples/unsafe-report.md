# Отчёт о состоянии безопасности VPS

Цель: `disposable-example`
Режим: offline; Синтетические данные: true
Время оценки: 2026-10-09T01:00:00+00:00

Сводка: pass=0, fail=10, unknown=0, not_run=0

Свидетельства переданы извне и независимо не проверены. Проверки сети и провайдера не выполнялись.

## NET-01 — Публичные порты и панели

Статус: **fail**; severity (риск): high; confidence (достоверность): synthetic
Небезопасные факты: public_admin_panel, unexpected_ports.
Свидетельство: `net-01`; источник: synthetic; собрано: 2026-10-09T00:00:00Z
Факты: public_admin_panel=True, unexpected_ports=10
Рекомендация: Ограничьте административный доступ и закройте неожиданные порты.

## SSH-01 — Вход и алгоритмы SSH

Статус: **fail**; severity (риск): high; confidence (достоверность): synthetic
Небезопасные факты: password_auth, root_login, weak_algorithms.
Свидетельство: `ssh-01`; источник: synthetic; собрано: 2026-10-09T00:00:00Z
Факты: password_auth=True, root_login=True, weak_algorithms=True
Рекомендация: Отключите вход по паролю и root, исключите слабые алгоритмы SSH.

## FW-01 — Облачный firewall и IPv6

Статус: **fail**; severity (риск): critical; confidence (достоверность): synthetic
Небезопасные факты: attached, default_deny_v4, default_deny_v6, world_open_admin.
Свидетельство: `fw-01`; источник: synthetic; собрано: 2026-10-09T00:00:00Z
Факты: attached=False, default_deny_v4=False, default_deny_v6=False, ipv6_enabled=True, world_open_admin=True
Рекомендация: Привяжите firewall с запретом по умолчанию для обеих адресных семей и ограничьте административный входящий трафик.

## IAM-01 — IAM провайдера и токены API

Статус: **fail**; severity (риск): critical; confidence (достоверность): synthetic
Небезопасные факты: least_privilege, rotation_policy, shared_tokens, tokens_expire.
Свидетельство: `iam-01`; источник: synthetic; собрано: 2026-10-09T00:00:00Z
Факты: least_privilege=False, rotation_policy=False, shared_tokens=True, tokens_expire=False
Рекомендация: Используйте минимальные права, индивидуальные токены со сроком действия и политику ротации.

## MFA-01 — MFA провайдера и восстановление доступа

Статус: **fail**; severity (риск): critical; confidence (достоверность): synthetic
Небезопасные факты: all_admins_mfa, recovery_isolated.
Свидетельство: `mfa-01`; источник: synthetic; собрано: 2026-10-09T00:00:00Z
Факты: all_admins_mfa=False, recovery_isolated=False
Рекомендация: Включите MFA для каждого администратора и изолируйте каналы восстановления.

## META-01 — Cloud-init и metadata

Статус: **fail**; severity (риск): high; confidence (достоверность): synthetic
Небезопасные факты: metadata_protected, user_data_contains_secrets.
Свидетельство: `meta-01`; источник: synthetic; собрано: 2026-10-09T00:00:00Z
Факты: metadata_protected=False, user_data_contains_secrets=True
Рекомендация: Удалите секреты из user-data и ограничьте доступ к metadata внутри гостевой системы.

## DNS-01 — Владение DNS и инвентаризация

Статус: **fail**; severity (риск): high; confidence (достоверность): synthetic
Небезопасные факты: dangling_records, records_match_inventory.
Свидетельство: `dns-01`; источник: synthetic; собрано: 2026-10-09T00:00:00Z
Факты: dangling_records=True, records_match_inventory=False
Рекомендация: Сверьте записи DNS с инвентаризацией и удалите ссылки на отсутствующие ресурсы.

## TLS-01 — Идентичность и срок действия TLS

Статус: **fail**; severity (риск): high; confidence (достоверность): synthetic
Небезопасные факты: chain_valid, days_remaining, identity_valid, weak_protocols.
Свидетельство: `tls-01`; источник: synthetic; собрано: 2026-10-09T00:00:00Z
Факты: chain_valid=False, days_remaining=0, identity_valid=False, weak_protocols=True
Рекомендация: Исправьте идентичность и цепочку сертификата, обновите его и отключите слабые протоколы.

## BAK-01 — Защита резервных копий

Статус: **fail**; severity (риск): critical; confidence (достоверность): synthetic
Небезопасные факты: encrypted, immutable, isolated, retention_days, scheduled.
Свидетельство: `bak-01`; источник: synthetic; собрано: 2026-10-09T00:00:00Z
Факты: encrypted=False, immutable=False, isolated=False, retention_days=0, scheduled=False
Рекомендация: Настройте расписание зашифрованных, изолированных и неизменяемых копий с достаточным сроком хранения.

## REC-01 — Восстановление и его цели

Статус: **fail**; severity (риск): critical; confidence (достоверность): synthetic
Небезопасные факты: restore_success, restore_tested, rpo_minutes, rto_minutes.
Свидетельство: `rec-01`; источник: synthetic; собрано: 2026-10-09T00:00:00Z
Факты: restore_success=False, restore_tested=False, rpo_minutes=1000, rto_minutes=1000
Рекомендация: Проверьте восстановление на изолированном одноразовом стенде и достигните согласованных RPO/RTO.
