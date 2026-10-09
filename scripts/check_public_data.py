"""Targeted public-source guard, not a comprehensive secret-detection guarantee."""
import ipaddress
from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[1]
PATTERNS = [re.compile(r'-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----'),
            re.compile(r'\bgh[pousr]_[A-Za-z0-9]{30,}\b'),
            re.compile(r'\bgithub_pat_[A-Za-z0-9_]{30,}\b'),
            re.compile(r'\b(?:AKIA|ASIA)[A-Z0-9]{16}\b'),
            re.compile(r'(?i)(?:api[_-]?key|password|secret|token)\s*[:=]\s*["\x27][A-Za-z0-9/+_-]{24,}["\x27]')]
ALLOWED_V4 = [ipaddress.ip_network(n) for n in ['192.0.2.0/24', '198.51.100.0/24', '203.0.113.0/24', '127.0.0.0/8']]


def main():
    paths = [ROOT / p for p in ['README.md', 'SECURITY.md', 'LICENSE', 'pyproject.toml', 'requirements-build.txt']]
    for directory in ['src', 'tests', 'docs', 'schemas', 'fixtures', 'examples', 'scripts', '.github']:
        paths += [p for p in (ROOT / directory).rglob('*') if p.is_file()
                  and '__pycache__' not in p.parts and not any(part.endswith('.egg-info') for part in p.parts)]
    failures = []
    for path in paths:
        content = path.read_text()
        if any(pattern.search(content) for pattern in PATTERNS):
            failures.append(f'{path.relative_to(ROOT)}: possible credential')
        for match in re.finditer(r'(?<![\w.])(?:\d{1,3}\.){3}\d{1,3}(?![\w.])', content):
            try:
                addr = ipaddress.ip_address(match.group())
            except ValueError:
                continue
            if not any(addr in network for network in ALLOWED_V4):
                failures.append(f'{path.relative_to(ROOT)}: non-documentation IPv4')
    if failures:
        raise SystemExit('FAIL:\n' + '\n'.join(sorted(set(failures))))
    print(f'PASS: targeted public-data/credential patterns across {len(paths)} files; manual review still required')


if __name__ == '__main__':
    main()
