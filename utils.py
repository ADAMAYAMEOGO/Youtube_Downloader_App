# utils.py
import os
from settings import DEFAULT_DOWNLOAD_PATH


def create_download_folder():
    if not os.path.exists(DEFAULT_DOWNLOAD_PATH):
        os.makedirs(DEFAULT_DOWNLOAD_PATH)


def validate_url(url):
    return True if url.startswith('https://www.youtube.com/watch?v=') else False


def format_bytes(size):
    power = 2 ** 10
    n = 0
    power_labels = {0: '', 1: 'k', 2: 'M', 3: 'G', 4: 'T'}
    while size > power:
        size /= power
        n += 1
    return "%.2f %sB" % (size, power_labels[n])
