import argparse


def parse_args():
    # Создание парсера аргументов командной строки
    parser = argparse.ArgumentParser(
        description='Log file processor',  # Описание программы
        formatter_class=argparse.ArgumentDefaultsHelpFormatter  # Показывать значения по умолчанию в справке
    )

    # Обязательный аргумент: пути к файлам логов (один или несколько)
    parser.add_argument(
        '--file',
        nargs='+',  # Принимает один или несколько значений
        required=True,  # Обязательный параметр
        help='Log file path(s)'  # Описание параметра
    )

    # Обязательный аргумент: тип отчета
    parser.add_argument(
        '--report',
        required=True,  # Обязательный параметр
        help='Report type to generate'  # Описание параметра
    )

    # Опциональный аргумент: фильтр по дате
    parser.add_argument(
        '--date',
        help='Filter logs by date (YYYY-MM-DD)'  # Формат даты
    )

    # Возвращает распарсенные аргументы
    return parser.parse_args()
