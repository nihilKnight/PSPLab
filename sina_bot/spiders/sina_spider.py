import scrapy
from sina_bot.items import SinaBotItem


class SinaSpiderSpider(scrapy.Spider):
    name = "sina_spider"
    # allowed_domains = ["www.sina.com.cn"]  # Comment this line to disable cross-site filter.
    start_urls = ["https://www.sina.com.cn"]
    finished = 0

    def parse(self, response):
        url_list = response.xpath('//*[@id="syncad_0"]/ul[1]/li/a[1]/@href').extract()

        for url in url_list:
            yield scrapy.Request(url=url, callback=self.parse_content)


    def parse_content(self, response):
        title = response.xpath('/html/body/div[2]/h1/text()').extract()
        date = response.xpath('//*[@id="top_bar"]/div/div[2]/span[1]/text()').extract()
        content = response.xpath('//*[@id="article"]/p/text()').extract()

        if title + date + content != []:
            article_item = SinaBotItem()
            article_item['title'] = title
            article_item['date'] = date
            article_item['content'] = content
            self.finished += 1
            print(f"Finished articles: {self.finished}")

            yield article_item

