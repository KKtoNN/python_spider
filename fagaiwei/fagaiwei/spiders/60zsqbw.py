# -*- coding: utf-8 -*-
import scrapy
from fagaiwei.items import FagaiweiItem
from fagaiwei.settings import session, NewsItemInfo
from fagaiwei.keyword_others import keyword


class ZsqbwSpider(scrapy.Spider):
    # 中商情报网
    name = 'zhongshangqingbaowang'
    allowed_domains = ['askci.com']

    def start_requests(self):
        urls = ['http://www.askci.com/news/finance/', 'http://www.askci.com/news/chanye/']
        for url in urls:
            yield scrapy.Request(url, callback=self.parse)

    def parse(self, response):
        # 获取文章链接
        url_list = response.xpath('//div[@class="ct_b_l_list"]//a[@class="ct_b_l_l_tb_tltie"]/@href').extract()
        for url in url_list:
            result = session.query(NewsItemInfo).filter_by(url=url, web_id=60).count()
            if result:
                # print("{} 存在".format(url))
                pass
            else:
                yield scrapy.Request(url, callback=self.process_detail, meta={"web": response.url})

    def process_detail(self, response):
        # 从文章详情页获取信息
        item = FagaiweiItem()
        item['web_id'] = 60
        item['url'] = response.url
        item['title'] = response.xpath('//div[@class="content_b_tltie"]/h1/text()').extract_first(default='')
        item['web'] = response.meta.get("web")
        item['webname'] = response.xpath('//div[@class="c_b_t_bq_atow"]/a[1]/@title').extract_first(default='')
        item['pub_time'] = ''.join(response.xpath('//div[@class="c_b_t_bq_atow"]/a[2]/text()').extract()).strip()
        item['content'] = '\n'.join(response.xpath('//*[@id="DivNewsContent"]/p/text() | \
                                              //*[@id="DivNewsContent"]/p/b/text()| \
                                            //*[@id="DivNewsContent"]/p/a/text()|\
                                             //*[@id="DivNewsContent"]/p/strong/text() | \
                                             //*[@id="DivNewsContent"]/p/p/text() | \
                                             //*[@id="DivNewsContent"]/p/span/text() ').extract()).replace('\xa0', '')
        item["keyword"] = keyword.get_keyword(item["content"])
        yield item
