# -*- coding: utf-8 -*-
import re
import scrapy
from fagaiwei.items import FagaiweiItem
from fagaiwei.settings import session, NewsItemInfo
from fagaiwei.keyword_others import keyword


class ZjzxSpider(scrapy.Spider):
    # 阿斯达克新闻
    name = 'aastocks'
    allowed_domains = ['aastocks.com']

    def start_requests(self):
        url1 = [
            'http://www.aastocks.com/sc/stocks/analysis/china-hot-topic.aspx',  # 中国市场新闻
            'http://www.aastocks.com/sc/stocks/news/aamm/aamm-all-category',  # 市场异动
            'http://www.aastocks.com/sc/forex/news/search.aspx',  # 财经和 外汇 链接
            'http://www.aastocks.com/sc/funds/news/search.aspx',
        ]
        for url in url1:
            yield scrapy.Request(url, callback=self.parse)
        url = 'http://www.aastocks.com/sc/stocks/news/aafn'  # 财经新闻 包含多模块
        yield scrapy.Request(url, callback=self.process_list)

    def process_list(self, response):
        # 专门处理财经新闻多板块链接的
        url_list = response.xpath('//*[@id="news-sub-header"]/div/@onclick').extract()[:-5]
        for url in url_list:
            url = re.search(r"\('(.*?)',", url).group(1)
            urls = response.urljoin(url)
            result = session.query(NewsItemInfo).filter_by(url=urls, web_id=51).count()
            if result:
                # print("{} 存在".format(url))
                pass
            else:
                if 'lci' in urls:
                    yield scrapy.Request(urls, callback=self.process_file, meta={'web': urls})
                else:
                    yield scrapy.Request(urls, callback=self.parse, meta={'web': urls})

    def parse(self, response):
        url_list = response.xpath('//*[@class="content"]/div[@ref]/div[2]/div[1]/a/@href | \
                                     //div[contains(@class,"content")]/div[@class="common_box"]/div/div[1]/a/@href').extract()
        for url in url_list:
            url = response.urljoin(url)
            result = session.query(NewsItemInfo).filter_by(url=url, web_id=51).count()
            if result:
                # print("{} 存在".format(url))
                pass
            else:
                if 'comment' in url:
                    yield scrapy.Request(url, callback=self.other_process_detail, meta={'web': response.url})
                else:
                    yield scrapy.Request(url, callback=self.process_detail, meta={'web': response.url})

    def process_detail(self, response):
        # 处理除 基金新闻和 外汇新闻 和公司公告 外的详情页面
        item = FagaiweiItem()
        item['web_id'] = 51
        item['url'] = response.url
        item['title'] = response.xpath('//div[@class="newshead5"]/text()').extract_first(default='').strip()
        item['web'] = response.meta.get('web')
        item['webname'] = '阿斯达克新闻'
        item['pub_time'] = response.xpath('//div[contains(@class,"newstime5")]/text()').extract_first(default='')
        item['content'] = '\n'.join(response.xpath('string(//*[@id="spanContent"])').extract()) \
            .replace('\t', '').replace('\xa0', '')
        item["keyword"] = keyword.get_keyword(item["content"])
        yield item

    def other_process_detail(self, response):
        # 处理基金新闻和外汇新闻详情页面
        item = FagaiweiItem()
        item['web_id'] = 51
        item['url'] = response.url
        item['title'] = response.xpath('//td[@class="newshead1"]/span/text()').extract_first(default='')
        item['web'] = response.meta.get('web')
        item['webname'] = '阿斯达克新闻'
        item['pub_time'] = response.xpath('//td[@class="newstime1"]/span/text()').extract_first(default='')
        item['content'] = '\n'.join(response.xpath('//*[@id="spanContent"]/text()').extract()).replace('\t', '')
        item["keyword"] = keyword.get_keyword(item["content"])
        yield item

    def process_file(self, response):
        # 处理详情页面是文件如公司公告
        # print('this is file !')
        item = FagaiweiItem()
        for tmp in response.xpath('//*[@class="content"]/div[@ref]/div[2]'):
            item['web_id'] = 51
            item['url'] = tmp.xpath('./div[1]/a/@href').extract_first()
            item['title'] = tmp.xpath('./div[1]/a/text()').extract_first(default='')
            item['web'] = response.meta.get('web')
            item['keyword'] = ''
            item['webname'] = '阿斯达克新闻'
            item_time = tmp.xpath('./div[@class="newstime4"]/text()').extract_first(default='')
            item['pub_time'] = ' '.join(item_time.split()[1:]).replace('/', '-')
            item['content'] = '这是一个文件，查看原文链接进行打开！！'

            result = session.query(NewsItemInfo).filter_by(url=item['url'], web_id=51).count()
            if result:
                # print("{} 存在".format(item['url']))
                pass
            else:
                yield item
