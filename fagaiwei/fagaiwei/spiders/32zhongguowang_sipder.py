# -*- coding: utf-8 -*-
import re
import time
import scrapy
from fagaiwei.items import FagaiweiItem
from fagaiwei.keyword_others import keyword
from fagaiwei.settings import session, NewsItemInfo


class ZhongguowangSipderSpider(scrapy.Spider):
    name = 'china_sipder'
    allowed_domains = ['media.china.com.cn']
    # start_urls = ['http://media.china.com.cn/']
    PUB_URL = 'http://media.china.com.cn'

    def start_requests(self):
        urls = [
            "http://media.china.com.cn/cmyw/",
            "http://media.china.com.cn/gdxw/",
            "http://media.china.com.cn/ftzb/",
            "http://media.china.com.cn/cmjujiao/",
            "http://media.china.com.cn/dfcm/",
            "http://media.china.com.cn/cmsp/",
            "http://media.china.com.cn/cmgc/",
            "http://media.china.com.cn/cmrw/",
            "http://media.china.com.cn/yqfw/",
            "http://media.china.com.cn/cmgl/",
            "http://media.china.com.cn/cmcy/",
            "http://media.china.com.cn/cmwx/",
            "http://media.china.com.cn/ty/",
            "http://media.china.com.cn/cmyj/",
            "http://media.china.com.cn/hzlt/",
            "http://media.china.com.cn/it/",
            "http://media.china.com.cn/cmys/",
        ]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        urls = response.xpath("//p[@class='bt']/a/@href")[0:14].getall()
        for url in urls:
            url_s = self.PUB_URL + url
            result = session.query(NewsItemInfo).filter_by(url=url_s, web_id=32).count()
            if result:
                # print("{} 存在".format(url_s))
                pass
            else:
                yield scrapy.Request(url=url_s, callback=self.parse_page, meta={'web_url': response.url})

    def parse_page(self, response):
        item = FagaiweiItem()
        laiyuans = response.xpath("//div[@class='rqly']")
        for laiyuan in laiyuans:
            data_time = laiyuan.xpath("./text()").get()
            item['pub_time'] = re.search('^[0-9]{4}-[0-9]{0,2}-[0-9]{0,2} [0-9]{0,2}:[0-9]{0,2}:[0-9]{0,2}',
                                         data_time).group()
            item['webname'] = laiyuan.xpath("./a/text()").get()
            web = laiyuan.xpath("./a/@href").get()
            if web == '':
                item['web'] = response.meta['web_url']
            else:
                item['web'] = web
        item['title'] = response.xpath("//h1/text()").get()
        item['content'] = ''.join(list(response.xpath("//div[@class='box_con']//text()").getall())).strip().replace(
            '\r', '').replace('\n', '').replace('\u3000', '').replace('\t', '')
        item['url'] = response.url
        item['add_time'] = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        item["keyword"] = keyword.get_keyword(item["content"])

        item['web_id'] = 32
        return item

        pass
