# -*- coding: utf-8 -*-
import re
import scrapy
from fagaiwei.items import FagaiweiItem
from fagaiwei.keyword_others import keyword
from fagaiwei.settings import session, NewsItemInfo


class TzzwSpider(scrapy.Spider):
    # 投资者网
    name = 'touzizhewang'
    allowed_domains = ['investorchina.com.cn']
    start_urls = ['http://www.investorchina.com.cn/article/type/1-1.html',
                  'http://www.investorchina.com.cn/article/type/3-1.html',
                  'http://www.investorchina.com.cn/article/type/4-1.html',
                  'http://www.investorchina.com.cn/article/type/6-1.html',
                  'http://www.investorchina.com.cn/article/type/9-1.html'
                  ]

    def parse(self, response):
        # 获取详情页连接
        url_list = response.xpath(
            '//*[@id="list_article"]/li/div[1]/a/@href|//h2[contains(@class,"ellipsis-2")]/a/@href').extract()
        for url in url_list:
            result = session.query(NewsItemInfo).filter_by(url='http://www.investorchina.com.cn' + url,
                                                           web_id=27).count()
            if result:
                # print("{} 存在".format('http://www.investorchina.com.cn' + url))
                pass
            else:
                yield scrapy.Request('http://www.investorchina.com.cn' + url, callback=self.process_detail,
                                     meta={'web': response.url})

    def process_detail(self, response):
        # 处理详情页信息
        item = FagaiweiItem()
        item['web_id'] = 27
        item['url'] = response.url
        item['title'] = response.xpath('//h2[contains(@class,"f-35 cf")]/text()').extract_first(default='')
        item['web'] = response.meta.get('web')
        news_about = response.xpath('//h3[contains(@class,"f-16 cf")]/span[1]/text()').extract_first(default='')
        laiyuan = news_about.split()[0]
        item['webname'] = '投资者网' if '1' in laiyuan else laiyuan
        item['pub_time'] = ''.join(re.findall(r'(\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2})', news_about))
        content = '\n'.join(response.xpath('//div[contains(@class,"f-16 cf con")]/text() | \
                                             //div[contains(@class,"f-16 cf con")]/div/text() | \
                                                  //div[contains(@class,"f-16 cf con")]/p/text() ').extract())
        item['content'] = re.sub(r'\s+\n', '', content).replace('\t', '\n')
        item["keyword"] = keyword.get_keyword(item["content"])

        yield item
