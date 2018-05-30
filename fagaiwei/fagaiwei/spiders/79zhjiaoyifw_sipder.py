# -*- coding: utf-8 -*-
from datetime import datetime
import scrapy
from fagaiwei.items import FagaiweiItem
from fagaiwei.keyword_others import keyword
from fagaiwei.settings import session, NewsItemInfo
from fagaiwei.jvchao_pdf import pdf_to_txt as pdf


class xiamenSipderSpider(scrapy.Spider):
    name = 'zhjiaoyifw_spider'
    allowed_domains = ['cesc.com', 'amazonaws.com']

    start_urls = [
        'https://www.cesc.com/sc/index.html',
    ]

    def parse(self, response):
        titles = response.xpath("//div[contains(@class,'title')]/a/text()").getall()
        urls = response.xpath("//div[contains(@class,'items-col')]/a/@href").getall()
        dates = response.xpath("//div[@class='items']/div[contains(@class,'date')]/text()").getall()
        dabao = zip(urls, titles, dates)
        # print(len(urls), len(dates))
        for url, title, time in dabao:
            if url[-4:] == '.pdf':
                result = session.query(NewsItemInfo).filter_by(url=url, web_id=79).count()
                if result:
                    # print("PDF 文件地址： {} 存在".format(url))
                    pass
                else:
                    item = FagaiweiItem()
                    item['webname'] = '中华交易服务'
                    item['web'] = response.url
                    title = ''.join(list(title)).replace('*', '').replace('/', '').replace('<', '').replace('>', '') \
                        .replace('|', '').replace(':', '').replace('"', '').replace('?', '') \
                        .replace('？', '').replace('\t', '')
                    time = time.replace('/', '-')
                    item['pub_time'] = datetime.strptime(time, '%d-%m-%Y')
                    item['url'] = url
                    item['title'] = title
                    content = pdf.main(url=url, fileName=title)
                    if content == '':
                        item['content'] = '请点击原文链接查看' + response.url
                    else:
                        item['content'] = ''.join(list(content))
                    # item['add_time'] = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
                    item["keyword"] = keyword.get_keyword(item["content"])
                    item['web_id'] = 79
                    # print(item)
                    yield item
            else:

                pass
