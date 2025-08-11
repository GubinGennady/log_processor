from unittest import mock
import pytest
from src.log_processor.cli import parse_args


class TestCommandLineInterface:
    """Тесты для обработки аргументов командной строки"""

    def test_basic_arguments(self):
        """Тест базовых аргументов (--file, --report)"""
        test_args = [
            'program.py',
            '--file', 'access.log',
            '--report', 'average'
        ]

        with mock.patch('sys.argv', test_args):
            args = parse_args()

            assert args.file == ['access.log']
            assert args.report == 'average'
            assert args.date is None

    def test_multiple_files(self):
        """Тест обработки нескольких файлов"""
        test_args = [
            'program.py',
            '--file', 'file1.log', 'file2.log', 'file3.log',
            '--report', 'average'
        ]

        with mock.patch('sys.argv', test_args):
            args = parse_args()
            assert args.file == ['file1.log', 'file2.log', 'file3.log']

    def test_date_argument(self):
        """Тест аргумента --date"""
        test_args = [
            'program.py',
            '--file', 'data.log',
            '--report', 'average',
            '--date', '2025-06-22'
        ]

        with mock.patch('sys.argv', test_args):
            args = parse_args()
            assert args.date == '2025-06-22'

    def test_missing_required_args(self, capsys):
        """Тест обработки отсутствия обязательных аргументов"""
        test_args = ['program.py']  # Нет обязательных аргументов

        with mock.patch('sys.argv', test_args):
            with pytest.raises(SystemExit):
                parse_args()

            captured = capsys.readouterr()
            assert 'the following arguments are required: --file, --report' in captured.err

    def test_actual_parsing(self):
        """Тест фактического разбора аргументов"""

        # Используем mock для sys.argv
        test_args = [
            'program.py',
            '--file', 'access.log', 'error.log',
            '--report', 'average',
            '--date', '2025-06-22'
        ]

        with mock.patch('sys.argv', test_args):
            args = parse_args()

            assert args.file == ['access.log', 'error.log']
            assert args.report == 'average'
            assert args.date == '2025-06-22'

    def test_actual_parsing_minimal(self):
        """Тест минимального набора аргументов"""
        test_args = [
            'program.py',
            '--file', 'single.log',
            '--report', 'average'
        ]

        with mock.patch('sys.argv', test_args):
            args = parse_args()

            assert args.file == ['single.log']
            assert args.report == 'average'
            assert args.date is None

    def test_date_argument_missing_value(self, capsys):
        """Тест отсутствия значения для --date"""
        test_args = [
            'program.py',
            '--file', 'data.log',
            '--report', 'average',
            '--date'  # Нет значения
        ]

        with mock.patch('sys.argv', test_args):
            with pytest.raises(SystemExit):
                parse_args()

            captured = capsys.readouterr()
            assert 'expected one argument' in captured.err

    def test_file_argument_missing_value(self, capsys):
        """Тест отсутствия значения для --file"""
        test_args = [
            'program.py',
            '--file',  # Нет значения
            '--report', 'average'
        ]

        with mock.patch('sys.argv', test_args):
            with pytest.raises(SystemExit):
                parse_args()

            captured = capsys.readouterr()
            assert 'expected at least one argument' in captured.err
