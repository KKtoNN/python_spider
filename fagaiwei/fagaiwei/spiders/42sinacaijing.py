# -*- coding: utf-8 -*-
import scrapy
from datetime import datetime
from fagaiwei.settings import session, NewsItemInfo
from fagaiwei.items import FagaiweiItem
class ZjzxSpider(scrapy.Spider):
    #新浪财经
    name = 'sinacaijing'
    allowed_domains = ['sina.com.cn']
    start_urls = [
        'http://finance.sina.com.cn/roll/index.d.html?cid=56995'  ,   #期市要闻
        'http://roll.finance.sina.com.cn/finance/jj4/index_1.shtml' , #基金新闻
        'http://finance.sina.com.cn/forex/'         ,                 #外汇
        'http://finance.sina.com.cn/nmetal/'      ,                   #黄金
                  ]

    def parse(self, response):
        url_list = response.xpath('//ul[@data-client="scroll"]/li/a/@href | //ul[@class="list_009"]/li/a/@href ').extract()
        for url in url_list:
            result = session.query(NewsItemInfo).filter_by(url=url, web_id=42).count()
            if result:
            # print("{} 存在".format(url))
                pass
            else:
                yield scrapy.Request(url,callback=self.process_detail,meta={'web':response.url})

    def process_detail(self,response):
        if response.xpath('//*[@id="artibody"]'):
            item = FagaiweiItem()
            item['web_id'] = 42
            item['url'] = response.url
            item['title'] =   response.xpath('//div[contains(@class,"main-content")]/h1/text()').extract_first(default='')
            item['web'] = response.meta.get('web')
            item['keyword'] = ''
            item['webname'] = response.xpath('//a[contains(@class,"source")]/text()|//span[contains(@class,"source")]/text()').extract_first(default='新浪财经')
            item['pub_time'] =  response.xpath('//span[@class="date"]/text()').extract_first(default=datetime.now().strftime("%Y-%m-%d %H:%M")).replace('年','-').replace('月','-').replace('日','')
            content = '\n'.join(response.xpath('//*[@id="artibody"]/p/text() | \
                                     //*[@id="artibody"]//p/span/a/text() | \
                                     //*[@id="artibody"]//p/span/text() | \
                                      //*[@id="artibody"]/div//p/text()').extract())
            if not content:
                content = '这可能是图片或者文件，打开查看！'
            item['content'] = content.replace('\u3000','').replace('\xa0','').replace('\t\t\t\n','').replace('\n\n','')
            yield item