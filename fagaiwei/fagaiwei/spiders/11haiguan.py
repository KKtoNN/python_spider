# -*- coding: utf-8 -*-
import datetime
import time
import scrapy
from fagaiwei.settings import session, NewsItemInfo
from fagaiwei.items import FagaiweiItem
from fagaiwei.keyword_others import keyword


class HaiguanSpider(scrapy.Spider):
    name = 'haiguan'
    allowed_domains = ['customs.gov.cn']
    start_urls = ['http://customs.gov.cn/']

    def start_requests(self):
        urls = [
            "http://www.customs.gov.cn/customs/302249/ywjj/index.html",  # 信息公开-要闻聚焦
            "http://www.customs.gov.cn/customs/302249/mtjj35/index.html",  # 信息公开-媒体聚焦
            # "http://www.customs.gov.cn/customs/302249/302426/index.html",  # 信息公开-国务院要闻=重复了 国务院里爬过了
            "http://www.customs.gov.cn/customs/302249/302425/index.html",  # 信息公开-今日海关
            "http://www.customs.gov.cn/customs/zsgk93/302256/302258/index.html",  # 信息公开-总署概况-总署通告-最新署令
            "http://www.customs.gov.cn/customs/zsgk93/302256/302257/index.html",  # 信息公开-总署概况-总署通告-最新公告
            "http://www.customs.gov.cn/customs/302452/302457/jqzxxwfb/index.html",  # 信息公开-总署概况-总署通告-近期在线新闻发布
        ]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        # print(response.text)
        message_list = response.xpath('//ul[@class="conList_ul"]/li|\
                                        //ul[@class="govpushinfo150203"]/li')
        # print(len(message_list))
        for message in message_list:
            title = "".join(message.xpath('a/text()').extract())
            href = "".join(message.xpath('a/@href').extract())
            date = "".join(message.xpath('span/text()').extract())
            # print(title, href, date)
            try:
                date = datetime.datetime.strptime(str(date).replace('/', '-'), '%Y-%m-%d')
                # print(date)
            except Exception as e:
                # print(e)
                date = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
            if "http://fangtan.customs.gov.cn" in href:
                url = href
            else:
                url = "http://www.customs.gov.cn" + href
            result = session.query(NewsItemInfo).filter_by(url=url, web_id=11).count()
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
        item["webname"] = "海关总署"
        item["web"] = response.meta["laiyuan"]
        item["web_id"] = 11
        contents = "".join(response.xpath('//*[@id="easysiteText"]/p/text()|\
                                            //p[@class="p1"]/text()|\
                                            //p[@class="p1"]/span/text()|\
                                            //*[@id="easysiteText"]/p/strong/text()|\
                                            //*[@id="easysiteText"]/p/strong/text()').extract())
        # print(contents)
        if contents != "":
            item["content"] = contents.replace("\u3000", "").replace("\xa0", "")
        else:
            item["content"] = "可能是图片 请打开详情页查看"
        item["keyword"] = keyword.get_keyword(item["content"])
        return item
