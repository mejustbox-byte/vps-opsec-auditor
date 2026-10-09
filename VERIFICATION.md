# Проверки и пределы доказательства

## Подтверждённая история
[PR #1](https://github.com/mejustbox-byte/vps-opsec-auditor/pull/1) слит в
`e5c504bfa6349c6e51cb00a87c963aea9e02c8e1`;
[PR #2](https://github.com/mejustbox-byte/vps-opsec-auditor/pull/2) — в
`069c2e93fc85fb45bc997f95e00730cef036a1c3` (tag v0.1.0a1).
[CI продукта](https://github.com/mejustbox-byte/vps-opsec-auditor/actions/runs/37923861951)
успешен. [PR #3](https://github.com/mejustbox-byte/vps-opsec-auditor/pull/3) — workflow,
merge `170d549fbacee01af090a0dfa185be21d291c1cb`.
[CI main](https://github.com/mejustbox-byte/vps-opsec-auditor/actions/runs/37925368402)
и [выпуск](https://github.com/mejustbox-byte/vps-opsec-auditor/actions/runs/37925383868)
успешны. Публичные assets 0.1.0a1 скачаны: обе SHA256 верны, содержимое совпало со
сборкой tag, wheel установлен и оценил синтетический пример. Gitleaks утечек не нашёл.

## 0.1.0a2: локальная проверка и приёмка
19 тестов с подслучаями правил проходят. Проверены русская справка/отчёт/ошибки,
версии и схемы, стабильные ключи, отсутствие раскрытия некорректных аргументов.
Выполнены setup, документы/ссылки/публичные данные, повторная сборка с совпадением
контрольных сумм. PR/main CI, выпуск и проверка публичных assets a2 подтверждаются
после фактического выполнения в notes и итоговом отчёте; заранее успех не заявляется.

Повторяемые команды: `bash scripts/setup_environment.sh`,
`PYTHONPATH=src python3 -m unittest discover -s tests -v`,
`python3 scripts/check_docs.py`, `python3 scripts/check_public_data.py`,
`.venv/bin/python scripts/build_release.py`,
`.venv/bin/python scripts/check_packages.py` (после сборки).
Тесты могут завершиться ошибкой; нулевой набор не считается проверкой.

## НЕ ВЫПОЛНЕНО
Реальные порты/панели/SSH; cloud firewall/IPv6; IAM/API tokens/MFA/recovery;
cloud-init/metadata; DNS/TLS; backup/restore/RPO/RTO. Причина — нет отдельно разрешённого
стенда, реальные учётные данные запрещены задачей. Также не выполнены macOS/Windows/
WSL2 и независимые проверки Python 3.13+. Прямой Windows не поддерживается.
Синтетика, существование asset или код 0 не доказывают защиту провайдера.
[План проверки](LOCAL-PC.md), [лабораторный протокол](docs/lab.md).
