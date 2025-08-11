from datetime import datetime

import pytest
from src.log_processor.file_reader import read_logs, validate_log


@pytest.fixture
def sample_logs(tmp_path):
    log_file = tmp_path / "test.log"

    logs = [
        '{"@timestamp": "2025-06-22T13:57:32+00:00", "status": 200, "url": "/api/context/...", "request_method": "GET","response_time": 0.02, "http_user_agent": "..."}',
    ]

    with open(log_file, 'w') as f:
        f.write('\n'.join(logs))

    return log_file


def test_read_logs(sample_logs):
    logs = read_logs([sample_logs])
    assert len(logs) == 1
    assert logs[0]['@timestamp'] == "2025-06-22T13:57:32+00:00"


def test_date_filter(sample_logs):
    logs = read_logs([sample_logs], date_filter=datetime(2025, 6, 22).date())
    assert len(logs) == 1
