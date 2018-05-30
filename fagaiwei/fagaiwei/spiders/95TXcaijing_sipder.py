# coding:utf-8
import scrapy

import jsonpath
from fagaiwei.items import FagaiweiItem
import time
from fagaiwei.settings import session, NewsItemInfo


class xiamenSipderSpider(scrapy.Spider):
    name = 'TXcaijing_sipder'
    allowed_domains = ['qq.com']
    start_urls = [
        'http://finance.qq.com/hgjj.htm',  # 宏观经济
        'http://finance.qq.com/gdyw.htm',  # 滚动要闻
        'http://finance.qq.com/jrsc.htm',  # 金融市场
        'http://finance.qq.com/gjcj.htm',  # 国际财经

    ]

    def parse(self, response):
        urls = response.xpath("//div[@class='Q-tpWrap']/em/a/@href|"
                              "//h3/a/@href").getall()
        for url in urls:
            url = 'https://finance.qq.com' + url
            result = session.query(NewsItemInfo).filter_by(url=url, web_id=95).count()
            if result:
                # print("URL文件地址： {} 存在".format(url))
                pass
            else:
                yield scrapy.Request(url=url, callback=self.parse_page,
                                     meta={'url': response.url})

    def parse_page(self, response):
        item = FagaiweiItem()
        pub_time = response.xpath("//span[@class='a_time']/text()").get()
        item['title'] = response.xpath("//h1/text()").get()
        laiyuan = response.xpath("//span[@class='a_source']/a/text()").get()
        laiyuan_url = response.xpath("//span[@class='a_source']/a/@href").get()
        content = ''.join(list(response.xpath("//div[@class='Cnt-Main-Article-QQ']//p[not(script)]//text()").getall()))
        if laiyuan is None:
            item['webname'] = '腾讯财经'
        else:
            item['webname'] = laiyuan
        if laiyuan_url is None:
            item['web'] = response.meta['url']
        else:
            item['web'] = laiyuan_url

        item['url'] = response.url

        if pub_time is not None:
            item['pub_time'] = pub_time
        else:
            item['pub_time'] = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())

        if content == '':
            item['content'] = '请点击原文来链接查看'
        else:
            item['content'] = content

        item['add_time'] = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        item['keyword'] = ''
        item['web_id'] = 95
        # print(item)
        yield item
