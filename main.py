import constant

from scanner import ScanMode, Scanner


if __name__ == "__main__":
    targets = ["https://bilibili.com"]
    s = Scanner(targets, constant.STATIC_DICT_PATH, ScanMode.Static)
    s.scan(constant.OUTPUT_DIR)

