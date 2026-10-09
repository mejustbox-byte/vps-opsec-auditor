# Матрица реализованных правил

Результаты относятся к переданным свидетельствам. Реальные провайдерские и лабораторные
проверки **не выполнены**. Для каждой строки есть синтетические положительные,
отрицательные, пропущенные, устаревшие, неподдерживаемые и ошибочные случаи.
Неизвестный факт даёт unknown; известный небезопасный факт — fail даже при неполноте.

| ID / требование | Предикат pass по актуальным observed facts | Риск (severity) | Ограничение свидетельства |
| --- | --- | --- | --- |
| NET-01 / R01 | unexpected_ports=0; public_admin_panel=false | high | Классификацию портов/панелей передаёт владелец; сканирования нет |
| SSH-01 / R02 | password_auth=false; root_login=false; weak_algorithms=false | high | Политику входа нельзя выводить только из баннера |
| FW-01 / R03 | attached=true; default_deny_v4=true; world_open_admin=false; явный ipv6_enabled и default_deny_v6=true при включённом IPv6 | critical | Владелец нормализует эффективные правила/привязки; анализатора исходных правил нет |
| IAM-01 / R04 | least_privilege=true; tokens_expire=true; rotation_policy=true; shared_tokens=false | critical | Обобщённые утверждения об инвентаризации; секреты/API-права не проверяются |
| MFA-01 / R04 | all_admins_mfa=true; recovery_isolated=true | critical | API или свидетельство владельца; unsupported даёт unknown |
| META-01 / R05 | user_data_contains_secrets=false; metadata_protected=true | high | Нужны разрешённые внутренние данные; внешнего предположения недостаточно |
| DNS-01 / R06 | records_match_inventory=true; dangling_records=false | high | Сверку DNS передаёт владелец; захват ресурсов не предпринимается |
| TLS-01 / R06 | identity_valid=true; chain_valid=true; weak_protocols=false; days_remaining >= min_tls_days | high | Владелец фиксирует хранилище доверенных сертификатов/SNI/часы; соединения нет |
| BAK-01 / R07 | scheduled=true; encrypted=true; isolated=true; immutable=true; retention_days >= min_retention_days | critical | Наличие копии не доказывает восстановление |
| REC-01 / R07 | restore_tested=true; restore_success=true; rpo_minutes <= max_rpo_minutes; rto_minutes <= max_rto_minutes | critical | Нужны данные восстановления владельцем на одноразовом стенде |

Риск (severity) — оцениваемый риск, а не число доказанных уязвимостей. Для pass нужны все
применимые факты и актуальность. Явно выключенный IPv6 принимается как утверждение,
но его истинность аудитор не доказывает. Частные ссылки/время/источник сохраняются
вне git и проверяются до принятия операционных решений.

Корневой самостоятельный раздел: [CORE-CONTRACT.md](../CORE-CONTRACT.md).
