import subprocess
import schedule
import time


def job():
    res = subprocess.run(["python3", "run.py", "sina_incremental_spider"], stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
    date_str = time.strftime("%Y%m%d", time.localtime())
    log_file_name = f"logs/log_{date_str}.txt"

    with open(log_file_name, '+a', encoding="UTF-8") as log:
        log.write("-" * 42 + '\n')
        log.write(f"|  Crawled at {time.asctime(time.localtime(time.time()))}.  |\n")
        log.write("-" * 42 + '\n')
        log.write(res.stdout)
        log.write('\n\n\n')


if __name__ == '__main__':
    # schedule.every(10).minutes.do(job)
    schedule.every(5).seconds.do(job)

    while True:
        schedule.run_pending()
        time.sleep(1)
