# -*- coding: utf-8 -*-
import time
import requests
from lxml import etree
import scrapy
from fagaiwei.settings import DEFAULT_REQUEST_HEADERS
from fagaiwei.settings import session, NewsItemInfo
from fagaiwei.keyword_others import keyword
from fagaiwei.items import FagaiweiItem


class HuaerjiejianwenSpider(scrapy.Spider):
    name = 'huaerjiejianwen'
    allowed_domains = ['wallstreetcn.com', "weexcn.com"]
    start_urls = ['http://wallstreetcn.com/']

    def start_requests(self):
        urls = [
            "https://wallstreetcn.com/news/global",  # 华尔街见闻 最新
            "https://wallstreetcn.com/news/shares",  # 华尔街见闻 股市
            "https://wallstreetcn.com/news/bonds",  # 华尔街见闻 债市
            "https://wallstreetcn.com/news/commodities",  # 华尔街见闻 商品
            "https://wallstreetcn.com/news/forex",  # 华尔街见闻 外汇
            "https://wallstreetcn.com/news/enterprise",  # 华尔街见闻 公司
            "https://wallstreetcn.com/news/economy",  # 华尔街见闻 经济
            "https://wallstreetcn.com/news/charts",  # 华尔街见闻 数据
            "https://wallstreetcn.com/news/china",  # 华尔街见闻 中国
            "https://wallstreetcn.com/news/us",  # 华尔街见闻 美国
            "https://wallstreetcn.com/news/europe",  # 华尔街见闻 欧洲
            "https://wallstreetcn.com/news/japan",  # 华尔街见闻 日本
        ]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        message_list = response.xpath('//div[@class="wscn-tabs__content"]/div/div')
        # print(len(message_list))
        for message in message_list:
            # date = "".join(message.xpath('span/a/text()|span/text()').extract())
            # date = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
            title = "".join(message.xpath('div/div/a[1]/text()').extract()).replace(" ", "").replace("\n", "")
            href = "".join(message.xpath('div/div/a[1]/@href').extract())
            # print(title, href)
            if "http" in href:
                url = href
            else:
                url = "https://wallstreetcn.com" + href
            result = session.query(NewsItemInfo).filter_by(url=url, web_id=46).count()
            if result:
                # print("{} 存在".format(url))
                pass
            else:
                yield scrapy.Request(url=url, callback=self.get_detail,
                                     meta={"title": title, "laiyuan": response.url})

    def get_detail(self, response):
        item = FagaiweiItem()
        item["url"] = response.url
        date = "".join(response.xpath('//div[@class="article__heading"]/div/div/span/text()').extract())
        pub_time = date.split("\n")[0]
        if pub_time:
            item["pub_time"] = pub_time
        else:
            item["pub_time"] = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
        item["title"] = response.meta["title"]
        item["webname"] = "华尔街见闻"
        item["web"] = response.meta["laiyuan"]
        item["web_id"] = 46
        contents = "".join(response.xpath('//div[@class="article__content"]/div/div/text()|\
                                           //div[@class="article__content"]/div/div/p/text()|\
                                           //div[@class="article__content"]/div/div/p/strong/text()|\
                                           //div[@class="article__content"]/div/div/h2/text()|\
                                           //div[@class="article__content"]/div/div/h2/strong/text()|\
                                           //div[@class="article__content"]/div/p/text()|\
                                           //div[@class="article__content"]/div/p/strong/text()|\
                                           //div[@class="article__content"]/div/h2/text()|\
                                           //div[@class="pa-main__content preview"]/p/text()|\
                                           //div[@class="pa-main__content preview"]/p/strong/text()|\
                                           //div[@class="pa-main__content"]/p/text()|\
                                           //div[@class="pa-main__content"]/p/span/text()|\
                                           //div[@class="pa-main__content"]/p/span/span/text()|\
                                           //div[@class="pa-main__content"]/p/span/strong/text()|\
                                           //div[@class="pa-main__content"]/p/span/strong/span/text()|\
                                           //div[@class="article__content"]/div/div/h2/p/text()').extract())
        # print(contents)
        if contents != "":
            item["content"] = contents.replace("\u3000", "").replace("\xa0", "")
        else:
            u = response.url
            article_id = u.split('/')[-1]
            url = "https://api-prod.wallstreetcn.com/apiv1/content/articles/{}?extract=0".format(article_id)
            # url = "https://api-prod.wallstreetcn.com/apiv1/content/articles/3297387?extract=0"
            res = requests.get(url, headers=DEFAULT_REQUEST_HEADERS)
            result = res.json()
            ress = result["data"]["content"]
            tree = etree.HTML(ress)
            content_sss = "".join(tree.xpath('//p/text()|//span/text()|//strong/text()'))
            # print(content_sss)
            if content_sss:
                item["content"] = content_sss
            else:
                item["content"] = "可能是图片 请打开详情页查看"
        item["keyword"] = keyword.get_keyword(item["content"])
        if item["url"] == item["web"]:
            pass
        else:
            # pass
            # print(item)
            return item
