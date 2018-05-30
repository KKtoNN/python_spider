# -*- coding: utf-8 -*-
import datetime
import time
import scrapy
from fagaiwei.settings import session, NewsItemInfo
from fagaiwei.keyword_others import keyword
from fagaiwei.items import FagaiweiItem


class HuanqiuxinwenSpider(scrapy.Spider):
    name = 'huanqiuxinwen'
    allowed_domains = ['huanqiu.com']
    start_urls = ['http://huanqiu.com/']

    def start_requests(self):
        urls = [
            "http://china.huanqiu.com/article/",  # 环球新闻 国内 滚动新闻
            "http://china.huanqiu.com/leaders/",  # 环球新闻 国内 高层动态
            "http://world.huanqiu.com/",  # 环球新闻 国际要闻
            "http://oversea.huanqiu.com/",  # 环球新闻 海外看中国
            "http://taiwan.huanqiu.com/?",  # 环球新闻 台海
            "http://mil.huanqiu.com/world/",  # 环球新闻 军情动态
        ]

        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        message_list = response.xpath('//div[@class="fallsFlow"]/ul/li|\
                                        //div[@class="listPad"]/ul/li|\
                                        //div[@class="leftList"]/ul/li')
        # print(len(message_list))
        for message in message_list:
            date = "".join(message.xpath('h6/text()').extract())
            if not date:
                date = time.strftime('%Y-%m-%d %H:%M', time.localtime(time.time()))
            title = "".join(message.xpath('h3/a/text()|a/dl/dt/h3/text()|a[1]/text()').extract()).replace(" ",
                                                                                                          "").replace(
                "\n", "")
            href = "".join(message.xpath('h3/a/@href|a[1]/@href').extract())
            # print(date)
            try:
                date = datetime.datetime.strptime(str(date).replace('/', '-'), '%Y-%m-%d %H:%M')
                # print(date)
            except Exception as e:
                # print(e)
                date = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
            # print(date)
            # print(title, href, date)
            if "http" in href:
                url = href
            else:
                url = "http://news.cri.cn" + href
            # print(date, url, title)
            result = session.query(NewsItemInfo).filter_by(url=url, web_id=35).count()
            if result:
                # print("{} 存在".format(url))
                pass
            else:
                yield scrapy.Request(url=url, callback=self.get_detail,
                                     meta={"date": date, "title": title, "laiyuan": response.url})

    def get_detail(self, response):
        item = FagaiweiItem()
        item["url"] = response.url
        pub_time = "".join(response.xpath('//span[@class="la_t_a"]/text()|//*[@id="pubtime_baidu"]/text()').extract())
        try:
            pub_time = datetime.datetime.strptime(str(pub_time).replace('/', '-'), '%Y-%m-%d %H:%M')
            try:
                pub_time = datetime.datetime.strptime(str(pub_time).replace('/', '-'), '%Y-%m-%d %H:%M:%S')
            except Exception as e:
                # print(e)
                pub_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
            # print(date)
        except Exception as e:
            # print(e)
            pub_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
        if pub_time:
            item["pub_time"] = pub_time
        else:
            item["pub_time"] = response.meta["date"]
        item["title"] = response.meta["title"]
        form_s = "".join(response.xpath('//span[@class="la_t_b"]/a/text()|//*[@id="source_baidu"]/a/text()').extract())
        if form_s:
            item["webname"] = form_s
        else:
            item["webname"] = "国际在线 新闻"
        web_form = "".join(response.xpath('//span[@class="la_t_b"]/a/@href').extract())
        if web_form:
            item["web"] = web_form
        else:
            item["web"] = response.meta["laiyuan"]
        item["web_id"] = 35
        contents = "".join(response.xpath('//div[@class="la_con"]/p/text()|\
                                            //*[@id="text"]/p/text()|\
                                            //*[@id="text"]/p/strong/text()').extract())
        if contents:
            item["content"] = contents.replace("\u3000", "").replace("\r", "").replace("\u200b", "").replace("\xa0", "")
        else:
            item["content"] = "可能是图片 打开原文链接查看"
        # print(item)
        item["keyword"] = keyword.get_keyword(item["content"])
        if item["url"] == "http://error.huanqiu.com/404.html":
            pass
        else:
            return item
