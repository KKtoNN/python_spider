# -*- coding: utf-8 -*-
import datetime
import time
import scrapy
from fagaiwei.settings import session, NewsItemInfo
from fagaiwei.items import FagaiweiItem
from fagaiwei.keyword_others import keyword

class XinfangjuSpider(scrapy.Spider):
    name = 'xinfangju'
    allowed_domains = ['gjxfj.gov.cn']  # , 'xinhuanet.com'
    start_urls = ['http://gjxfj.gov.cn/']

    def start_requests(self):
        urls = [
            "http://www.gjxfj.gov.cn/xwzx/gzdt.htm",  # 国家信访局-工作动态-部委动态+地方动态
            "http://www.gjxfj.gov.cn/xwzx/zyxw.htm",  # 国家信访局-重要新闻-头条要闻+工作要闻+时政要闻
            "http://www.gjxfj.gov.cn/xwzx/xwfb.htm",  # 国家信访局-新闻发布
        ]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        message_list = response.xpath('//*[@id="the1"]/ul/li|\
                                        //*[@id="the2"]/ul/li|\
                                        //*[@id="the3"]/ul/li|\
                                        //div[@class="pannel-inner"]/ul/li')
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
            url = href
            result = session.query(NewsItemInfo).filter_by(url=url, web_id=19).count()
            if result:
                # print("{}=={} 存在".format(result, url))
                pass
            else:
                yield scrapy.Request(url=url, callback=self.get_detail,
                                     meta={"date": date, "title": title, "laiyuan": response.url})

    def get_detail(self, response):
        item = FagaiweiItem()
        item["url"] = response.url
        item["pub_time"] = response.meta["date"]
        item["title"] = response.meta["title"]
        form_s = "".join(response.xpath('//*[@id="time_tex"]/text()|//span[@class="aticle-src"]/text()').extract())
        form_s = form_s.split("： ")[-1]
        if form_s != "":
            item["webname"] = form_s.replace(" ", "").replace("\r", "").replace("\n", "").replace("\t", "")
        else:
            item["webname"] = "国家信访局"
        item["web"] = response.meta["laiyuan"]
        # item["keyword"] = ""
        item["web_id"] = 19
        contents = "".join(response.xpath('//*[@id="tex"]/p/text()|\
                                            //*[@id="tex"]/p/strong/text()|\
                                            //*[@id="tex"]/p/strong/font/text()|\
                                            //*[@id="tex"]/p/font/font/span/text()|\
                                            //*[@id="tex"]/div/p/font/text()|\
                                            //*[@id="tex"]/div/p/strong/font/text()|\
                                            //*[@id="tex"]/span/font/font/p/text()|\
                                            //*[@id="tex"]/span/font/font/p/span/text()|\
                                            //*[@id="p-detail"]/p/text()|\
                                            //*[@id="p-detail"]/p/font/text()|\
                                            //*[@id="p-detail"]/p/font/strong/text()|\
                                            //*[@id="p-detail"]/p/font/span/text()|\
                                            //*[@id="p-detail"]/div/p/text()|\
                                            //*[@id="p-detail"]/div/p/span/text()|\
                                            //*[@id="p-detail"]/div/p/span/font/text()|\
                                            //*[@id="p-detail"]/div/p/font/font/span/text()|\
                                            //*[@id="p-detail"]/div/p/font/font/font/text()|\
                                            //*[@id="p-detail"]/div/p/font/font/font/span/text()|\
                                            //*[@id="content"]/p/text()|\
                                            //*[@id="content"]/p/strong/text()|\
                                            //*[@id="content"]/p/strong/font/text()|\
                                            //*[@id="tex"]/p/font/text()').extract())
        # print(contents)
        if contents != "":
            item["content"] = contents.replace("\u3000", "").replace("\xa0", "").replace("\u2002", "")
        else:
            item["content"] = "可能是图片 请打开详情页查看"
        item["keyword"] = keyword.get_keyword(item["content"])

        return item
