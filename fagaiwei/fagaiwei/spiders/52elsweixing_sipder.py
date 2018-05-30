# -*- coding: utf-8 -*-
import time
import scrapy
from fagaiwei.items import FagaiweiItem
from fagaiwei.settings import session, NewsItemInfo
from fagaiwei.keyword_others import keyword


class xiamenSipderSpider(scrapy.Spider):
    name = 'elsweixing_sipder'
    allowed_domains = ['sputniknews.cn']

    start_urls = [
        'http://sputniknews.cn/archive/',
    ]

    def parse(self, response):
        xq_urls = response.xpath("//h2[@class='b-plainlist__title']/a/@href").getall()
        lz_url = response.url
        for url in xq_urls:
            urls = 'http://sputniknews.cn' + url
            # print(urls)
            result = session.query(NewsItemInfo).filter_by(url=urls.replace("\n", ""), web_id=52).count()
            if result:
                # print("{} 存在".format(urls))
                pass
            else:
                yield scrapy.Request(url=urls, callback=self.parse_page, meta={'url': lz_url})

    def parse_page(self, response):
        item = FagaiweiItem()
        item['webname'] = '俄罗斯卫星通讯社'
        item['title'] = ''.join(list(response.xpath("//h1/text()").get())).replace('\u3000', '')
        times = response.xpath("//time[@class='b-article__refs-date']/@datetime").get()
        item['pub_time'] = times.replace('T', ' ')
        item['web'] = response.meta['url']
        item['url'] = response.url.replace("\n", "")
        content1 = ''.join(list(response.xpath("//div[@class='b-article__lead']//text()").getall()))
        content2 = ''.join(list(response.xpath("//div[@class='b-article__text']//text()").getall())).replace(
            '\u3000', '').replace('\t', '').replace('\r', '').replace('©', '').replace('\xa0', '')
        item['content'] = content1 + content2
        item['add_time'] = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        item["keyword"] = keyword.get_keyword(item["content"])
        item['web_id'] = 52
        # print(item)
        return item
