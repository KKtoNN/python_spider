# -*- coding: utf-8 -*-
from datetime import datetime
import scrapy
from fagaiwei.items import FagaiweiItem
from fagaiwei.keyword_others import keyword
from fagaiwei.settings import session, NewsItemInfo


class ZjzxSpider(scrapy.Spider):
    # 参考消息
    name = 'cankaoxiaoxi'
    allowed_domains = ['cankaoxiaoxi.com']
    start_urls = [
        'http://china.cankaoxiaoxi.com/',  # 中国
        'http://world.cankaoxiaoxi.com/',  # 国际
        'http://mil.cankaoxiaoxi.com/',  # 军事
        'http://finance.cankaoxiaoxi.com/',  # 财经
    ]

    def parse(self, response):
        url_list = response.xpath('//*[@id="zuixin"]/div[contains(@class,"elem")]/a/@href').extract()
        for url in url_list:
            result = session.query(NewsItemInfo).filter_by(url=url, web_id=94).count()
            if result:
                # print("{} 存在".format(url))
                pass
            else:
                yield scrapy.Request(url, callback=self.process_detail, meta={'web': response.url})

    def process_detail(self, response):
        item = FagaiweiItem()
        item['web_id'] = 94
        item['url'] = response.url
        item['title'] = response.xpath('//div[@class="bg-content"]/h1/text()').extract_first(default='')
        item['web'] = response.meta.get('web')
        item['webname'] = response.xpath('//div[@class="bg-content"]/span[@id="source_baidu"]/a/text()').extract_first(
            default='参考消息网')
        item['pub_time'] = response.xpath('//div[@class="bg-content"]/span[@id="pubtime_baidu"]/text()').extract_first(
            default=datetime.now())
        content = ''.join(response.xpath('//p[contains(@class,"cont-detail")]/span/text()| \
                                         //*[@id="ctrlfscont"]/p/strong/text() | \
                                         //*[@id="ctrlfscont"]/p/strong/a/text() | \
                                         //*[@id="ctrlfscont"]/p/text() | \
                                         //*[@id="ctrlfscont"]/p/span/text()').extract())
        if not content:
            content = '这可能是图片或者文件，打开查看！'
        item['content'] = content
        item["keyword"] = keyword.get_keyword(item["content"])
        yield item
