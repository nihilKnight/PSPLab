import subprocess
import schedule
import time


def job():
    res = subprocess.run(["scrapy", "crawl", "sina_spider", "-o", "sina_news.json"], stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
    with open("log.txt", '+a') as log:
        log.write("-" * 42 + '\n')
        log.write(f"|  Crawled at {time.asctime(time.localtime(time.time()))}.  |\n")
        log.write("-" * 42 + '\n')
        log.write(res.stdout)
        log.write('\n\n\n')


if __name__ == '__main__':
    schedule.every(10).minutes.do(job)
    # schedule.every(5).seconds.do(job)

    while True:
        schedule.run_pending()
        time.sleep(1)
