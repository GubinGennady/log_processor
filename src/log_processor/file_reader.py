import json
import os
from datetime import datetime


def read_logs(file_paths, date_filter=None):
    all_logs = []
    current_dir = os.getcwd()
    print(f"Текущая директория: {current_dir}")

    for path in file_paths:
        abs_path = os.path.abspath(path)
        print(f"Поиск файла: {abs_path}")

        if not os.path.exists(abs_path):
            print(f"ОШИБКА: Файл не существует - {abs_path}")
            continue



# def read_logs(file_paths, date_filter=None):
#     all_logs = []
#     for path in file_paths:
#         if not os.path.isfile(path):
#             print(f"Файл не найден: {path}")
#             continue

        try:
            with open(path, 'r') as f:
                for line in f:
                    try:
                        log = json.loads(line.strip())
                        if validate_log(log):
                            if date_filter:
                                log_date = datetime.fromisoformat(log['@timestamp']).date()
                                if log_date == date_filter:
                                    all_logs.append(log)
                            else:
                                all_logs.append(log)
                    except (json.JSONDecodeError, KeyError, ValueError):
                        continue
        except IOError as e:
            print(f"Чтение с ошибкой {path}: {str(e)}")

    return all_logs


def validate_log(log):
    required_keys = {'@timestamp', 'url', 'response_time'}
    return all(key in log for key in required_keys)