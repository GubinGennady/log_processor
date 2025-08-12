import json
import os
import sys
from datetime import datetime


def read_logs(file_paths, date_filter=None):
    """Читает и фильтрует логи из файлов"""
    all_logs = []  # Хранение обработанных логов
    current_dir = os.getcwd()
    print(f"Текущая директория: {current_dir}")

    for path in file_paths:  # Обработка каждого переданного файла
        abs_path = os.path.abspath(path)
        print(f"Поиск файла: {abs_path}")

        # Проверка существования файла
        if not os.path.exists(abs_path):
            print(f"ОШИБКА: Файл не существует - {abs_path}")
            sys.exit(5)  # Выход с кодом ошибки

        try:
            with open(path, 'r') as f:
                for line in f:  # Чтение файла построчно
                    try:
                        log = json.loads(line.strip())  # Парсинг JSON
                        # Валидация и фильтрация лога
                        if validate_log(log):
                            if date_filter:
                                # Извлечение даты из лога
                                log_date = datetime.fromisoformat(log['@timestamp']).date()

                                # Фильтр по дате
                                if log_date == date_filter:
                                    all_logs.append(log)
                            else:
                                all_logs.append(log)
                    # Игнорирование некорректных записей
                    except (json.JSONDecodeError, KeyError, ValueError):
                        continue
        except IOError as e:  # Обработка ошибок чтения файла
            print(f"Чтение с ошибкой {path}: {str(e)}")

    return all_logs


def validate_log(log):
    """Проверяет обязательные поля в логе"""
    required_keys = {'@timestamp', 'url', 'response_time'}
    return all(key in log for key in required_keys)
