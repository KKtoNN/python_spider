# -*- coding: utf-8 -*-
import datetime
import time
import scrapy
from fagaiwei.settings import session, NewsItemInfo
from fagaiwei.keyword_others import keyword
from fagaiwei.items import FagaiweiItem


class ZjhnewsSpider(scrapy.Spider):
    name = 'zjhnews'
    allowed_domains = ['csrc.gov.cn']
    start_urls = ['http://csrc.gov.cn/']

    def start_requests(self):
        urls = [
            "http://www.csrc.gov.cn/pub/newsite/zjhxwfb/xwdd/",  # 证监会-新闻发布-证监会要闻
            # "http://www.csrc.gov.cn/pub/newsite/zjhxwfb/",  # 证监会-新闻发布-时政要闻部门--》跳转到了国务院网站
        ]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)
        pass

    def parse(self, response):
        message_list = response.xpath('//*[@id="myul"]/li')
        for message in message_list:
            title = "".join(message.xpath('a/text()').extract())
            href = "".join(message.xpath('a/@href').extract())
            date = "".join(message.xpath('span/text()').extract())
            url = response.url + href[2:]
            try:
                date = datetime.datetime.strptime(str(date).replace('/', '-'), '%Y-%m-%d')
                # print(date)
            except Exception as e:
                # print(e)
                date = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))

            # print(title, date, urls)
            result = session.query(NewsItemInfo).filter_by(url=url, web_id=58).count()
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
        item["pub_time"] = response.meta["date"]
        contents = "".join(response.xpath('\
                                        //div[@class="Custom_UnionStyle"]/p/span/text()|\
                                        //div[@class="Custom_UnionStyle"]/p/span/strong/text()|\
                                        //div[@class="Custom_UnionStyle"]/p/strong/span/text()|\
                                        //div[@class="Custom_UnionStyle"]/div/p/span/text()|\
                                        //div[@class="Custom_UnionStyle"]/div/div/p/span/text()').extract())
        # print(contents)
        if contents == "":
            item["content"] = "可能是图片或表格 打开原网站查看"
        else:
            item["content"] = contents.replace("\u3000", " ").replace("\xa0", "  ")
        form_s = "".join(response.xpath('//div[@class="time"]/span[3]/text()').extract()).replace("来源：", "")
        if form_s == "":
            form_s = "证监会"
        else:
            form_s = form_s
        item["webname"] = form_s.replace("来源：", "")
        item["web"] = response.meta["laiyuan"]
        item["keyword"] = keyword.get_keyword(item["content"])
        # print(item)
        item["web_id"] = 58
        return item
