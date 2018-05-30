# -*- coding: utf-8 -*-
import re
from datetime import datetime, timedelta
import scrapy
from fagaiwei.items import FagaiweiItem
from fagaiwei.keyword_others import keyword
from fagaiwei.settings import session, NewsItemInfo


class ZjzxSpider(scrapy.Spider):
    # 观察者网
    name = 'guanchazhewang'
    allowed_domains = ['guancha.cn']

    def start_requests(self):
        url = 'http://user.guancha.cn/?s=dhfengwen'
        urls = ['http://www.guancha.cn/internation?s=dhguoji',  # 国际
                'http://www.guancha.cn/military-affairs?s=dhjunshi',  # 军事
                'http://www.guancha.cn/economy?s=dhcaijing',  # 财经
                ]
        yield scrapy.Request(url, callback=self.parse_url_list)
        for url2 in urls:
            yield scrapy.Request(url2, callback=self.parse_urls_list)

    def parse_url_list(self, response):
        url_list = response.xpath(
            '//ul[contains(@class,"article-list")]/li/div[@class="list-item"]/h4/a/@href').extract()
        for url in url_list:
            news_url = 'http://user.guancha.cn' + url
            result = session.query(NewsItemInfo).filter_by(url=news_url, web_id=96).count()
            if result:
                # print("{} 存在".format(news_url))
                pass
            else:
                yield scrapy.Request(news_url, callback=self.process_detail, meta={'web': response.url})

    def parse_urls_list(self, response):
        url_list = response.xpath('//ul[@class="img-List"]/li/h4/a/@href').extract()
        for url in url_list:
            news_url = 'http://www.guancha.cn' + url
            result = session.query(NewsItemInfo).filter_by(url=news_url, web_id=96).count()
            if result:
                # print("{} 存在".format(news_url))
                pass
            else:
                referer = response.url
                headers = {'Referer': referer}
                yield scrapy.Request(news_url, callback=self.process_urls_detail, meta={'web': response.url},
                                     headers=headers)

    def process_detail(self, response):
        item = FagaiweiItem()
        item['web_id'] = 96
        item['url'] = response.url
        item['title'] = response.xpath('//div[@class="article-content"]/h1/text()').extract_first(default='')
        item['web'] = response.meta.get('web')
        news_about = response.xpath(
            '//div[@class="article-content"]/div[contains(@class,"user-info-box")]//span[@class="time1"]/text()').extract_first()
        item['webname'] = '观察者网'
        item['pub_time'] = self.process_time(news_about)
        content = '\n'.join(response.xpath('//div[contains(@class,"article-txt")]/div/p/text() | \
                               //div[contains(@class,"article-txt")]/div/p/strong/text() | \
                           //div[contains(@class,"article-txt")]/p/text() | \
                               //div[contains(@class,"article-txt")]/p/text() | \
                               //div[contains(@class,"article-txt")]/p/a/text()').extract()) \
            .replace('\r\n', '').replace('\xa0', '')
        if not content:
            content = '这可能是图片或者文件，打开查看！'
        item['content'] = content
        item["keyword"] = keyword.get_keyword(item["content"])
        yield item

    def process_urls_detail(self, response):
        item = FagaiweiItem()
        item['web_id'] = 96
        item['url'] = response.url
        item['title'] = response.xpath('//li[contains(@class,"left-main")]/h3/text()').extract_first(default='')
        item['web'] = response.meta.get('web')
        webname = response.xpath(
            '//li[contains(@class,"left-main")]/div[contains(@class,"time fix")]/span[last()]/text()').extract_first() + ' '
        item['webname'] = ''.join(re.findall(r'来源：(.*?)\s', webname))
        item['pub_time'] = response.xpath(
            '//li[contains(@class,"left-main")]/div[contains(@class,"time fix")]/span[1]/text()').extract_first(
            datetime.now())
        content = '\n'.join(response.xpath('//div[contains(@class,"all-txt")]/p/text() | \
                                  //div[contains(@class,"all-txt")]/p/a/text() | \
                                  //div[contains(@class,"all-txt")]/p/strong/text()').extract())
        if not content:
            content = '这可能是图片或者文件，打开查看！'
        item['content'] = content.replace('\r\n', '').replace('\t\n', '')
        item["keyword"] = keyword.get_keyword(item["content"])
        yield item

    def process_time(self, news_about):
        current_time = datetime.now()
        digit = re.search(r'(\d+)', news_about).group(1)
        if '分钟' in news_about:
            pre = timedelta(minutes=int(digit))
        if '小时' in news_about:
            pre = timedelta(hours=int(digit))
        if '昨天' in news_about:
            pre = timedelta(days=1)
        pub_time = current_time - pre
        return pub_time
