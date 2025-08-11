import pytest
from src.log_processor.file_reader import read_logs, validate_log

@pytest.fixture
def sample_logs(tmp_path):
    log_file = tmp_path / "test.log"
    logs = [
        '{"path": "/api", "response_time": 100, "timestamp": "2025-01-01T12:00:00"}',
        'INVALID JSON',
        '{"missing_keys": true}'
    ]
    with open(log_file, 'w') as f:
        f.write("\n".join(logs))
    return log_file

def test_read_logs(sample_logs):
    logs = read_logs([sample_logs])
    assert len(logs) == 1
    assert logs[0]['path'] == "/api"

def test_date_filter(sample_logs):
    logs = read_logs([sample_logs], date_filter=datetime(2025, 1, 1).date())
    assert len(logs) == 1