# -*- coding: utf-8 -*-
import datetime
import time
import scrapy
from fagaiwei.settings import session, NewsItemInfo
from fagaiwei.items import FagaiweiItem
from fagaiwei.keyword_others import keyword

class LuyoujuSpider(scrapy.Spider):
    name = 'luyouju'
    allowed_domains = ['cnta.gov.cn']
    start_urls = ['http://cnta.gov.cn/']

    def start_requests(self):
        urls = [
            "http://www.cnta.gov.cn/xxfb/mrgx/",  # 信息发布-每日更新=====好像这个网站最新的内容就都在这个地址
            "http://www.cnta.gov.cn/xxfb/xwlb/",  # 信息发布-新闻联播
            "http://www.cnta.gov.cn/zwgk/cxts/",  # 信息发布-出行提示
            "http://www.cnta.gov.cn/zwgk/tzggnew/gztz/",  # 政府信息公开>通知公告>工作通知
            "http://www.cnta.gov.cn/xxfb/jjgat/",  # 首页>信息发布>聚焦港澳台
            "http://www.cnta.gov.cn/xxfb/hydt/",  # 首页>信息发布>行业动态
            "http://www.cnta.gov.cn/zdgz/csgm/",  # 首页>重点工作>厕所革命
            "http://www.cnta.gov.cn/zdgz/qyly/",  # 首页>重点工作>全域旅游
            "http://www.cnta.gov.cn/zdgz/lyrc/",  # 首页>重点工作>旅游人才
            "http://www.cnta.gov.cn/zdgz/sctg/",  # 首页>重点工作>市场推广
            "http://www.cnta.gov.cn/zdgz/lyxf/",  # 首页>重点工作>旅游消费
            "http://www.cnta.gov.cn/zdgz/lyssc/",  # 首页>重点工作>旅游“双+双创”
            "http://www.cnta.gov.cn/zdgz/scjg/",  # 首页>重点工作>市场监管
            "http://www.cnta.gov.cn/zdgz/lytz/",  # 首页>重点工作>旅游投资
            "http://www.cnta.gov.cn/English_Column/",  # 首页>English Column
            # "http://www.cnta.gov.cn/xxfb/szxw/",  # 首页>信息发布>时政新闻====链接到了国务院的网站 可以忽略
            "http://www.cnta.gov.cn/xxfb/xxfb_dfxw/",  # 首页>信息发布>地方新闻
            "http://www.cnta.gov.cn/xxfb/jdxwnew2/",  # 首页>信息发布>焦点新闻
        ]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        message_list = response.xpath('//div[@class="lie_main_m"]/ul/li|//div[@class="lie_main_m"]/li')
        for message in message_list:
            title = "".join(message.xpath('a/text()').extract())
            # keyword = "".join(message.xpath('span/text()').extract())
            href = "".join(message.xpath('a/@href').extract())
            date = "".join(message.xpath('a/span/text()').extract())
            # print(href)
            try:
                date = datetime.datetime.strptime(str(date).replace('/', '-'), '%Y-%m-%d')
                # print(date)
            except Exception as e:
                # print(e)
                date = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))

            url = response.url + href
            # print(title, date, url)
            result = session.query(NewsItemInfo).filter_by(url=url, web_id=20).count()
            if result:
                # print("{} 存在".format(url))
                pass
            else:
                yield scrapy.Request(url=url, callback=self.get_detail,
                                     meta={"date": date,
                                           "title": title.replace("\r", "").replace("\n", "").replace("\t", ""),
                                           "laiyuan": response.url})

    def get_detail(self, response):
        item = FagaiweiItem()
        item["url"] = response.url
        item["pub_time"] = response.meta["date"]
        item["title"] = response.meta["title"]
        form_s = "".join(response.xpath('//div[@class="main_t"]/span[2]/text()').extract())
        form_s = form_s.split("：")[-1]
        if form_s != "":
            item["webname"] = form_s.replace(" ", "").replace("\r", "").replace("\n", "").replace("\t", "")
        else:
            item["webname"] = "中华人民共和国文化和旅游部"
        item["web"] = response.meta["laiyuan"]
        # item["keyword"] = ""
        item["web_id"] = 20
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
        item["content"] = contents.replace("\xa0", "").replace("\u3000", "")
        item["keyword"] = keyword.get_keyword(item["content"])

        return item
