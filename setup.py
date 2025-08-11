from setuptools import setup, find_packages

setup(
    name='log_processor',
    version='0.1.0',
    packages=find_packages(where='src'),
    package_dir={'': 'src'},
    install_requires=[
        'tabulate>=0.9.0',
    ],
    entry_points={
        'console_scripts': [
            'log-processor=log_processor.main:main',
        ],
    },
    extras_require={
        'test': [
            'pytest>=7.4.0',
            'pytest-cov>=4.1.0'
        ]
    },
)