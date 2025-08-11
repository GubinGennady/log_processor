import sys
from datetime import datetime
from tabulate import tabulate

from src.log_processor.cli import parse_args
from src.log_processor.file_reader import read_logs
from src.log_processor.reporters import REPORTERS


def main():
    args = parse_args()

    # Преобразование даты
    date_filter = None
    if args.date:
        try:
            date_filter = datetime.strptime(args.date, '%Y-%m-%d').date()
        except ValueError:
            print("Неверный формат даты. Пожалуйста, используйте ГГГГ-ММ-ДД")
            return 'invalid-date\n'

    # Чтение логов
    logs = read_logs(args.file, date_filter)

    if not logs:
        print("Не найдено журналов, соответствующих критериям")
        return

    # Генерация отчета
    if args.report not in REPORTERS:
        print(f"Неизвестный тип отчета: {args.report}")
        print(f"Доступные отчеты: {', '.join(REPORTERS.keys())}")
        sys.exit(3)

    reporter = REPORTERS[args.report]
    report_data = reporter.generate_report(logs)

    # Вывод таблицы
    headers = {
        'endpoint': 'Endpoint',
        'count': 'Request Count',
        'avg_time': 'Avg Response Time (s)'
    }

    print(tabulate(
        report_data,
        headers=headers,
        tablefmt='grid',
        floatfmt=".4f",
        numalign="right"
    ))
