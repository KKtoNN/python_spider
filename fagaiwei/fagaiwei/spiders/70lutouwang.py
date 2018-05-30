# -*- coding: utf-8 -*-
import scrapy
import requests
from datetime import datetime
from fagaiwei.settings import session, NewsItemInfo
from fagaiwei.keyword_others import keyword
from fagaiwei.items import FagaiweiItem
class ZjzxSpider(scrapy.Spider):
    #路透网
    name = 'lutouw'
    allowed_domains = ['lutouwang.net']
    start_urls = [
        'http://www.lutouwang.net/?channel=%E8%B4%A2%E7%BB%8F'  #财经
                  ]

    def parse(self, response):
        url_list = response.xpath('//ul[@id="feed-wrapper"]/li/table/tr/td[2]/h2/a/@href').extract()
        for url in url_list:
            new_url = response.urljoin(url)
            result = session.query(NewsItemInfo).filter_by(url=new_url, web_id=70).count()
            if result:
                # print("{} 存在".format(url))
                pass
            else:
                yield scrapy.Request(new_url,callback=self.process_detail,meta={'web':response.url})

    def process_detail(self,response):
        item = FagaiweiItem()
        item['web_id'] = 70
        item['url'] = response.url
        item['title'] = response.xpath('//div[@class="article-detail"]/h1/text()').extract_first(default='')
        item['web'] = response.meta.get('web')
        item['keyword'] = ''
        source = response.xpath('//div[@class="article-detail"]/div[@class="source-time"]/span[1]/text()').extract_first()
        item['webname'] = source if source else "路透网"
        item['pub_time'] = response.xpath('//div[@class="article-detail"]/div[@class="source-time"]/span[2]/text()').extract_first(default=datetime.now())
        p=1
        content=[]
        while 1:
            con,next = self.get_content(response.url,p)
            content.append(con)
            if '下一页' in next:
                p+=1
            else:
                break
        if not content:
            content = '这可能是图片或者文件，打开查看！'
        item['content'] = ''.join(content)
        yield item

    def get_content(self,url,page):
        params={'p':page}
        res = requests.get(url,params=params)
        doc = scrapy.selector.Selector(res)
        content = '\n'.join(doc.xpath('//div[@class="article-content"]/p/text()').extract())
        next = doc.xpath('//*[@id="page"]/a[last()]/text()').extract_first(default='')
        return content,next