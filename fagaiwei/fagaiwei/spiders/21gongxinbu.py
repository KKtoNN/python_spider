# -*- coding: utf-8 -*-
import datetime
import time
import scrapy
from fagaiwei.settings import session, NewsItemInfo
from fagaiwei.items import FagaiweiItem
from fagaiwei.keyword_others import keyword


class HainanSpider(scrapy.Spider):
    name = 'gongxinbu'
    allowed_domains = ['miit.gov.cn']
    start_urls = ['http://www.miit.gov.cn']

    def start_requests(self):
        urls = [
            "http://www.miit.gov.cn/n1146290/n1146407/index.html",  # 首页>新闻动态>对外交流
            "http://www.miit.gov.cn/n1146290/n1146402/n1146455/index.html",  # 首页>新闻动态>产业动态
            "http://www.miit.gov.cn/n1146290/n1146402/n1146445/index.html",  # 首页>新闻动态>部属单位
            "http://www.miit.gov.cn/n1146290/n1146402/n1146450/index.html",  # 首页>新闻动态>地方工作
            "http://www.miit.gov.cn/n1146290/n1146402/n1146440/index.html",  # 首页>新闻动态>司局动态
            "http://www.miit.gov.cn/n1146290/n4388791/index.html",  # 首页>新闻动态>重点工作
            "http://www.miit.gov.cn/n1146290/n1146397/index.html",  # 首页>新闻动态>领导活动
            "http://www.miit.gov.cn/n1146290/n1146392/index.html",  # 首页>新闻动态>时政要闻

        ]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        message_list = response.xpath('//div[@class="clist_con"]/ul/li')
        for message in message_list:
            date = "".join(message.xpath('span/a/text()|span/text()').extract())
            title = "".join(message.xpath('a/text()').extract()).replace("· ", "")
            href = "".join(message.xpath('a/@href').extract())
            # print(date)
            try:
                date = datetime.datetime.strptime(str(date).replace('-', '-'), '%Y-%m-%d')
            except Exception as e:
                date = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
            if str("www.miit.gov.cn") in href:
                result = session.query(NewsItemInfo).filter_by(url=href, web_id=21).count()
                if result:
                    # print("{} 存在".format(href))
                    pass
                else:
                    yield scrapy.Request(url=href, callback=self.get_detail,
                                         meta={"date": date, "title": title, "laiyuan": response.url})
            else:

                url = response.url.replace("index.html", "") + href
                result = session.query(NewsItemInfo).filter_by(url=url, web_id=21).count()
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
        form_s = "".join(response.xpath('//div[@class="cinfo center"]/span[2]/text()').extract())
        if form_s:
            item["webname"] = form_s.split("：")[-1].replace(" ", "")
        else:
            item["webname"] = "中华人民共和国工业和信息化部"
        item["web"] = response.meta["laiyuan"]
        # item["keyword"] = ""
        item["web_id"] = 21
        contents = "".join(response.xpath('//*[@id="con_con"]/p/text()|\
                                           //*[@id="con_con"]/p/span/text()|\
                                           //*[@id="con_con"]/p/span/font/text()|\
                                           //*[@id="con_con"]/div/p/text()|\
                                           //*[@id="con_con"]/p/strong/text()').extract())
        # print(contents)
        if contents != "":
            item["content"] = contents.replace("\u3000", "").replace("\xa0", "")
        else:
            item["content"] = "可能是图片 请打开详情页查看"
        item["keyword"] = keyword.get_keyword(item["content"])

        return item


if __name__ == "__main__":
    pass
