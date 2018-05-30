# -*- coding: utf-8 -*-
import scrapy
from fagaiwei.items import FagaiweiItem
from fagaiwei.settings import session, NewsItemInfo
from fagaiwei.keyword_others import keyword


class ZjzxSpider(scrapy.Spider):
    # 证券时报网
    name = 'zqsbw'
    allowed_domains = ['stcn.com']
    start_urls = [
        'http://kuaixun.stcn.com/index.shtml',  # 快讯
        'http://news.stcn.com/',  # 要闻
        'http://www.stcn.com/gdxw/1.shtml',  # 滚动新闻
        'http://stock.stcn.com/dapan/index.shtml',  # 大盘信息
        'http://stock.stcn.com/bankuai/index.shtml',  # 板块
    ]

    def parse(self, response):
        url_list = response.xpath('//*[@id="mainlist"]/ul/li/p/a/@href|//ul[@id="idData"]/li/p[1]/a/@href').extract()
        for url in url_list:
            if '1' in url:
                result = session.query(NewsItemInfo).filter_by(url=url, web_id=61).count()
                if result:
                    # print("{} 存在".format(url))
                    pass
                else:
                    yield scrapy.Request(url, callback=self.process_detail, meta={'web': response.url})

    def process_detail(self, response):
        item = FagaiweiItem()
        item['web_id'] = 61
        item['url'] = response.url
        item['title'] = response.xpath('//div[@class="intal_tit"]/h2/text()').extract_first(default='')
        item['web'] = response.meta.get('web')
        news_about = response.xpath('string(//div[@class="intal_tit"]/div[@class="info"])').extract_first()
        item['webname'] = news_about.split('来源：')[-1].strip()
        item['pub_time'] = news_about.split('来源：')[0].strip()
        content = '\n'.join(response.xpath('//*[@id="ctrlfscont"]/p/text() | \
                                           //*[@id="ctrlfscont"]/p/strong/text()').extract())
        if not content:
            content = '可能是图片或者文件，打开查看！'
        item['content'] = content
        item["keyword"] = keyword.get_keyword(item["content"])
        yield item
