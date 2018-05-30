# coding:utf-8
import scrapy

import jsonpath
from fagaiwei.items import FagaiweiItem
import time
from fagaiwei.settings import session, NewsItemInfo


class xiamenSipderSpider(scrapy.Spider):
    name = 'ZGchanyejingji_sipder'
    allowed_domains = ['cinic.org.cn']
    start_urls = [
        'http://www.cinic.org.cn/xw/cjxw/',     # 产经要闻
        'http://www.cinic.org.cn/xw/szxw/',     # 时政新闻
        'http://www.cinic.org.cn/xw/tjsj/',     # 统计数据
        'http://www.cinic.org.cn/xw/bwdt/',     # 部委动态
        'http://www.cinic.org.cn/xw/schj/',     # 市场环境
        'http://www.cinic.org.cn/xw/kx/',       # 快讯
        'http://www.cinic.org.cn/xw/#',         # 新闻
    ]

    def parse(self, response):

        urls = response.xpath("//h3/a/@href").getall()
        pub_times = response.xpath("//span[@class='sp2']/text()").getall()
        dabao = zip(urls, pub_times)
        for url, pub_time in dabao:
            url = 'http://www.cinic.org.cn' + url
            result = session.query(NewsItemInfo).filter_by(url=url, web_id=91).count()
            if result:
                # print("URL文件地址： {} 存在".format(url))
                pass
            else:
                yield scrapy.Request(url=url, callback=self.parse_page,
                                     meta={'url': response.url, 'pub_time': pub_time})

    def parse_page(self, response):
        item = FagaiweiItem()

        item['web'] = response.meta['url']
        item['url'] = response.url
        item['webname'] = '中国产业经济信息网'
        item['title'] = ''.join(list(response.xpath("//h1//text()").getall()))
        pub_time = response.meta['pub_time']
        if pub_time is not None:
            item['pub_time'] = pub_time.replace("年", '-').replace("月", '-').replace("日", '').replace("更新于", '')
        else:
            item['pub_time'] = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        content = response.xpath(
            "//div[@class='dc-ccm1']//div[not(@class)]//text()|//div[@class='dc-ccm1']/p//text()").getall()
        content = ''.join(list(content)).replace('\r', '').replace("\u3000", '') \
            .replace('版权及免责声明：凡本网所属版权作品，转载时须获得授权并注明来源“中国产业经济信息网”，违者本网将保留追究其相关法律责任的权力。'
                     '凡转载文章，不代表本网观点和立场。版权事宜请联系：010-65363056。', '').replace('延伸阅读', '').strip()
        if len(content) == 0:
            # print(response.url)
            item['content'] = '请点击原文来链接查看'
        else:
            # print(content)
            item['content'] = content

        item['add_time'] = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        item['keyword'] = ''
        item['web_id'] = 91
        # print(item)
        yield item
