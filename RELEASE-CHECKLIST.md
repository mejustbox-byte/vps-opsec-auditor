# Контроль выпуска

## До tag
- Документы и интерфейс на русском; кодовые имена/ключи/пути/ID сохранены.
- Версия pyproject.toml, __version__, примеры, файлы wheel/source и workflows согласованы.
- Setup без сохранённого venv, тесты/схема/ссылки, сборка, gitleaks и PR/main CI успешны.
- Данные только синтетические; реальные непроверенные стенды явно перечислены.
- PR проверен и слит; checkout синхронизирован с финальным main без посторонних изменений.

## Tag и существующий draft
Для VPS новый tag — v0.1.0a2, пакет — 0.1.0a2. Зафиксируйте точный SHA main;
убедитесь в успехе CI этого SHA. Создайте новый annotated tag один раз и push.
Существующий v0.1.0a1 не меняется и старый release не удаляется.
Создайте отдельный prerelease draft с русскими notes и target_commitish=этот SHA.
Получите его ID из API. Release workflow получает commit и release_id этого draft:

```sh
gh workflow run release.yml --repo mejustbox-byte/vps-opsec-auditor --ref main -f commit=ТОЧНЫЙ_SHA -f release_id=ID_DRAFT
```

Значения-заполнители не являются рабочими SHA/ID. Workflow проверяет tag/commit/main,
собирает и тестирует именно tag. Только publish имеет contents:write и штатный
GITHUB_TOKEN; новых credentials нет. Не создавать второй release для того же tag.

## После публикации
API: draft=false, prerelease=true, tag/target_commitish правильные; ровно три непустых
uploaded assets: wheel, source archive, SHA256SUMS. Скачайте их после публикации,
выполните sha256sum -c SHA256SUMS, проверьте содержимое относительно tag и чистую
установку скачанного wheel с синтетическим smoke. Ещё раз проверьте старый и новый
tag. Notes содержат реальные PR/commit/CI/workflow ссылки и НЕ ВЫПОЛНЕНО.
Пустой draft, отдельная ветка с архивом и только успешный build не являются выпуском.
При ошибке сохранить данные причины и продолжить штатным способом, не обходить auth.
