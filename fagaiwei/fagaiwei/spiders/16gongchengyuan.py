# -*- coding: utf-8 -*-
import datetime
import time
import scrapy
from fagaiwei.settings import session, NewsItemInfo
from fagaiwei.items import FagaiweiItem
from fagaiwei.keyword_others import keyword


class GongchengyuanSpider(scrapy.Spider):
    name = 'gongchengyuan'
    allowed_domains = ['cae.cn']
    start_urls = ['http://cae.cn/']

    def start_requests(self):
        urls = [
            "http://www.cae.cn/cae/html/main/col132/column_132_1.html",  # 首页 > 人才培养 > 教育部工程科技人才培养研究专项 > 通知公告
            "http://www.cae.cn/cae/html/main/col125/column_125_1.html",  # 首页 > 人才培养 > 工作动态
            "http://www.cae.cn/cae/html/main/col104/column_104_1.html",  # 首页 > 科技合作 > 要闻快递
            "http://www.cae.cn/cae/html/main/col84/column_84_1.html",  # 首页 > 战略咨询 > 研究动态
            "http://www.cae.cn/cae/html/main/col1/column_1_1.html",  # 首页 > 新闻 > 工程院要闻
        ]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        message_list = response.xpath('//div[@class="right_md_list"]/ul/li')
        for message in message_list:
            title = "".join(message.xpath('a/text()').extract())
            href = "".join(message.xpath('a/@href').extract())
            date = "".join(message.xpath('span/text()').extract())
            try:
                date = datetime.datetime.strptime(str(date).replace('/', '-'), '%Y-%m-%d')
                # print(date)
            except Exception as e:
                # print(e)
                date = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))

            url = "http://www.cae.cn" + href
            # print(title, url, date)
            result = session.query(NewsItemInfo).filter_by(url=url, web_id=16).count()
            if result:
                # print("{} 存在".format(url))
                pass
            else:
                yield scrapy.Request(url=url, callback=self.get_detail,
                                     meta={"title": title, "date": date, "laiyuan": response.url})

    def get_detail(self, response):
        item = FagaiweiItem()
        item["url"] = response.url
        item["pub_time"] = response.meta["date"]
        item["title"] = response.meta["title"]
        form_s = "".join(response.xpath('//div[@class="right_md_laiy"]/h4/text()').extract())
        form_s = form_s.split("　")[0].replace("一", "")
        if form_s != "":
            item["webname"] = form_s
        else:
            item["webname"] = "中国工程院"
        item["web"] = response.meta["laiyuan"]
        # item["keyword"] = ""
        item["web_id"] = 16
        contents = "".join(response.xpath('\
                                     //*[@id="zoom"]/div/p/text()|\
                                     //*[@id="zoom"]/div/p/span/text()|\
                                     //*[@id="zoom"]/strong/span/p/strong/text()|\
                                     //*[@id="zoom"]/p/text()|\
                                     //*[@id="zoom"]/p/a/text()|\
                                     //*[@id="zoom"]/p/b/span/text()|\
                                     //*[@id="zoom"]/p/strong/text()|\
                                     //*[@id="zoom"]/p/span/text()|\
                                     //*[@id="zoom"]/p/span/span/text()|\
                                     //*[@id="zoom"]/span/p/text()|\
                                     //*[@id="zoom"]/span/p/a/text()|\
                                     //*[@id="zoom"]/span/p/a/font/text()|\
                                     //*[@id="zoom"]/span/span/span/span/span/strong/span/span/strong/span/p/span/strong/span/span/strong/text()|\
                                     //*[@id="zoom"]/span/span/span/span/span/strong/span/span/p/span/text()|\
                                     //*[@id="zoom"]/span/span/span/span/span/strong/span/span/p/text()|\
                                     //*[@id="zoom"]/span/strong/span/span/p/strong/text()').extract())

        # print(contents)
        if contents != "":
            item["content"] = contents.replace("\u3000", "").replace("\xa0", "").replace("\u2002", "")
        else:
            item["content"] = "可能是图片 请打开详情页查看"
        item["keyword"] = keyword.get_keyword(item["content"])

        return item
