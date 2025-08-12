from setuptools import setup, find_packages

# Конфигурация пакета для установки
setup(
    name='log_processor',  # Название пакета
    version='0.1.0',  # Версия пакета (сематическое версионирование)

    # Поиск пакетов в директории src
    packages=find_packages(where='src'),
    # Указание что исходные коды находятся в src
    package_dir={'': 'src'},

    # Зависимости для работы пакета
    install_requires=[
        'tabulate>=0.9.0',  # Минимальная версия библиотеки для табличного вывода
    ],

    # Создание консольной команды
    entry_points={
        'console_scripts': [
            # Регистрация команды log-processor
            # которая вызывает функцию main в модуле log_processor.main
            'log-processor=log_processor.main:main',
        ],
    },

    # Дополнительные зависимости для тестирования
    extras_require={
        'test': [  # Группа зависимостей для тестов
            'pytest>=7.4.0',  # Фреймворк для тестирования
            'pytest-cov>=4.1.0'  # Плагин для оценки покрытия кода тестами
        ]
    },
)