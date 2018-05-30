# -*- coding: utf-8 -*-
import datetime
import time
import scrapy
from fagaiwei.settings import session, NewsItemInfo
from fagaiwei.keyword_others import keyword
from fagaiwei.items import FagaiweiItem


class GuojizaixianSpider(scrapy.Spider):
    name = 'guojizaixian'
    allowed_domains = ['cri.cn']
    start_urls = ['http://cri.cn/']

    def start_requests(self):
        urls = [
            "http://news.cri.cn/roll",  # 国际在线 新闻滚动
        ]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        message_list = response.xpath('//div[@class="list-box"]/div/ul/li')
        # print(len(message_list))
        for message in message_list:
            date = "".join(message.xpath('div/h4/i/text()').extract())
            # date = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
            title = "".join(message.xpath('div/h4/a[1]/text()').extract()).replace(" ", "").replace("\n", "")
            href = "".join(message.xpath('div/h4/a[1]/@href').extract())
            date = time.strftime('%Y', time.localtime(time.time())) + "-" + date
            # print(date)
            try:
                date = datetime.datetime.strptime(str(date).replace('/', '-'), '%Y-%m-%d %H:%M')
                # print(date)
            except Exception as e:
                # print(e)
                date = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
            # print(date)
            # print(title, href)
            if "http" in href:
                url = href
            else:
                url = "http://news.cri.cn" + href
            result = session.query(NewsItemInfo).filter_by(url=url, web_id=47).count()
            if result:
                # print("{} 存在".format(url))
                pass
            else:
                yield scrapy.Request(url=url, callback=self.get_detail,
                                     meta={"date": date, "title": title, "laiyuan": response.url})

    def get_detail(self, response):
        item = FagaiweiItem()
        item["url"] = response.url
        pub_time = response.meta["date"]
        if pub_time:
            item["pub_time"] = pub_time
        else:
            item["pub_time"] = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
        item["title"] = response.meta["title"]
        form_s = "".join(response.xpath('//*[@id="asource"]/a/text()').extract())
        if form_s:
            item["webname"] = form_s
        else:
            item["webname"] = "国际在线 新闻"
        web_form = "".join(response.xpath('//*[@id="asource"]/a/@href').extract())
        if web_form:
            item["web"] = web_form
        else:
            item["web"] = response.meta["laiyuan"]
        item["web_id"] = 47
        contents = "".join(response.xpath('//*[@id="abody"]/p/text()|//*[@id="abody"]/p/a/text()').extract())
        if contents:
            item["content"] = contents.replace("\u3000", "")
        else:
            item["content"] = "可能是图片 请打开原文链接查看"
        # print(item)
        item["keyword"] = keyword.get_keyword(item["content"])
        return item
