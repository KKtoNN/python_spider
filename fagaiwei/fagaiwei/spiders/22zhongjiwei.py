# -*- coding: utf-8 -*-
import re
import scrapy
from fagaiwei.items import FagaiweiItem
from fagaiwei.keyword_others import keyword
from fagaiwei.settings import session, NewsItemInfo


class ZjzxSpider(scrapy.Spider):
    # 中纪委
    name = 'zjw'
    allowed_domains = ['ccdi.gov.cn']
    start_urls = [
        'http://www.ccdi.gov.cn/ldhd/gcsy/',  # 领导声音
        'http://www.ccdi.gov.cn/xxgk/hyzl/',  # 会议报告
        'http://www.ccdi.gov.cn/scdc/',  # 审读调查
        'http://www.ccdi.gov.cn/xsxc/',  # 中央巡查
    ]

    def parse(self, response):
        info_list = response.xpath('//ul[contains(@class,"list_news_dl")]/li')
        for info in info_list:
            url = info.xpath('./a/@href').extract_first()
            new_url = response.urljoin(url)
            result = session.query(NewsItemInfo).filter_by(url=new_url, web_id=22).count()
            if result:
                # print("{} 存在".format(new_url))
                pass
            else:
                title = ''.join(info.xpath('./a/text()').extract()).strip()
                yield scrapy.Request(new_url, callback=self.process_detail, meta={'web': response.url, 'title': title})

    def process_detail(self, response):
        item = FagaiweiItem()
        item['web_id'] = 22
        item['url'] = response.url
        item['title'] = response.meta.get('title')
        item['web'] = response.meta.get('web')
        # item['keyword'] = ''
        news_about = response.xpath(
            '//div[@class="Article_61"]/h3[@class="daty"]/div/em[1]/text()').extract_first() + ' '
        item['webname'] = ''.join(re.findall(r'来源：(.*?)\s', news_about))
        time = response.xpath('//div[@class="Article_61"]/h3[@class="daty"]/div/em[2]/text()').extract_first()
        item['pub_time'] = ''.join(re.findall(r'\d{4}-\d{2}-\d{2} \d{2}:\d{2}', time))
        content = '\n'.join(response.xpath('//div[@class="Article_61"]/div[@class="content"]/div/div/p/text() | \
                                //div[@class="Article_61"]/div[@class="content"]/div/div/p/font/text() | \
                                 //div[@class="Article_61"]/div[@class="content"]/div/div/p/strong/text() ').extract())
        if not content:
            content = '这可能是图片或者文件，打开查看！'
        item['content'] = content
        item["keyword"] = keyword.get_keyword(item["content"])

        yield item
