Log Processor
=======
[![Python](https://img.shields.io/badge/Python-3.10%2B-blue)](https://python.org)

# Описание проекта

Log Processor — инструмент для анализа лог-файлов веб-приложений. Он обрабатывает логи в формате JSONL (JSON Lines),
вычисляет метрики производительности и генерирует отчеты в удобном табличном виде.

✅ **Ключевые возможности:**

- Анализ времени ответа сервера по эндпоинтам
- Фильтрация логов по дате
- Поддержка обработки нескольких файлов одновременно
- Гибкая система отчетов с возможностью расширения

🛠 **Технологии**

- Python 3.10+
- pytest для тестирования

## Установка

1. **Клонировать репозиторий**
    ```bash
    https://github.com/GubinGennady/log_processor.git

2. **Создать и активировать виртуальное окружение**
   ```bash
   python -m venv env
   source env/bin/activate  # Linux/MacOS
   env\Scripts\activate.bat  # Windows

3. **Установить зависимости**
   ```bash
   pip install -r requirements.txt

## Использование

1. **Основной скрипт**
   ```bash
   python run.py --file file.log --report average
   
2. **Доступные отчеты**

   - average: Среднее время ответа по эндпоинтам

3. **Пример вывода:**
   ```text
   +--------------------------+----------------+--------------------------+
   | Endpoint                 |   Request Count |   Avg Response Time (s) |
   +==========================+================+==========================+
   | /api/home                |            55241 |                  0.0926 |
   +--------------------------+----------------+--------------------------+
   | /api/context             |            43907 |                  0.0194 |
   +--------------------------+----------------+--------------------------+

4. **Формат входных данных**
   
   - Лог-файлы должны содержать записи в формате JSON Lines. Каждая строка — отдельный JSON-объект.

5. **Формат входных данных**
   - @timestamp: Временная метка (ISO 8601)
   - url: URL эндпоинта
   - response_time: Время ответа в секундах

6. **Пример записи:**
   ```json
   {"@timestamp": "2025-06-22T13:57:32+00:00", "url": "/api/home", "response_time": 0.12, "status": 200}
   

## Тестирование

1. **Запуск всех тестов**
   ```bash
   pytest --cov=src --cov-report=term-missing

2. **Отдельные тест-сьюты**
   ```bash
   # Тесты CLI
   pytest tests/test_cli.py -v

   # Тесты чтения файлов
   pytest tests/test_file_reader.py -v
   
   # Тесты основного скрипта
   pytest tests/test_main.py -v
   
   # Тесты генерации отчетов
   pytest tests/test_reporters.py -v

## 📂 Структура проекта

      log_processor/
      ├── src/                         # Исходный код
      │   └── log_processor/
      │       ├── __init__.py
      │       ├── cli.py               # Парсинг аргументов командной строки
      │       ├── file_reader.py       # Чтение и валидация логов
      │       ├── main.py              # Основная логика приложения
      │       └── reporters.py         # Генераторы отчетов
      ├── tests/                       # Тесты
      │   ├── __init__.py      
      │   ├── test_cli.py
      │   ├── test_file_reader.py
      │   ├── test_main.py
      │   └── test_reporters.py
      ├── run.py                       # Скрипт запуска
      ├── setup.py                     # Конфигурация пакета
      └── README.md                    # Документация
