import copy
from datetime import datetime, timezone
import json
import os
import re
import tomllib
from pathlib import Path
import socket
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch

from vps_opsec_auditor.audit import RULES, audit
from vps_opsec_auditor.validation import InputError, MAX_BYTES, load

ROOT = Path(__file__).resolve().parents[1]
NOW = datetime(2026, 10, 9, 1, tzinfo=timezone.utc)


def fixture(name='safe'):
    return json.loads((ROOT / f'fixtures/{name}.json').read_text())


def checked(data):
    return load(json.dumps(data).encode())


class RuleTests(unittest.TestCase):
    def test_every_rule_safe_and_unsafe(self):
        for name, expected in [('safe', 'pass'), ('unsafe', 'fail')]:
            report = audit(checked(fixture(name)), NOW)
            self.assertEqual(len(report['findings']), 10)
            for finding in report['findings']:
                with self.subTest(name=name, check=finding['check_id']):
                    self.assertEqual(finding['status'], expected)
                    self.assertTrue(finding['remediation'])
                    self.assertTrue(finding['evidence']['facts'])
                    self.assertEqual(finding['confidence'], 'synthetic')

    def test_each_boolean_violation_fails(self):
        safe = fixture()
        for cid, item in safe['checks'].items():
            for key, value in item['facts'].items():
                if type(value) is not bool or key == 'ipv6_enabled':
                    continue
                with self.subTest(check=cid, fact=key):
                    data = copy.deepcopy(safe)
                    data['checks'][cid]['facts'][key] = not value
                    result = audit(checked(data), NOW)
                    finding = next(f for f in result['findings'] if f['check_id'] == cid)
                    self.assertEqual(finding['status'], 'fail')
                    self.assertIn(key, finding['reason'])

    def test_every_rule_missing_stale_future_unsupported_error_not_run(self):
        for cid in RULES:
            for case, expected in [('missing', 'not_run'), ('empty', 'unknown'),
                                   ('stale', 'unknown'), ('future', 'unknown'),
                                   ('unsupported', 'unknown'), ('error', 'unknown'),
                                   ('not_run', 'not_run')]:
                with self.subTest(check=cid, case=case):
                    data = fixture()
                    item = data['checks'][cid]
                    if case == 'missing':
                        del data['checks'][cid]
                    elif case == 'empty':
                        item['facts'] = {}
                    elif case in ['stale', 'future']:
                        item['collected_at'] = '2026-10-07T00:00:00Z' if case == 'stale' else '2026-10-10T00:00:00Z'
                    else:
                        item['state'] = case
                        item['facts'] = {}
                    finding = next(f for f in audit(checked(data), NOW)['findings'] if f['check_id'] == cid)
                    self.assertEqual(finding['status'], expected)

    def test_partial_known_failure_dominates_missing(self):
        data = fixture()
        data['checks']['SSH-01']['facts'] = {'password_auth': True}
        finding = audit(checked(data), NOW)['findings'][1]
        self.assertEqual(finding['status'], 'fail')
        self.assertIn('отсутствует часть', finding['reason'])

    def test_ipv6_gap_and_disabled(self):
        for enabled, deny, expected in [(True, False, 'fail'), (True, None, 'unknown'),
                                        (False, None, 'pass'), (None, True, 'unknown')]:
            with self.subTest(enabled=enabled, deny=deny):
                data = fixture()
                facts = data['checks']['FW-01']['facts']
                for key, value in [('ipv6_enabled', enabled), ('default_deny_v6', deny)]:
                    if value is None:
                        facts.pop(key, None)
                    else:
                        facts[key] = value
                self.assertEqual(audit(checked(data), NOW)['findings'][2]['status'], expected)

    def test_numeric_policy_boundaries(self):
        for cid, fact, limit, unsafe in [('NET-01', 'unexpected_ports', 0, 1),
                                       ('TLS-01', 'days_remaining', 30, 29),
                                       ('BAK-01', 'retention_days', 7, 6),
                                       ('REC-01', 'rpo_minutes', 60, 61),
                                       ('REC-01', 'rto_minutes', 120, 121)]:
            for value, expected in [(limit, 'pass'), (unsafe, 'fail')]:
                with self.subTest(check=cid, fact=fact, value=value):
                    data = fixture()
                    data['checks'][cid]['facts'][fact] = value
                    result = next(f for f in audit(checked(data), NOW)['findings'] if f['check_id'] == cid)
                    self.assertEqual(result['status'], expected)

    def test_age_boundary_and_offset(self):
        data = fixture()
        item = data['checks']['NET-01']
        item['collected_at'] = '2026-10-08T06:00:00+05:00'
        self.assertEqual(audit(checked(data), NOW)['findings'][0]['status'], 'pass')
        item['collected_at'] = '2026-10-08T05:59:59+05:00'
        self.assertEqual(audit(checked(data), NOW)['findings'][0]['status'], 'unknown')

    def test_no_network(self):
        with patch.object(socket, 'socket', side_effect=AssertionError('network forbidden')):
            self.assertEqual(audit(checked(fixture()), NOW)['summary']['pass'], 10)


