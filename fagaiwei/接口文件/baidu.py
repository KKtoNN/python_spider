# -*- coding: utf-8 -*-
import re
from datetime import timedelta, datetime
from urllib.parse import quote
import scrapy
from fagaiwei.items import FagaiweiItem



class ZjzxSpider(scrapy.Spider):
    # 百度热点新闻
    name = 'baidu'
    allowed_domains = ['baidu.com']
    start_urls = ['http://top.baidu.com/buzz?b=1&c=513&fr=topbuzz_b341_c513']

    def parse(self, response):
        news_list = response.xpath('//table[@class="list-table"]/tr/td[@class="keyword"]/a[1]/text()').extract()
        search_url = 'https://www.baidu.com/s?tn=baidurt&rtt=1&bsst=1&wd={keyword}&origin=ps'
        headers = {'Host': 'www.baidu.com',
                   }
        for keyword in news_list:
            url = search_url.format(keyword=quote(keyword))
            yield scrapy.Request(url, headers=headers, callback=self.search_page, meta={'title': keyword, 'web': url})

    def search_page(self, response):
        item = FagaiweiItem()
        try:
            text = re.findall(r'<table cellpadding(.*?)</table>', response.text, re.S)[1]
            item['web_id'] = 72
            # item['url'] = response.xpath('//div[@class="content"]/table/tr/td/h3/a/@href').extract_first()
            item["url"] = re.search(r'href="(.*?)"', text, re.S).group(1)
            item['title'] = response.meta.get('title')
            item['web'] = response.meta.get('web')
            item['keyword'] = ''
            news_about = re.search(r'realtime">(.*?)</div>', text, re.S).group(1).split()
            item['webname'] = news_about[0].replace('&nbsp;-&nbsp;', '')
            current_time = datetime.now()
            digit = time = re.search(r'(\d+)', news_about[-1]).group(1)
            if '分钟' in news_about[-1]:
                pre = timedelta(minutes=int(digit))
            if '小时' in news_about[-1]:
                pre = timedelta(hours=int(digit))
            item['pub_time'] = current_time - pre
            # content = ''.join(response.xpath('//div[@class="content"]/table/tr/td/div[@class="rt_photo_cont"]/font/text()| \
            #                                  //div[@class="content"]/table/tr/td/div[@class="rt_photo_cont"]/font/em/text()').extract()).strip()
            content = re.search(r'realtime">.*?</div>(.*?)<br>', text, re.S).group(1).replace('<em>', '').strip()
            if not content:
                content = '这可能是图片或者文件，打开查看！'
            item['content'] = content.replace('<em>', '').replace('</em>', '')
            yield item
        except:
            yield scrapy.Request(response.url, callback=self.search_page,
                                 meta={'title': response.meta.get('title'), 'web': response.meta.get('url')})
