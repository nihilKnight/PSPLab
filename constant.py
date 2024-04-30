import os

class constant:

    STATIC_DICT_PATH = "dicts/static_dict.txt"
    OUTPUT_DIR = "outputs/"
    EXTS = [".bak", ".nr", ".7z", ".swp", ".rar", ".tar.gz", ".tar", ".zip", ".jsp", ".doc", ".txt", ".py", ".json"]
    USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36"
    BANNED_STAT = list(range(400, 600))
    DEFAULT_COLOR_LABEL = "1;32;40"
    WAITING_COLOR_LABEL = "1;36;40"
    TERMINAL_WIDTH = os.get_terminal_size().columns
    MAX_THREADS = 64
