"""Проверка лицензий, метаданных и документации в готовых пакетах."""
from email.parser import BytesParser
from pathlib import Path
import tarfile
import tomllib
import zipfile

ROOT = Path(__file__).resolve().parents[1]
version = tomllib.loads((ROOT / 'pyproject.toml').read_text())['project']['version']
name = f'vps_opsec_auditor-{version}'
with zipfile.ZipFile(ROOT / 'dist' / f'{name}-py3-none-any.whl') as wheel:
    metadata = BytesParser().parsebytes(wheel.read(f'{name}.dist-info/METADATA'))
    assert metadata['Version'] == version
    assert metadata['License-Expression'] == 'MIT'
    assert set(metadata.get_all('License-File', [])) == {'LICENSE', 'LICENSE.ru.md'}
    for license_file in ('LICENSE', 'LICENSE.ru.md'):
        assert wheel.read(f'{name}.dist-info/licenses/{license_file}') == (ROOT / license_file).read_bytes()
with tarfile.open(ROOT / 'dist' / f'{name}.tar.gz') as source:
    for path in [ROOT / 'LICENSE', *ROOT.glob('*.md')]:
        member = source.extractfile(f'{name}/{path.name}')
        assert member is not None and member.read() == path.read_bytes(), path.name
print('УСПЕХ: MIT и обе лицензии включены в wheel/source; корневая документация в исходном архиве')
