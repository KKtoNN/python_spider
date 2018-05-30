# -*- coding: utf-8 -*-
import re
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from fagaiwei.items import FagaiweiItem
from fagaiwei.settings import session, NewsItemInfo
from fagaiwei.keyword_others import keyword

class SzseSpider(CrawlSpider):
    name = 'szse'
    allowed_domains = ['szse.cn']
    start_urls = ['http://www.szse.cn/main/disclosure/bsgg_front/',  # 深证证券交易所：本所公告
                  'http://www.szse.cn/main/aboutus/bsyw/',  # 深证证券交易所：本所要闻
                  'http://www.szse.cn/main/aboutus/bsdt_left/xwfbh/']  # 深证证券交易所： 新闻发布会

    rules = (
        Rule(LinkExtractor(allow=r'/main/disclosure/bsgg_front/[0-9]+.shtml'), callback='parse_item'),  # 深证证券交易所：本所公告
        Rule(LinkExtractor(allow=r'/main/aboutus/bsyw/[0-9]+.shtml'), callback='parse_item'),  # 深证证券交易所：本所要闻
        Rule(LinkExtractor(allow=r'/main/aboutus/bsdt_left/xwfbh/[0-9]+.shtml'), callback='parse_item')
        # 深证证券交易所： 新闻发布会
    )

    def parse_item(self, response):
        item = FagaiweiItem()
        item['webname'] = '深圳证券交易所'
        item['web'] = re.split(r'[0-9]+', response.url)[0]
        item['url'] = response.url
        item['title'] = str(response.css('.yellow_bt15::text').extract_first(default='')).strip()
        item['pub_time'] = re.split(r'：', response.css('.botborder1::text').extract_first())[-1].strip()
        content = ''.join(response.xpath('//div[@class="news_zw"]/p/span/text()|\
                                                //div[@class="news_zw"]/span/p/span/text() | \
                                                //div[@class="news_zw"]/span/p/span/a/text() | \
                                                //div[@class="news_zw"]/span/p/span/span/text() | \
                                                //div[@class="news_zw"]/p/span/span/text()| \
                                                //div[@class="news_zw"]/p/b/span/text() | \
                                                //div[@class="news_zw"]/p/span/text() | \
                                                //div[@class="news_zw"]/p/span/span/text() | \
                                                //div[@class="news_zw"]/p/b/span/span/text()').extract())
        content = re.sub(r'\n?(-?[0-9]+)\n', r'\1', content)
        item['content'] = content
        item["keyword"] = keyword.get_keyword(item["content"])
        # item['add_time'] = datetime.datetime.now().strftime('%Y-%m-%d %H-%M-%S')
        item['web_id'] = 59
        # print(item)
        result = session.query(NewsItemInfo).filter_by(url=response.url, web_id=59).count()
        if result:
            # print("{} 存在".format(response.url))
            pass
        else:
            yield item


if __name__ == '__main__':
    pass
