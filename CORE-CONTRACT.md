# Контракты CLI, JSON и библиотеки

HTTP API, маршрутов сервера и провайдерского SDK нет. Контракты относятся к локальному
CLI и Python-модулям, описанным ниже. Ключи/ID/enum неизменны; пояснения на русском.

## CLI
`vps-opsec-auditor input [--format json|markdown] [--output path] [--at timestamp]
[--fail-on none|fail|incomplete]`; также --help и --version.
input — обычный файл до 1 МиБ. --output создаёт только новый файл 0600.
--at принимает время ISO с часовым поясом; без него текущий UTC. Не используйте
повторное время для сокрытия устаревания реальных данных.
Коды: 0 — корректный отчёт при выполненной политике выхода; 1 — условие --fail-on;
2 — неверные аргументы/данные/часы/файлы. none допускает fail в отчёте; fail учитывает
только fail; incomplete также unknown/not_run. Сообщения не повторяют секретные значения.

## Вход JSON v1
Обязательные schema_version=1, synthetic, target_alias, policy, checks.
Поля policy: max_age_hours, min_tls_days, min_retention_days, max_rpo_minutes,
Поле max_rto_minutes — положительные ограниченные целые. Схема определяет точные пределы.
checks: только NET-01/SSH-01/FW-01/IAM-01/MFA-01/META-01/DNS-01/TLS-01/BAK-01/REC-01.
Запись: state, source, evidence_id, collected_at, facts. state: observed/unsupported/
Состояния: not_run/error; source: synthetic/operator/provider_export/lab. Не observed требует
пустых facts. synthetic должен соответствовать source всех записей. Псевдонимы —
1–64 ASCII-буквы/цифры/underscore/hyphen, первый символ буквенно-цифровой.
Никаких raw exports, токенов или IP. [Схема](schemas/input-v1.schema.json),
[подробности](docs/input.md), [предикаты](docs/checks.md).

## Выход JSON
Корневые поля: schema_version, auditor_version, mode=offline, synthetic, target_alias, evaluated_at,
Остальные поля: policy, summary, limitations, findings. summary считает pass/fail/unknown/not_run.
Поля каждой findings-записи: check_id, title, status, severity, confidence, reason, evidence,
Рекомендация: remediation. Риск severity — high/critical; confidence — synthetic/supplied_evidence.
evidence — null при отсутствии записи; иначе source/evidence_id/collected_at/state.
Свежая observed-запись дополнительно сохраняет типизированные facts.
Не используйте русские title/reason/remediation как машинные ID; анализируйте ключи/enum.

## Python и расширение правил
`validation.load(raw_bytes)` возвращает валидированный dict или InputError.
`audit.audit(validated_data, now=None)` возвращает dict отчёта; вызывающий сначала
валидирует данные, а явное now передаёт как datetime с часовым поясом.
`audit.markdown(report)` возвращает строку; `cli.main(argv=None)` — код возврата.
Внутренние evaluate/validate/read_input не считаются стабильным внешним API.

Новое правило: добавить ID/русские title/remediation и ожидаемые факты в RULES,
предикаты evaluate, поля в обеих копиях схемы, безопасный/небезопасный набор,
матрицу, IDS в check_docs и исторический эскиз. Добавить missing/stale/future/
unsupported/error/not_run и пороговые тесты, обновить примеры отчётов и проверить
чистую установку. Нет сети внутри rules. Несовместимая схема требует новой версии
контракта и документированной миграции, а не молчаливого приведения типов.