class ValidationTests(unittest.TestCase):
    def test_invalid_json_duplicate_nonfinite_deep_large(self):
        for raw in [b'{', b'\xff', b'{"schema_version":1,"schema_version":1}',
                    b'{"x":NaN}', b'{"x":Infinity}', b'[' * 2000 + b']' * 2000,
                    b' ' * (MAX_BYTES + 1), b'1', b'null', b'[]']:
            with self.subTest(raw_length=len(raw)):
                with self.assertRaises(InputError):
                    load(raw)

    def test_unknown_field_secret_is_not_echoed(self):
        data = fixture()
        data['token'] = 'SYNTHETIC_SENTINEL_DO_NOT_ECHO'
        with self.assertRaises(InputError) as context:
            checked(data)
        self.assertNotIn(data['token'], str(context.exception))

    def test_wrong_types_ranges_aliases_timestamps_and_sources(self):
        changes = [(['schema_version'], True), (['schema_version'], 2),
                   (['policy', 'max_age_hours'], 0), (['policy', 'max_age_hours'], 1.5),
                   (['policy'], {}), (['target_alias'], 'x\n<script>'),
                   (['checks', 'NET-01', 'facts', 'unexpected_ports'], -1),
                   (['checks', 'NET-01', 'facts', 'unexpected_ports'], True),
                   (['checks', 'NET-01', 'facts', 'public_admin_panel'], 'false'),
                   (['checks', 'NET-01', 'collected_at'], '2026-10-09T00:00:00'),
                   (['checks', 'NET-01', 'collected_at'], '2026-10-09\n00:00:00Z'),
                   (['checks', 'NET-01', 'collected_at'], '2026-02-30T00:00:00Z'),
                   (['checks', 'NET-01', 'collected_at'], '2026-10-09T00:00:00+00:60'),
                   (['checks', 'NET-01', 'source'], 'provider_export'),
                   (['checks', 'NET-01', 'state'], 'pass'),
                   (['checks', 'NET-01', 'state'], 'not_run')]
        for path, value in changes:
            with self.subTest(path=path, value=value):
                data = fixture()
                parent = data
                for key in path[:-1]:
                    parent = parent[key]
                parent[path[-1]] = value
                with self.assertRaises(InputError):
                    checked(data)

    def test_non_synthetic_report_stays_unverified(self):
        data = fixture()
        data['synthetic'] = False
        for item in data['checks'].values():
            item['source'] = 'operator'
        report = audit(checked(data), NOW)
        self.assertEqual(report['findings'][0]['confidence'], 'supplied_evidence')
        self.assertIn('независимо не проверены', report['limitations'][1])

    def test_packaged_schema_matches_public_schema(self):
        self.assertEqual((ROOT / 'schemas/input-v1.schema.json').read_bytes(),
                         (ROOT / 'src/vps_opsec_auditor/input-v1.schema.json').read_bytes())


