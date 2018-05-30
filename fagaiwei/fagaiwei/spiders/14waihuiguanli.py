# -*- coding: utf-8 -*-
import datetime
import re
import time
import scrapy
from fagaiwei.settings import session, NewsItemInfo
from fagaiwei.items import FagaiweiItem
from fagaiwei.keyword_others import keyword


class WaihuiguanliSpider(scrapy.Spider):
    name = 'waihuiguanli'
    allowed_domains = ['safe.gov.cn']
    start_urls = ['http://safe.gov.cn/']

    def start_requests(self):
        urls = [
            "http://www.safe.gov.cn/wps/portal/sy/news_ywfb",  # 外汇新闻-要闻发布
            "http://www.safe.gov.cn/wps/portal/sy/szyw",  # 外汇新闻-时政要闻
            "http://www.safe.gov.cn/wps/portal/sy/whxw",  # 外汇新闻-外汇新闻
        ]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        res = response.text
        com_title = re.compile(r"titleString1124='(.*?)';")
        titles = re.findall(com_title, res)
        # print(len(titles))
        message_list = response.xpath('//table[@class="menulist"]/tr')
        # print(len(message_list))
        for index, message in enumerate(message_list):
            href = "".join(message.xpath('td[1]/a/@href').extract())
            date = "".join(message.xpath('td[2]/text()').extract())
            date = date.replace("[", "").replace("]", "").replace('/', '-').replace("\xa0", "")
            title = titles[index // 2].replace("<br />", "")
            # print(index,title)
            # print(title, href, date)
            try:
                date = datetime.datetime.strptime(str(date).replace('/', '-'), '%Y-%m-%d')
                # print(date)
            except Exception as e:
                # print(e)
                date = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
            if "http://" in href:
                url = href
            else:
                url = response.url + href
            result = session.query(NewsItemInfo).filter_by(url=url, web_id=14).count()
            if result:
                # print("{} 存在".format(url))
                pass
            else:
                yield scrapy.Request(url=url, callback=self.get_detail,
                                     meta={"date": date, "title": title, "laiyuan": response.url})

    def get_detail(self, response):
        item = FagaiweiItem()
        item["url"] = response.url
        item["pub_time"] = response.meta["date"]
        item["title"] = response.meta["title"]
        item["webname"] = "国家外汇管理局"
        item["web"] = response.meta["laiyuan"]
        item["web_id"] = 14
        contents = "".join(response.xpath('//*[@id="newsContent"]/p/text()|\
                                            //*[@id="newsContent"]/p/span/text()|\
                                            //*[@id="newsContent"]/p/span/span/text()|\
                                            //*[@id="newsContent"]/p/font/span/text()|\
                                            //*[@id="newsContent"]/p/span/font/text()|\
                                            //p[@class="MsoNormal"]/text()|\
                                            //p[@class="MsoNormal"]/span/text()|\
                                        //*[@id="newsContent"]/p/span/text()').extract())
        if contents != "":
            item["content"] = contents.replace("\u3000", "").replace("\xa0", "").replace("\u2002", "")
        else:
            item["content"] = "可能是图片 请打开详情页查看"
        item["keyword"] = keyword.get_keyword(item["content"])

        return item
