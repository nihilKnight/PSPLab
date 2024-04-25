import requests
import threading
import os

from enum import Enum


EXTS = [".bak", ".nr", ".7z", ".swp", ".rar", ".tar.gz", ".tar", ".zip", ".jsp", ".doc", ".txt", ".py", ".json"]
USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36"
BANNED_STAT = list(range(403, 404)) + list(range(500, 600))

class ScanMode(Enum):
    Static = 0
    Dynamic = 1

class Scanner:

    def __init__(self, targets: list[str], static_dict_path: str, mode=ScanMode.Static ,threads=64) -> None:
        targets = targets
        static_dict_path = static_dict_path
        mode = mode
        threads = threads

    def url_generator(self, target: str, dict_path: str):
        with open(dict_path, "r", encoding="utf-8") as dp:
            for line in dp:
                word = line.strip().strip("/")
                yield f"{target}/{word}"
                if "." not in word:
                    for ext in EXTS:
                        yield f"{target}/{word}{ext}"
    
    def url_test(self, url: str) -> bool:
        try:
            req = requests.get(url, headers={"User-Agent": USER_AGENT})
            if req.status_code not in BANNED_STAT:
                return True
            else:
                return False
        except Exception as e:
            print(e)

    def scan(self, output_dir: str) -> None:
        target_scanners = []
        for target in self.targets:
            target_scanner = {}
            target_scanner["gen"] = self.url_generator(target, self.static_dict_path)
            target_scanner["lock"] = threading.Lock()
            target_scanner["output"] = os.path.join(output_dir, target + ".txt")
            target_scanners.append(target_scanner)
        
            


