# -*- coding: utf-8 -*-
import re
import scrapy
from fagaiwei.items import FagaiweiItem
from fagaiwei.settings import session, NewsItemInfo
from fagaiwei.keyword_others import keyword

class ZjzxSpider(scrapy.Spider):
    # 证券日报网
    name = 'zhengquanribao'
    allowed_domains = ['zqrb.cn']
    start_urls = [
        'http://www.zqrb.cn/jrjg/bank/index.html',  # 金融：银行
        'http://www.zqrb.cn/fund/jijindongtai/',  # 金融： 基金
        'http://www.zqrb.cn/money/qihuo/index.html',  # 金融 ：  期货
        'http://www.zqrb.cn/jrjg/insurance/index.html',  # 金融： 保险
        'http://www.zqrb.cn/jrjg/xintuo/index.html',  # 金融： 信托
        # 'http://www.zqrb.cn/jrjg/quanshang/index.html'  #,金融： 券商    消息过旧
        # 'http://www.zqrb.cn/simu/'        ,              #金融：   私募  消息过旧
        'http://www.zqrb.cn/money/index.html',  # 金融：  理财
        'http://www.zqrb.cn/stock/redian/index.html',  # 市场   热点
        'http://www.zqrb.cn/stock/dashiyanpan/index.html',  # 市场  大势
        'http://www.zqrb.cn/finance/hongguanjingji/index.html',  # 财经 宏观经济
        'http://www.zqrb.cn/finance/jgzs/index.html',  # 财经 监管之声
    ]
    custom_settings = {'LOG_LEVEL': 'INFO'}

    def parse(self, response):
        url_list = response.xpath('//div[@class="listMain"]/ul/li/a/@href').extract()[:10]
        for url in url_list:
            result = session.query(NewsItemInfo).filter_by(url=url, web_id=65).count()
            if result:
                # print("{} 存在".format(url))
                pass
            else:
                yield scrapy.Request(url, callback=self.process_detail, meta={'web': response.url})

    def process_detail(self, response):
        item = FagaiweiItem()
        item['web_id'] = 65
        item['url'] = response.url
        item['title'] = response.xpath('//div[@class="news_content"]/h1/text()').extract_first(default='')
        item['web'] = response.meta.get('web')
        news_about = response.xpath('//div[@class="news_content"]/div[@class="info_news"]/text()').extract_first(
            default='') + ' '
        item['webname'] = re.search(r'来源：(.*?)\s', news_about).group(1)
        item['pub_time'] = re.search(r'(\d{4}-\d{2}-\d{2} \d{2}:\d{2})', news_about).group(1)
        content = '\n'.join(response.xpath('//div[@class="news_content"]/div[@class="content"]/p/text() | \
                                     //div[@class="news_content"]/div[@class="content"]/p/strong/text()').extract()).replace(
            '\u2002', '').replace('\xa0', '')
        if not content:
            content = '这可能是图片或者文件，打开查看！'
        item['content'] = content
        item["keyword"] = keyword.get_keyword(item["content"])
        yield item
