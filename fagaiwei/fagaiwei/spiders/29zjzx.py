# -*- coding: utf-8 -*-
import re
import scrapy
from fagaiwei.items import FagaiweiItem
from fagaiwei.keyword_others import keyword
from fagaiwei.settings import session, NewsItemInfo


class ZjzxSpider(scrapy.Spider):
    # 中金在线
    name = 'zhongjinzaixian'
    allowed_domains = ['cnfol.com']
    start_urls = ['http://news.cnfol.com/',  # 财经
                  'http://stock.cnfol.com/',  # 股票
                  'http://fund.cnfol.com/',  # 基金
                  'http://money.cnfol.com/',  # 理财
                  'http://xg.stock.cnfol.com/'  # 新股
                  ]

    def parse(self, response):
        url_list = response.xpath(
            '//div[@class="mBlock"]/div[@class="artBlock"]/a/@href|//*[@id="artList"]/div/a/@href').extract()
        for url in url_list:
            result = session.query(NewsItemInfo).filter_by(url=url, web_id=29).count()
            if result:
                # print("{} 存在".format(url))
                pass
            else:
                yield scrapy.Request(url, callback=self.process_detail, meta={'web': response.url})

    def process_detail(self, response):
        item = FagaiweiItem()
        item['web_id'] = 29
        item['url'] = response.url
        item['title'] = ''.join(
            response.xpath('//div[contains(@class,"artMain mBlock")]/h3[@class="artTitle"]/text()').extract())
        item['web'] = response.meta.get('web')
        # item['keyword'] = ''
        news_about = response.xpath('//div[@class="artDes"]/span/text()').extract()
        webname = news_about[1].split(':')[1]
        if not webname:
            webname = response.xpath('//div[@class="artDes"]/span[2]/a/text()').extract_first(default='中金在线')
        item['webname'] = webname
        item['pub_time'] = news_about[0]
        content = '\n'.join(response.xpath('//div[@class="Article"]/text() | \
                                                   //div[@class="Article"]/span/text() | \
                                                   //div[@class="Article"]/a/text()').extract())
        content = re.sub('\u3000|\r\n|\n\n', '', content)
        item['content'] = content
        item["keyword"] = keyword.get_keyword(item["content"])

        yield item
