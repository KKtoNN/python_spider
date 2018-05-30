# -*- coding: utf-8 -*-
import time
import scrapy
from fagaiwei.items import FagaiweiItem
from fagaiwei.settings import session, NewsItemInfo
from fagaiwei.keyword_others import keyword

class xiamenSipderSpider(scrapy.Spider):
    name = 'xianggangwen_sipder'
    allowed_domains = ['wenweipo.com']

    # start_urls = [
    #     'http://paper.wenweipo.com/',
    # ]
    def start_requests(self):
        urls = [
            "http://paper.wenweipo.com/006FI/",
            "http://paper.wenweipo.com/003HK/",
            "http://paper.wenweipo.com/002CH/",
            "http://paper.wenweipo.com/003TW/",
            "http://paper.wenweipo.com/004GJ/",
            "http://paper.wenweipo.com/008ED/",
            "http://paper.wenweipo.com/009OT/",
            "http://paper.wenweipo.com/010SP/",

        ]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):

        xq_urls = response.xpath("//div[contains(@class,'column-2')]//div/a/@href").getall()

        lz_url = response.url
        for url in xq_urls:
            result = session.query(NewsItemInfo).filter_by(url=url, web_id=45).count()
            if result:
                # print("{} 存在".format(url))
                pass
            else:
                yield scrapy.Request(url=url, callback=self.parse_page, meta={'url': lz_url})

    def parse_page(self, response):
        item = FagaiweiItem()
        item['webname'] = '香港文汇报'
        item['title'] = ''.join(list(response.xpath("//h1/text()").get())).replace('\u3000', '')
        times = response.xpath("//div[@class='foot-left']/span/text()").get()
        item['pub_time'] = times  # +' 00:00:00'
        item['web'] = response.meta['url']
        item['url'] = response.url
        item['content'] = ''.join(list(response.xpath("//div[@id='main-content']//text()").getall())).replace(
            '\u3000', '').replace('\t', '').replace('\r', '')
        item['add_time'] = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        item['web_id'] = 45
        # print(item)
        item["keyword"] = keyword.get_keyword(item["content"])
        return item
        pass