class CLITests(unittest.TestCase):
    def run_cli(self, *args):
        return subprocess.run([sys.executable, '-m', 'vps_opsec_auditor', *map(str, args)],
                              cwd=ROOT, capture_output=True, text=True, timeout=10)

    def test_json_markdown_and_exit_policies(self):
        common = ['--at', '2026-10-09T01:00:00Z']
        result = self.run_cli('fixtures/safe.json', '--format', 'json', '--fail-on', 'incomplete', *common)
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(json.loads(result.stdout)['summary']['pass'], 10)
        result = self.run_cli('fixtures/unsafe.json', '--fail-on', 'fail', *common)
        self.assertEqual(result.returncode, 1)
        self.assertIn('Синтетические данные: true', result.stdout)
        self.assertIn('Рекомендация:', result.stdout)
        result = self.run_cli('fixtures/missing.json', '--fail-on', 'incomplete', *common)
        self.assertEqual(result.returncode, 1)
        self.assertIn('not_run=10', result.stdout)
        self.assertEqual(self.run_cli('fixtures/unsafe.json', *common).returncode, 0)

    def test_output_no_overwrite_private_mode_symlink_and_input_preserved(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / 'report.json'
            args = ['fixtures/safe.json', '--format', 'json', '--output', path, '--at', '2026-10-09T01:00:00Z']
            self.assertEqual(self.run_cli(*args).returncode, 0)
            self.assertEqual(path.stat().st_mode & 0o777, 0o600)
            original = path.read_bytes()
            self.assertEqual(self.run_cli(*args).returncode, 2)
            self.assertEqual(path.read_bytes(), original)
            link = Path(directory) / 'link'
            link.symlink_to(path)
            self.assertEqual(self.run_cli('fixtures/safe.json', '--output', link).returncode, 2)
            self.assertEqual(path.read_bytes(), original)
            input_path = Path(directory) / 'input.json'
            input_path.write_text(json.dumps(fixture()))
            before = input_path.read_bytes()
            self.assertEqual(self.run_cli(input_path, '--output', input_path).returncode, 2)
            self.assertEqual(input_path.read_bytes(), before)

    def test_safe_errors_empty_stdout_and_no_traceback(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / 'input.json'
            path.write_text('{"token":"SYNTHETIC_SENTINEL_DO_NOT_ECHO"}')
            result = self.run_cli(path)
            self.assertEqual(result.returncode, 2)
            self.assertEqual(result.stdout, '')
            self.assertNotIn('SYNTHETIC_SENTINEL', result.stderr)
            self.assertNotIn('Traceback', result.stderr)
            self.assertEqual(self.run_cli('fixtures/safe.json', '--at', 'bad').returncode, 2)
            self.assertEqual(self.run_cli(Path(directory) / 'missing').returncode, 2)
            self.assertEqual(self.run_cli(directory).returncode, 2)
            fifo = Path(directory) / 'fifo'
            os.mkfifo(fifo)
            self.assertEqual(self.run_cli(fifo).returncode, 2)

    def test_russian_help_report_and_version(self):
        from vps_opsec_auditor import __version__
        help_result = self.run_cli('--help')
        self.assertEqual(help_result.returncode, 0)
        for text in ['Использование:', 'Позиционные аргументы:', 'Параметры:', 'показать справку']:
            self.assertIn(text, help_result.stdout)
        self.assertNotIn('usage:', help_result.stdout)
        report = audit(checked(fixture()), NOW)
        for finding in report['findings']:
            for key in ['title', 'reason', 'remediation']:
                self.assertRegex(finding[key], r'[А-Яа-яЁё]')
        metadata = tomllib.loads((ROOT / 'pyproject.toml').read_text())
        self.assertEqual(metadata['project']['version'], __version__)
        schema = json.loads((ROOT / 'schemas/input-v1.schema.json').read_text())
        self.assertRegex(schema['title'], r'[А-Яа-яЁё]')
        self.assertRegex(schema['description'], r'[А-Яа-яЁё]')

    def test_argument_errors_are_russian_and_do_not_echo_values(self):
        result = self.run_cli('--unknown', 'SYNTHETIC_SENTINEL_DO_NOT_ECHO')
        self.assertEqual(result.returncode, 2)
        self.assertIn('ошибка: неверные аргументы', result.stderr)
        self.assertNotIn('SYNTHETIC_SENTINEL', result.stderr)
        self.assertEqual(result.stdout, '')

    def test_examples_are_reproducible(self):
        result = self.run_cli('fixtures/safe.json', '--at', '2026-10-09T01:00:00Z', '--format', 'json')
        self.assertEqual(result.stdout, (ROOT / 'examples/safe-report.json').read_text())
        result = self.run_cli('fixtures/unsafe.json', '--at', '2026-10-09T01:00:00Z')
        self.assertEqual(result.stdout, (ROOT / 'examples/unsafe-report.md').read_text())


if __name__ == '__main__':
    unittest.main()
