# -*- coding:utf-8 -*-
__author__ = "jake"
__email__ = "jakejie@163.com"
"""
Project:fagaiwei
FileName = PyCharm
Version:1.0
CreateDay:2018/5/8 12:40
"""
import datetime
import time
from fagaiwei.settings import session, NewsItemInfo
from fagaiwei.items import FagaiweiItem
from fagaiwei.keyword_others import keyword

allowed_domains = ['ndrc.gov.cn']


def url_fagaiwei(response):
    data_list = {}
    message_list = response.xpath('//ul[@class="list_02 clearfix"]/li')
    for message in message_list:
        date = "".join(message.xpath('font/text()').extract())
        title = "".join(message.xpath('a/text()').extract())
        href = "".join(message.xpath('a/@href').extract())
        if title != "":
            try:
                date = datetime.datetime.strptime(str(date).replace('/', '-'), '%Y-%m-%d')
                # print(date)
            except Exception as e:
                # print(e)
                date = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
            if "www.xinhuanet.com" in href:
                url = href
            elif href.endswith("pdf"):
                pass
            elif "http" in href:
                url = href
            else:
                url = response.url + href
            result = session.query(NewsItemInfo).filter_by(url=url, web_id=2).count()
            if result:
                # print("{} 存在".format(url))
                pass
            else:
                data_list['date'] = date
                data_list['url'] = url
                data_list['title'] = title
                yield data_list


def parse_fagaiwei(response, item):
    item = FagaiweiItem()
    item["url"] = response.url
    contents = "".join(response.xpath('-\
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
                                //div[@class="TRS_Editor"]/div/a/text()|\
                                //div[@class="TRS_Editor"]/div/span/text()|\
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
                                //div[@class="TRS_Editor"]/div/p/font/span/text()|\
                                //div[@class="TRS_Editor"]/div/p/font/span/span/text()|\
                                //div[@class="TRS_Editor"]/div/p/font/font/span/text()|\
                                //div[@class="TRS_Editor"]/div/p/font/font/font/span/text()|\
                                //div[@class="TRS_Editor"]/div/p/font/font/span/span/text()|\
                                //div[@class="TRS_Editor"]/div/p/font/font/span/span/font/text()|\
                                //div[@class="TRS_Editor"]/div/p/font/font/span/span/font/span/text()|\
                                //div[@class="TRS_Editor"]/div/p/span/text()|\
                                //div[@class="TRS_Editor"]/div/p/a/span/text()|\
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
                                //div[@class="TRS_Editor"]/div/div/p/font/span/text()|\
                                //div[@class="TRS_Editor"]/div/div/p/font/font/span/text()|\
                                //div[@class="TRS_Editor"]/div/div/span/text()|\
                                //div[@class="TRS_Editor"]/div/div/span/span/text()|\
                                //div[@class="TRS_Editor"]/div/div/span/p/span/text()|\
                                //div[@class="TRS_Editor"]/div/div/div/p/span/text()|\
                                //div[@class="TRS_Editor"]/div/div/div/p/font/font/span/text()|\
                                //div[@class="TRS_Editor"]/div/div/div/span/p/text()|\
                                //div[@class="TRS_Editor"]/div/div/div/span/p/span/text()|\
                                //div[@class="TRS_Editor"]/div/div/div/span/p/font/font/span/text()|\
                                //div[@class="TRS_Editor"]/div/div/div/div/span/p/text()|\
                                //font[@face="Calibri"]/text()|\
                                //font[@face="Calibri"]/span/text()|\
                                //font[@face="Calibri"]/span/span/text()|\
                                //div[@class="txt1"]/text()|\
                                //div[@class="txt1"]/a/text()|\
                                //div[@class="txt1"]/a/font/text()|\
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
    item["content"] = contents
    item["pub_time"] = response.meta["date"]
    item["title"] = response.meta["title"]
    from_s = "".join(response.xpath('//*[@id="dSourceText"]/a/text()').extract())
    from_s_url = "".join(response.xpath('//*[@id="dSourceText"]/a/@href').extract())
    if from_s == "":
        webname = "发改委"
        depart_url = response.meta["laiyuan"]
    else:
        webname = from_s
        depart_url = from_s_url
    item["webname"] = webname
    item["web"] = depart_url
    item["keyword"] = keyword.get_keyword(item["content"])
    item["web_id"] = 2
    yield item
