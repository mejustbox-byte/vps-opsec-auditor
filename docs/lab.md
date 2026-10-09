# Лаборатория

## Сейчас
Только файлы synthetic fixtures, без сетевых probes и без cloud resources.
Адреса примеров: documentation ranges 192.0.2.0/24, 198.51.100.0/24,
203.0.113.0/24, 2001:db8::/32; домены .invalid. Эти адреса не сканировать.
Fixture — пример отчётного контракта, не fake pass реального провайдера.

## Будущая локальная лаборатория
Отдельные одноразовые процессы/контейнеры без cloud credentials, host mounts,
privileged mode и доступа к реальному metadata. Порты только loopback, изолированная
сеть, mock API для IAM/MFA/firewall/backup и mock metadata без реальных токенов.
Case manifest фиксирует expected outcome, разрешённый endpoint, методы и budget.
TLS использует ephemeral test CA; host trust store не изменяется.
DNS/IPv6 cases тестируются в изоляции; отсутствие IPv6 capability → skipped с причиной.
Cleanup удаляет только ресурсы стенда по manifest и проверяет отсутствие остаточных
процессов, портов, temporary credentials и artifacts. Стенд сейчас не создавался.

## Будущий provider стенд — отдельный gate
Требуются явное разрешение владельца и отдельный одноразовый проект/аккаунт,
доказанные read-only credentials, точный scope и endpoint allowlist, бюджет,
RPO/RTO, cleanup owner и срок жизни. В этой задаче платные ресурсы запрещены.
Даже бесплатный provider стенд сейчас не создаётся. Provision/restore/cleanup
выполняется отдельным процессом владельца, не аудитором.
Фиксируются provider/version, API capability, IPv4/IPv6, ожидаемые результаты,
request IDs в private evidence и дата; в публичный git — только синтетические аналоги.
Без такого стенда все реальные проверки провайдера остаются unverified.

## Реальный лабораторный протокол для offline MVP
1. Владелец задаёт RPO/RTO, TLS/backup thresholds, scope и expiry для отдельного
   одноразового стенда. Никакие платные ресурсы в этой задаче не создаются.
2. Независимо собирает inventory/ports/panels/SSH policy; effective firewall rules
   и attachments для IPv4/IPv6; IAM/MFA/recovery; cloud-init/metadata; DNS/TLS;
   backup policy и результаты восстановления. Без brute force и exploit.
3. Хранит raw evidence вне git, обезличивает до schema v1 facts и aliases;
   source=lab/provider_export/operator, synthetic=false, честные timestamps.
4. Запускает установленный CLI с текущим временем и --fail-on incomplete,
   сверяет каждое правило с expected outcome. Проверяет safe и unsafe configs,
   expired evidence, unsupported MFA API, IPv6 gap и backup-with-failed-restore.
5. Сохраняет private evidence references и coverage gaps. Публикует только synthetic
   аналоги. Владелец выполняет cleanup по manifest и подтверждает отсутствие остатков.

Не выполнены: live public-port/SSH/TLS/DNS observations, provider IAM/API/MFA,
cloud firewall/IPv6, guest cloud-init/metadata, backup/restore/RPO/RTO.
Причина: отдельный разрешённый реальный стенд и реальные credentials не предоставлены;
использование реальных credentials запрещено текущим заданием. Offline tests этого не заменяют.
