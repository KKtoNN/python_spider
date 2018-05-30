# -*- coding: utf-8 -*-
import datetime
import re
import time
import scrapy
from fagaiwei.settings import session, NewsItemInfo
from fagaiwei.items import FagaiweiItem
from fagaiwei.keyword_others import keyword

class LiangshijuSpider(scrapy.Spider):
    name = 'liangshiju'
    allowed_domains = ['chinagrain.gov.cn', 'gov.cn']
    start_urls = ['http://chinagrain.gov.cn/']

    def start_requests(self):
        urls = [
            "http://www.chinagrain.gov.cn/n787423/index.html",  # 国家粮食和物资储备局 > 新闻中心
            "http://www.chinagrain.gov.cn/n316987/index.html",  # 国家粮食和物资储备局 > 专题专栏
            "http://www.chinagrain.gov.cn/n317135/index.html",  # 国家粮食和物资储备局 > 媒体声音
            "http://www.chinagrain.gov.cn/n317130/index.html",  # 国家粮食和物资储备局 > 行业报道
            "http://www.chinagrain.gov.cn/n317120/index.html",  # 国家粮食和物资储备局 > 政策通知
            "http://www.chinagrain.gov.cn/n317115/index.html",  # 国家粮食和物资储备局 > 工作动态
            # "http://www.chinagrain.gov.cn/n317125/index.html",  # 国家粮食和物资储备局 > 时政要闻==反爬=js==对接的国务院网站-已爬
            # "http://www.gov.cn/pushinfo/v150203/pushinfo.js",  # 国家粮食和物资储备局 > 时政要闻==反爬=js
        ]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        if response.url != "http://www.gov.cn/pushinfo/v150203/pushinfo.js":
            message_list = response.xpath('//ul[@class="list_01"]/li')
            for message in message_list:
                title = "".join(message.xpath('a/text()').extract())
                href = "".join(message.xpath('a/@href').extract())
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
                    url = response.url.replace("index.html", "") + href
                # print(title, date, url)
                result = session.query(NewsItemInfo).filter_by(url=url, web_id=18).count()
                if result:
                    # print("{} 存在".format(url))
                    pass
                else:
                    yield scrapy.Request(url=url, callback=self.get_detail,
                                         meta={"date": date, "title": title.replace("\r", "").replace("\n", ""),
                                               "laiyuan": response.url})
        else:
            href = re.findall(re.compile(r"href='(.*?htm)'"), response.text)
            title = re.findall(re.compile(r"blank'>(.*?)</a>"), response.text)
            date = re.findall(re.compile(r"<span>(.*?)</span>"), response.text)
            # print(title, date, href)
            # print(len(title), len(date), len(href))
            pass

    def get_detail(self, response):
        item = FagaiweiItem()
        item["url"] = response.url
        item["pub_time"] = response.meta["date"]
        item["title"] = response.meta["title"]
        form_s = "".join(response.xpath('//div[@class="right_md_laiy"]/h4/text()').extract())
        if form_s != "":
            item["webname"] = form_s
        else:
            item["webname"] = "国家粮食和物资储备局门户网站 "
        item["web"] = response.meta["laiyuan"]
        # item["keyword"] = ""
        item["web_id"] = 18
        contents = "".join(
            response.xpath('//div[@class="detail-pane search-help"]/table/tr/td/p/font/text()|\
                           //ul[@class="lsj_spe_list"]/li/div/text()|\
                            //*[@id="UCAP-CONTENT"]/p/text()|\
                            //*[@id="UCAP-CONTENT"]/p/span/span/text()|\
                            //div[@class="pages_content"]/p/text()|\
                            //div[@class="pages_content"]/p/a/text()|\
                            //div[@class="pages_content"]/div/p/text()|\
                            //*[@id="UCAP-CONTENT"]/p/span/text()|\
                           //ul[@class="lsj_spe_list"]/li/div/a/text()').extract())

        if contents != "":
            item["content"] = contents.replace("\u3000", "").replace("\xa0", "").replace("\u2002", "")
        else:
            item["content"] = "可能是图片 请打开详情页查看"
        item["keyword"] = keyword.get_keyword(item["content"])

        return item
