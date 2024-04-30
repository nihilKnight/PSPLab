from crawler import SubDirCrawler
from scanner import colored_print

if __name__ == "__main__":
    # tg = "https://cst.buaa.edu.cn/"
    tg = "https://www.bilibili.com/"
    depth = 3
    subdir_gen = SubDirCrawler(depth=depth).recursive_parse(tg)
    try:
        print("[+] Starting crawling url: " + tg + " with recursive depth " + str(depth) + "...")
        while True:
            subdir = next(subdir_gen)
            colored_print("[-] Founded: " + tg + subdir)
    except StopIteration:
        print("[+] Finished.")

