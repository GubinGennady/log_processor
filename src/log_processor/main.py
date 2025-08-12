import sys
from datetime import datetime
from tabulate import tabulate  # Библиотека для табличного вывода

from src.log_processor.cli import parse_args
from src.log_processor.file_reader import read_logs
from src.log_processor.reporters import REPORTERS  # Доступные генераторы отчетов


def main():
    args = parse_args()  # Парсинг аргументов

    # Обработка параметра даты (если передан)
    date_filter = None
    if args.date:
        try:
            # Преобразование строки в объект даты
            date_filter = datetime.strptime(args.date, '%Y-%m-%d').date()
        except ValueError:
            print("Неверный формат даты. Пожалуйста, используйте ГГГГ-ММ-ДД")
            return 'invalid-date\n'

    # Чтение и фильтрация логов
    logs = read_logs(args.file, date_filter)

    # Проверка наличия логов
    if not logs:
        print("Не найдено журналов, соответствующих критериям")
        return

    # Проверка существования запрошенного отчета
    if args.report not in REPORTERS:
        print(f"Неизвестный тип отчета: {args.report}")
        print(f"Доступные отчеты: {', '.join(REPORTERS.keys())}")
        sys.exit(3)  # Выход с кодом ошибки

    # Генерация отчета
    reporter = REPORTERS[args.report]
    report_data = reporter.generate_report(logs)

    # Настройки заголовков для таблицы
    headers = {
        'endpoint': 'Endpoint',
        'count': 'Request Count',
        'avg_time': 'Avg Response Time (s)'
    }

    # Вывод форматированной таблицы
    print(tabulate(
        report_data,
        headers=headers,
        tablefmt='grid',  # Сеточный стиль
        floatfmt=".4f",  # Формат чисел с плавающей точкой
        numalign="right"  # Выравнивание чисел по правому краю
    ))
