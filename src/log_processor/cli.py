import argparse

def parse_args():
    parser = argparse.ArgumentParser(
        description='Log file processor',
        formatter_class=argparse.ArgumentDefaultsHelpFormatter
    )
    parser.add_argument(
        '--file', 
        nargs='+',
        required=True,
        help='Log file path(s)'
    )
    parser.add_argument(
        '--report',
        required=True,
        choices=['average'],
        help='Report type to generate'
    )
    parser.add_argument(
        '--date',
        help='Filter logs by date (YYYY-MM-DD)'
    )
    return parser.parse_args()