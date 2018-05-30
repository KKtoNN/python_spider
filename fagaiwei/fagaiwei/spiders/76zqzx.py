# -*- coding: utf-8 -*-
from datetime import datetime
import scrapy
from fagaiwei.items import FagaiweiItem
from fagaiwei.settings import session, NewsItemInfo
from fagaiwei.keyword_others import keyword


class ZjzxSpider(scrapy.Spider):
    # 证券之星
    name = 'zqzx'
    allowed_domains = ['stockstar.com']
    start_urls = [
        'http://finance.stockstar.com/list/1117.shtml',  # 市场评论
        'http://finance.stockstar.com/list/1303.shtml',  # 名家观点
        'http://finance.stockstar.com/list/2921.shtml',  # 行业观点
        'http://finance.stockstar.com/list/1221.shtml',  # 国内经济
        #   'http://www.stockstar.com/roll/all.shtml'      ,    #滚动新闻     其中有些链接超时 浏览器也无法打开  暂时不获取
    ]

    def parse(self, response):
        info_list = response.xpath('//div[contains(@class,"content")]/ul[@class="list-line"]/li')
        for info in info_list:
            url = info.xpath('./a/@href').extract_first(default='')
            if url:
                result = session.query(NewsItemInfo).filter_by(url=url, web_id=76).count()
                if result:
                    # print("{} 存在".format(url))
                    pass
                else:
                    title = info.xpath('./a/text()').extract_first(default='')
                    pub_time = info.xpath('./span/text()').extract_first(default=datetime.now())
                    yield scrapy.Request(url, callback=self.process_detail,
                                         meta={'web': response.url, 'title': title, 'pub_time': pub_time})

    def process_detail(self, response):
        item = FagaiweiItem()
        item['web_id'] = 76
        item['url'] = response.url
        item['title'] = response.meta.get('title')
        item['web'] = response.meta.get('web')
        item['webname'] = response.xpath('//span[@id="source_baidu"]/a/text() ').extract_first(default='证券之星综合')
        item['pub_time'] = response.meta.get('pub_time')
        content = '\n'.join(response.xpath('//div[@id="container-article"]/p/text() | \
                                 //div[@id="container-article"]/p/a/text()').extract())
        if not content:
            content = '这可能是图片或者文件，打开查看！'
        item['content'] = content
        item["keyword"] = keyword.get_keyword(item["content"])
        yield item
