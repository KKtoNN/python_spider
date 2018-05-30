# -*- coding: utf-8 -*-
import datetime
import re
import time
import scrapy
from fagaiwei.settings import session, NewsItemInfo
from fagaiwei.items import FagaiweiItem
from fagaiwei.keyword_others import keyword


class RendaSpider(scrapy.Spider):
    name = 'renda'
    allowed_domains = ['npc.gov.cn']
    start_urls = ['http://npc.gov.cn/']

    def start_requests(self):
        urls = [
            "http://www.npc.gov.cn/npc/xinwen/node_16265.htm",  # 权威发布
            "http://www.npc.gov.cn/npc/xinwen/node_12491.htm",  # 权威发布-报告
            "http://www.npc.gov.cn/npc/xinwen/node_12490.htm",  # 权威发布-任免
            "http://www.npc.gov.cn/npc/xinwen/node_12489.htm",  # 权威发布-会议决定
            "http://www.npc.gov.cn/npc/xinwen/node_12487.htm",  # 权威发布-讲话论述
            # "http://www.npc.gov.cn/npc/xinwen/syxw/node_238.htm",  # 首页新闻====bug不返回数据了。。。
            "http://www.npc.gov.cn/npc/xinwen/node_12835.htm",  # 代表大会新闻发布会
            "http://www.npc.gov.cn/npc/xinwen/node_12836.htm",  # 常委会新闻发布会
            "http://www.npc.gov.cn/npc/xinwen/node_10134.htm",  # 滚动新闻
            "http://www.npc.gov.cn/npc/xinwen/dfrd/gzdt/node_223.htm",  # 地方人大工作-工作动态

        ]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        message_list = response.xpath('//ul[@class="clist"]/li')
        for message in message_list:
            href = "".join(message.xpath('a/@href').extract())
            title = "".join(message.xpath('a/text()').extract())
            date = "".join(message.xpath('span/text()').extract())
            try:
                date = datetime.datetime.strptime(str(date).replace('/', '-'), '%Y-%m-%d')
                # print(date)
            except Exception as e:
                # print(e)
                date = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
            # print(href, title, date)
            # print(href)
            if response.url == "http://www.npc.gov.cn/npc/xinwen/dfrd/gzdt/node_223.htm":
                if href[:3] == "../":
                    url = "http://www.npc.gov.cn/npc/xinwen/dfrd/" + href[3:]
                else:
                    url = "http://www.npc.gov.cn/npc/xinwen/dfrd/gzdt/" + href
                result = session.query(NewsItemInfo).filter_by(url=url, web_id=4).count()
                if result:
                    # print("{} 存在".format(url))
                    pass
                else:
                    yield scrapy.Request(url=url, callback=self.get_detail,
                                     meta={"date": date, "title": title, "laiyuan": response.url})
            elif response.url == "http://www.npc.gov.cn/npc/xinwen/syxw/node_238.htm":
                if href[:3] == "../":
                    url = "http://www.npc.gov.cn/npc/xinwen/" + href[3:]
                else:
                    url = "http://www.npc.gov.cn/npc/xinwen/syxw/" + href
                result = session.query(NewsItemInfo).filter_by(url=url, web_id=4).count()
                if result:
                    # print("{} 存在".format(url))
                    pass
                else:
                    yield scrapy.Request(url=url, callback=self.get_detail,
                                     meta={"date": date, "title": title, "laiyuan": response.url})
            else:
                if href[:3] == "../":
                    url = "http://www.npc.gov.cn/npc/" + href[3:]
                else:
                    url = "http://www.npc.gov.cn/npc/xinwen/" + href
                    # url = "".join(str(response.url).split('/')[:-1]) + href
                result = session.query(NewsItemInfo).filter_by(url=url, web_id=4).count()
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
        # print(item)
        item["content"] = "\n".join(response.xpath('\
                                    //*[@id="mid2"]/div/div/div/h2/text()|\
                                    //*[@id="mid2"]/div/div/div/h2/font/text()|\
                                    //*[@id="mid2"]/div/div/div/p/text()|\
                                    //div[@class="content"]/div/div/h2/text()|\
                                    //div[@class="content"]/div/div/h2/font/text()|\
                                    //div[@class="content"]/div/div/p/text()|\
                                    //div[@class="livepicbox wonderful"]/div/div/h2/text()|\
                                    //div[@class="livepicbox wonderful"]/div/div/h2/font/text()|\
                                    //div[@class="livepicbox wonderful"]/div/div/p/text()|\
                                    //*[@id="Zoom"]/div/p/text()|\
                                    //*[@id="Zoom"]/div/p/span/text()|\
                                    //*[@id="Zoom"]/strong/span/p/strong/text()|\
                                    //*[@id="Zoom"]/p/text()|\
                                    //*[@id="Zoom"]/p/a/text()|\
                                    //*[@id="Zoom"]/p/font/text()|\
                                    //*[@id="Zoom"]/p/font/span/text()|\
                                    //*[@id="Zoom"]/p/font/span/span/text()|\
                                    //*[@id="Zoom"]/p/font/font/span/text()|\
                                    //*[@id="Zoom"]/p/font/font/span/span/text()|\
                                    //*[@id="Zoom"]/p/strong/text()|\
                                    //*[@id="Zoom"]/p/span/text()|\
                                    //*[@id="Zoom"]/p/span/font/text()|\
                                    //*[@id="Zoom"]/span/p/text()|\
                                    //*[@id="Zoom"]/span/p/a/text()|\
                                    //*[@id="Zoom"]/span/p/a/font/text()|\
                                    //*[@id="Zoom"]/span/span/span/span/span/strong/span/span/strong/span/p/span/strong/span/span/strong/text()|\
                                    //*[@id="Zoom"]/span/span/span/span/span/strong/span/span/p/span/text()|\
                                    //*[@id="Zoom"]/span/span/span/span/span/strong/span/span/p/text()|\
                                    //*[@id="Zoom"]/span/strong/span/span/p/strong/text()').extract()) \
            .replace("\xa0", "").replace("\u3000", "")
        date = "".join(response.xpath('//div[@class="fl w680"]/div[2]/text()').extract())
        form_s = "".join(re.findall(re.compile(r'来源： (.*?)网'), date))
        if form_s == "":
            form_s = "全国人民代表大会"
        else:
            form_s = form_s + "网"
        item["webname"] = form_s
        item["web"] = response.meta["laiyuan"]
        date_s = "".join(re.findall(re.compile(r'\d+年\d+月\d+日 \d+:\d+:\d+'), date))
        date = date_s.replace("年", "-").replace("月", "-").replace("日", "")
        try:
            date = datetime.datetime.strptime(str(date).replace('/', '-'), '%Y-%m-%d %H:%M:%S')
        except Exception as e:
            date = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
        item["pub_time"] = date
        item["web_id"] = 4
        item["keyword"] = keyword.get_keyword(item["content"])
        return item
