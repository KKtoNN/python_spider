# -*- coding: utf-8 -*-
import re
import time
from datetime import datetime
import scrapy
from fagaiwei.items import FagaiweiItem
from fagaiwei.settings import session, NewsItemInfo
from fagaiwei.keyword_others import keyword


class HostnewsSpider(scrapy.Spider):
    # 热点新闻
    name = 'hostnews'
    allowed_domains = ['kan.china.com']
    start_urls = ['http://kan.china.com/data/jsonp/?path=list_3_1&__t={}&callback=__callbackHomeData'.format(
        str(time.time())[0:8]),
        # 军事
        'http://kan.china.com/data/jsonp/?path=list_9_1&__t={}&callback=__callbackHomeData '.format(
            str(time.time())[0:8]),
        # 国际
        'http://kan.china.com/data/jsonp/?path=list_12_1&__t={}&callback=__callbackHomeData'.format(
            str(time.time())[0:8])
        # 财经
    ]

    def parse(self, response):
        url_list = re.findall(r'(/article.*?html)', response.text)
        for url in url_list:
            url = url.replace('\\', '')
            result = session.query(NewsItemInfo).filter_by(url='http://kan.china.com' + url, web_id=34).count()
            if result:
                # print("{} 存在".format('http://kan.china.com' + url))
                pass
            else:
                yield scrapy.Request('http://kan.china.com' + url, callback=self.process_detail)

    def process_detail(self, response):
        item = FagaiweiItem()
        item['web_id'] = 34
        item['url'] = response.url
        item['title'] = response.xpath('//div[@class="article-header"]/h1/text()').extract_first(default='')
        item['web'] = 'http://kan.china.com/'
        item['webname'] = response.xpath('//*[@id="article-source"]/text()').extract_first(default='热点新闻')
        item['pub_time'] = response.xpath('//*[@id="article-data"]/text()').extract_first(default=datetime.now())
        item['content'] = '\n'.join(response.xpath('//*[@id="main-content"]/p/text() | \
                                           //*[@id="main-content"]/p/strong/text() | \
                                           //*[@id="main-content"]/p/strong/span/text()').extract())
        item["keyword"] = keyword.get_keyword(item["content"])
        yield item
