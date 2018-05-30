# -*- coding: utf-8 -*-
import scrapy
from fagaiwei.settings import session, NewsItemInfo
from fagaiwei.items import FagaiweiItem
class ZjzxSpider(scrapy.Spider):
    #中国新金融网
    name = 'zgxjr'
    allowed_domains = ['xinjr.com']
    start_urls = [
        'http://www.xinjr.com/caijing/'  , #财经
        'http://www.xinjr.com/waihui/'  ,  #外汇
        'http://www.xinjr.com/golds/'   ,  #黄金
        'http://www.xinjr.com/jijin/'   ,  #基金
        'http://www.xinjr.com/zhengquan/' , #股票
        'http://www.xinjr.com/yinhang/'  ,#银行
        'http://www.xinjr.com/waihui/' , #外汇
                  ]

    def parse(self, response):
        url_list = response.xpath('//ul[@class="g_md"]/li/a/@href').extract()
        for url in url_list:
            new_url = response.urljoin(url)
            result = session.query(NewsItemInfo).filter_by(url=new_url, web_id=82).count()
            if result:
                # print("{} 存在".format(url))
                pass
            else:
                yield scrapy.Request(new_url,callback=self.process_detail,meta={'web':response.url})

    def process_detail(self,response):
        item = FagaiweiItem()
        item['web_id'] = 82
        item['url'] = response.url
        item['title'] = response.xpath('//div[@class="avMain"]/div[@class="arcHd"]/h1/text()').extract_first(default='')
        item['web'] = response.meta.get('web')
        item['keyword'] = ''
        item['webname'] = '中国新金融网'
        item['pub_time'] = response.xpath('//div[@class="avMain"]/div[@class="arcHd"]/div/div[1]/text()').extract_first(default='')
        content = '\n'.join(response.xpath('//div[contains(@class,"arcBody clearfix")]/text() | \
                                     //div[contains(@class,"arcBody clearfix")]/strong/text() | \
                                           //div[contains(@class,"arcBody clearfix")]/p/text() | \
                                   //div[contains(@class,"arcBody clearfix")]/p/font/text() | \
                                 //div[contains(@class,"arcBody clearfix")]/p/span/strong/text() | \
                                //div[contains(@class,"arcBody clearfix")]/p/span/font/text() | \
                                //div[contains(@class,"arcBody clearfix")]/p/b/text() | \
                                //div[contains(@class,"arcBody clearfix")]/p/b/font/text() | \
                                    //div[contains(@class,"arcBody clearfix")]/p/font/b/text() | \
                                    //div[contains(@class,"arcBody clearfix")]/p/strong/text()| \
                                    //div[contains(@class,"arcBody clearfix")]/p/strong/span/text()| \
                                       //div[contains(@class,"arcBody clearfix")]/p/span/text()| \
                                        //div[contains(@class,"arcBody clearfix")]/div/text() | \
                                        //div[contains(@class,"arcBody clearfix")]/div/p/text() | \
                                         //div[contains(@class,"arcBody clearfix")]/div/p/span/text() | \
                                         //div[contains(@class,"arcBody clearfix")]/div/span/text() | \
                                          //div[contains(@class,"arcBody clearfix")]/div/span/span/text()| \
                                          //div[contains(@class,"arcBody clearfix")]/div/p/span/span/text()| \
                                          //div[contains(@class,"arcBody clearfix")]//div[@id="blogDetailDiv"]/div/p/text()| \
                                          //div[contains(@class,"arcBody clearfix")]//div[@id="blogDetailDiv"]/div/div/text() ').extract())
        if not content:
            content = '这可能是图片或者文件，打开查看！'
        item['content'] = content.replace('\u3000','').replace('\xa0','').replace('\u2003','').replace('\r\n','').replace('\n\n','')
        yield item