from scanner import ScanMode, Scanner
from constant import constant


if __name__ == "__main__":
    # targets = ["https://bilibili.com"]
    targets = ["https://www.bilibili.com/"]
    s = Scanner(targets, constant.STATIC_DICT_PATH, ScanMode.Dynamic)
    s.scan(constant.OUTPUT_DIR)

