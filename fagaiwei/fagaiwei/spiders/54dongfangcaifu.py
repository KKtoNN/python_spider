# -*- coding: utf-8 -*-
import scrapy
from datetime import datetime
from fagaiwei.settings import session, NewsItemInfo
from fagaiwei.keyword_others import keyword
from fagaiwei.items import FagaiweiItem
class ZjzxSpider(scrapy.Spider):
    #东方财富网
    name = 'dfcfw'
    allowed_domains = ['eastmoney.com']
    start_urls = [
        'http://finance.eastmoney.com/news/cgsxw.html'   ,  #公司新闻
        'http://finance.eastmoney.com/news/czqyw.html'   ,  #证券要闻
        'http://finance.eastmoney.com/news/cgjjj.html'   ,  #国际经济
        'http://finance.eastmoney.com/news/cgnjj.html'    ,  #国内经济
        'http://finance.eastmoney.com/news/cywjh.html'   ,    #要闻精华
                  ]

    def parse(self, response):
        url_list = response.xpath('//ul[@id="newsListContent"]/li/div/p[1]/a/@href').extract()
        for url in url_list:
            result = session.query(NewsItemInfo).filter_by(url=url, web_id=54).count()
            if result:
                # print("{} 存在".format(url))
                pass
            else:
                yield scrapy.Request(url,callback=self.process_detail,meta={'web':response.url})

    def process_detail(self,response):
        item = FagaiweiItem()
        item['web_id'] = 54
        item['url'] = response.url
        item['title'] = response.xpath('//div[@class="newsContent"]/h1/text()').extract_first(default='')
        item['web'] = response.meta.get('web')
        item['keyword'] = ''
        item['webname'] = response.xpath('//div[@class="newsContent"]/div[@class="Info"]/div/div[contains(@class,"source data-source")]/@data-source| \
                                        //div[@class="newsContent"]/div[@class="info"]/div/div[contains(@class,"source data-source")]/text() ').extract_first(default='东方财富网')
        item['pub_time'] = response.xpath('//div[@class="newsContent"]/div[@class="info"]/div/div[@class="time"]/text()').extract_first(default=datetime.now().strftime("%Y-%m-%d %H:%M")).replace('年','-').replace('月','-').replace('日','')
        content = ''.join(response.xpath('//*[@id="ContentBody"]/p/text() | \
                                 //*[@id="ContentBody"]/p/span/text()').extract())
        if not content:
            content = '这可能是图片或者文件，打开查看！'
        item['content'] = content.replace('\u3000','')
        yield item