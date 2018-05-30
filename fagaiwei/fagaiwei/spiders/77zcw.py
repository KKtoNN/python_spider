# -*- coding: utf-8 -*-
import re
from datetime import datetime
import scrapy
from fagaiwei.items import FagaiweiItem
from fagaiwei.keyword_others import keyword
from fagaiwei.settings import session, NewsItemInfo


class ZjzxSpider(scrapy.Spider):
    # 中财网
    name = 'zcw'
    allowed_domains = ['cfi.cn']
    start_urls = [
        'http://industry.cfi.cn/BCA0A4127A4128A4132.html',  # 经济        取前10
        'http://industry.cfi.cn/BCA0A4127A4128A4135.html',  # 金融    取前10
        'http://industry.cfi.cn/BCA0A4127A4128A4136.html',  # 证券    取前10
        'http://industry.cfi.cn/BCA0A4127A4128A4137.html',  # 贸易   取前10
        # 'http://industry.cfi.cn/BCA0A4127A4128A4139.html'        #能源     信息过旧 舍弃
        'http://industry.cfi.cn/BCA0A4127A4128A4143.html',  # IT
        # 'http://industry.cfi.cn/BCA0A4127A4128A4145.html'         #国际    信息过旧 舍弃
    ]

    def parse(self, response):
        url_list = response.xpath('//div[@class="zidiv2"]/a/@href').extract()[:10]
        for url in url_list:
            new_url = 'http://industry.cfi.cn/' + url
            result = session.query(NewsItemInfo).filter_by(url=new_url, web_id=77).count()
            if result:
                # print("{} 存在".format(new_url))
                pass
            else:
                yield scrapy.Request(new_url, callback=self.process_detail, meta={'web': response.url})

    def process_detail(self, response):
        item = FagaiweiItem()
        item['web_id'] = 77
        item['url'] = response.url
        item['title'] = response.xpath('//*[@id="tdcontent"]/h1/text()').extract_first(default='')
        item['web'] = response.meta.get('web')
        news_about = response.xpath('//*[@id="tdcontent"]/table/tr/td[2]/text()').extract_first(default='')
        if news_about:
            webname = news_about.split('&nbsp')[-1]
            time = news_about.split('&nbsp')[0].split('时间：')[-1].strip()
            pub_time = re.sub(r'年|月|日', '-', time)
        else:
            webname = "中财网"
            pub_time = datetime.now()
        item['webname'] = webname if webname else ''
        item['pub_time'] = pub_time if pub_time else datetime.now()
        content = '\n'.join(response.xpath('//*[@id="tdcontent"]/text()').extract()).replace('\r\n\n', '')
        if not content:
            content = '这可能是图片或者文件，打开查看！'
        item['content'] = re.sub(r'\u3000|\r\n', '', content)
        item["keyword"] = keyword.get_keyword(item["content"])
        yield item
