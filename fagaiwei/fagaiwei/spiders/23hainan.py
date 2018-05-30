# -*- coding: utf-8 -*-
import datetime
import re
import time
import scrapy
from fagaiwei.settings import session, NewsItemInfo
from fagaiwei.items import FagaiweiItem
from fagaiwei.keyword_others import keyword


class HainanSpider(scrapy.Spider):
    name = 'hainan'
    allowed_domains = ['hainan.gov.cn']

    # start_urls = ['http://hainan.gov.cn/']

    def start_requests(self):
        urls = [
            "http://www.hainan.gov.cn/hn/yw/zwdt/tj/",  # 今日要闻-政务动态-厅局
            "http://www.hainan.gov.cn/hn/yw/zwdt/sx/",  # 今日要闻-政务动态-市县
            "http://www.hainan.gov.cn/hn/yw/jrhn/",  # 今日要闻-今日海南
            "http://www.hainan.gov.cn/hn/yw/ldhd/",  # 今日要闻-领导活动
            "http://www.hainan.gov.cn/hn/yw/mtkhn/",  # 今日要闻-媒体看海南
            "http://www.hainan.gov.cn/hn/zwgk/rsrm/gbrm/",  # 政务公开-人事信息-干部任免
            "http://www.hainan.gov.cn/hn/zwgk/rsrm/rqgs/",  # 政务公开-人事信息-任前公示
            # # "http://www.hainan.gov.cn/hn/zwgk/rsrm/gbxb/",  # 政务公开-人事信息-干部选拔
            "http://www.hainan.gov.cn/hn/zwgk/xwfb/szf/",  # 政务公开-海南省新闻发布-省政府新闻发布会
            "http://www.hainan.gov.cn/hn/zwgk/xwfb/bm/",  # 政务公开-海南省新闻发布-省直部门新闻发布会
            "http://www.hainan.gov.cn/hn/zwgk/xwfb/sx/",  # 政务公开-海南省新闻发布-市县新闻发布会
        ]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        message_list = response.xpath('//ul[@class="flfg_03"]/li')
        for message in message_list:
            date = "".join(message.xpath('span/text()').extract())
            title = "".join(message.xpath('a/text()').extract()).replace("· ", "")
            href = "".join(message.xpath('a/@href').extract())
            try:
                date = datetime.datetime.strptime(str(date).replace('-', '-'), '%Y-%m-%d')
            except Exception as e:
                date = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
            if str("www.hainan.gov.cn") in href:
                result = session.query(NewsItemInfo).filter_by(url=href, web_id=23).count()
                if result:
                    # print("{} 存在".format(href))
                    pass
                else:
                    if str(href) == "http://www.hainan.gov.cn/":
                        pass
                    else:
                        yield scrapy.Request(url=href, callback=self.get_detail,
                                             meta={"date": date, "title": title, "laiyuan": response.url})
            else:
                url = response.url + href  # .replace("./", "")
                result = session.query(NewsItemInfo).filter_by(url=url, web_id=23).count()
                if result:
                    # print("{} 存在".format(url))
                    pass
                else:
                    if str(url) == "http://www.hainan.gov.cn/":
                        pass
                    else:
                        yield scrapy.Request(url=url, callback=self.get_detail,
                                             meta={"date": date, "title": title, "laiyuan": response.url})

    def get_detail(self, response):
        item = FagaiweiItem()
        item["url"] = response.url
        item["title"] = response.meta["title"]
        item["pub_time"] = response.meta["date"]
        contents = "\n".join(response.xpath('\
                                            //*[@id="Zoom"]/span/p/text()|\
                                            //*[@id="Zoom"]/span/p/font/text/text()|\
                                            //*[@id="Zoom"]/span/p/font/strong/text/text()|\
                                            //div[@class="TRS_Editor"]/div/b/text()|\
                                            //div[@class="TRS_Editor"]/p/text()|\
                                            //div[@class="TRS_Editor"]/p/font/text()|\
                                            //div[@class="TRS_Editor"]/p/strong/text()|\
                                            //div[@class="TRS_Editor"]/p/a/text()|\
                                            //div[@class="TRS_Editor"]/p/a/font/text()|\
                                            //div[@class="TRS_Editor"]/div/p/text()|\
                                            //div[@class="TRS_Editor"]/div/text/text()|\
                                            //*[@id="neirongText"]/div/p/text()|\
                                            //*[@id="neirongText"]/div/p/text/text()\
                                            //*[@id="neirongText"]/div/p/strong/text/text()').extract())
        if contents == "":
            item["content"] = "可能是图片或表格 打开原网站查看"
        else:
            item["content"] = contents.replace("\u3000", " ").replace("\xa0", "  ")
        form_s = "".join(response.xpath('//ul/li[1]/text()').extract())
        if form_s == "":
            # 只能使用正则进行匹配
            com = re.compile(r'laiyuan  = "(.*?)";')
            form_s = "".join(re.findall(com, response.text))
            if form_s == "":
                form_s = "海南省政府网站"
        else:
            form_s = form_s
        item["webname"] = form_s.replace("来源：", "")
        item["web"] = response.meta["laiyuan"]
        item["keyword"] = keyword.get_keyword(item["content"])

        item["web_id"] = 23
        return item
