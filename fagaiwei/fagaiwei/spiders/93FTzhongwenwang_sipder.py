# coding:utf-8
import scrapy

import jsonpath
from fagaiwei.items import FagaiweiItem
import time
from fagaiwei.settings import session, NewsItemInfo


class xiamenSipderSpider(scrapy.Spider):
    name = 'FTzhognwenwang_sipder'
    allowed_domains = ['ftchinese.com']
    start_urls = [
        'http://www.ftchinese.com/interactive/9826#',
        'http://www.ftchinese.com/',

    ]

    def parse(self, response):
        # print(response.url)
        if response.url != 'http://www.ftchinese.com/interactive/9826#':
            titles = response.xpath("//div[@class='items']//a[@class='item-headline-link ']/text()").getall()
            urls = response.xpath("//div[@class='items']//a[@class='item-headline-link ']/@href").getall()
            dabao = zip(titles, urls)
            for title, url in dabao:
                url = 'http://www.ftchinese.com' + url + '?full=y'
                if url == 'http://www.ftchinese.com/interactive/9826?full=y':
                    pass
                else:
                    result = session.query(NewsItemInfo).filter_by(url=url, web_id=93).count()
                    if result:
                        # print("URL文件地址： {} 存在".format(url))
                        pass
                    else:
                        yield scrapy.Request(url=url, callback=self.parse_page, meta={'url': response.url, 'title': title})
        else:
            url = response.url
            result = session.query(NewsItemInfo).filter_by(url=url, web_id=93).count()
            if result:
                # print("URL文件地址： {} 存在".format(url))
                pass
            else:
                item = FagaiweiItem()
                item['title'] = response.xpath("//h1/text()").get()
                item['web'] = url
                item['url'] = url
                item['webname'] = 'FT中文网'
                pub_time = response.xpath("//h3/text()").get()
                if pub_time is not None:
                    pub_time = pub_time.replace("年",'-').replace('月','-01')
                    item['pub_time'] = pub_time
                else:
                    item['pub_time'] = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())

                content = '\n'.join(
                    list(response.xpath(
                        "//p//text()").getall())).strip().replace(
                    '\n', '').replace('\xa0','')
                if content == '':
                    item['content'] = '请点击原文来链接查看'
                else:
                    item['content'] = content
                item['add_time'] = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
                item['keyword'] = ''
                item['web_id'] = 93
                # print(item)
                yield item

    def parse_page(self, response):
        item = FagaiweiItem()
        item['title'] = response.meta['title']
        item['web'] = response.meta['url']
        item['url'] = response.url
        item['webname'] = 'FT中文网'
        pub_time = response.xpath("//span[@class='story-time']/text()").get()
        if pub_time is not None:
            item['pub_time'] = pub_time.replace("年", '-').replace("月", '-').replace("日", '').replace("更新于", '')
        else:
            item['pub_time'] = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())

        content = '\n'.join(
            list(response.xpath(
                "//div[@class='story-container']//div[not(script)]//text()").getall())).strip().replace(
            '\n', '')
        if content == '':
            item['content'] = '请点击原文来链接查看'
        else:
            content = content.replace(
                "document.write (writeAdNew({devices: ['PC','iPhoneWeb','AndroidWeb','iPhoneApp','AndroidApp'],pattern:'MPU',position:'Middle1',container:'mpuInStory'}))",
                '') \
                .replace(
                "document.write (writeAdNew({devices: ['iPhoneWeb','AndroidWeb','iPhoneApp','AndroidApp'],pattern:'MPU',position:'Middle2',container:'mpuInStory'}));",
                '').replace("版权声明：本文版权归FT中文网所有，未经允许任何单位或个人不得转载，复制或以任何其他方式使用本文全部或部分，侵权必究。", '')
            item['content'] = content

        item['add_time'] = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        item['keyword'] = ''
        item['web_id'] = 93
        # print(item)
        yield item
