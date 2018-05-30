# -*- coding: utf-8 -*-
import datetime
import time
import scrapy
from fagaiwei.settings import session, NewsItemInfo
from fagaiwei.items import FagaiweiItem
from fagaiwei.keyword_others import keyword


class MinzushiwuSpider(scrapy.Spider):
    name = 'minzushiwu'
    allowed_domains = ['seac.gov.cn']
    start_urls = ['http://seac.gov.cn/']

    def start_requests(self):
        urls = [
            "http://www.seac.gov.cn/col/col149/index.html",  # 民族事务委员会-信息公开-规划统计-发展规划
            "http://www.seac.gov.cn/col/col144/index.html",  # 民族事务委员会-信息公开-文件公告-通知公告
            "http://www.seac.gov.cn/col/col34/index.html",  # 民族事务委员会-新闻中心-委属动态
            "http://www.seac.gov.cn/col/col33/index.html",  # 民族事务委员会-新闻中心-部委动态
            "http://www.seac.gov.cn/col/col32/index.html",  # 民族事务委员会-新闻中心-民委动态
            "http://www.seac.gov.cn/col/col36/index.html",  # 民族事务委员会-新闻中心-地方动态
            "http://www.seac.gov.cn/col/col31/index.html",  # 民族事务委员会-新闻中心-要闻
        ]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        message_list = response.xpath('//*[@id="2258"]/div/a|//*[@id="2705"]/div/a')
        for message in message_list:
            title = "".join(message.xpath('text()').extract())
            href = "".join(message.xpath('@href').extract())
            url = "http://www.seac.gov.cn" + href
            # print(title, url)
            result = session.query(NewsItemInfo).filter_by(url=url, web_id=12).count()
            if result:
                # print("{} 存在".format(url))
                pass
            else:
                yield scrapy.Request(url=url, callback=self.get_detail,
                                     meta={"title": title, "laiyuan": response.url})

    def get_detail(self, response):
        item = FagaiweiItem()
        item["url"] = response.url
        date = "".join(response.xpath('//*[@id="article"]/tr[2]/td/table/tr/td[1]/text()').extract())
        date = date.replace(" ", "").replace("\t", "").replace("\r", "").replace("\n", "").replace("日期：", "")
        try:
            date = datetime.datetime.strptime(str(date).replace('/', '-'), '%Y-%m-%d')
            # print(date)
        except Exception as e:
            # print(e)
            date = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
        item["pub_time"] = date
        item["title"] = response.meta["title"]
        form_s = "".join(response.xpath('//*[@id="article"]/tr[2]/td/table/tr/td[3]/text()').extract())
        form_s = form_s.replace(" ", "").replace("\t", "").replace("\r", "").replace("\n", "").replace("来源：", "")
        if form_s != "":
            item["webname"] = form_s
        else:
            item["webname"] = "民族事务委员会"
        item["web"] = response.meta["laiyuan"]
        item["web_id"] = 12
        contents = "".join(response.xpath('\
                                    //*[@id="zoom"]/div/p/text()|\
                                    //*[@id="zoom"]/div/p/span/text()|\
                                    //*[@id="zoom"]/strong/span/p/strong/text()|\
                                    //*[@id="zoom"]/p/text()|\
                                    //*[@id="zoom"]/p/a/text()|\
                                    //*[@id="zoom"]/p/b/span/text()|\
                                    //*[@id="zoom"]/p/strong/text()|\
                                    //*[@id="zoom"]/p/span/text()|\
                                    //*[@id="zoom"]/p/span/span/text()|\
                                    //*[@id="zoom"]/span/p/text()|\
                                    //*[@id="zoom"]/span/p/a/text()|\
                                    //*[@id="zoom"]/span/p/a/font/text()|\
                                    //*[@id="zoom"]/span/span/span/span/span/strong/span/span/strong/span/p/span/strong/span/span/strong/text()|\
                                    //*[@id="zoom"]/span/span/span/span/span/strong/span/span/p/span/text()|\
                                    //*[@id="zoom"]/span/span/span/span/span/strong/span/span/p/text()|\
                                    //*[@id="zoom"]/span/strong/span/span/p/strong/text()').extract())
        # print(contents)
        if contents != "":
            item["content"] = contents.replace("\u3000", "").replace("\xa0", "")
        else:
            item["content"] = "可能是图片或者表格文件 请打开详情页查看"
        item["keyword"] = keyword.get_keyword(item["content"])

        return item
