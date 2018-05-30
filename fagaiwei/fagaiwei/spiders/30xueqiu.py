# -*- coding: utf-8 -*-
import json
import time
from datetime import datetime
import scrapy
import demjson
from fagaiwei.items import FagaiweiItem
from fagaiwei.keyword_others import keyword
from fagaiwei.settings import session, NewsItemInfo


class ZjzxSpider(scrapy.Spider):
    # 雪球网
    name = 'xueqiu'
    allowed_domains = ['xueqiu.com']
    category_code = ['105', '111', '102', '110', '104', '101']  # 分别为 沪深 房产  港股 保险 基金 美股code
    start_urls = (
        'https://www.xueqiu.com/v4/statuses/public_timeline_by_category.json?since_id=-1&max_id=-1&count=10&category=' + code
        for code in category_code)

    def start_requests(self):
        url = 'https://www.xueqiu.com'
        yield scrapy.Request(url, callback=self.first)

    def first(self, response):
        for url in self.start_urls:
            yield scrapy.Request(url, callback=self.parse)

    def parse(self, response):
        news_list = json.loads(response.text)['list']
        for news in news_list:
            data = demjson.decode(news['data'])
            url = data['target']
            # url=re.search(r'"target":\s?"(.*?)",',data).group(1)
            result = session.query(NewsItemInfo).filter_by(url='https://xueqiu.com' + url, web_id=30).count()
            if result:
                # print("{} 存在".format('https://xueqiu.com' + url))
                pass
            else:
                yield scrapy.Request('https://xueqiu.com' + url, callback=self.process_detail)

    def process_detail(self, response):
        item = FagaiweiItem()
        item['web_id'] = 30
        item['url'] = response.url
        item['title'] = response.xpath('//article[@class="article__bd"]/h1/text()').extract_first(default='')
        item['web'] = 'https://www.xueqiu.com'
        item['webname'] = response.xpath(
            '//article[@class="article__bd"]/div[@class="article__bd__from"]/a/text()').extract_first(default='雪球网')
        timestamp = response.xpath('//div[@class="avatar__subtitle"]/a/@data-created_at').extract_first(
            default=time.time())[:-3]
        item['pub_time'] = datetime.fromtimestamp(int(timestamp))
        item['content'] = '\n'.join(response.xpath('//div[@class="article__bd__detail"]/p/text() | \
                                          //div[@class="article__bd__detail"]/p/b/text()').extract())
        item["keyword"] = keyword.get_keyword(item["content"])

        yield item
