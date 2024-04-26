import requests
import threading
import time
import os
import io


from itertools import chain
from concurrent.futures import Future, ThreadPoolExecutor
from enum import Enum
from urllib.parse import urljoin
from crawler import SubDirCrawler
from constant import constant


class ScanMode(Enum):
    Static = 0
    Dynamic = 1

class Scanner:

    def __init__(self, targets: list[str], static_dict_path: str, mode=ScanMode.Static ,threads=128) -> None:
        self.targets = targets
        self.static_dict_path = static_dict_path
        self.mode = mode
        self.threads = threads
        self.lock = threading.Lock()

    def static_generator(self, target: str):
        with open(self.static_dict_path, "r", encoding="utf-8") as dp:
            for line in dp:
                word = line.strip().strip("/")
                yield target + word
                if "." not in word:
                    for ext in constant.EXTS:
                        yield target + word + ext

    def dynamic_generator(self, target: str):
        subdir_gen = chain([""], SubDirCrawler().recursive_parse(target))
        with open(self.static_dict_path, "r", encoding="utf-8") as dp:
            while True:
                try:
                    subdir = next(subdir_gen)
                    dp_ = dp
                    for line in dp_:
                        word = line.strip().strip("/")
                        yield urljoin(target, subdir) + word
                        if "." not in word:
                            for ext in constant.EXTS:
                                yield urljoin(target, subdir) + word + ext
                except StopIteration:
                    return
                
    
    def url_test_and_write(self, url: str, op: io.TextIOWrapper) -> None:
        try:
            req = requests.get(url=url, headers={"User-Agent": constant.USER_AGENT})
            if req.status_code not in constant.BANNED_STAT:
                self.lock.acquire()
                colored_print(f"[-] {req.status_code} ==> {url}")
                op.write(url + "\n")
                self.lock.release()
        except Exception as e:
            print(e)

    def scan(self, output_dir: str) -> None:
        print("[+] mode: " + ("static" if self.mode == ScanMode.Static else "dynamic"))
        print("[+] threads: " + str(self.threads))
        print("[+] output directory: " + output_dir)
        print()
        for target in self.targets:
            print("[+] scanning target: " + target + "...")
            gen = self.static_generator(target) if self.mode == ScanMode.Static else self.dynamic_generator(target)
            output = os.path.join(output_dir, "dyn_target" + ".txt")
            with open(output, "w", encoding="utf-8") as op:
                with ThreadPoolExecutor(max_workers=self.threads) as executor:
                    while True:
                        try:
                            url = next(gen)
                            res = executor.submit(self.url_test_and_write, url, op)
                            executor.submit(waiting, res, url)
                        except StopIteration:
                            break
                        except Exception as e:
                            print(e)

def waiting(res: Future, url: str) -> None:
    while not res.done():
        colored_print(f"[/] {url}", end="\r", color_label=constant.WAITING_COLOR_LABEL)
        time.sleep(0.05)
        colored_print(f"[-] {url}", end="\r", color_label=constant.WAITING_COLOR_LABEL)
        time.sleep(0.05)
        colored_print(f"[\] {url}", end="\r", color_label=constant.WAITING_COLOR_LABEL)
        time.sleep(0.05)
        colored_print(f"[|] {url}", end="\r", color_label=constant.WAITING_COLOR_LABEL)
        time.sleep(0.05)

def colored_print(s: str, end='\n', color_label=constant.DEFAULT_COLOR_LABEL) -> None:
    print((f'\x1b[{color_label}m' + s + '\x1b[0m').ljust(constant.TERMINAL_WIDTH-1, " "), end=end, flush=True)
