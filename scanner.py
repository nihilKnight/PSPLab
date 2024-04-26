import requests
import threading
import time
import os
import io

import constant

from concurrent.futures import ThreadPoolExecutor
from enum import Enum


class ScanMode(Enum):
    Static = 0
    Dynamic = 1

class Scanner:

    def __init__(self, targets: list[str], static_dict_path: str, mode=ScanMode.Static ,threads=64) -> None:
        self.targets = targets
        self.static_dict_path = static_dict_path
        self.mode = mode
        self.threads = threads
        self.lock = threading.Lock()

    def static_generator(self, target: str, dict_path: str):
        with open(dict_path, "r", encoding="utf-8") as dp:
            for line in dp:
                word = line.strip().strip("/")
                yield f"{target}/{word}"
                if "." not in word:
                    for ext in constant.EXTS:
                        yield f"{target}/{word}{ext}"

    def dynamic_generator(self, target: str):
        pass
    
    def url_test_and_write(self, url: str, op: io.TextIOWrapper) -> None:
        try:
            req = requests.get(url=url, headers={"User-Agent": constant.USER_AGENT})
            if req.status_code not in constant.BANNED_STAT:
                while True: 
                    waiting(url)
                    if self.lock.acquire():
                        break
                colored_print(f"[-] {req.status_code} ==> {url}")
                op.write(url + "\n")
                self.lock.release()
        except Exception as e:
            print(e)

    def scan(self, output_dir: str) -> None:
        print("[+] mode: " + "static" if self.mode == ScanMode.Static else "dynamic")
        print("[+] threads: " + str(self.threads))
        print("[+] output directory: " + output_dir)
        print()
        for target in self.targets:
            print("[+] scanning target: " + target + "...")
            gen = self.static_generator(target, self.static_dict_path) if self.mode == ScanMode.Static else self.dynamic_generator(target)
            output = os.path.join(output_dir, "target" + ".txt")
            with open(output, "w", encoding="utf-8") as op:
                with ThreadPoolExecutor(max_workers=self.threads) as executor:
                    while True:
                        try:
                            url = next(gen)
                            executor.submit(self.url_test_and_write, url, op)
                        except StopIteration:
                            break
                        except Exception as e:
                            print(e)

def waiting(url: str) -> None:
    colored_print(f"[/] {url}", end="\r", color_label="4;34;40")
    time.sleep(0.2)
    colored_print(f"[-] {url}", end="\r", color_label="4;34;40")
    time.sleep(0.2)
    colored_print(f"[\] {url}", end="\r", color_label="4;34;40")
    time.sleep(0.2)
    colored_print(f"[|] {url}", end="\r", color_label="4;34;40")
    time.sleep(0.2)

def colored_print(s: str, end='\n', color_label=constant.DEFAULT_COLOR_LABEL) -> None:
    print(f'\x1b[{color_label}m' + s + '\x1b[0m', end=end, flush=True)
