"""Автономный CLI: ограниченный ввод, безопасные ошибки, создание только новых файлов."""
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
    # FIFO/устройство может блокировать исполнение или давать бесконечные данные.
    fd = os.open(path, os.O_RDONLY | os.O_NONBLOCK)
    try:
        if not stat.S_ISREG(os.fstat(fd).st_mode):
            raise InputError('вход должен быть обычным файлом')
        with os.fdopen(fd, 'rb', closefd=False) as handle:
            return handle.read(MAX_BYTES + 1)
    finally:
        os.close(fd)


def write_output(path, content):
    # Нет перезаписи входа или целей symlink; права файла частные.
    fd = os.open(path, os.O_WRONLY | os.O_CREAT | os.O_EXCL, 0o600)
    try:
        with os.fdopen(fd, 'w', encoding='utf-8', closefd=False) as handle:
            handle.write(content)
    except BaseException:
        Path(path).unlink(missing_ok=True)
        raise
    finally:
        os.close(fd)


class RussianArgumentParser(argparse.ArgumentParser):
    def format_usage(self):
        return super().format_usage().replace('usage:', 'Использование:', 1)

    def format_help(self):
        return (super().format_help().replace('usage:', 'Использование:', 1)
                .replace('positional arguments:', 'Позиционные аргументы:')
                .replace('options:', 'Параметры:'))

    def error(self, message):
        self.print_usage(sys.stderr)
        self.exit(2, 'ошибка: неверные аргументы; используйте --help\n')


def main(argv=None):
    parser = RussianArgumentParser(prog='vps-opsec-auditor', add_help=False, description='Автономный аудитор свидетельств о VPS только на чтение; сеть и API провайдера не используются.')
    parser.add_argument('-h', '--help', action='help', help='показать справку и завершить работу')
    parser.add_argument('--version', action='version', version=__version__, help='показать версию и завершить работу')
    parser.add_argument('input', help='Обезличенный файл свидетельств JSON (до 1 МиБ)')
    parser.add_argument('--format', choices=['json', 'markdown'], default='markdown', help='формат отчёта')
    parser.add_argument('--output', help='Новый частный выходной файл; существующие пути не перезаписываются')
    parser.add_argument('--at', help='Время оценки с часовым поясом для воспроизводимого аудита')
    parser.add_argument('--fail-on', choices=['none', 'fail', 'incomplete'], default='none',
                        help='Код 1 при fail либо fail/unknown/not_run; корректный отчёт по умолчанию даёт 0')
    args = parser.parse_args(argv)
    try:
        data = load(read_input(args.input))
        report = audit(data, timestamp(args.at) if args.at else None)
        content = json.dumps(report, indent=2, ensure_ascii=False, allow_nan=False) + '\n' if args.format == 'json' else markdown(report) + '\n'
        if args.output:
            write_output(args.output, content)
        else:
            sys.stdout.write(content)
        summary = report['summary']
        return int((args.fail_on != 'none' and summary['fail'] > 0) or
                   (args.fail_on == 'incomplete' and (summary['unknown'] + summary['not_run']) > 0))
    except (InputError, OSError, UnicodeError):
        # Пути и фрагменты ввода могут содержать секреты: не повторяем их.
        sys.stderr.write('ошибка: неверный ввод, время оценки или недоступный/существующий выходной файл; см. схему и --help\n')
        return 2


if __name__ == '__main__':
    raise SystemExit(main())
