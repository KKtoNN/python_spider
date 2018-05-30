# -*- coding: utf-8 -*-
import re
import time
import scrapy
from fagaiwei.items import FagaiweiItem
from fagaiwei.keyword_others import keyword
from fagaiwei.settings import session, NewsItemInfo


class xiamenSipderSpider(scrapy.Spider):
    name = 'touzishibao_sipder'
    allowed_domains = ['zmoney.com', 'zmoney.com.cn']

    # start_urls = ['http://www.zmoney.com.cn/']

    def start_requests(self):
        urls = [
            'http://www.zmoney.com.cn/',
            'http://www.zmoney.com.cn/touzi/',
            'http://www.zmoney.com.cn/shangshi/',
            'http://www.zmoney.com.cn/car/',
            'http://www.zmoney.com.cn/yanjiu/',
        ]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        # print(response.text)
        # 获取页面详情页的url
        url1 = response.url
        contens_urls = response.xpath("//ul[@id='jiazai']/li/b/a/@href|"
                                      "//div[@class='imgholder']/a/@href").extract()  # .getall()
        for contens_url in contens_urls:
            result = session.query(NewsItemInfo).filter_by(url=contens_url, web_id=28).count()
            if result:
                # print("{} 存在".format(contens_url))
                pass
            else:
                yield scrapy.Request(url=contens_url, callback=self.parse_page, meta={'url': url1})

    def parse_page(self, response):
        item = FagaiweiItem()
        item['webname'] = '投资时报'
        item['web'] = response.meta['url']
        item['title'] = response.xpath("//h2/text()").get().replace('\xa0', '/n')
        item['url'] = response.url
        item['content'] = ''.join(list(response.xpath("//div[@class='para_ycont']/p/text()|"
                                                      "//div[@class='para_ycont']/p/span/text()|"
                                                      "//div[@class='para_ycont']/div/text()|"
                                                      "//div[@class='para_ycont']/text()").getall())) \
            .replace('\r\n', '').replace('\xa0', '')
        times = ''.join(list(response.xpath("//p[contains(@class,'s14')]/text()|"
                                            "//p[contains(@class,'s14')][1]/text()").getall()))
        item['pub_time'] = re.search(r'[0-9]{4}-[0-9]{2}-[0-9]{2} [0-9]{2}:[0-9]{2}', times).group() + ':00'
        item['add_time'] = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        item["keyword"] = keyword.get_keyword(item["content"])

        item['web_id'] = 28
        # time.sleep(0.5)

        return item
        pass
