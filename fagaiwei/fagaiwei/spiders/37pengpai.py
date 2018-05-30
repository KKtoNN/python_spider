# -*- coding: utf-8 -*-
import scrapy
from fagaiwei.items import FagaiweiItem
from fagaiwei.settings import session, NewsItemInfo
from fagaiwei.keyword_others import keyword


class PengpaiSpider(scrapy.Spider):
    # 澎湃新闻
    name = 'pengpai'
    allowed_domains = ['thepaper.cn']
    start_urls = ['https://www.thepaper.cn/channel_25950', 'https://www.thepaper.cn/channel_25951',
                  'https://www.thepaper.cn/gov_publish.jsp']

    def parse(self, response):
        url_list = response.xpath(
            '//div[@class="news_li"]/h2/a/@href | //*[@id="listContent"]/div/div[2]//a/@href').extract()

        for url in url_list:
            result = session.query(NewsItemInfo).filter_by(url='https://www.thepaper.cn/' + url, web_id=37).count()
            if result:
                # print("{} 存在".format('https://www.thepaper.cn/' + url))
                pass
            else:
                yield scrapy.Request('https://www.thepaper.cn/' + url, callback=self.process_detail,
                                     meta={"web": response.url})

    def process_detail(self, response):
        item = FagaiweiItem()
        if response.xpath('//div[@class="news_txt"]'):  # 为了排除几个特殊的网址加入判断
            item["web_id"] = 37
            item["url"] = response.url
            item["title"] = response.xpath('//h1[@class="news_title"]/text()').extract_first()
            item["pub_time"] = response.xpath('//div[@class="news_about"]/p[2]/text()').extract_first().strip()
            item["content"] = '\n'.join(response.xpath('//div[@class="news_txt"]/div/text() | \
                                              //div[@class="news_txt"]/text() | \
                                              //div[@class="news_txt"]/strong/text() ').extract())
            item["webname"] = response.xpath('//div[@class="news_about"]/p[1]/text()').extract_first().strip()
            item["web"] = response.meta.get('web')
            item["keyword"] = keyword.get_keyword(item["content"])
            yield item
