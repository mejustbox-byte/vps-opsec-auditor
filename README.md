# vps-opsec-auditor

Аудитор обезличенных свидетельств о внешней поверхности VPS и контрольной плоскости
провайдера. Работает **автономно, только на чтение**; версия пакета **0.1.0a2**.
Реальные лабораторные проверки провайдера и сети **не выполнены**. Сетевого сканера,
клиента API и автоматического исправления настроек нет. Статус `pass` относится
к переданным свидетельствам, а не подтверждает защиту реальной инфраструктуры.

## Установка: Python 3.12+ и POSIX

Скачайте wheel, исходный архив и SHA256SUMS из одного выпуска в одну папку:

```sh
sha256sum -c SHA256SUMS
python3 -m venv .venv
.venv/bin/python -m pip install --no-index --no-deps vps_opsec_auditor-0.1.0a2-py3-none-any.whl
.venv/bin/vps-opsec-auditor --version
```

Полная проверка SHA256SUMS требует оба архива. При скачивании только wheel проверьте
соответствующую строку. Контрольные суммы обнаруживают повреждение, но не удостоверяют
личность издателя: получайте файлы через доверенный канал выпуска.
Активация окружения необязательна: исполняемый файл находится внутри `.venv`.

Из checkout команда `bash scripts/setup_environment.sh` выполняет установку и
проверки без сохранённого виртуального окружения. Только установка:

```sh
python3 -m venv .venv
.venv/bin/python -m pip install --require-hashes -r requirements-build.txt
.venv/bin/python -m pip install --no-build-isolation --no-deps .
```

## Запуск синтетических примеров

Из checkout:

```sh
.venv/bin/vps-opsec-auditor fixtures/safe.json --at 2026-10-09T01:00:00Z --format json
.venv/bin/vps-opsec-auditor fixtures/unsafe.json --at 2026-10-09T01:00:00Z --format markdown
.venv/bin/vps-opsec-auditor fixtures/missing.json --at 2026-10-09T01:00:00Z --fail-on incomplete
```

Последняя команда ожидаемо возвращает код **1**: ни одна проверка не запускалась.
Время примеров зафиксировано; без `--at` данные со временем устаревают (`unknown`).
Для wheel и исходного архива, скачанных отдельно, сначала распакуйте архив:
`tar -xzf vps_opsec_auditor-0.1.0a2.tar.gz`; передайте путь вида
`vps_opsec_auditor-0.1.0a2/fixtures/safe.json` вместо `fixtures/safe.json`.

Реальный аудит использует текущее время и отдельно хранимые обезличенные сведения.
CLI не требует и не принимает учётные данные или IP цели. `--output /private/new-report.json`
создаёт только новый файл с правами 0600. Не сохраняйте реальные данные и отчёты
в этом публичном checkout.

Статусы: **pass** — правило выполнено по данным; **fail** — выявлено небезопасное
свидетельство; **unknown** — данных недостаточно, они устарели, источник не поддерживается
или сбор завершился ошибкой; **not_run** — сбор не выполнялся.
Корректный отчёт по умолчанию даёт код 0; `--fail-on fail` даёт 1 при `fail`,
`--fail-on incomplete` также учитывает `unknown/not_run`. Неверный ввод, время или
операции с файлами дают 2 без раскрытия содержимого входа.

Десять правил охватывают публичные порты/панели, SSH, firewall/IPv6, IAM/токены,
MFA/восстановление доступа, cloud-init/metadata, DNS, TLS, резервные копии и
измеренные цели восстановления. Схема принимает типизированные обезличенные факты,
псевдонимы и ссылки на свидетельства, а не исходные выгрузки, секреты или IP.
См. [входные данные](docs/input.md), [дизайн и план MVP](docs/README.md),
[лабораторный протокол](docs/lab.md), [границы безопасности](SECURITY.md),
[заметки к выпуску](docs/release-notes.md), [участие](CONTRIBUTING.md)
и [историю изменений](CHANGELOG.md).

## Разработка и проверки

```sh
PYTHONPATH=src python3 -m unittest discover -s tests -v
python3 scripts/check_docs.py
python3 scripts/check_public_data.py
.venv/bin/python scripts/build_release.py
.venv/bin/python scripts/check_packages.py
```

Тесты автономные, данные синтетические. Инструмент сборки закреплён версией и хешем;
wheel, исходный архив и контрольные суммы создаются в `dist`.
CI выполняет тесты, проверку секретов и пробный запуск после чистой установки wheel.
Лицензия: MIT.

## Полный индекс документов

| Раздел | Самостоятельный документ | Подробности, сохранённые в docs |
| --- | --- | --- |
| Назначение, компоненты и данные | [ARCHITECTURE](ARCHITECTURE.md) | [Архитектура](docs/architecture.md) |
| Выбор стека и закрепление | [TECH-STACK](TECH-STACK.md) | [ADR](docs/adr/0001-stack.md) |
| Установка wheel/source, OS и удаление | [INSTALL](INSTALL.md) | [Среда](docs/environment.md) |
| Разработка и ревью | [CONTRIBUTING](CONTRIBUTING.md) | [Описание PR](docs/pull-request.md) |
| Этапы и приёмка | [ROADMAP](ROADMAP.md) | [Требования](docs/requirements.md), [MVP](docs/mvp.md) |
| Безопасность и угрозы | [SECURITY](SECURITY.md), [THREAT-MODEL](THREAT-MODEL.md) | [Угрозы](docs/threat-model.md) |
| Реальные CLI/JSON/Python контракты | [CORE-CONTRACT](CORE-CONTRACT.md) | [Вход](docs/input.md), [Матрица](docs/checks.md) |
| Эксплуатация и частные отчёты | [RUNBOOK](RUNBOOK.md) | [Контракт](docs/input.md) |
| Cloud, сохранение и восстановление | [CLOUD-DEVELOPMENT](CLOUD-DEVELOPMENT.md) | [Среда](docs/environment.md) |
| Отдельная локальная лаборатория | [LOCAL-PC](LOCAL-PC.md) | [Реальный протокол](docs/lab.md) |
| Доказательства и НЕ ВЫПОЛНЕНО | [VERIFICATION](VERIFICATION.md) | [Ограничения](docs/release-notes.md) |
| Tag, release, assets и checksum | [RELEASE-CHECKLIST](RELEASE-CHECKLIST.md) | [Среда](docs/environment.md) |
| Notes и история | [RELEASE-NOTES](RELEASE-NOTES.md), [CHANGELOG](CHANGELOG.md) | [Notes](docs/release-notes.md) |

Смысловое покрытие приведено к набору прежних проектов из задания пользователя.
Функции, результаты и стек других проектов не приписываются этому автономному MVP.

### Дополнительные документы безопасности и лицензии

[Свидетельства и срок хранения](EVIDENCE-POLICY.md), [цепочка поставок](SUPPLY-CHAIN.md),
[security-проверки](SECURITY-TESTING.md), [правила следующих циклов](AGENTS.md),
[стандартный MIT](LICENSE), [русский перевод](LICENSE.ru.md).
