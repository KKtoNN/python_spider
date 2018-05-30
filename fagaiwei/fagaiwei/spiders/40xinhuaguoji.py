# -*- coding: utf-8 -*-
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
import re
import datetime
from fagaiwei.items import FagaiweiItem
from fagaiwei.settings import session, NewsItemInfo
from fagaiwei.keyword_others import keyword

class XinhuaguojiSpider(CrawlSpider):
    # 新华网
    name = 'xinhuaguoji'
    allowed_domains = ['news.cn', 'xinhuanet.com']
    start_urls = [
        'http://www.xinhuanet.com/politics/',
        'http://www.xinhuanet.com/local/index.htm',
        'http://www.xinhuanet.com/legal/index.htm',
        'http://www.xinhuanet.com/world/index.htm',
        'http://www.xinhuanet.com/mil/index.htm',
        'http://www.xinhuanet.com/talking/index.htm',  # 访谈 爬去对象 未明确
        'http://www.xinhuanet.com/fortune/',
        'http://www.xinhuanet.com/money/index.htm',
        'http://www.xinhuanet.com/datanews/index.htm',  # 数据 爬去数据未明确
        'http://www.xinhuanet.com/yuqing/index.htm',
        'http://www.xinhuanet.com/politics/rs.htm',
        'http://www.xinhuanet.com/politics/xhll.htm',
        'http://www.xinhuanet.com/gangao/index.htm',
        'http://www.xinhuanet.com/tw/index.htm',
        'http://www.xinhuanet.com/overseas/index.htm',
        'http://education.news.cn/',  # 教育
        'http://www.xinhuanet.com/tech/index.htm',
        'http://www.xinhuanet.com/energy/index.htm',
    ]

    rules = (
        Rule(LinkExtractor(allow=r'http://education\.news\.cn/.*?\.htm'), callback='parse_item'),
        Rule(LinkExtractor(allow=r'http://www\.xinhuanet\.com/.*?\.htm', restrict_xpaths=('//ul[@class="dataList"]')),
             callback='parse_item'),
    )

    def testprint(self, response):
        pass

    def parse_item(self, response):

        conten_detail = response.xpath('//*[@id="p-detail"]').extract_first(default='')
        if response.status != 200 or not conten_detail:
            pass
        else:
            item = FagaiweiItem()
            item['webname'] = response.css('#source::text').extract_first('新华国际')
            item['web'] = re.split(r'[0-9]+', response.url)[0]
            item['title'] = response.xpath('//div[@class="h-title"]/text()').extract_first(default=None).strip()
            item['pub_time'] = response.css('.h-time::text').extract_first()
            content = '\n'.join(response.xpath('//div[@id="p-detail"]//p//strong/text() | \
                                                 //div[@id="p-detail"]//p//strong/font/text() | \
                                                //div[@id="p-detail"]//p/font/text() |\
                                                //div[@id="p-detail"]//p/text()| \
                                                //div[@id="p-detail"]//p/font/strong/text()| \
                                                //div[@id="p-detail"]//p/p/text() ').extract())
            if content != '\n':
                content = re.sub('\u3000', '', content)
            item['content'] = content
            item['url'] = response.url
            item['add_time'] = datetime.datetime.now().strftime('%Y-%m-%d %H-%M-%S')
            item['web_id'] = 40
            item["keyword"] = keyword.get_keyword(item["content"])
            result = session.query(NewsItemInfo).filter_by(url=item['url'], web_id=40).count()
            if result:
                # print("{} 存在".format(item['url']))
                pass
            else:
                yield item


if __name__ == '__main__':
    pass
