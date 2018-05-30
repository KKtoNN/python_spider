# -*- coding: utf-8 -*-
import datetime
import time
import scrapy
from fagaiwei.settings import session, NewsItemInfo
from fagaiwei.items import FagaiweiItem
from fagaiwei.keyword_others import keyword


class TiyuSpider(scrapy.Spider):
    name = 'tiyu'
    allowed_domains = ['sport.gov.cn']
    start_urls = ['http://sport.gov.cn/']

    def start_requests(self):
        urls = [
            "http://www.sport.gov.cn/n316/n336/index.html",  # 国家体育总局-新闻资讯-通知公告
            "http://www.sport.gov.cn/n316/n337/index.html",  # 国家体育总局-新闻资讯-总局动态
            "http://www.sport.gov.cn/n316/n338/index.html",  # 国家体育总局-新闻资讯-地方动态
            "http://www.sport.gov.cn/n316/n340/index.html",  # 国家体育总局-新闻资讯-信息发布
            "http://www.sport.gov.cn/n316/n342/index.html",  # 国家体育总局-新闻资讯-观点声音
            "http://www.sport.gov.cn/n10503/index.html",  # 国家体育总局-重要信息
        ]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        message_list = response.xpath('//table[@class="sv_yh_14_30"]/tr/td/table/tr')
        # print(len(message_list))
        for message in message_list:
            title = "".join(message.xpath('td[2]/a/text()').extract())
            href = "".join(message.xpath('td[2]/a/@href').extract())
            date = "".join(message.xpath('td[3]/text()').extract())
            # print(title, href, date)
            date = date.replace('[', '').replace(']', '')
            try:
                date = datetime.datetime.strptime(str(date).replace('/', '-'), '%Y-%m-%d')
                # print(date)
            except Exception as e:
                # print(e)
                date = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
            if href != "":
                url = response.url.replace("index.html", "") + href
                result = session.query(NewsItemInfo).filter_by(url=url, web_id=9).count()
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
        item["web"] = response.meta["laiyuan"]
        item["web_id"] = 9
        contents = "".join(response.xpath('//*[@id="ziti"]/p/text()|\
                                            //table[@class="MsoNormalTable"]/tbody/tr/td/p/span/span/span/text()|\
                                            //table[@class="MsoNormalTable"]/tbody/tr/td/p/span/span/span/span/text()|\
                                            //*[@id="ziti"]/p/font/text()|\
                                            //*[@id="ziti"]/p/span/text()|\
                                            //*[@id="ziti"]/p/span/font/text()|\
                                            //*[@id="ziti"]/p/span/span/text()|\
                                            //*[@id="ziti"]/p/span/span/span/text()|\
                                            //*[@id="ziti"]/p/span/span/span/span/text()|\
                                            //*[@id="ziti"]/p/span/span/span/span/span/text()|\
                                            //*[@id="ziti"]/p/span/span/span/span/span/span/text()|\
                                            //*[@id="ziti"]/p/b/span/span/span/text()|\
                                            //*[@id="ziti"]/p/span/span/span/font/text()|\
                                            //*[@id="ziti"]/p/text()').extract())
        # print(contents)
        if contents != "":
            item["content"] = contents.replace("\u3000", "").replace("\xa0", "")
        else:
            item["content"] = "国家体育局 可能是图片 打开原文查看"
        form_s = "".join(response.xpath('//div[@class="wz_info"]/span[2]/text()').extract())
        form_s = form_s.replace("来源：", "")
        if form_s != "":
            webname = form_s
        else:
            webname = "国家体育局"
        item["webname"] = webname
        item["keyword"] = keyword.get_keyword(item["content"])
        return item
