# Модель угроз

## Активы и границы доверия
Активы: доступ к VPS и панели, provider account, DNS, токены, user-data,
резервные копии, recovery channels, доказательства аудита.
Границы: оператор → runner → недоверенная сеть/endpoints; runner → provider API;
provider control plane → guest metadata; backup storage → restore lab;
private evidence → redacted public report. Каждый ответ и импорт — недоверенный ввод.

| Угроза | Последствие | Контроль / предел доказательства |
| --- | --- | --- |
| Открытая панель или SSH во всех сетях | Захват доступа | Ports/panel/SSH + firewall IPv4/IPv6; без попыток входа |
| Ошибка IPv6 или unattached firewall | Обход ingress policy | Сопоставление A/AAAA, attachments и effective rules |
| Кража provider token/аккаунта | Изменение VPS, DNS и backup | Least privilege, expiry, MFA, отдельный recovery; MFA часто manual |
| Секреты в cloud-init/metadata | Lateral movement | Обезличенное свидетельство и отдельный metadata lab; не внешняя догадка |
| Dangling DNS / TLS mismatch | Перехват трафика | Проверка владения и цепочки; без регистрации чужого ресурса |
| Удаление backup вместе с аккаунтом | Невосстановимость | Изоляция, retention, immutability, измеренный restore |
| SSRF, DNS rebinding, redirects | Аудит вне scope | Проверка каждого назначения, запрет переходов, request budget |
| Вредоносный API export/баннер | Инъекция в отчёт или DoS | Размеры, строгая схема, escaped output, без shell interpolation |
| Утечка через git/log/artifact | Публичные секреты | Synthetic-only CI, минимизация, ручной review и secret scan перед push |
| Устаревшее/частичное свидетельство | Ложная уверенность | Timestamp, источник, confidence, unknown/not_run, coverage gaps |

## Допущения и исключения
Оператор подтверждает владение endpoints; provider API и экспорт не считаются
полным источником истины. Скомпрометированный control plane может лгать.
Не охватываются kernel hardening, локальный privilege escalation, malware detection,
DDoS нагрузочное тестирование, эксплуатация уязвимостей и социнженерия.
Read-only auditor не гарантирует непрерывную защиту после момента наблюдения.
Критические пути: takeover provider account → удаление backup; IPv6 bypass →
панель; SSRF в auditor → metadata credentials. Они требуют отдельных negative lab cases.

## Контроли реализованного offline MVP
Сеть, API и shell отсутствуют; SSRF/rebinding не могут возникнуть внутри текущего CLI.
Вход ограничен 1 MiB и regular files, схема закрыта, строки вывода ограничены aliases,
source enums и timestamps. Duplicate keys/NaN/типовые coercions запрещены.
Output не перезаписывает существующие файлы и создаётся с 0600. Diagnostics не
печатают значения ввода. No-network и filesystem safety проверены тестами.
False evidence остаётся угрозой: операторские утверждения не аутентифицированы.
Source/synthetic flag не заменяют provenance; сознательная ложь может дать pass.
Идентификаторы aliases могут быть чувствительными: не публиковать real reports.
Не защищаем от скомпрометированного локального пользователя/интерпретатора или диска.
