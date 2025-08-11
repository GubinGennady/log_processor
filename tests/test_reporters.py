from src.log_processor.reporters import AverageReporter


def test_average_report_with_real_data():
    logs = [
        {"@timestamp": "2025-06-22T13:57:32+00:00", "url": "/api/home", "response_time": 0.1},
        {"@timestamp": "2025-06-22T13:57:33+00:00", "url": "/api/home", "response_time": 0.2},
        {"@timestamp": "2025-06-22T13:57:34+00:00", "url": "/api/data", "response_time": 0.3},
    ]

    report = AverageReporter.generate_report(logs)

    assert len(report) == 2
    assert report[0]['endpoint'] == '/api/home'
    assert report[0]['count'] == 2
    assert report[0]['avg_time'] == 0.15

    assert report[1]['endpoint'] == '/api/data'
    assert report[1]['count'] == 1
    assert report[1]['avg_time'] == 0.3