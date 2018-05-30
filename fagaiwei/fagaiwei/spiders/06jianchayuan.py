# -*- coding: utf-8 -*-
import datetime
import time
import scrapy
from fagaiwei.settings import session, NewsItemInfo
from fagaiwei.items import FagaiweiItem
from fagaiwei.keyword_others import keyword


class JianchayuanSpider(scrapy.Spider):
    name = 'jianchayuan'
    allowed_domains = ['spp.gov.cn']
    start_urls = ['http://spp.gov.cn/']

    def start_requests(self):
        urls = [
            "http://www.spp.gov.cn/spp/gjybs/index.shtml",  # 检察新闻-最高检新闻
            # "http://www.spp.gov.cn/spp/qwfb/index.shtml",  # 检察新闻-权威发布-全部
            "http://www.spp.gov.cn/spp/qwfb/2018nian/index.shtml",  # 检察新闻-权威发布-2018-只要2018的就行了-最新的
            "http://www.spp.gov.cn/spp/dfjcdt/index.shtml",  # 检察新闻-地方动态
            "http://www.spp.gov.cn/spp/wsfbt/index.shtml",  # 检察新闻-网上发布厅
        ]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        message_list = response.xpath('//div[@class="commonList_con"]/ul/li')
        for message in message_list:
            title = "".join(message.xpath('a/text()|a/span/text()').extract())
            href = "".join(message.xpath('a/@href').extract())
            date = "".join(message.xpath('span/text()').extract())
            date = date.replace("年", "-").replace("月", "-").replace("日", "-")
            try:
                date = datetime.datetime.strptime(str(date).replace('/', '-'), '%Y-%m-%d')
                # print(date)
            except Exception as e:
                # print(e)
                date = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
            # print(title, href, date)
            if "http" in href:
                url = href
            else:
                url = "http://www.spp.gov.cn" + href
            # print(url,title)
            result = session.query(NewsItemInfo).filter_by(url=url.replace("#1", ""), web_id=6).count()
            if result:
                # print("{} 存在".format(url))
                pass
            else:
                yield scrapy.Request(url=url, callback=self.get_detail,
                                     meta={"date": date,
                                           "title": title.replace('\t', '').replace('\n', '').replace('\r', ''),
                                           "laiyuan": response.url})

    def get_detail(self, response):
        item = FagaiweiItem()
        item["url"] = response.url.replace("#1", "")
        item["pub_time"] = response.meta["date"]
        item["title"] = response.meta["title"]
        # print(item)
        contents = "\n".join(response.xpath('//div[@class="Custom_UnionStyle"]/p/text()|\
                                        //div[@class="TRS_Editor"]/p/text()|\
                                        //div[@class="TRS_Editor"]/div/p/text()|\
                                        //div[@class="mainbox"]/span/p/text()|\
                                        //div[@class="Custom_UnionStyle"]/p/text()|\
                                        //div[@class="Custom_UnionStyle"]/span/p/text()|\
                                        //div[@class="Custom_UnionStyle"]/div/text()|\
                                        //div[@class="Custom_UnionStyle"]/div/p/text()|\
                                        //div[@class="Custom_UnionStyle"]/div/div/p/text()|\
                                        //*[@id="fontzoom"]/div[1]/p/text()|\
                                        //*[@id="fontzoom"]/div/p/text()|\
                                        //*[@id="fontzoom"]/div/text()|\
                                        //*[@id="fontzoom"]/div/h2/text()|\
                                        //*[@id="fontzoom"]/div/p/strong/text()|\
                                        //*[@id="fontzoom"]/div/span/text()|\
                                        //*[@id="fontzoom"]/div/span/p/text()|\
                                        //*[@id="fontzoom"]/div/span/div/p/text()|\
                                        //*[@id="fontzoom"]/div/div/text()|\
                                        //*[@id="fontzoom"]/div/div/p/text()|\
                                        //*[@id="fontzoom"]/div/div/span/p/text()|\
                                        //*[@id="fontzoom"]/div/div/div/p/text()|\
                                        //*[@id="fontzoom"]/p/text()|\
                                        //*[@id="fontzoom"]/p/span/text()').extract())
        item["content"] = contents.replace("\u3000", "")
        form_s = "".join(response.xpath('//div[@class="detail_extend"]/div[1]/text()').extract())
        name = form_s.split("：")[-1]
        if name != "":
            item["webname"] = name
        else:
            item["webname"] = "最高人民检察院"
        item["web"] = response.meta["laiyuan"]
        item["web_id"] = 6
        item["keyword"] = keyword.get_keyword(item["content"])
        return item
