# -*- coding: utf-8 -*-
import re
import time
import scrapy
from fagaiwei.items import FagaiweiItem
from fagaiwei.settings import session, NewsItemInfo
from fagaiwei.keyword_others import keyword


class ZjzxSpider(scrapy.Spider):
    # 中国新闻网
    name = 'zhongguonews'
    allowed_domains = ['chinanews.com']

    def start_requests(self):
        start_urls = [
            'http://www.chinanews.com/china/',  # 时政
            'http://www.chinanews.com/world/',  # 国际
            'http://fortune.chinanews.com/'  # 金融
        ]
        for url in start_urls:
            yield scrapy.Request(url, callback=self.parse)
        timstamp = str(time.time())[0:14].replace('.', '')
        url = [
            'http://channel.chinanews.com/cns/s/channel:sh.shtml?pager=0&pagenum=20&_={}'.format(timstamp),  # 社会    JS
            'http://channel.chinanews.com/cns/s/channel:cj.shtml?pager=0&pagenum=20&_={}'.format(timstamp)  # 财经     JS
        ]
        for url in url:
            yield scrapy.Request(url, callback=self.parse_js)

    def parse_js(self, response):
        url_list = re.findall(r'"url"\s?:\s?"(.*?)"', response.text)
        for url in url_list:
            result = session.query(NewsItemInfo).filter_by(url=url, web_id=36).count()
            if result:
                # print("{} 存在".format(url))
                pass
            else:
                yield scrapy.Request(url, callback=self.process_detail, meta={'web': response.url})

    def parse(self, response):
        url_list = response.xpath('//*[@id="ent0"]/li//div[@class="news_title"]/em/a/@href').extract()
        # print(url_list)
        for url in url_list:
            result = session.query(NewsItemInfo).filter_by(url='https:' + url, web_id=36).count()
            if result:
                # print("{} 存在".format('https:' + url))
                pass
            else:
                yield scrapy.Request('https:' + url, callback=self.process_detail, meta={'web': response.url})

    def process_detail(self, response):
        item = FagaiweiItem()
        item['web_id'] = 36
        item['url'] = response.url
        item['title'] = response.xpath('//*[@id="cont_1_1_2"]/h1/text()').extract_first(default='').strip()
        item['web'] = response.meta.get('web')
        news_about = response.xpath('//div[@class="left-t"]/text()').extract()[0]
        webname = news_about.split("来源：")[-1].strip()
        if not webname:
            webname = response.xpath('//div[@class="left-t"]/a[1]/text()').extract()
        item['webname'] = webname
        item['pub_time'] = re.sub('年|月|日', '-', news_about.split("来源：")[0].strip())
        item['content'] = '\n'.join(response.xpath('//div[@class="left_zw"]/p/text() | \
                                          //div[@class="left_zw"]/p/strong/text() ').extract())
        item["keyword"] = keyword.get_keyword(item["content"])
        yield item
