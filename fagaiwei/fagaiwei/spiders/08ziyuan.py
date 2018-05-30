# -*- coding: utf-8 -*-
import re
import datetime
import time
import scrapy
import requests
from lxml import etree
from fagaiwei.settings import session, NewsItemInfo
from fagaiwei.items import FagaiweiItem
from fagaiwei.keyword_others import keyword


class ZiyuanSpider(scrapy.Spider):
    name = 'ziyuan'
    allowed_domains = ['mlr.gov.cn']
    start_urls = ['http://mlr.gov.cn/']

    def start_requests(self):
        urls = [
            "http://www.mlr.gov.cn/xwdt/bmdt/",  # 自然资源部-新闻动态-部位动态
            "http://www.mlr.gov.cn/xwdt/xwpl/",  # 自然资源部-新闻动态-评论
            "http://www.mlr.gov.cn/xwdt/chxw/",  # 自然资源部-新闻动态-测绘新闻
            "http://www.mlr.gov.cn/xwdt/hyxw/",  # 自然资源部-新闻动态-海洋新闻
            "http://www.mlr.gov.cn/xwdt/kyxw/",  # 自然资源部-新闻动态-矿产新闻
            "http://www.mlr.gov.cn/xwdt/dzdc/",  # 自然资源部-新闻动态-地质调查
            "http://www.mlr.gov.cn/xwdt/tddcxw/",  # 自然资源部-新闻动态-土地督察新闻
            "http://www.mlr.gov.cn/xwdt/tdxw/",  # 自然资源部-新闻动态-土地新闻
            "http://www.mlr.gov.cn/xwdt/dfdt/",  # 自然资源部-新闻动态-地方动态
            "http://www.mlr.gov.cn/xwdt/zfhy/xwfb/",  # 自然资源部-新闻动态-会议活动-新闻发布会
            "http://www.mlr.gov.cn/xwdt/zfhy/",  # 自然资源部-新闻动态-会议活动
            "http://www.mlr.gov.cn/xwdt/ldhd/",  # 自然资源部-新闻动态-领导活动
            "http://www.mlr.gov.cn/xwdt/jrxw/",  # 自然资源部-新闻动态-要闻播报
        ]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        # print(response.text)
        message_list = response.xpath('//*[@id="con"]/tr')
        for message in message_list:
            title = "".join(message.xpath('td[2]/a/text()').extract())
            href = "".join(message.xpath('td[2]/a/@href').extract())
            date = "".join(message.xpath('td[3]/text()').extract())
            date = date.replace(".", "-")
            # 防止空白行 只有提取到了标题的内容 才进行数据提取
            if title != "":
                try:
                    date = datetime.datetime.strptime(str(date).replace('/', '-'), '%Y-%m-%d')
                    # print(date)
                except Exception as e:
                    # print(e)
                    date = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
                # print(title, url, date)
                # 新闻发布会的数据内容不一样
                if "http://www.mlr.gov.cn" in href:
                    url = href.replace("index.htm", "")
                    # print(url)
                    result = session.query(NewsItemInfo).filter_by(url=url, web_id=8).count()
                    if result:
                        # print("{} 存在".format(url))
                        pass
                    else:
                        yield scrapy.Request(url=url, callback=self.get_detail_fbh,
                                             meta={"date": date, "title": title, "laiyuan": response.url})
                else:
                    url = response.url + href
                    result = session.query(NewsItemInfo).filter_by(url=url, web_id=8).count()
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
                                    //div[@class="TRS_Editor"]/div/span/p/text()|\
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
                                    //div[@class="TRS_Editor"]/div/div/div/p/text()|\
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
        item["content"] = contents.replace("\u3000", "").replace("\xa0", "")
        fo = "".join(response.xpath('//td[@class="Gray12"]/text()').extract())
        fo_s = fo.replace("\n", "").replace("\r", "").replace("\t", "").replace(" ", "")
        form_s = "".join(re.findall(re.compile(r'来源：(.*?)分享'), fo_s))
        # print(form_s)
        if form_s == "":
            form_s = "中华人民共和国自然资源部"
        item["webname"] = form_s
        item["web"] = response.meta["laiyuan"]
        item["web_id"] = 8
        item["keyword"] = keyword.get_keyword(item["content"])
        # print(item)
        return item

    def get_detail_fbh(self, response):
        item = FagaiweiItem()
        item["url"] = response.url
        item["title"] = response.meta["title"]
        item["pub_time"] = response.meta["date"]
        url = response.url + "jiabin/index_1217.xml"
        res = requests.get(url)
        res.encoding = 'gb2312'
        # print(res.text)
        tree = etree.HTML(res.text.encode('utf-8'))
        contents = "".join(tree.xpath('//text()'))
        # print(contents)
        item["content"] = contents.replace("\u3000", "").replace("\xa0", "").replace("\r", "").replace("\t", "")
        fo = "".join(response.xpath('//td[@class="Gray12"]/text()').extract())
        fo_s = fo.replace("\n", "").replace("\r", "").replace("\t", "").replace(" ", "")
        form_s = "".join(re.findall(re.compile(r'来源：(.*?)分享'), fo_s))
        # print(form_s)
        if form_s == "":
            if response.meta["laiyuan"] == "http://www.mlr.gov.cn/xwdt/zfhy/xwfb/":
                form_s = "中华人民共和国自然资源部-新闻发布会"
            else:
                form_s = "中华人民共和国自然资源部"
        item["webname"] = form_s
        item["web"] = response.meta["laiyuan"]
        item["web_id"] = 8
        item["keyword"] = keyword.get_keyword(item["content"])
        return item
