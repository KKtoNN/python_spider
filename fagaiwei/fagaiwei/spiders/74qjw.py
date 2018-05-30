# -*- coding: utf-8 -*-
import scrapy
from fagaiwei.items import FagaiweiItem
from fagaiwei.settings import session, NewsItemInfo
from fagaiwei.keyword_others import keyword


class ZjzxSpider(scrapy.Spider):
    # 全景网
    name = 'quanjingwang'
    allowed_domains = ['p5w.net']
    start_urls = [
        'http://www.p5w.net/'  # 全景网首页
    ]

    def parse(self, response):
        info_list = response.xpath('//div[@class="mainbox_left2"]/div[@class="navtents"]')[:4]
        for tmp in info_list:
            url_list = tmp.xpath('./div[@class="manlist"]/ul/li/h2/a/@href| \
                                 ./div[@class="manlist2"]/ul/li/h2/a/@href').extract()
            for url in url_list:
                result = session.query(NewsItemInfo).filter_by(url=url, web_id=74).count()
                if result:
                    # print("{} 存在".format(url))
                    pass
                else:
                    yield scrapy.Request(url, callback=self.process_detail, meta={'web': response.url})

    def process_detail(self, response):
        item = FagaiweiItem()
        item['web_id'] = 74
        item['url'] = response.url
        item['title'] = ''.join(response.xpath('//div[@class="newscontent_right2"]/h1/text()| \
                                       //div[@class="newscontent_right"]/h1/text() ').extract())
        item['web'] = response.meta.get('web')
        item['webname'] = response.xpath('//div[@class="newscontent_right2"]/div[@class="content_info clearfix"]/span[1]/i[@class="zhuoze"]/a/@title | \
                                         //div[@class="newscontent_right2"]/div[@class="content_info clearfix"]/span[1]/i[@class="zhuoze"]/text()').extract_first(
            default='全景网').strip()
        time = ''.join(response.xpath('//div[@class="newscontent_right2"]/div[@class="content_info clearfix"]/span[1]/time/text()|\
                              //div[contains(@class,"content_info")]/span[@class="left"]/text()').extract()).strip().replace(
            '月', '-').replace('日', '')
        if '2018' not in time:
            time = '2018-' + time
        item['pub_time'] = time
        content = '\n'.join(response.xpath('//div[@class="newscontent_right2"]/div[@class="article_content2"]//div/p/text()| \
                                    //div[@class="newscontent_right2"]/div[@class="article_content2"]//div/p/a/text()| \
                                    //div[@class="newscontent_right2"]/div[@class="article_content2"]//div/p/a/text()| \
                                    //div[@class="newscontent_right2"]/div[@class="article_content2"]/div[2]/div/p/text()| \
                                    //div[@class="newscontent_right2"]/div[@class="article_content2"]/div[2]/p/font/text()| \
                                     //div[@class="newscontent_right2"]/div[@class="article_content2"]/div[2]/div/p//strong/text()| \
                                       //div[@class="newscontent_right2"]/div[@class="article_content2"]/div[2]/div/p//font/text()| \
                                        //div[@class="article_content"]/p/text()').extract())
        if not content:
            content = '这可能是图片或者文件，打开查看！'
        item['content'] = content.replace('\u3000', '')
        item["keyword"] = keyword.get_keyword(item["content"])
        yield item
