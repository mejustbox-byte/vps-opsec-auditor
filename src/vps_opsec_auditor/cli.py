"""Offline CLI with bounded input, safe errors and exclusive output creation."""
import argparse
import json
import os
import stat
import sys
from pathlib import Path
from . import __version__
from .audit import audit, markdown
from .validation import InputError, MAX_BYTES, load, timestamp


def read_input(path):
    # Opening an attacker-controlled FIFO/device can block or read indefinitely.
    fd = os.open(path, os.O_RDONLY | os.O_NONBLOCK)
    try:
        if not stat.S_ISREG(os.fstat(fd).st_mode):
            raise InputError('input must be a regular file')
        with os.fdopen(fd, 'rb', closefd=False) as handle:
            return handle.read(MAX_BYTES + 1)
    finally:
        os.close(fd)


def write_output(path, content):
    # No overwrites, including input files and symlink destinations. Private permissions.
    fd = os.open(path, os.O_WRONLY | os.O_CREAT | os.O_EXCL, 0o600)
    try:
        with os.fdopen(fd, 'w', encoding='utf-8', closefd=False) as handle:
            handle.write(content)
    except BaseException:
        Path(path).unlink(missing_ok=True)
        raise
    finally:
        os.close(fd)


def main(argv=None):
    parser = argparse.ArgumentParser(description='Offline read-only VPS evidence auditor; never scans or calls provider APIs.')
    parser.add_argument('--version', action='version', version=__version__)
    parser.add_argument('input', help='Sanitized JSON evidence file (maximum 1 MiB)')
    parser.add_argument('--format', choices=['json', 'markdown'], default='markdown')
    parser.add_argument('--output', help='New private output file; existing paths are never overwritten')
    parser.add_argument('--at', help='Timezone-aware evaluation time for reproducible audits')
    parser.add_argument('--fail-on', choices=['none', 'fail', 'incomplete'], default='none',
                        help='Exit 1 on failures, or on failures/unknown/not_run; default exits 0 for valid reports')
    args = parser.parse_args(argv)
    try:
        data = load(read_input(args.input))
        report = audit(data, timestamp(args.at) if args.at else None)
        content = json.dumps(report, indent=2, allow_nan=False) + '\n' if args.format == 'json' else markdown(report) + '\n'
        if args.output:
            write_output(args.output, content)
        else:
            sys.stdout.write(content)
        summary = report['summary']
        return int((args.fail_on != 'none' and summary['fail'] > 0) or
                   (args.fail_on == 'incomplete' and (summary['unknown'] + summary['not_run']) > 0))
    except (InputError, OSError, UnicodeError):
        # Paths and parser excerpts may contain secrets. Never echo them.
        sys.stderr.write('error: invalid input, evaluation time, or inaccessible/existing output; see input schema and CLI help\n')
        return 2


if __name__ == '__main__':
    raise SystemExit(main())
