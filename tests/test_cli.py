from unittest import mock
import pytest
from src.log_processor.cli import parse_args


class TestCommandLineInterface:
    """Тест-кейсы для обработки аргументов командной строки"""

    def test_basic_arguments(self):
        """Тест парсинга обязательных аргументов (--file и --report)"""
        test_args = [
            'program.py',
            '--file', 'access.log',
            '--report', 'average'
        ]

        with mock.patch('sys.argv', test_args):  # Подмена системных аргумента

            args = parse_args()

            # Проверка корректности распарсенных значений
            assert args.file == ['access.log']
            assert args.report == 'average'
            assert args.date is None  # Дата не передавалась

    def test_multiple_files(self):
        """Тест обработки нескольких файлов в аргументе --file"""
        test_args = [
            'program.py',
            '--file', 'file1.log', 'file2.log', 'file3.log',
            '--report', 'average'
        ]

        with mock.patch('sys.argv', test_args):
            args = parse_args()
            # Проверка, что все 3 файла корректно распознаны
            assert args.file == ['file1.log', 'file2.log', 'file3.log']

    def test_date_argument(self):
        """Тест корректной обработки аргумента --date"""
        test_args = [
            'program.py',
            '--file', 'data.log',
            '--report', 'average',
            '--date', '2025-06-22'
        ]

        with mock.patch('sys.argv', test_args):
            args = parse_args()
            assert args.date == '2025-06-22'  # Проверка значения даты

    def test_missing_required_args(self, capsys):
        """Тест обработки отсутствия обязательных аргументов"""
        test_args = ['program.py']  # Не переданы обязательные аргументы

        with mock.patch('sys.argv', test_args):
            with pytest.raises(SystemExit):  # Ожидаем завершение программы
                parse_args()

            captured = capsys.readouterr()  # Перехват вывода
            # Проверка сообщения об ошибке
            assert 'the following arguments are required: --file, --report' in captured.err

    # Остальные тесты используют аналогичный подход:

    def test_actual_parsing(self):
        """Тест комплексного парсинга всех аргументов"""
        # Проверяет комбинацию file+report+date

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
        # Только обязательные параметры

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
        # Проверяет обработку синтаксической ошибки

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
        # Проверяет обработку ошибки для nargs='+'

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
