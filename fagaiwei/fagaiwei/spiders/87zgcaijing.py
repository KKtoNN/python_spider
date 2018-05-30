# -*- coding: utf-8 -*-
import scrapy
from datetime import datetime
from fagaiwei.settings import session, NewsItemInfo
from fagaiwei.items import FagaiweiItem
class ZjzxSpider(scrapy.Spider):
    #中国财经
    name = 'zgcj'
    allowed_domains = ['prcfe.com']
    start_urls = [
          'http://www.prcfe.com/web/caizheng/'   ,  #财政
        'http://www.prcfe.com/web/shuishou/'   ,    #税收
        'http://www.prcfe.com/web/jinrong/'    ,     #金融
        'http://www.prcfe.com/shuju/jrtz/'     ,    #理财
        'http://www.prcfe.com/shuju/hongguang/' ,   #宏观
                  ]

    def parse(self, response):
        url_list = response.xpath('//div[@class="macroscopic"]/ul/li/div/p[@class="h1"]/a/@href').extract()
        for url in url_list:
            new_url = response.urljoin(url)
            result = session.query(NewsItemInfo).filter_by(url=new_url, web_id=87).count()
            if result:
                # print("{} 存在".format(url))
                pass
            else:
                yield scrapy.Request(new_url,callback=self.process_detail,meta={'web':response.url})

    def process_detail(self,response):
        item = FagaiweiItem()
        item['web_id'] = 87
        item['url'] = response.url
        item['title'] = response.xpath('//div[@class="main"]/div[@class="top-line"]/h1/span/text()').extract_first(default='')
        item['web'] = response.meta.get('web')
        item['keyword'] = ''
        item['webname'] = response.xpath('//div[@class="main"]/div[@class="top-line"]/ul[@class="left"]/li[2]/span/em/text()').extract_first(default='')
        item['pub_time'] = response.xpath('//div[@class="main"]/div[@class="top-line"]/ul[@class="left"]/li[1]/span/text()').extract_first(datetime.now())
        content = '\n'.join(response.xpath('//div[@class="main"]/div[@class="main-left"]/div[1]/p/text()').extract())
        if not content:
            content = '这可能是图片或者文件，打开查看！'
        item['content'] = content.replace('\xa0','')
        # print(item)
        yield  item