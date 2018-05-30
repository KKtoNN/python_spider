# -*- coding: utf-8 -*-
import re
import time
import scrapy
from fagaiwei.items import FagaiweiItem
from fagaiwei.settings import session, NewsItemInfo
from fagaiwei.keyword_others import keyword


class xiamenSipderSpider(scrapy.Spider):
    name = 'zgzhengjuanwang_spider'
    allowed_domains = ['cnstock.com']

    def start_requests(self):
        urls = [
            "http://news.cnstock.com/news/sns_yw/index.html",
            "http://blog.cnstock.com/NewsList.aspx?cat=djsy",
            "http://news.cnstock.com/industry/sid_rdjj",
            "http://news.cnstock.com/bwsd/index.html",
        ]

        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        urls = response.xpath("//ul[contains(@class,'article-mini')]//li/a/@href|"
                              "//ul[@class='nf-list']//a/@href").getall()
        urla = response.url
        for url in urls:
            # print("{}+++++++++++++++{}".format(urla, url))
            result = session.query(NewsItemInfo).filter_by(url=url, web_id=66).count()
            if result:
                # print("{} 存在".format(url))
                pass
            else:
                yield scrapy.Request(url=url, callback=self.parse_page, meta={'url': urla})

    def parse_page(self, response):
        item = FagaiweiItem()
        item['url'] = response.url
        times = ''.join(list(response.xpath("//span[@class='timer']//text()|"
                                            "//div[@class='ll-time']/text()|"
                                            "//td[@class='name']//text()[-1]").getall()))
        if times is not None:
            time5 = re.search(r'^[0-9]{4}-[0-9]{0,2}-[0-9]{0,2} [0-9]{0,2}:[0-9]{0,2}:[0-9]{0,2}', times)
            if time5 is not None:
                item['pub_time'] = time5.group()
            else:
                item['pub_time'] = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        else:
            item['pub_time'] = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())

        item['title'] = ''.join(list(response.xpath("//h1//text()|"
                                                    "//div[@class='title']/text()").get())) \
            .replace('&nbsp', '').replace('\xa0', '')
        content1 = ' '.join(list(response.xpath("//span[@class='author']/text()").getall()))
        content2 = '\n'.join(list(response.xpath("//div[@class='content']/p/text()|"
                                                 "//div[@class='logtext']//p//text()|"
                                                 "//div[@class='logtext']//text()|"
                                                 "//td[@class='logtext']//text()|"
                                                 "//p[@class='des']/text()").getall())) \
            .replace('\u3000', '').replace('\xa0', '')
        if content1 != '':
            item['content'] = content1 + '\n' + content2
        else:
            if content2 == '':
                item['content'] = '请点击原文链接查看'
            else:
                item['content'] = content2

        item['web'] = response.meta['url']
        laiyuan = response.xpath("//span[@class='source']/text()").get()
        if laiyuan is not None:
            laiyuan = laiyuan.replace('来源：', '')
            if laiyuan == '':
                item['webname'] = '中国证券网'
            else:

                item['webname'] = laiyuan
        else:
            item['webname'] = '中国证券网'

        item['add_time'] = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        item["keyword"] = keyword.get_keyword(item["content"])
        item['web_id'] = 66
        # print(item)
        return item
        pass
