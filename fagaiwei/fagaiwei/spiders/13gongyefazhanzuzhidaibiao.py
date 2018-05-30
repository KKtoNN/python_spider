# -*- coding: utf-8 -*-
import datetime
import re
import time
import scrapy
from fagaiwei.settings import session, NewsItemInfo
from fagaiwei.items import FagaiweiItem
from fagaiwei.keyword_others import keyword


class GongyefazhanzuzhidaibiaoSpider(scrapy.Spider):
    name = 'gongyefazhanzuzhidaibiao'
    allowed_domains = ['mofcom.gov.cn']
    start_urls = ['http://mofcom.gov.cn/']

    def start_requests(self):
        urls = [
            "http://vienna.mofcom.gov.cn/article/cy/",  # 会议发言及表态
            "http://vienna.mofcom.gov.cn/article/ddfg/",  # 联合国国际贸易法委员会
            "http://vienna.mofcom.gov.cn/article/ddgk/",  # 联合国工业发展组织
            "http://vienna.mofcom.gov.cn/article/jmxw/",  # 要闻动态
            "http://vienna.mofcom.gov.cn/article/ztdy/",  # 业务研究
        ]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        message_list = response.xpath('//div[@class="alist"]/ul/li')
        for message in message_list:
            title = "".join(message.xpath('a/text()').extract())
            href = "".join(message.xpath('a/@href').extract())
            date = "".join(message.xpath('span/text()').extract())
            # print(title, href, date)
            try:
                date = datetime.datetime.strptime(str(date).replace('/', '-'), '%Y-%m-%d %H:%M:%S')
                # print(date)
            except Exception as e:
                # print(e)
                date = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))

            url = "http://vienna.mofcom.gov.cn" + href
            if title:
                result = session.query(NewsItemInfo).filter_by(url=url, web_id=13).count()
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
        # form_s = "".join(response.xpath('//*[@id="arsource"]/table/tr/td[1]/text()').extract())
        form_s = "".join(re.findall(re.compile(r'var source = "(.*?)";'), response.text))
        # print(form_s)
        form_s = form_s.replace(" ", "").replace("\t", "").replace("\r", "").replace("\n", "")  # .replace("文章来源：", "")
        if form_s != "":
            item["webname"] = form_s
        else:
            item["webname"] = "中华人民共和国常驻联合国工业发展组织代表处"
        item["web"] = response.meta["laiyuan"]
        item["web_id"] = 13
        contents = "".join(response.xpath('\
                                          //*[@id="zoom"]/div/p/text()|\
                                          //*[@id="zoom"]/div/p/span/text()|\
                                          //*[@id="zoom"]/strong/span/p/strong/text()|\
                                          //*[@id="zoom"]/p/text()|\
                                          //*[@id="zoom"]/p/a/text()|\
                                          //*[@id="zoom"]/p/a/strong/text()|\
                                          //*[@id="zoom"]/p/a/strong/span/text()|\
                                          //*[@id="zoom"]/p/b/span/text()|\
                                          //*[@id="zoom"]/p/strong/text()|\
                                          //*[@id="zoom"]/p/strong/span/text()|\
                                          //*[@id="zoom"]/p/span/text()|\
                                          //*[@id="zoom"]/p/span/a/text()|\
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
            if contents.replace(" ", "") == "":
                item["content"] = "可能是图片 请打开详情页查看"
            else:
                item["content"] = contents.replace("\u3000", "").replace("\xa0", "")
        else:
            item["content"] = "可能是图片 请打开详情页查看"
        item["keyword"] = keyword.get_keyword(item["content"])
        return item
