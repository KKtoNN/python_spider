# coding:utf-8
import re
import time
import scrapy
from fagaiwei.items import FagaiweiItem
from fagaiwei.settings import session, NewsItemInfo
from fagaiwei.keyword_others import keyword

class xiamenSipderSpider(scrapy.Spider):
    name = 'dagongwang_sipder'
    allowed_domains = ['takungpao.com']
    start_urls = [
        'http://news.takungpao.com/paper/list-{}.html'.format(time.strftime("%Y%m%d", time.localtime())),
    ]

    def parse(self, response):
        pub_title = '大公报'
        data_tiitle = ''.join(list(response.xpath("//div[@class='pannel_inner01']/div//text()").getall())) \
            .replace('/n', '')
        web2 = 'http://news.takungpao.com.hk/paper/{}.html'.format(time.strftime("%Y%m%d", time.localtime()))
        url2s = response.xpath("//a[@class ='bluelink']/text()").getall()
        for url2 in url2s:
            item = FagaiweiItem()
            param = re.search(r'第(\w+)版', url2).group(1)
            url = web2 + '?' + param
            result = session.query(NewsItemInfo).filter_by(url=url, web_id=41).count()
            if result:
                # print("PDF 文件地址： {} 存在".format(url))
                pass
            else:
                item['url'] = url
                item['title'] = pub_title + data_tiitle + param
                item['content'] = '该页面为电子版报纸请点原链接查看'
                item['web'] = response.url
                item['webname'] = pub_title
                item['pub_time'] = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
                item["keyword"] = keyword.get_keyword(item["content"])
                item['web_id'] = 41
                yield item
