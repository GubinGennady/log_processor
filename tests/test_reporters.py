from src.log_processor.reporters import AverageReporter


def test_average_report_with_real_data():
    """Тест генерации отчета со средней скоростью ответа"""

    # Тестовые данные
    logs = [
        {"@timestamp": "2025-06-22T13:57:32+00:00", "url": "/api/home", "response_time": 0.1},
        {"@timestamp": "2025-06-22T13:57:33+00:00", "url": "/api/home", "response_time": 0.2},
        {"@timestamp": "2025-06-22T13:57:34+00:00", "url": "/api/data", "response_time": 0.3},
    ]

    # Генерация отчета
    report = AverageReporter.generate_report(logs)

    # Проверка структуры отчета
    assert len(report) == 2  # Должно быть 2 уникальных endpoint

    # Проверка данных для /api/home
    home_report = next(r for r in report if r['endpoint'] == '/api/home')
    assert home_report['count'] == 2
    assert home_report['avg_time'] == 0.15  # (0.1 + 0.2) / 2

    # Проверка данных для /api/data
    data_report = next(r for r in report if r['endpoint'] == '/api/data')
    assert data_report['count'] == 1
    assert data_report['avg_time'] == 0.3


def test_report_sorting():
    """Тест сортировки результатов по убыванию количества запросов"""
    logs = [
        {"url": "/low", "response_time": 0.1},  # 1 запрос
        {"url": "/high", "response_time": 0.2},  # 3 запроса
        {"url": "/high", "response_time": 0.2},
        {"url": "/high", "response_time": 0.2},
        {"url": "/mid", "response_time": 0.3},  # 2 запроса
        {"url": "/mid", "response_time": 0.3},
    ]

    report = AverageReporter.generate_report(logs)

    # Проверка порядка endpoint: /high -> /mid -> /low
    assert report[0]['endpoint'] == '/high'
    assert report[1]['endpoint'] == '/mid'
    assert report[2]['endpoint'] == '/low'
