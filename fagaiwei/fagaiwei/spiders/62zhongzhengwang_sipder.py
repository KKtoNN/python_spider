# -*- coding: utf-8 -*-
import time
import scrapy
from fagaiwei.items import FagaiweiItem
from fagaiwei.settings import session, NewsItemInfo
from fagaiwei.keyword_others import keyword


class ZhongZhengSipderSpider(scrapy.Spider):
    name = 'zhongzhengwang_sipder'
    allowed_domains = ['cs.com.cn']

    start_urls = [
        'http://www.cs.com.cn/sylm/jsxw/',
    ]

    def parse(self, response):

        pub_url = 'http://www.cs.com.cn/'
        urls = response.xpath("//div[contains(@class,'fl')]//dt/a/@href").getall()
        # print(urls)
        for url in urls:
            if url.startswith('./'):
                url = url.replace('./', '')
                url = response.url + url
            else:
                url = url.replace('../', '')
                url = pub_url + url
            result = session.query(NewsItemInfo).filter_by(url=url, web_id=62).count()
            if result:
                # print("{} 存在".format(url))
                pass
            else:
                yield scrapy.Request(url=url, callback=self.parse_page)

    def parse_page(self, response):
        item = FagaiweiItem()
        item['url'] = response.url
        item['pub_time'] = response.xpath("//span[@class='Ff']/text()").get()
        item['title'] = response.xpath("//h1/text()").get()
        content1 = ' '.join(list(response.xpath("//div[@class='artical_t']//span//text()")[0:-1].getall()))
        content2 = '\n'.join(list(response.xpath("//div[@class='artical_c']/p/text()").getall())) \
            .replace('\u3000', '').replace('\xa0', '')
        item['content'] = content1 + '\n' + content2
        item['web'] = 'http://www.cs.com.cn/sylm/jsxw/'
        item['webname'] = '中证网'
        item['add_time'] = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        item["keyword"] = keyword.get_keyword(item["content"])
        item['web_id'] = 62
        return item
        pass
