# -*- coding: utf-8 -*-
import scrapy
from fagaiwei.settings import session, NewsItemInfo
from fagaiwei.items import FagaiweiItem
from datetime import datetime


class ZjzxSpider(scrapy.Spider):
    # 中国金融新闻网
    name = 'zgjrxww'
    allowed_domains = ['financialnews.com.cn']
    start_urls = [
        'http://www.financialnews.com.cn/if/',  # 互联网金融
        'http://www.financialnews.com.cn/gc/',  # 观察
        'http://www.financialnews.com.cn/cj/',  # 要闻
        'http://www.financialnews.com.cn/hg/',  # 宏观
        'http://www.financialnews.com.cn/jg/',  # 监管
    ]

    def parse(self, response):
        url_list = response.xpath(
            '//div[contains(@class,"news_article")]/div/h3/a/@href | //ul[@id="list"]/li/a/@href').extract()
        for url in url_list:
            new_url = response.urljoin(url)

            result = session.query(NewsItemInfo).filter_by(url=new_url, web_id=81).count()
            if result:
                # print("{} 存在".format(url))
                pass
            else:
                yield scrapy.Request(new_url, callback=self.process_detail, meta={'web': response.url})

    def process_detail(self, response):
        item = FagaiweiItem()
        item['web_id'] = 81
        item['url'] = response.url
        item['title'] = ''.join(response.xpath(
            '//div[@class="content_title"]/text()|//div[@class="content_title"]/p/text()|//div[@class="content_title"]/p/font/text()|//div[@class="content_title"]/font/text()').extract())
        item['web'] = response.meta.get('web')
        item['keyword'] = ''
        item['webname'] = \
        response.xpath('//div[@class="content_info"]/span[1]/text()').extract_first(default='').split('来源：')[-1]
        item['pub_time'] = \
        response.xpath('//div[@class="content_info"]/span[3]/text()').extract_first(datetime.now()).split('日期：')[-1]
        content = '\n'.join(response.xpath('//div[@id="Zoom1"]//p/text()| \
                                            //div[@id="Zoom1"]//div/text()').extract())
        if not content:
            content = '这可能是图片或者文件，打开查看！'
        item['content'] = content.replace('\u3000', '')
        yield item
