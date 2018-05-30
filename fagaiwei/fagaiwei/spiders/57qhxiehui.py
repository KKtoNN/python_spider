# -*- coding: utf-8 -*-
import datetime
import re
import time
import scrapy
from fagaiwei.settings import session, NewsItemInfo
from fagaiwei.keyword_others import keyword
from fagaiwei.items import FagaiweiItem


class QhxiehuiSpider(scrapy.Spider):
    name = 'qhxiehui'
    allowed_domains = ['cfachina.org']
    start_urls = ['http://cfachina.org/']

    def start_requests(self):
        urls = [
            # "http://www.cfachina.org/ggxw/XHGG/",  # 期货业协会-通知公告==这个地址没有数据
            "http://www.cfachina.org/was5/web/search?\
                token=32.1411618300917.53&channelid=249363&templet=tongzhigonggao.jsp",  # 期货业协会-通知公告
            "http://www.cfachina.org/ggxw/MTKQS/",  # 期货业协会-媒体看期市
            "http://www.cfachina.org/ggxw/XYDT/",  # 期货业协会-会员通告
            "http://www.cfachina.org/ggxw/xhdt/",  # 期货业协会-协会新闻==有pdf简报
            "http://www.cfachina.org/ggxw/LXHYDT/",  # 期货业协会-地方协会
            "http://www.cfachina.org/ggxw/hytg/",  # 期货业协会-会员动态
        ]
        for url in urls:
            if "token=32.1411618300917.53&channelid" in url.lower():
                yield scrapy.Request(url=url, callback=self.parse_tz)
            else:
                yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        message_list = response.xpath('//ul[@class="nr_neirong"]/li')
        # print(len(message_list))
        for message in message_list:
            title = "".join(message.xpath('span/a/text()').extract())
            href = "".join(message.xpath('span/a/@href').extract())
            date = "".join(message.xpath('font/text()').extract())
            if "http" in href:
                url = href
            else:
                url = response.url + href
            # print(title, url, date)
            try:
                date = datetime.datetime.strptime(str(date).replace('/', '-'), '%Y-%m-%d')
                # print(date)
            except Exception as e:
                # print(e)
                date = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
            if ".pdf" not in str(url[:-5]).lower():
                result = session.query(NewsItemInfo).filter_by(url=url, web_id=57).count()
                if result:
                    # print("{} 存在".format(url))
                    pass
                else:
                    yield scrapy.Request(url=url, callback=self.get_detail,
                                         meta={"title": title, "date": date, "laiyuan": response.url})
            else:
                result = session.query(NewsItemInfo).filter_by(url=url, web_id=57).count()
                if result:
                    # print("{} 存在".format(url))
                    pass
                else:
                    item = FagaiweiItem()
                    item["url"] = url
                    item["pub_time"] = date
                    item["title"] = title
                    item["content"] = "可能是图片或表格 打开原网站查看"
                    item["webname"] = "中国期货业协会"
                    item["web_id"] = 57
                    item["keyword"] = keyword.get_keyword(item["content"])
                    yield item

    def parse_tz(self, response):
        message_list = response.xpath('//tbody/tr')
        # print(len(message_list))
        for message in message_list:
            title = "".join(message.xpath('td/a/text()').extract())
            href = "".join(message.xpath('td/a/@href').extract())
            date = "".join(message.xpath('td[2]/text()').extract())
            try:
                date = datetime.datetime.strptime(str(date).replace('/', '-'), '%Y-%m-%d')
                # print(date)
            except Exception as e:
                # print(e)
                date = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
            # print(title, href, date)
            url = href
            if ".pdf" not in str(url[:-5]).lower():
                result = session.query(NewsItemInfo).filter_by(url=url, web_id=57).count()
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
        contents = "".join(response.xpath('\
                                    //div[@class="TRS_Editor"]/font/font/span/p/text()|\
                                    //div[@class="TRS_Editor"]/font/font/span/p/span/text()|\
                                    //div[@class="TRS_Editor"]/font/font/span/p/span/span/text()|\
                                    //div[@class="TRS_Editor"]/span/span/p/font/text()|\
                                    //div[@class="TRS_Editor"]/span/span/p/font/span/text()|\
                                    //div[@class="TRS_Editor"]/span/span/p/font/span/span/text()|\
                                    //div[@class="TRS_Editor"]/div/font/font/span/span/p/span/text()|\
                                    //div[@class="TRS_Editor"]/div/span/span/p/font/span/text()|\
                                    //div[@class="TRS_Editor"]/div/span/span/p/span/font/text()|\
                                    //div[@class="TRS_Editor"]/div/span/p/font/font/font/span/text()|\
                                    //div[@class="TRS_Editor"]/div/span/p/font/font/font/span/span/text()|\
                                    //div[@class="TRS_Editor"]/div/span/span/span/p/span/font/strong/text()|\
                                    //div[@class="TRS_Editor"]/div/span/span/span/p/strong/font/font/font/font/font/font/span/text()|\
                                    //div[@class="TRS_Editor"]/div/span/span/p/font/font/font/span/text()|\
                                    //div[@class="TRS_Editor"]/span/text()|\
                                    //div[@class="TRS_Editor"]/span/font/text()|\
                                    //div[@class="TRS_Editor"]/span/span/text()|\
                                    //div[@class="TRS_Editor"]/span/font/p/span/font/text()|\
                                    //div[@class="TRS_Editor"]/span/font/p/span/font/span/text()|\
                                    //div[@class="TRS_Editor"]/span/h2/span/text()|\
                                    //div[@class="TRS_Editor"]/span/p/text()|\
                                    //div[@class="TRS_Editor"]/span/p/span/text()|\
                                    //div[@class="TRS_Editor"]/span/strong/span/span/p/strong/text()|\
                                    //div[@class="TRS_Editor"]/span/p/span/span/text()|\
                                    //div[@class="TRS_Editor"]/span/p/span/font/text()|\
                                    //div[@class="TRS_Editor"]/div/span/p/span/text()|\
                                    //div[@class="TRS_Editor"]/div/span/p/span/span/text()|\
                                    //div[@class="TRS_Editor"]/div/span/p/span/font/text()|\
                                    //div[@class="TRS_Editor"]/div/span/p/font/font/font/span/text()|\
                                    //div[@class="TRS_Editor"]/b/span/span/p/span/text()|\
                                    //div[@class="TRS_Editor"]/b/span/span/p/b/span/text()|\
                                    //div[@class="TRS_Editor"]/strong/font/p/text()|\
                                    //div[@class="TRS_Editor"]/strong/font/p/a/text()|\
                                    //div[@class="TRS_Editor"]/strong/font/p/a/font/text()|\
                                    //div[@class="TRS_Editor"]/p/text()|\
                                    //div[@class="TRS_Editor"]/p/a/text()|\
                                    //div[@class="TRS_Editor"]/p/b/text()|\
                                    //div[@class="TRS_Editor"]/p/b/span/text()|\
                                    //div[@class="TRS_Editor"]/p/a/span/text()|\
                                    //div[@class="TRS_Editor"]/p/u/span/a/text()|\
                                    //div[@class="TRS_Editor"]/p/span/a/span/text()|\
                                    //div[@class="TRS_Editor"]/p/span/text()|\
                                    //div[@class="TRS_Editor"]/p/span/span/text()|\
                                    //div[@class="TRS_Editor"]/p/strong/text()|\
                                    //div[@class="TRS_Editor"]/p/strong/font/text()|\
                                    //div[@class="TRS_Editor"]/p/a/font/text()|\
                                    //div[@class="TRS_Editor"]/p/font/text()|\
                                    //div[@class="TRS_Editor"]/p/font/a/text()|\
                                    //div[@class="TRS_Editor"]/p/font/span/text()|\
                                    //div[@class="TRS_Editor"]/p/font/span/font/text()|\
                                    //div[@class="TRS_Editor"]/p/font/strong/text()|\
                                    //div[@class="TRS_Editor"]/p/font/font/text()|\
                                    //div[@class="TRS_Editor"]/p/font/font/font/text()|\
                                    //div[@class="TRS_Editor"]/p/font/font/font/span/text()|\
                                    //div[@class="TRS_Editor"]/p/font/font/font/font/font/font/text()|\
                                    //div[@class="TRS_Editor"]/p/font/font/font/font/font/font/font/text()|\
                                    //div[@class="TRS_Editor"]/p/font/font/font/font/font/font/font/span/text()|\
                                    //div[@class="TRS_Editor"]/p/font/font/font/a/text()|\
                                    //div[@class="TRS_Editor"]/p/font/font/a/text()|\
                                    //div[@class="TRS_Editor"]/p/font/font/a/font/text()|\
                                    //div[@class="TRS_Editor"]/p/font/font/font/a/font/text()|\
                                    //div[@class="TRS_Editor"]/p/font/font/font/font/font/text()|\
                                    //div[@class="TRS_Editor"]/p/font/font/span/text()|\
                                    //div[@class="TRS_Editor"]/p/font/font/strong/text()|\
                                    //div[@class="TRS_Editor"]/p/span/font/text()|\
                                    //div[@class="TRS_Editor"]/text()|\
                                    //div[@class="TRS_Editor"]/a/text()|\
                                    //div[@class="TRS_Editor"]/font/text()|\
                                    //div[@class="TRS_Editor"]/div/text()|\
                                    //div[@class="TRS_Editor"]/div/a/text()|\
                                    //div[@class="TRS_Editor"]/div/b/text()|\
                                    //div[@class="TRS_Editor"]/div/span/text()|\
                                    //div[@class="TRS_Editor"]/div/span/a/span/text()|\
                                    //div[@class="TRS_Editor"]/div/span/p/span/span/text()|\
                                    //div[@class="TRS_Editor"]/div/span/p/span/span/a/text()|\
                                    //div[@class="TRS_Editor"]/div/span/span/text()|\
                                    //div[@class="TRS_Editor"]/div/span/span/p/span/text()|\
                                    //div[@class="TRS_Editor"]/div/span/span/p/font/span/text()|\
                                    //div[@class="TRS_Editor"]/div/span/span/p/font/span/span/text()|\
                                    //div[@class="TRS_Editor"]/div/span/span/p/span/span/text()|\
                                    //div[@class="TRS_Editor"]/div/span/span/span/span/p/span/text()|\
                                    //div[@class="TRS_Editor"]/div/font/text()|\
                                    //div[@class="TRS_Editor"]/div/font/span/text()|\
                                    //div[@class="TRS_Editor"]/div/font/span/sup/text()|\
                                    //div[@class="TRS_Editor"]/div/font/sup/span/text()|\
                                    //div[@class="TRS_Editor"]/div/font/p/span/text()|\
                                    //div[@class="TRS_Editor"]/div/font/p/span/span/text()|\
                                    //div[@class="TRS_Editor"]/div/font/span/p/span/text()|\
                                    //div[@class="TRS_Editor"]/div/font/span/p/span/span/text()|\
                                    //div[@class="TRS_Editor"]/div/p/b/span/text()|\
                                    //div[@class="TRS_Editor"]/div/p/b/span/span/text()|\
                                    //div[@class="TRS_Editor"]/div/p/text()|\
                                    //div[@class="TRS_Editor"]/div/p/font/text()|\
                                    //div[@class="TRS_Editor"]/div/p/font/span/text()|\
                                    //div[@class="TRS_Editor"]/div/p/font/span/span/text()|\
                                    //div[@class="TRS_Editor"]/div/p/font/font/span/text()|\
                                    //div[@class="TRS_Editor"]/div/p/font/font/font/span/text()|\
                                    //div[@class="TRS_Editor"]/div/p/font/font/font/span/font/text()|\
                                    //div[@class="TRS_Editor"]/div/p/font/font/font/font/span/text()|\
                                    //div[@class="TRS_Editor"]/div/p/font/font/font/font/span/font/text()|\
                                    //div[@class="TRS_Editor"]/div/p/font/font/span/span/text()|\
                                    //div[@class="TRS_Editor"]/div/p/font/font/span/span/font/text()|\
                                    //div[@class="TRS_Editor"]/div/p/font/font/span/span/font/span/text()|\
                                    //div[@class="TRS_Editor"]/div/p/span/text()|\
                                    //div[@class="TRS_Editor"]/div/p/span/a/strong/text()|\
                                    //div[@class="TRS_Editor"]/div/p/a/span/text()|\
                                    //div[@class="TRS_Editor"]/div/p/a/strong/span/font/text()|\
                                    //div[@class="TRS_Editor"]/div/p/span/a/text()|\
                                    //div[@class="TRS_Editor"]/div/p/span/font/text()|\
                                    //div[@class="TRS_Editor"]/div/p/span/font/span/text()|\
                                    //div[@class="TRS_Editor"]/div/p/span/span/text()|\
                                    //div[@class="TRS_Editor"]/div/p/span/span/span/text()|\
                                    //div[@class="TRS_Editor"]/div/table/tbody/tr/td/p/span/text()|\
                                    //div[@class="TRS_Editor"]/div/table/tbody/tr/td/p/span/a/span/text()|\
                                    //div[@class="TRS_Editor"]/div/text()|\
                                    //div[@class="TRS_Editor"]/div/div/text()|\
                                    //div[@class="TRS_Editor"]/div/div/p/text()|\
                                    //div[@class="TRS_Editor"]/div/div/p/span/text()|\
                                    //div[@class="TRS_Editor"]/div/div/p/span/span/text()|\
                                    //div[@class="TRS_Editor"]/div/div/p/span/font/text()|\
                                    //div[@class="TRS_Editor"]/div/div/p/font/text()|\
                                    //div[@class="TRS_Editor"]/div/div/p/font/font/text()|\
                                    //div[@class="TRS_Editor"]/div/div/p/font/span/text()|\
                                    //div[@class="TRS_Editor"]/div/div/p/font/font/span/text()|\
                                    //div[@class="TRS_Editor"]/div/div/span/text()|\
                                    //div[@class="TRS_Editor"]/div/div/span/span/text()|\
                                    //div[@class="TRS_Editor"]/div/div/span/p/span/text()|\
                                    //div[@class="TRS_Editor"]/div/div/div/p/span/text()|\
                                    //div[@class="TRS_Editor"]/div/div/div/p/font/font/span/text()|\
                                    //div[@class="TRS_Editor"]/div/div/div/div/p/font/font/font/font/text()|\
                                    //div[@class="TRS_Editor"]/div/div/div/div/p/font/font/font/font/span/font/text()|\
                                    //div[@class="TRS_Editor"]/div/div/div/div/p/font/font/font/font/font/font/font/span/text()|\
                                    //div[@class="TRS_Editor"]/div/div/div/div/p/font/font/font/font/font/font/font/font/span/text()|\
                                    //div[@class="TRS_Editor"]/div/div/div/span/p/text()|\
                                    //div[@class="TRS_Editor"]/div/div/div/span/p/span/text()|\
                                    //div[@class="TRS_Editor"]/div/div/div/span/p/font/font/span/text()|\
                                    //div[@class="TRS_Editor"]/div/div/div/div/span/p/text()|\
                                    //div[@class="cen_main"]/div/h1/text()|\
                                    //div[@class="cen_main"]/div/div/p/text()|\
                                    //div[@class="cen_main"]/div/div/p/span/text()|\
                                    //div[@class="cen_main"]/div/div/p/span/span/text()|\
                                    //div[@class="cen_main"]/div/div/div/p/span/text()|\
                                    //div[@class="cen_main"]/div/div/div/p/span/span/text()|\
                                    //font[@face="Calibri"]/text()|\
                                    //font[@face="Calibri"]/span/text()|\
                                    //font[@face="Calibri"]/span/span/text()|\
                                    //*[@id="ozoom"]/p/text()|\
                                    //*[@id="zoom"]/div/p/text()|\
                                    //*[@id="zoom"]/div/p/span/text()|\
                                    //*[@id="zoom"]/strong/span/p/strong/text()|\
                                    //*[@id="zoom"]/p/text()|\
                                    //*[@id="zoom"]/p/a/text()|\
                                    //*[@id="zoom"]/p/strong/text()|\
                                    //*[@id="zoom"]/p/span/text()|\
                                    //*[@id="zoom"]/span/p/text()|\
                                    //*[@id="zoom"]/span/p/a/text()|\
                                    //*[@id="zoom"]/span/p/a/font/text()|\
                                    //*[@id="zoom"]/span/span/span/span/span/strong/span/span/strong/span/p/span/strong/span/span/strong/text()|\
                                    //*[@id="zoom"]/span/span/span/span/span/strong/span/span/p/span/text()|\
                                    //*[@id="zoom"]/span/span/span/span/span/strong/span/span/p/text()|\
                                    //*[@id="zoom"]/span/strong/span/span/p/strong/text()').extract())

        if contents == "":
            contents = "可能是图片或表格 打开原网站查看"
        item["content"] = contents.replace("\u3000", "").replace("\xa0", "") \
            .replace("\t\n", "").replace("\t", "")  # .replace("  ", "")
        item["keyword"] = "".join(response.xpath('//dl[@class="xl_guanjc"]/dd/text()').extract())
        if item["keyword"] == "":
            item["keyword"] = keyword.get_keyword(item["content"])
        # form_s = "".join(response.xpath('//div[@class="xilan_nengr"]/h2/text()').extract())
        # print(form_s)
        webname = "".join(re.findall(re.compile(r'var docsource="(.*?)";'), response.text))
        if webname == "":
            webname = "中国期货业协会"
        else:
            webname = webname
        item["webname"] = webname
        item["web"] = response.meta["laiyuan"]
        item["web_id"] = 57
        return item
