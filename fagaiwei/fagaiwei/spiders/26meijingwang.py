# -*- coding: utf-8 -*-
import datetime
import time
import scrapy
from fagaiwei.settings import session, NewsItemInfo
from fagaiwei.items import FagaiweiItem
from fagaiwei.keyword_others import keyword


class MeijingwangSpider(scrapy.Spider):
    name = 'meijingwang'
    allowed_domains = ['nbd.com.cn']
    start_urls = ['nbd.com.cn/']

    def start_requests(self):
        urls = [
            "http://finance.nbd.com.cn/",  # 金融
            "http://industry.nbd.com.cn/",  # 公司
            "http://money.nbd.com.cn/",  # 基金
            "http://tmt.nbd.com.cn/",  # 未来商业
            "http://cd.nbd.com.cn/",  # 城市
            "http://xinsanban.nbd.com.cn/",  # 新经济
            "http://stocks.nbd.com.cn/",  # 证券
            "http://economy.nbd.com.cn/",  # 宏观
            "http://www.nbd.com.cn/columns/3",  # 要闻
            "http://live.nbd.com.cn/",
        ]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        # print(response.url)
        if response.url == "http://live.nbd.com.cn/":
            message_list = response.xpath('//ul[@class="live-list"]/li')
            # print(len(message_list))
            for message in message_list[:10]:
                item = FagaiweiItem()
                date = "".join(message.xpath('div[1]/p/span/text()').extract())
                content = "".join(message.xpath('div[2]/a/text()').extract())
                href = "".join(message.xpath('div[2]/a/@href').extract())
                days = time.strftime('%Y-%m-%d', time.localtime(time.time()))
                date = days + " " + date
                try:
                    dates = datetime.datetime.strptime(str(date), '%Y-%m-%d %H:%M:%S')
                except:
                    dates = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
                # print(dates, content, href)
                result = session.query(NewsItemInfo).filter_by(url=href, web_id=26).count()
                if result:
                    # print("{} 存在".format(href))
                    pass
                else:
                    item["url"] = href
                    item["pub_time"] = dates
                    item["title"] = content[:30]
                    item["webname"] = "每经网"
                    item["web"] = response.url
                    item["web_id"] = 26
                    item["content"] = content
                    # print(item)
                    item["keyword"] = keyword.get_keyword(item["content"])
                    yield item
        else:
            message_list = response.xpath('//ul[@class="m-columnnews-list"]/li|\
                                            //ul[@class="mt-ul"]/li|\
                                            //ul[@class="u-news-list"]/li')
            # print(len(message_list))
            for message in message_list:
                date_1 = "".join(message.xpath('//p[@class="u-channeltime"]/text()').extract())
                date_1 = date_1.replace(" ", "").replace("\n", "").replace("\t", "").replace("\r", "")
                date = "".join(message.xpath('div/div/p/span[2]/text()|div/p[2]/text()|span/text()').extract())
                title = "".join(message.xpath('div/div/a[1]/text()|div/a/text()|a/text()').extract())
                href = "".join(message.xpath('div/div/a/@href').extract())
                if not href:
                    href = "".join(message.xpath('div/a/@href').extract())
                    if not href:
                        href = "".join(message.xpath('a/@href').extract())
                date = date.replace(" ", "").replace("\n", "").replace("\t", "").replace("\r", "")
                date = date_1 + " " + date
                # print(date)
                try:
                    date = datetime.datetime.strptime(str(date).replace('-', '-'), '%Y-%m-%d %H:%M:%S')
                except Exception as e:
                    date = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
                url = href
                result = session.query(NewsItemInfo).filter_by(url=url.replace("#", ""), web_id=26).count()
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
        form_s = "".join(
            response.xpath('//span[@class="source"]/text()|//p[@class="article-meta"]/small/text()').extract())
        form_s = form_s.replace(" ", "").replace("\n", "").replace("\t", "").replace("\r", "")
        form_s = "".join([x for x in str(form_s) if str(x) not in
                          ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9", ':', '-']])
        if form_s:
            item["webname"] = form_s.replace(" ", "").replace("\n", "").replace("\t", "").replace("\r", "")
        else:
            item["webname"] = "每经网"
        item["web"] = response.meta["laiyuan"]

        item["web_id"] = 26
        contents = "".join(response.xpath('//div[@class="g-article"]/div/p/text()|\
                                            //div[class="nbd-con"]/blockquote/strong/text()|\
                                            //*[@id="vedioPlayer"]/p/text()|\
                                          //div[class="nbd-con"]/blockquote/p/text()').extract())
        if contents != "":
            item["content"] = contents.replace("\u3000", "").replace("\xa0", "").replace("\u2002", "")
        else:
            item["content"] = "可能是图片 请打开详情页查看"
        item["keyword"] = keyword.get_keyword(item["content"])
        yield item
