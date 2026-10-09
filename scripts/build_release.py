"""Build the pinned wheel, deterministic public source bundle and checksums."""
import gzip
import hashlib
import os
from pathlib import Path
import tarfile
import setuptools
from setuptools.build_meta import build_wheel

ROOT = Path(__file__).resolve().parents[1]
os.chdir(ROOT)
if setuptools.__version__ != '80.9.0':
    raise SystemExit('Install requirements-build.txt with --require-hashes first')
os.environ['SOURCE_DATE_EPOCH'] = '1791504000'
DIST = ROOT / 'dist'
DIST.mkdir(exist_ok=True)
wheel = build_wheel(str(DIST))
version = '0.1.0a1'
name = f'vps_opsec_auditor-{version}'
archive = DIST / f'{name}.tar.gz'
paths = [ROOT / p for p in ['README.md', 'LICENSE', 'pyproject.toml', 'requirements-build.txt', '.gitignore']]
for directory in ['src', 'tests', 'docs', 'schemas', 'fixtures', 'examples', 'scripts', '.github']:
    paths += [p for p in (ROOT / directory).rglob('*') if p.is_file()
              and '__pycache__' not in p.parts and not any(part.endswith('.egg-info') for part in p.parts)
              and p.suffix != '.pyc']
with archive.open('wb') as raw:
    with gzip.GzipFile(fileobj=raw, mode='wb', mtime=0, filename='') as zipped:
        with tarfile.open(fileobj=zipped, mode='w', format=tarfile.PAX_FORMAT) as tar:
            for path in sorted(paths):
                info = tar.gettarinfo(str(path), arcname=f'{name}/{path.relative_to(ROOT).as_posix()}')
                info.uid = info.gid = info.mtime = 0
                info.uname = info.gname = ''
                info.mode = 0o644
                with path.open('rb') as handle:
                    tar.addfile(info, handle)
artifacts = [DIST / wheel, archive]
(DIST / 'SHA256SUMS').write_text(''.join(f'{hashlib.sha256(p.read_bytes()).hexdigest()}  {p.name}\n' for p in artifacts))
print('Built wheel, source bundle and SHA256SUMS; no infrastructure validation claimed.')
