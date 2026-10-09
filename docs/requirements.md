# Требования

## Цель и пользователи
Владелец VPS получает воспроизводимый отчёт о внешней экспозиции и защите аккаунта
провайдера с доказательствами, ограничениями и рекомендациями без изменения ресурсов.
Приоритет: внешняя поверхность, затем контрольная плоскость, затем восстановление.

## Обязательный охват
- R01: инвентаризация явно разрешённых endpoints, IPv4/IPv6, публичных TCP-портов,
  административных панелей; неизвестные сервисы не получают статус безопасных.
- R02: SSH — доступность, host key/алгоритмы по handshake; password/root policy
  только из разрешённых обезличенных сведений, не из предположений по баннеру.
- R03: cloud firewall — attachment, effective ingress/egress, приоритет правил,
  IPv4/IPv6, default deny, расхождение с наблюдаемой экспозицией.
- R04: IAM — владельцы, роли, least privilege, API token scope/expiry/rotation,
  MFA и recovery channels; содержимое токенов никогда не собирается.
- R05: cloud-init/user-data и metadata — отсутствие секретов по обезличенному
  свидетельству, версия/защита metadata endpoint. Внешний probe не доказывает защиту внутри VPS.
- R06: DNS/TLS — A/AAAA, CNAME, dangling records, certificate SAN/expiry/chain,
  протоколы и соответствие владельцу; takeover не предпринимается.
- R07: backup — расписание, retention, шифрование, изоляция доступа, immutability,
  свидетельство восстановления, измеренные RPO/RTO.
- R08: отчёт JSON и Markdown с check_id, target alias, timestamp, evidence source,
  severity, confidence, status, remediation и причиной отсутствия данных.
- R09: offline-first; сеть только после явного выбора разрешённого стенда.
- R10: провайдерские capabilities описываются явно; отсутствие API для MFA
  или восстановления означает manual/unknown, а не pass.

## Ограничения и контракт безопасности
Только чтение: запрещены изменения firewall/IAM/DNS, создание ресурсов, exploit,
brute force, login attempts, выполнение команд через SSH и автоматическое remediation.
Read-only запрос может попасть в журналы и вызвать rate limit: это указывается в отчёте.
Нет массового discovery, произвольных адресов или автоматически разрешённых redirect.
Для будущих probes: allowlist адресов/портов и владельца, повторная проверка DNS перед
подключением, запрет расширения scope через CNAME/redirect, ограниченные timeout,
concurrency, request budget и отмена. Link-local/metadata доступны только специально
изолированной лаборатории; обычный внешний runner их блокирует.

Никаких реальных IP, ключей, токенов, raw exports, user-data или персональных данных
в git и CI artifacts. Только aliases и documentation ranges. Реальные свидетельства
хранятся отдельно, с минимизацией, сроком хранения и доступом владельца.

## Реализованный MVP и приёмка
Offline CLI частично покрывает R01–R07 через обезличенные typed facts, выполняет R08 и R09
без сетевых запросов и отражает unavailable capabilities для R10. Сбор сведений,
вычисление effective firewall rules из raw exports и проверка реального provider
не реализованы. Boolean claims требуют самостоятельного подтверждения владельцем. Egress, порядок
firewall rules, token expiry timestamps, TLS chain details и полный DNS inventory
не анализируются этим MVP; сохраняются как private evidence для подтверждения claims.

Статусы: pass/fail/unknown/not_run. Missing/stale/unsupported/error → unknown;
отсутствие проверки или explicit not_run → not_run. Known unsafe fact → fail даже
при частичной неполноте. Не предусмотрен not_applicable: исключённый check остаётся
not_run, чтобы отсутствие покрытия было видно. Future timestamps → unknown.
Для всех 10 правил проверяются safe/unsafe/missing/stale/unsupported/error случаи,
policy boundaries, CLI/installation и безопасная обработка некорректного ввода.
RPO/RTO и остальные пороги явно задаёт владелец. Никакая synthetic проверка не
подтверждает защиту реальной инфраструктуры. Реальные provider checks не выполнены.

Выпуск prerelease допустим после доступных локальных тестов и CI; стабильный релиз
требует отдельного разрешённого стенда. Commit/push/PR/merge/release разрешены текущим
заданием; сканирование произвольных адресов, реальные credentials и платные ресурсы запрещены.
