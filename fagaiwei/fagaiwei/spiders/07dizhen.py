# -*- coding: utf-8 -*-
import time
import datetime
import scrapy
from fagaiwei.items import FagaiweiItem
from fagaiwei.settings import session, NewsItemInfo
from fagaiwei.keyword_others import keyword


class DizhenSpider(scrapy.Spider):
    name = 'dizhen'
    allowed_domains = ['cea.gov.cn', "xinhuanet.com"]
    start_urls = ['http://cea.gov.cn/']

    def start_requests(self):
        urls = [
            "http://www.cea.gov.cn/publish/dizhenj/464/478/index.html",  # 防震减灾要闻
            "http://www.cea.gov.cn/publish/dizhenj/464/102620/index.html",  # 要闻播报
            "http://www.cea.gov.cn/publish/dizhenj/464/495/index.html",  # 行业动态
            "http://www.cea.gov.cn/publish/dizhenj/464/102140/index.html",  # 市县工作
            "http://www.cea.gov.cn/publish/dizhenj/464/522/index.html",  # 媒体播报
            "http://www.cea.gov.cn/publish/dizhenj/464/515/index.html",  # 热点报道
            "http://www.cea.gov.cn/publish/dizhenj/464/479/index.html",  # 震情速递
        ]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        message_list = response.xpath('//ul/li')
        # print(len(message_list))
        for message in message_list:
            href = "".join(message.xpath('a/@href').extract())
            title = "".join(message.xpath('a/text()').extract())
            date = "".join(message.xpath('span/text()').extract())
            if date != "":
                if "http" in href.lower():
                    url = href
                else:
                    url = "http://www.cea.gov.cn" + href
                date = date.replace('[', '').replace(']', '')
                # print(date)
                try:
                    date = datetime.datetime.strptime(str(date).replace('/', '-'), '%Y-%m-%d %H:%M:%S')
                    # print(date)
                except Exception as e:
                    # print(e)
                    date = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
                result = session.query(NewsItemInfo).filter_by(url=url, web_id=7).count()
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
        contents = "".join(response.xpath('//div[@class="detail_main_right_con"]/div/div/div/text()|\
                                        //div[@class="detail_main_right_con"]/div/div/div/p/text()|\
                                        //*[@id="p-detail"]/div/p/text()|\
                                        //div[@class="detail_main_right_con"]/div/div/div/script/text()').extract())
        # print(contents)
        item["content"] = contents.replace("\n", "").replace("\xa0", "").replace('subStringLocationLongitude("', '') \
            .replace('");', ' ,').replace('subStringLocationLatitude("', '').replace('origTime("', '') \
            .replace('shengdu("', '').replace("\u3000", "")
        from_s = "".join(response.xpath('//div[@class="detail_main_right_con"]/div[1]/div[1]/div[3]/text()').extract())
        from_s = from_s.split("：")[-1]
        # print(from_s)
        if from_s != "":
            item["webname"] = from_s.replace(" ", "").replace("\n", "").replace("\t", "").replace("\r", "")
        else:
            item["webname"] = "中国地震局办公室"
        item["web"] = response.meta["laiyuan"]
        item["web_id"] = 7
        item["keyword"] = keyword.get_keyword(item["content"])
        # print(item)
        return item
