import scrapy
from ..items import TedItem


class TedSpider(scrapy.Spider):
    name = 'ted'
    start_urls = ['https://www.ted.com/talks']

    def parse(self, response):
        results = response.xpath('//*[@id="browse-results"]/div[1]/div[@class="col"]')
        for element in results:
            tedItem = TedItem()
            # 取文本
            tedItem['talk'] = element.xpath('./div/div/div/div[2]/h4[2]/a/text()').extract_first()
            # 取属性
            tedItem['link'] = element.xpath('./div/div/div/div[2]/h4[2]/a/@href').extract_first()
            # 将数据放到管道里
            yield tedItem
