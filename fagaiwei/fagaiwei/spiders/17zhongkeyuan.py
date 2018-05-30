# -*- coding: utf-8 -*-
import datetime
import time
import scrapy
from fagaiwei.settings import session, NewsItemInfo
from fagaiwei.items import FagaiweiItem
from fagaiwei.keyword_others import keyword


class ZhongkeyuanSpider(scrapy.Spider):
    name = 'zhongkeyuan'
    allowed_domains = ['cas.cn', 'xinhuanet.com']
    start_urls = ['http://cas.cn/']

    def start_requests(self):
        urls = [
            "http://www.cas.cn/djcx/gz/",  # 首页-党建与创新文化-工作动态
            "http://www.cas.cn/yw/",  # 首页 > 中科院要闻
            "http://www.cas.cn/gj/",  # 首页 > 国家
            "http://www.cas.cn/xs/",  # 首页 > 学术会议
            "http://www.cas.cn/tz/",  # 首页 > 通知公告
            "http://www.cas.cn/kj/",  # 首页 > 科技动态
            "http://www.cas.cn/yx/",  # 首页 > 一线动态
            "http://www.cas.cn/zjs/",  # 首页 > 专家视点
            "http://www.cas.cn/cm/",  # 首页 > 传媒扫描
            "http://www.cas.cn/syky/",  # 首页 > 科研进展
        ]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        message_list = response.xpath('//div[@class="ztlb_ld_mainR_box01_list"]/ul/li')
        # print(len(message_list))
        for message in message_list:
            title = "".join(message.xpath('span/a/text()').extract())
            href = "".join(message.xpath('span/a/@href').extract())
            date = "".join(message.xpath('span/text()').extract())
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
            # print(title, url, date)
            result = session.query(NewsItemInfo).filter_by(url=url, web_id=17).count()
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
        form_s = "".join(response.xpath('//*[@id="source"]/span/text()|//span[@class="aticle-src"]/text()').extract())
        form_s = form_s.split("　")[0].replace("一", "")
        if form_s != "":
            item["webname"] = form_s.replace("\r", "").replace("\n", "").replace(" ", "")
        else:
            item["webname"] = "中国科学院"
        item["web"] = response.meta["laiyuan"]
        # item["keyword"] = ""
        item["web_id"] = 17
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
                                    //div[@class="TRS_Editor"]/div/div/div/p/text()|\
                                    //div[@class="TRS_Editor"]/div/div/div/p/span/text()|\
                                    //div[@class="TRS_Editor"]/div/div/div/p/font/font/span/text()|\
                                    //div[@class="TRS_Editor"]/div/div/div/span/p/text()|\
                                    //div[@class="TRS_Editor"]/div/div/div/span/p/span/text()|\
                                    //div[@class="TRS_Editor"]/div/div/div/span/p/font/font/span/text()|\
                                    //div[@class="TRS_Editor"]/div/div/div/div/p/text()|\
                                    //div[@class="TRS_Editor"]/div/div/div/div/span/p/text()|\
                                    //div[@class="TRS_Editor"]/div/div/div/div/div/text()|\
                                    //div[@class="TRS_Editor"]/div/div/div/div/div/div/text()|\
                                    //div[@class="TRS_Editor"]/div/div/div/div/div/div/p/text()|\
                                    //font[@face="Calibri"]/text()|\
                                    //font[@face="Calibri"]/span/text()|\
                                    //font[@face="Calibri"]/span/span/text()|\
                                    //*[@id="p-detail"]/p/text()|\
                                    //*[@id="p-detail"]/p/font/text()|\
                                    //*[@id="p-detail"]/p/font/strong/text()|\
                                    //*[@id="p-detail"]/p/font/span/text()|\
                                    //*[@id="p-detail"]/div/p/text()|\
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
        item["content"] = contents.replace("\u3000", "").replace("\xa0", "").replace("\u200b", "")
        item["keyword"] = keyword.get_keyword(item["content"])

        return item
