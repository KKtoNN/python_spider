# -*- coding: utf-8 -*-
import re
import scrapy
from fagaiwei.items import FagaiweiItem
from fagaiwei.jvchao_pdf import html_to_txt as txt
from fagaiwei.settings import session, NewsItemInfo
from fagaiwei.keyword_others import keyword


class xiamenSipderSpider(scrapy.Spider):
    # 中国证券信息纰漏平台
    name = 'zgzqxxpl2'
    allowed_domains = ['xinpi.cnstock.com']
    start_urls = [
        'http://xinpi.cnstock.com/ID_Search.aspx?ortherstyle=010101',  # 监管
        'http://xinpi.cnstock.com/Search.aspx?OrtherStyle=01010509'  # 基金
    ]

    def parse(self, response):
        item = FagaiweiItem()
        urls = response.xpath("//span[@class='tit']/a/@href").getall()
        # print(urls)
        titles = response.xpath("//span[@class='tit']/a/text()").getall()
        times = response.xpath("//span[@class='time']/text()").getall()
        dabao = zip(urls, titles, times)
        for url, title, time1 in dabao:
            filename = re.findall(r'=(\d+)', url)[0]
            url2 = 'http://php.cnstock.com/news_new/index.php/api/fileview?ID=' + filename + '&db=txt'
            if url2[-4:] == '=txt':
                # print("==================================\n{}".format(durl))
                result = session.query(NewsItemInfo).filter_by(url=url2, web_id=67).count()
                if result:
                    # print("TXT 文件地址： {} 存在".format(url2))
                    pass
                else:
                    content = txt.main(url=url2)
                    item['content'] = content
                    item['web_id'] = 67
                    item['title'] = title
                    time = time1.replace('(', '').replace(')', '')
                    item['pub_time'] = time
                    item['webname'] = '中国证券网信息披露平台'
                    item['web'] = response.url
                    item['url'] = url2
                    item["keyword"] = keyword.get_keyword(item["content"])
                    yield item
