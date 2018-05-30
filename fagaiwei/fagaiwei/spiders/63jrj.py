# -*- coding: utf-8 -*-
import scrapy
from fagaiwei.items import FagaiweiItem
from fagaiwei.settings import session, NewsItemInfo
from fagaiwei.keyword_others import keyword


class ZjzxSpider(scrapy.Spider):
    # 金融界
    name = 'jinrongjie'
    allowed_domains = ['jrj.com.cn']
    start_urls = ['http://stock.jrj.com.cn/company/'
                  ]
    custom_settings = {'LOG_LEVEL': 'INFO'}

    def parse(self, response):
        url_list = response.xpath('//dl[@class="mt20"]/dt/div[2]/div[1]/strong/b/a/@href').extract()
        for url in url_list:
            result = session.query(NewsItemInfo).filter_by(url=url, web_id=63).count()
            if result:
                # print("{} 存在".format(url))
                pass
            else:
                yield scrapy.Request(url, callback=self.process_detail, meta={'web': response.url})

    def process_detail(self, response):
        item = FagaiweiItem()
        item['web_id'] = 63
        item['url'] = response.url
        item['title'] = response.xpath('string(//div[@class="titmain"]/h1)').extract_first().strip()
        item['web'] = response.meta.get('web')
        webname = response.xpath('string(//div[@class="titmain"]/p[@class="inftop"]/span[2])').extract_first(
            default="金融界").strip()
        item['webname'] = webname.split("来源：")[-1]
        item['pub_time'] = response.xpath('//div[@class="titmain"]/p[@class="inftop"]/span[1]/text()').extract_first(
            default="金融界").strip()
        content = '\n'.join(response.xpath('//div[@class="texttit_m1"]/p/text() | \
                                   //div[@class="texttit_m1"]/p/a/text() | \
                                 //div[@class="texttit_m1"]/p/span/text() | \
                                     //div[@class="texttit_m1"]/p/strong/text() | \
                                     //div[@class="texttit_m1"]/p/strong/span/text() | \
                                     //div[@class="texttit_m1"]/p/strong/a/text() | \
                                    //div[@class="texttit_m1"]/p/strong/span/a/text() | \
                                  //div[@class="texttit_m1"]/p/span/span/text() ').extract())
        if not content:
            content = '这可能是图片或者文件，打开查看！'
        item['content'] = content
        item["keyword"] = keyword.get_keyword(item["content"])
        yield item
