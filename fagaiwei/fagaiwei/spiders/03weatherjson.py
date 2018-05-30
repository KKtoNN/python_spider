# -*- coding: utf-8 -*-
import json
import datetime
import time
import scrapy

from fagaiwei.settings import session, NewsItemInfo
from fagaiwei.items import FagaiweiItem
from fagaiwei.keyword_others import keyword


class WeatherSpider(scrapy.Spider):
    name = 'weather'
    allowed_domains = ['weather.com', 'cma.gov.cn', "weather.com.cn"]
    start_urls = ['http://weather.com/']

    def start_requests(self):
        urls = [
            # # "http://news.weather.com.cn/index.shtml",  # 中国天气 资讯==可以不要
            # # "http://www.cma.gov.cn/2011qxfw/2011qyjxx/",  # 中国气象局-首页-气象灾害预警
            "http://product.weather.com.cn/alarm/grepalarm.php?areaid=[0-9]{5,7}",  # 中国气象局-首页-气象灾害预警
            "http://www.cma.gov.cn/2011xwzx/2011xqxxw/2011xqxyw/",  # 中国气象局-首页-要闻播报
            "http://www.cma.gov.cn/2011xwzx/2011xqxxw/2011xjctz/",  # 中国气象局-首页-基层台站
            "http://www.cma.gov.cn/2011xwzx/2011xqxxw/2011xylsp/",  # 中国气象局-首页-言论时评
            "http://www.cma.gov.cn/2011xwzx/2011xmtjj/",  # 中国气象局-首页-媒体聚焦
            "http://www.cma.gov.cn/2011xwzx/2011xgzdt/",  # 中国气象局-首页-工作动态
            "http://www.cma.gov.cn/2011xwzx/2011xfzjz/2011xzxdt/",  # 中国气象局-首页-最新动态
        ]
        for url in urls:
            if "product.weather.com.cn" in url.lower():
                yield scrapy.Request(url=url, callback=self.parse)
            else:
                yield scrapy.Request(url=url, callback=self.parse_cma)

    def parse(self, response):
        # print(response.url)
        result = json.loads(response.text[14:-1])
        for data in result["data"]:
            place = data[0]
            files = data[1]
            # url = "http://www.weather.com.cn/alarm/newalarmcontent.shtml?file=" + str(files)
            url = "http://product.weather.com.cn/alarm/webdata/" + str(files)  # + str("?_=1524111043080")
            # print(place, url)
            result = session.query(NewsItemInfo).filter_by(url=url, web_id=3).count()
            if result:
                # print("{} 存在".format(url))
                pass
            else:
                yield scrapy.Request(url=url, callback=self.get_detail,
                                     meta={"title": place})

    def parse_cma(self, response):
        message_list = response.xpath('//a[@class="nblue"]')
        for message in message_list:
            title = "".join(message.xpath('text()').extract())
            href = "".join(message.xpath('@href').extract())
            url = response.url + href[2:]
            # print(title, url)
            result = session.query(NewsItemInfo).filter_by(url=url, web_id=3).count()
            if result:
                # print("{} 存在".format(url))
                pass
            else:
                yield scrapy.Request(url=url, callback=self.get_detail_cma,
                                     meta={"laiyuan": response.url, "title": title})

    def get_detail(self, response):
        item = FagaiweiItem()
        item["url"] = response.url
        result = json.loads(response.text[14:])
        item["title"] = result["head"]
        PROVINCE = result["PROVINCE"]  # 省份
        SIGNALTYPE = result["SIGNALTYPE"]  # 预警类型
        SIGNALLEVEL = result["SIGNALLEVEL"]  # 预警等级
        # TYPECODE = result["TYPECODE"]#类型代码
        # LEVELCODE = result["LEVELCODE"]#等级代码
        item["pub_time"] = result["ISSUETIME"]  # 时间
        item["content"] = result["ISSUECONTENT"]  # 简介
        # RELIEVETIME = result["RELIEVETIME"]
        # TIME = result["TIME"]
        item["keyword"] = "{} {} {}".format(PROVINCE, SIGNALTYPE, SIGNALLEVEL)
        item["webname"] = "中国气象局"
        item["web"] = "http://www.cma.gov.cn/2011qxfw/2011qyjxx/"
        # print(item)
        item["web_id"] = 3
        # item["keyword"] = keyword.get_keyword(item["content"])

        return item

    def get_detail_cma(self, response):
        item = FagaiweiItem()
        item["url"] = response.url
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
        form_s = "".join(response.xpath('//div[@class="news_textspan"]/div/span[1]/text()').extract())
        item["webname"] = form_s.replace("来源：", "")
        item["web"] = response.meta["laiyuan"]
        date = "".join(response.xpath('//div[@class="news_textspan"]/div/span[2]/text()').extract())
        date = date[:-5].replace("发布时间：", "").replace("年", "-").replace("月", "-").replace("日", "")
        try:
            date = datetime.datetime.strptime(str(date).replace('/', '-'), '%Y-%m-%d')
            # print(date)
        except Exception as e:
            # print(e)
            date = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
        item["pub_time"] = date
        # print(item)
        item["web_id"] = 3
        item["keyword"] = keyword.get_keyword(item["content"])
        return item
