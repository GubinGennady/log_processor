from collections import defaultdict


class BaseReporter:
    @staticmethod
    def get_endpoint(log):
        return log['url']


class AverageReporter(BaseReporter):
    @staticmethod
    def generate_report(logs):
        endpoint_stats = defaultdict(lambda: {'count': 0, 'total_time': 0.0})

        for log in logs:
            endpoint = AverageReporter.get_endpoint(log)
            endpoint_stats[endpoint]['count'] += 1
            endpoint_stats[endpoint]['total_time'] += log['response_time']

        report = []
        for endpoint, stats in endpoint_stats.items():
            avg_time = stats['total_time'] / stats['count']
            report.append({
                'endpoint': endpoint,
                'count': stats['count'],
                'avg_time': round(avg_time, 4)
            })

        return sorted(report, key=lambda x: x['count'], reverse=True)


# Реестр отчетов для легкого расширения
REPORTERS = {
    'average': AverageReporter
}