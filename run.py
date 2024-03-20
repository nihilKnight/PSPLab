import subprocess
import logging

if __name__ == "__main__":
    subprocess.run(["scrapy", "crawl", "sina_spider", "-o", "sina_news.json"])
