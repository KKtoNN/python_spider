# -*- coding: utf-8 -*-
import re
import scrapy
from fagaiwei.items import FagaiweiItem
from fagaiwei.settings import session, NewsItemInfo
from fagaiwei.keyword_others import keyword


class ZjzxSpider(scrapy.Spider):
    # 龙腾网
    name = 'longtengwang'
    allowed_domains = ['ltaaa.com']

    def start_requests(self):
        start_urls = [
            'http://www.ltaaa.com/wtfy-military-1.html',  # 军事新闻
            'http://www.ltaaa.com/wtfy-economics-1.html',  # 经济新闻
            'http://www.ltaaa.com/wtfy-politics-1.html',  # 时事新闻
            'http://www.ltaaa.com/china/',  # 大陆新闻
            'http://www.ltaaa.com/world/'  # 国际新闻
        ]
        for url in start_urls:
            yield scrapy.Request(url, callback=self.parse)

    def parse(self, response):
        url_list = response.xpath(
            '//ul[@class="wlist"]/li/div[1]/a/@href|//div[@class="china"]/ul/li/div[1]/a/@href').extract()
        for url in url_list:
            url = response.urljoin(url)
            # response.follow(url,callback=self.process_detail,meta={'web': response.url})
            result = session.query(NewsItemInfo).filter_by(url=url, web_id=39).count()
            if result:
                # print("{} 存在".format(url))
                pass
            else:
                yield scrapy.Request(url, callback=self.process_detail,
                                     meta={'web': response.url})

    def process_detail(self, response):
        # print(response.url)
        item = FagaiweiItem()
        item['web_id'] = 39
        item['url'] = response.url
        item['title'] = response.css('.post-title strong::text').extract_first(default='')
        item['web'] = response.meta.get('web')
        item['webname'] = "龙腾网"
        news_about = response.xpath('string(//div[@class="post-param"])').extract_first()
        item['pub_time'] = re.search(r'(\d{4}-\d{2}-\d{2})', news_about).group(1)
        content = ''.join(response.xpath('string(//div[@class="post-content"])').extract()).replace('\xa0', '').replace(
            '\r', '')
        comment = ''.join(response.xpath('string(//div[@class="post-comment"])').extract()).replace('\xa0', '').replace(
            '\r', '')
        item['content'] = "正文翻译:\n" + content + "评论翻译:\n" + comment
        item["keyword"] = keyword.get_keyword(item["content"])
        yield item
