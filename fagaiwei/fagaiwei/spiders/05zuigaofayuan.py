# -*- coding: utf-8 -*-
import time
import datetime
import scrapy
from fagaiwei.settings import session, NewsItemInfo
from fagaiwei.items import FagaiweiItem
from fagaiwei.keyword_others import keyword


class ZuigaofayuanSpider(scrapy.Spider):
    name = 'zuigaofayuan'
    allowed_domains = ['court.gov.cn']
    start_urls = ['http://court.gov.cn/']

    def start_requests(self):
        urls = [
            "http://www.court.gov.cn/zixun-gengduo-23.html",  # 要闻
            "http://www.court.gov.cn/zixun-gengduo-24.html",  # 最高人民法院新闻
            "http://www.court.gov.cn/zixun-gengduo-25.html",  # 地方法院新闻
            "http://www.court.gov.cn/zixun-gengduo-26.html",  # 新闻发布会
            "http://www.court.gov.cn/zixun-gengduo-39.html",  # 发布会实录
            "http://www.court.gov.cn/zixun-gengduo-40.html",  # 图文直播
            "http://www.court.gov.cn/zixun-gengduo-104.html",  # 典型案例发布
        ]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        message_list = response.xpath('//*[@id="container"]/div/ul/li')
        for message in message_list:
            title = "".join(message.xpath('a/text()').extract())
            href = "".join(message.xpath('a/@href').extract())
            date = "".join(message.xpath('i/text()').extract())
            # print(title, href, date)
            try:
                date = datetime.datetime.strptime(str(date).replace('/', '-'), '%Y-%m-%d')
                # print(date)
            except Exception as e:
                # print(e)
                date = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))

            url = "http://www.court.gov.cn" + href
            result = session.query(NewsItemInfo).filter_by(url=url, web_id=5).count()
            if result:
                # print("{} 存在".format(url))
                pass
            else:
                yield scrapy.Request(url=url, callback=self.get_detail,
                                     meta={"date": date, "title": title, "laiyuan": response.url})

    def get_detail(self, response):
        item = FagaiweiItem()
        item["url"] = response.url
        item["title"] = response.meta["title"]
        item["web"] = response.meta["laiyuan"]
        contents = "".join(response.xpath('\
                            //*[@id="zoom"]/p/text()|\
                            //*[@id="zoom"]/p/strong/text()|\
                            //*[@id="zoom"]/p/span/text()|\
                            //*[@id="zoom"]/p/span/span/text()|\
                            //*[@id="zoom"]/p/span/strong/span/text()|\
                            //*[@id="zoom"]/strong/text()|\
                            //*[@id="zoom"]/span/text()|\
                            //*[@id="zoom"]/div/span/text()|\
                            //*[@id="zoom"]/text()').extract())

        item["content"] = contents.replace("\u3000", "")
        form_s = "".join(response.xpath('//*[@id="container"]/div/div[2]/ul[1]/li[1]/text()').extract())
        if form_s == "":
            form_s = "最高人民法院新闻"
        item["webname"] = form_s.replace("来源：", "")
        date = "".join(response.xpath('//*[@id="container"]/div/div[2]/ul[1]/li[2]/text()').extract())
        date_s = date.split("间")[-1][1:]
        if date_s == "":
            date_s = response.meta["date"]
        item["pub_time"] = date_s
        item["web_id"] = 5
        item["keyword"] = keyword.get_keyword(item["content"])

        # print(item)
        return item
