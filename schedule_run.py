import subprocess
import schedule
import time
import sys


spider_name = ""

def job():
    res = subprocess.run(["python3", "run.py", spider_name], stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
    date_str = time.strftime("%Y%m%d", time.localtime())
    log_file_name = f"logs/log_{date_str}.txt"

    with open(log_file_name, '+a', encoding="UTF-8") as log:
        log.write("-" * 42 + '\n')
        log.write(f"|  Crawled at {time.asctime(time.localtime(time.time()))}.  |\n")
        log.write("-" * 42 + '\n')
        log.write(res.stdout)
        log.write('\n\n\n')


if __name__ == '__main__':
    spider_name = "sina_spider" if len(sys.argv) <= 1 else sys.argv[1]

    # schedule.every(10).minutes.do(job)
    schedule.every(5).seconds.do(job)

    while True:
        schedule.run_pending()
        time.sleep(1)
