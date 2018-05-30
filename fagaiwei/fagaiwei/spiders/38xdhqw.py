# -*- coding: utf-8 -*-
import scrapy
from fagaiwei.items import FagaiweiItem
from fagaiwei.settings import session, NewsItemInfo
from fagaiwei.keyword_others import keyword

class ZjzxSpider(scrapy.Spider):
    # 星岛环球网
    name = 'xingdaohuanqiu'
    allowed_domains = ['stnn.cc']
    start_urls = ['http://news.stnn.cc/hongkong/',  # 香港新闻
                  'http://news.stnn.cc/china/',  # 大陆新闻
                  'http://news.stnn.cc/hk_taiwan/',  # 台湾新闻
                  'http://news.stnn.cc/guoji/',  # 国际新闻

                  ]

    def parse(self, response):
        url_list = response.css('ul.box2 li a::attr(href)').extract()
        for url in url_list:
            result = session.query(NewsItemInfo).filter_by(url=url, web_id=38).count()
            if result:
                # print("{} 存在".format(url))
                pass
            else:
                yield scrapy.Request(url, callback=self.process_detail, meta={'web': response.url})

    def process_detail(self, response):
        item = FagaiweiItem()
        item['web_id'] = 38
        item['url'] = response.url
        item['title'] = response.css('div.inner h1::text').extract_first(default='')
        item['web'] = response.meta.get('web')
        item['webname'] = response.css('div.article-infos span.source::text').extract_first(default='').strip()
        item['pub_time'] = response.css('div.article-infos span.date::text').extract_first(default='')
        item['content'] = '\n'.join(response.css('div.article-content p>strong::text,p::text').extract())
        item["keyword"] = keyword.get_keyword(item["content"])
        yield item
