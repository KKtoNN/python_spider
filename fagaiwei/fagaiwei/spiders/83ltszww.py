# -*- coding: utf-8 -*-
import re
import scrapy
from fagaiwei.items import FagaiweiItem
from fagaiwei.keyword_others import keyword
from fagaiwei.settings import session, NewsItemInfo


class ZjzxSpider(scrapy.Spider):
    # 路透社中文网    新闻过旧
    name = 'ltszww'
    allowed_domains = ['acbgg.com']
    start_urls = [
        'http://www.acbgg.com/finance/gsdt/',  # 股市    新闻过旧
        'http://www.acbgg.com/finance/zqsc/',  # 证券    新闻过旧
        'http://www.acbgg.com/finance/licai/',  # 理财   新闻过旧
    ]

    def parse(self, response):
        url_list = response.xpath('//div[@class="newslist"]/ul/li/div[1]/a/@href').extract()
        for url in url_list:
            new_url = 'http://www.acbgg.com' + url
            result = session.query(NewsItemInfo).filter_by(url=new_url, web_id=83).count()
            if result:
                # print("{} 存在".format(new_url))
                pass
            else:
                yield scrapy.Request(new_url, callback=self.process_detail, meta={'web': response.url})

    def process_detail(self, response):
        item = FagaiweiItem()
        item['web_id'] = 83
        item['url'] = response.url
        item['title'] = response.xpath('//div[@class="conText"]/h1/text()').extract_first('')
        item['web'] = response.meta.get('web')
        item['webname'] = "路透社"
        news_about = response.xpath('//div[@class="conText"]/div[@class="summary"]/strong/text()').extract_first()
        item['pub_time'] = re.findall(r'(\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2})', news_about)[0]
        content = '\n'.join(response.xpath('//*[@id="text"]/p/text() | \
                                //*[@id="text"]/p/strong/text() | \
                                //*[@id="text"]/p/a/text() ').extract()).replace('\u3000', '')
        if not content:
            content = '这可能是图片或者文件，打开查看！'
        item['content'] = content
        item["keyword"] = keyword.get_keyword(item["content"])
        yield item
