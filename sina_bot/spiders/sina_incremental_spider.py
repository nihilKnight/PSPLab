import scrapy
import hashlib
import redis
from sina_bot.items import SinaBotItem


def connect_to_redis(host='localhost', port=6379):
    pool = redis.ConnectionPool(host=host, port=port, decode_responses=True)
    return redis.Redis(connection_pool=pool)

def digest_content(content: list):
    hasher = hashlib.md5()
    for piece in content:
        hasher.update(piece.encode("utf-8"))

    return hasher.digest()


class SinaIncrementalSpiderSpider(scrapy.Spider):
    name = "sina_incremental_spider"
    # allowed_domains = ["www.sina.com.cn"]  Comment this line to disable cross-site filter.
    start_urls = ["https://www.sina.com.cn"]
    # r = connect_to_redis("182.17.0.10")
    r = connect_to_redis()
    finished = 0

    def parse(self, response):
        url_list = response.xpath('//*[@id="syncad_0"]/ul[1]/li/a[1]/@href').extract()

        for url in url_list:
            yield scrapy.Request(url=url, callback=self.parse_content)


    def parse_content(self, response):
        title = response.xpath('/html/body/div[2]/h1/text()').extract()
        date = response.xpath('//*[@id="top_bar"]/div/div[2]/span[1]/text()').extract()
        content = response.xpath('//*[@id="article"]/p/text()').extract()
        hash = int.from_bytes(digest_content(content), "big")

        if title + date + content != [] and not self.r.exists(hash):
            article_item = SinaBotItem()
            article_item['title'] = title
            article_item['date'] = date
            article_item['content'] = content
            article_item['hash'] = hash
            self.r.set(article_item['hash'], 1)
            self.finished += 1
            print(f"Finished articles: {self.finished}")

            yield article_item

