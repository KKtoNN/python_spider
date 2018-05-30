# -*- coding: utf-8 -*-
import scrapy
from datetime import datetime
from fagaiwei.settings import session, NewsItemInfo
from fagaiwei.keyword_others import keyword
from fagaiwei.items import FagaiweiItem


class ZjzxSpider(scrapy.Spider):
    # 财经网
    name = 'cjw'
    allowed_domains = ['caijing.com.cn']
    start_urls = [
        # 'http://inno.caijing.com.cn/'   , #因果财经
        'http://economy.caijing.com.cn/index.html',  # 宏观首页
        'http://stock.caijing.com.cn/index.html',  # 证券首页
        'http://finance.caijing.com.cn/index.html',  # 金融首页

    ]

    def parse(self, response):
        url_list = response.xpath('//div[contains(@class,"ls_news")]/div[1]/a/@href').extract()
        for url in url_list:
            result = session.query(NewsItemInfo).filter_by(url=url, web_id=50).count()
            if result:
                # print("{} 存在".format(url))
                pass
            else:
                yield scrapy.Request(url, callback=self.process_detail, meta={'web': response.url})

    def process_detail(self, response):
        item = FagaiweiItem()
        item['web_id'] = 50
        item['url'] = response.url
        item['title'] = response.xpath('//h2[@id="cont_title"]/text()').extract_first(default='')
        item['web'] = response.meta.get('web')
        item['keyword'] = ''
        item['webname'] = response.xpath(
            '//span[@id="source_baidu"]/a/text()|//span[@id="source_baidu"]/text()').extract_first(default='财经网')
        item['pub_time'] = response.xpath('//span[@id="pubtime_baidu"]/text()').extract_first(datetime.now())
        content = '\n'.join(response.xpath('//div[@id="the_content"]/p/text()').extract())
        if not content:
            content = '这可能是图片或者文件，打开查看！'
        item['content'] = content
        yield item
