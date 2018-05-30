# -*- coding: utf-8 -*-
import datetime
import scrapy
from pyquery import PyQuery as pq

from fagaiwei.keyword_others import keyword
from fagaiwei.settings import session, NewsItemInfo
import scrapy
from ..items import FagaiweiItem
import re
from pyquery import PyQuery as pq
import datetime

class ZjzxSpider(scrapy.Spider):
    #微信搜狗
    name = 'sgwx'
    allowed_domains = ['weixin.qq.com','sogou.com']
    start_urls = ['http://weixin.sogou.com/'
                  ]
    custom_settings = {'LOG_LEVEL':'INFO'}
    def parse(self, response):
        doc = pq(response.text)
        keyword_list = doc('#topwords li a').text().split()
        url_list = doc('.news-list li')
        for content in url_list.items():
            webname= content('.account').text()
            web = response.url
            url = content('h3 a').attr('href')
            result = session.query(NewsItemInfo).filter_by(url=url, web_id=13).count()
            if result:
                # print("{} 存在".format(url))
                pass
            else:
                title = content('h3').text()
                timestamp = content('.s-p').attr('t')
                pub_time = datetime.datetime.fromtimestamp(int(timestamp)).strftime('%Y-%m-%d %H:%M:%S')
                yield scrapy.Request(url,callback=self.process_detail,meta={'webname':webname,'web':web,'title':title,'pub_time':pub_time})

    def process_detail(self,response):
        item = FagaiweiItem()
        item['web_id'] =71
        item['url'] = response.url
        item['title'] = response.meta.get('title')
        item['web'] = response.meta.get('web')
        item['keyword'] = ''
        item['webname'] =response.meta.get('webname')
        item['pub_time'] =response.meta.get('pub_time')
        content = ''.join(response.xpath('//*[@id="js_content"]//p/text()| \
                                         //*[@id="js_content"]//p/span/text()| \
                                         //*[@id="js_content"]//p/strong/text() | \
                                         //*[@id="js_content"]//p/strong/span/text()').extract()).strip()
        if not content:
            content = '这可能是图片或者文件，打开查看！'
        item['content'] = content
        yield item

