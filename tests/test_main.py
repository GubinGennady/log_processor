import sys
from unittest import mock
import pytest
from datetime import date
from tabulate import tabulate
from src.log_processor.main import main


class TestMain:
    """Тест-кейсы для основного скрипта (точки входа)"""

    @pytest.fixture
    def mock_args(self):
        """Фикстура стандартных аргументов"""
        return [
            'main.py', '--file', 'file.log', '--report', 'average'
        ]

    @pytest.fixture
    def mock_logs(self):
        """Фикстура тестовых логов"""
        return [
            {"@timestamp": "2025-06-22T13:57:32+00:00", "url": "/api/home", "response_time": 0.1},
            {"@timestamp": "2025-06-22T13:57:33+00:00", "url": "/api/home", "response_time": 0.2},
            {"@timestamp": "2025-06-22T13:57:34+00:00", "url": "/api/users", "response_time": 0.3},
        ]

    @pytest.fixture
    def expected_output(self):
        return [
            {'endpoint': '/api/homeworks/...', 'count': 55241, 'avg_time': 0.0926},
            {'endpoint': '/api/context/...', 'count': 43907, 'avg_time': 0.0194},
            {'endpoint': ' /api/specializations/...', 'count': 8329, 'avg_time': 0.0518},
            {'endpoint': '/api/challenges/...', 'count': 1475, 'avg_time': 0.0782},
            {'endpoint': '/api/users/...', 'count': 1446, 'avg_time': 0.0657},
        ]

    def test_successful_execution(self, mock_args, mock_logs, expected_output, capsys):
        """Тест успешного выполнения скрипта"""
        with mock.patch('sys.argv', mock_args), \
                mock.patch('src.log_processor.file_reader.read_logs', return_value=mock_logs):
            main()  # Запуск главной функции

            captured = capsys.readouterr()

            # Проверяем вывод таблицы
            expected_table = tabulate(
                expected_output,
                headers={'endpoint': 'Endpoint', 'count': 'Request Count', 'avg_time': 'Avg Response Time (s)'},
                tablefmt='grid',
                floatfmt=".4f",
                numalign="right"
            )
            assert expected_table in captured.out

    def test_invalid_date_format(self, mock_args, capsys):
        """Тест обработки неверного формата даты"""
        test_args = mock_args + ['--date', 'invalid-date']

        with mock.patch('sys.argv', test_args):
            main()

            captured = capsys.readouterr()
            # Проверка сообщения об ошибке
            assert "Неверный формат даты. Пожалуйста, используйте ГГГГ-ММ-ДД" in captured.out
            # assert "Invalid date format" not in captured.out  # Убедимся, что сообщение на русском

    def test_unknown_report_type(self, mock_args, capsys):
        """Тест обработки неизвестного типа отчета"""
        test_args = [
            'main.py',
            '--file', 'file.log',
            '--report', 'unknown_report'  # Несуществующий отчет
        ]

        with mock.patch('sys.argv', test_args):
            # Ожидаем SystemExit с кодом 3
            with pytest.raises(SystemExit) as exc_info:
                main()

            # Проверка кода ошибки (должен соответствовать коду в main.py)
            assert exc_info.value.code == 3

            captured = capsys.readouterr()
            # Проверка сообщения о доступных отчетах
            # assert "Неизвестный тип отчета: unknown_report" in captured.out
            assert "Доступные отчеты: average" in captured.out

    def test_file_read_error(self, mock_args, capsys):
        """Тест обработки ошибки чтения файла"""

        test_args = [
            'main.py',
            '--file', 'valid.log',
            '--report', 'average'
        ]

        with mock.patch('sys.argv', test_args), \
                mock.patch('src.log_processor.file_reader.read_logs', return_value=[]):
            with pytest.raises(SystemExit) as exc_info:
                main()

            assert exc_info.value.code == 5
