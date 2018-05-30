# -*- coding: utf-8 -*-
import datetime
import time
import scrapy
from fagaiwei.settings import session, NewsItemInfo
from fagaiwei.items import FagaiweiItem
from fagaiwei.keyword_others import keyword
# item["keyword"] = keyword.get_keyword(item["content"])

class GwycrawlSpider(scrapy.Spider):
    name = 'gwycrawl'
    allowed_domains = ['gov.cn']
    start_urls = ['http://gov.cn/']

    def start_requests(self):
        urls = [
            "http://www.gov.cn/pushinfo/v150203/index.htm",  # 国务院信息==很多地方网站链接到这里
            "http://www.gov.cn/zhengce/zuixin.htm",  # 最新政策
            "http://www.gov.cn/xinwen/gundong.htm",  # 滚动新闻
            "http://www.gov.cn/xinwen/yaowen.htm",  # 新闻-要闻
            "http://www.gov.cn/xinwen/fabu/qita.htm",  # 新闻-新闻发布-其他
            "http://www.gov.cn/xinwen/fabu/bumen.htm",  # 新闻-新闻发布-部门
            "http://www.gov.cn/xinwen/fabu/zccfh/index.htm",  # 新闻-新闻发布-国务院政策吹风会
            "http://www.gov.cn/xinwen/lianbo/difang.htm",  # 新闻-政务联播-地方
            "http://www.gov.cn/xinwen/lianbo/bumen.htm",  # 新闻-政务联播-部门
            "http://www.gov.cn/xinwen/lianbo/difang.htm",  # 新闻-政务联播-地方
            "http://www.gov.cn/xinwen/renmian/qita.htm",  # 其他人事信息
            "http://www.gov.cn/xinwen/renmian/zhuwai.htm",  # 驻外人事信息
            "http://www.gov.cn/xinwen/renmian/difang.htm",  # 地方人事信息
            "http://www.gov.cn/xinwen/renmian/zhongyang.htm",  # 中央人事信息
        ]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        # print(response.url)
        message_list = response.xpath('//div[@class="list list_1 list_2"]/ul/li')
        # print(len((message_list)))
        for message in message_list:
            data = "".join(message.xpath('h4/span/text()').extract())
            href = "".join(message.xpath('h4/a/@href').extract())
            title = "".join(message.xpath('h4/a/text()').extract())
            # print(data, title, href)
            try:
                date = datetime.datetime.strptime(str(data).replace('-', '-'), '%Y-%m-%d')
                # print(date)
            except Exception as e:
                # print(e)
                date = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))

            url = "http://www.gov.cn" + href
            result = session.query(NewsItemInfo).filter_by(url=url, web_id=1).count()
            if result:
                # print("{} 存在".format(url))
                pass
            else:
                yield scrapy.Request(url=url, callback=self.get_detail,
                                     meta={"date": date, "title": title, "laiyuan": response.url})

    def get_detail(self, response):
        item = FagaiweiItem()
        item["url"] = response.url
        # item["title"] = response.meta["title"]
        item["title"] = response.xpath("//h1/text()").get()

        # print(response.url)
        contents = "".join(response.xpath('//*[@id="UCAP-CONTENT"]/p/text()|\
                                        //*[@id="UCAP-CONTENT"]/p/span/span/text()|\
                                        //div[@class="pages_content"]/p/text()|\
                                        //div[@class="pages_content"]/p/a/text()|\
                                        //div[@class="pages_content"]/div/p/text()|\
                                        //*[@id="UCAP-CONTENT"]/p/span/text()').extract())
        if contents == "":
            item["content"] = "可能是图片或表格 打开原网站查看"
        else:
            item["content"] = contents
        date = "".join(response.xpath('//div[@class="pages-date"]/text()').extract())

        if date:
            dates = str(date).replace("  ", "").replace("\r", "").replace("\n", "") + ":00"
            date = datetime.datetime.strptime(dates, '%Y-%m-%d %H:%M:%S')
        else:
            date = response.meta["date"]
        item["pub_time"] = date
        from_s = "".join(response.xpath('//div[@class="pages-date"]/span/text()').extract())
        if from_s == "":
            webname = "国务院新闻"
        else:
            webname = from_s

        item["webname"] = webname.replace("来源：", "")
        item["web"] = response.meta["laiyuan"]
        item["keyword"] = keyword.get_keyword(item["content"])
        item["web_id"] = 1
        return item
