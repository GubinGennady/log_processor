from datetime import datetime

import pytest
from src.log_processor.file_reader import read_logs, validate_log


@pytest.fixture
def sample_logs(tmp_path):
    """Фикстура создания временного лог-файла для тестов"""
    log_file = tmp_path / "test.log"

    # Тестовые данные в формате JSON
    logs = [
        '{"@timestamp": "2025-06-22T13:57:32+00:00", "status": 200, "url": "/api/context/...", "request_method": "GET","response_time": 0.02, "http_user_agent": "..."}',
    ]

    # Создание файла с тестовыми данными
    with open(log_file, 'w') as f:
        f.write('\n'.join(logs))

    return log_file


def test_read_logs(sample_logs):
    """Тест чтения логов из файла"""
    logs = read_logs([sample_logs])
    # Проверка количества считанных записей
    assert len(logs) == 1
    # Проверка корректности распарсенных данных
    assert logs[0]['@timestamp'] == "2025-06-22T13:57:32+00:00"


def test_date_filter(sample_logs):
    """Тест фильтрации логов по дате"""
    # Чтение с фильтром по конкретной дате
    logs = read_logs([sample_logs], date_filter=datetime(2025, 6, 22).date())
    assert len(logs) == 1  # Должна вернуться 1 запись

    # Тест с другой датой (не должен вернуть записей)
    logs = read_logs([sample_logs], date_filter=datetime(2023, 1, 1).date())
    assert len(logs) == 0
