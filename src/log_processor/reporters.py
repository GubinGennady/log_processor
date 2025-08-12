from collections import defaultdict


class BaseReporter:
    """Базовый класс для генерации отчетов"""

    @staticmethod
    def get_endpoint(log):
        """Извлекает URL из лога"""
        return log['url']


class AverageReporter(BaseReporter):
    """Генератор отчета со средней скоростью ответа"""

    @staticmethod
    def generate_report(logs):
        """Создает отчет: URL, кол-во запросов, среднее время ответа"""
        # Словарь для агрегации данных: {url: {count, total_time}}
        endpoint_stats = defaultdict(lambda: {'count': 0, 'total_time': 0.0})

        # Обработка каждого лога
        for log in logs:
            endpoint = AverageReporter.get_endpoint(log)  # Извлечение URL
            # Агрегация данных
            endpoint_stats[endpoint]['count'] += 1
            endpoint_stats[endpoint]['total_time'] += log['response_time']

        # Формирование отчета
        report = []
        for endpoint, stats in endpoint_stats.items():
            # Расчет среднего времени
            avg_time = stats['total_time'] / stats['count']
            report.append({
                'endpoint': endpoint,
                'count': stats['count'],
                'avg_time': round(avg_time, 4)  # Округление
            })

        # Сортировка по убыванию количества запросов
        return sorted(report, key=lambda x: x['count'], reverse=True)


# Реестр доступных генераторов отчетов (для легкого расширения)
REPORTERS = {
    'average': AverageReporter  # Отчет по средней скорости
}
