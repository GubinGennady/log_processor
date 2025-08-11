import argparse
import sys
from unittest import mock
from src.log_processor.cli import parse_args


class TestCommandLineInterface:
    """Тесты для обработки аргументов командной строки"""

    @mock.patch('argparse.ArgumentParser.parse_args')
    def test_basic_arguments(self, mock_parse):
        """Тест базовых аргументов (--file, --report)"""
        mock_parse.return_value = argparse.Namespace(
            file=['access.log'],
            report='average',
            date=None
        )

        args = parse_args()

        assert args.file == ['access.log']
        assert args.report == 'average'
        assert args.date is None

    @mock.patch('argparse.ArgumentParser.parse_args')
    def test_multiple_files(self, mock_parse):
        """Тест обработки нескольких файлов"""
        mock_parse.return_value = argparse.Namespace(
            file=['file1.log', 'file2.log', 'file3.log'],
            report='average',
            date=None
        )

        args = parse_args()
        assert args.file == ['file1.log', 'file2.log', 'file3.log']

    @mock.patch('argparse.ArgumentParser.parse_args')
    def test_date_argument(self, mock_parse):
        """Тест аргумента --date"""
        mock_parse.return_value = argparse.Namespace(
            file=['data.log'],
            report='average',
            date='2025-06-22'
        )

        args = parse_args()
        assert args.date == '2025-06-22'

    @mock.patch('argparse.ArgumentParser.parse_args')
    def test_missing_required_args(self, mock_parse):
        """Тест обработки отсутствия обязательных аргументов"""
        # Имитируем ошибку при отсутствии обязательных аргументов
        mock_parse.side_effect = argparse.ArgumentError(
            argument=None,
            message="the following arguments are required: --file, --report"
        )

        with mock.patch.object(sys, 'stderr', new_callable=mock.MagicMock) as mock_stderr:
            try:
                parse_args()
            except SystemExit:
                pass  # Ожидаем выход при ошибке

            # Проверяем, что сообщение об ошибке было напечатано
            assert mock_stderr.write.called
            error_message = ''.join(call[0][0] for call in mock_stderr.write.call_args_list)
            assert 'required: --file, --report' in error_message

    @mock.patch('argparse.ArgumentParser.parse_args')
    def test_invalid_report_type(self, mock_parse):
        """Тест обработки недопустимого типа отчета"""
        # Имитируем ошибку при недопустимом значении --report
        mock_parse.side_effect = argparse.ArgumentError(
            argument=None,
            message="argument --report: invalid choice: 'invalid' (choose from 'average')"
        )

        with mock.patch.object(sys, 'stderr', new_callable=mock.MagicMock) as mock_stderr:
            try:
                parse_args()
            except SystemExit:
                pass

            assert mock_stderr.write.called
            error_message = ''.join(call[0][0] for call in mock_stderr.write.call_args_list)
            assert "invalid choice: 'invalid'" in error_message
            assert "(choose from 'average')" in error_message

    @mock.patch('argparse.ArgumentParser.parse_args')
    def test_help_output(self, mock_parse):
        """Тест вывода справки"""
        # Имитируем запрос справки
        mock_parse.side_effect = argparse.ArgumentError(
            argument=None,
            message="help requested"
        )

        with mock.patch.object(sys, 'stdout', new_callable=mock.MagicMock) as mock_stdout:
            try:
                parse_args()
            except SystemExit:
                pass

            assert mock_stdout.write.called
            help_output = ''.join(call[0][0] for call in mock_stdout.write.call_args_list)
            assert '--file FILE [FILE ...]' in help_output
            assert '--report {average}' in help_output
            assert '--date DATE' in help_output
            assert 'Log file processor' in help_output

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

    @mock.patch('argparse.ArgumentParser.parse_args')
    def test_date_argument_missing_value(self, mock_parse):
        """Тест отсутствия значения для --date"""
        mock_parse.side_effect = argparse.ArgumentError(
            argument=None,
            message="argument --date: expected one argument"
        )

        with mock.patch.object(sys, 'stderr', new_callable=mock.MagicMock) as mock_stderr:
            try:
                parse_args()
            except SystemExit:
                pass

            assert mock_stderr.write.called
            error_message = ''.join(call[0][0] for call in mock_stderr.write.call_args_list)
            assert 'expected one argument' in error_message