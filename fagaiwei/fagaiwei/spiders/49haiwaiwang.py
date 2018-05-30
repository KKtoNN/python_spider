# -*- coding: utf-8 -*-
import datetime
import json
import time
from lxml import etree
import scrapy
from fagaiwei.settings import session, NewsItemInfo
from fagaiwei.keyword_others import keyword
from fagaiwei.items import FagaiweiItem


class HaiwaiwangSpider(scrapy.Spider):
    name = 'haiwaiwang'
    allowed_domains = ['haiwainet.cn']
    start_urls = ['http://haiwainet.cn/']

    # "http://opa.haiwainet.cn/news/detail/31307637",  # 详细内容链接
    def start_requests(self):
        urls = [
            # "http://opa.haiwainet.cn/apis/news?catid=3541083&num=10&page=1&moreinfo=1&relation=1",  # 滚动部门
            # "http://opa.haiwainet.cn/apis/news?catid=3541088&num=10&seat=1&page=1&moreinfo=1&relation=1",  # 国际
            # "http://opa.haiwainet.cn/apis/news?catid=3541086&num=10&seat=1&page=1&moreinfo=1&relation=1",  # 国内
            # "http://opa.haiwainet.cn/apis/news?catid=3541093&num=10&seat=1&page=1&moreinfo=1&relation=1",  # 原创
            # "http://opa.haiwainet.cn/apis/news?catid=3541085&num=10&seat=1&page=1&moreinfo=1&relation=1",  # 首页
            "http://tw.haiwainet.cn/scroll-news/",  # 台湾>滚动>正文
            "http://hk.haiwainet.cn/news/",  # 香港频道>香港动态>
            "http://hk.haiwainet.cn/cjzh/",  # 香港频道>财经展会>
            "http://hk.haiwainet.cn/hkms/",  # 香港频道>香港民生>
            "http://mac.haiwainet.cn/cjzh/",  # 澳门频道>财经展会>
            "http://mac.haiwainet.cn/amdt/",  # 澳门频道>澳门动态>
            "http://nanhai.haiwainet.cn/observe/",  # 中国南海新闻网>南海观察>

        ]
        for url in urls:
            if "opa.haiwainet.cn" in str(url):
                yield scrapy.Request(url=url, callback=self.parse)
            else:
                yield scrapy.Request(url=url, callback=self.parse_2)

    def parse(self, response):
        result = json.loads(response.text)
        # print(result)
        message_list = result["result"]
        for message in message_list:
            guid = message["guid"]
            title = message["title"]
            link = message["link"]
            keywords = message["keywords"]
            pubtime = message["pubtime"]
            source = message["source"]
            try:
                pubtime = datetime.datetime.strptime(str(pubtime).replace('/', '-'), '%Y-%m-%d %H:%M:%S')
                # print(date)
            except Exception as e:
                # print(e)
                pubtime = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
            # print(guid, title, link, keywords, pubtime, source)
            url = "http://opa.haiwainet.cn/news/detail/{}".format(guid)
            result = session.query(NewsItemInfo).filter_by(url=url, web_id=49).count()
            if result:
                # print("{} 存在".format(url))
                pass
            else:
                yield scrapy.Request(url=url, callback=self.get_detail,
                                     meta={"title": title, "link": link, "keyword": keywords,
                                           "pubtime": pubtime, "source": source, "laiyuan": response.url})

    def parse_2(self, response):
        message_list = response.xpath('//div[@class="show_body clearfix"]/div[1]/ul/li')
        for message in message_list:
            title = "".join(message.xpath('a/text()').extract())
            href = "".join(message.xpath('a/@href').extract())
            date = "".join(message.xpath('span/text()').extract())
            date = date.replace("年", "-").replace("月", "-").replace("日", "")
            # print(date)
            try:
                date = datetime.datetime.strptime(str(date).replace('/', '-'), '%Y-%m-%d %H:%M')
                # print(date)
            except Exception as e:
                # print(e)
                date = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
            # print(title, href, date)
            result = session.query(NewsItemInfo).filter_by(url=href, web_id=49).count()
            if result:
                # print("{} 存在".format(href))
                pass
            else:
                yield scrapy.Request(url=href, callback=self.get_detail_2,
                                     meta={"title": title, "date": date, "laiyuan": response.url})

    def get_detail(self, response):
        item = FagaiweiItem()
        item["url"] = response.meta["link"]
        item["pub_time"] = response.meta["pubtime"]
        item["title"] = response.meta["title"]
        item["webname"] = response.meta["source"]
        item["web"] = response.meta["laiyuan"]
        item["keyword"] = response.meta["keyword"]
        item["web_id"] = 49
        result = json.loads(response.text)
        body = result["result"]["body"]
        tree = etree.HTML(body)
        contents = "".join(tree.xpath('//p/text()|//strong/text()'))
        if contents:
            item["content"] = contents.replace("\u3000", "").replace("\r", "").replace("\u200b", "").replace("\xa0", "")
        else:
            item["content"] = "可能是图片 打开原文链接查看"
        # print(item)

        return item

    def get_detail_2(self, response):
        item = FagaiweiItem()
        item["url"] = response.url
        item["pub_time"] = response.meta["date"]
        item["title"] = response.meta["title"]
        item["webname"] = "".join(response.xpath('//div[@class="contentExtra"]/span[2]/a/text()|\
                                                //div[@class="extra mlr20"]/span[2]/text()|\
                                                //*[@id="source_baidu"]/text()').extract()) \
            .replace("来源：", "")
        if not item["webname"]:
            item["webname"] = "新华国际"
        item["web"] = "".join(response.xpath('//div[@class="contentExtra"]/span[2]/a/@href').extract())
        if not item["web"]:
            item["web"] = response.meta["laiyuan"]
        item["web_id"] = 49

        contents = "".join(response.xpath('//div[@class="contentMain"]/p/text()|\
                                            //div[@class="contentMain"]/p/a/text()|\
                                            //*[@id="cen"]/p/a/text()|\
                                            //*[@id="con"]/p/text()|\
                                            //*[@id="con"]/p/a/text()|\
                                            //*[@id="cen"]/p/text()').extract())
        if contents:
            item["content"] = contents.replace("\u3000", "").replace("\r", "").replace("\u200b", "").replace("\xa0", "")
        else:
            item["content"] = "可能是图片 打开原文链接查看"
        # print(item)
        item["keyword"] = keyword.get_keyword(item["content"])
        return item
