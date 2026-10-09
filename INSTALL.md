# Установка, проверка и удаление

## Поддерживаемые среды
Подтверждены Python 3.12 и Linux/POSIX. Требуется Python >=3.12, venv и pip.
Прямой запуск на Windows не поддерживается: код защиты файлов использует POSIX
O_NONBLOCK/O_EXCL. macOS, Python 3.13+ и WSL2 независимо **НЕ ПРОВЕРЕНЫ**.
В WSL2 можно следовать POSIX-командам, но это не заявление о проверке WSL2.

## Готовый wheel
Скачайте wheel, исходный архив и SHA256SUMS одного выпуска в одну новую папку:

```sh
sha256sum -c SHA256SUMS
python3 -m venv .venv
.venv/bin/python -m pip install --no-index --no-deps vps_opsec_auditor-0.1.0a2-py3-none-any.whl
.venv/bin/python -m pip check
.venv/bin/vps-opsec-auditor --version
tar -xzf vps_opsec_auditor-0.1.0a2.tar.gz
.venv/bin/vps-opsec-auditor vps_opsec_auditor-0.1.0a2/fixtures/safe.json --at 2026-10-09T01:00:00Z --format json --fail-on incomplete
```

Ожидаются 0.1.0a2, код 0, synthetic=true и 10 pass. Дата нужна только для повторения
синтетики. Для реальных сведений используйте текущие часы. Только wheel не включает
fixtures; поэтому пример берёт файл из распакованного исходного архива.

## Исходный архив или checkout
Войдите в каталог с pyproject.toml. Сеть нужна только для скачивания закреплённого
setuptools с PyPI; сам аудитор сети не использует:

```sh
python3 -m venv .venv
.venv/bin/python -m pip install --require-hashes -r requirements-build.txt
.venv/bin/python -m pip install --no-build-isolation --no-deps .
.venv/bin/python -m pip check
```

`bash scripts/setup_environment.sh` дополнительно выполняет все проверки.
Без сети можно заранее получить проверенный wheel setuptools и установить его
через --no-index --find-links с тем же requirements-build.txt/--require-hashes.
Проверку TLS/хешей не отключать. Для дистрибутива продукта runtime-зависимостей нет.

## Обновление и удаление
Проверяйте SHA256SUMS новой версии; лучше создать новое venv и проверить отчёт
до замены используемой версии. Не объединяйте частные отчёты с исходниками.
Удаление пакета: `.venv/bin/python -m pip uninstall -y vps-opsec-auditor`.
Удаление только созданного вами venv: после проверки текущего каталога `rm -rf -- .venv`.
Частные входные данные и отчёты удаляются отдельно по политике хранения владельца;
ни установщик, ни uninstall их не очищают. [Эксплуатация](RUNBOOK.md).
