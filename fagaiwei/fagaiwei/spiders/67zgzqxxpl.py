# -*- coding: utf-8 -*-
import re
import scrapy
from fagaiwei.items import FagaiweiItem
from fagaiwei.jvchao_pdf import pdf_to_txt as pdf
from fagaiwei.settings import session, NewsItemInfo
from fagaiwei.keyword_others import keyword


class xiamenSipderSpider(scrapy.Spider):
    # 中国证券信息纰漏平台
    name = 'zgzqxxpl'
    allowed_domains = ['cnfol.com']
    start_urls = ['http://xinpi.cnstock.com/Search.aspx?Style=012001',  # 沪市
                  'http://xinpi.cnstock.com/Search.aspx?Style=012002',  # 深市
                  # 'http://xinpi.cnstock.com/ID_Search.aspx?ortherstyle=010101',       #监管
                  'http://xinpi.cnstock.com/Search.aspx?Style=012003'  # 中小板
                  'http://xinpi.cnstock.com/Search.aspx?Style=012015'  # 创业板
                  # 'http://xinpi.cnstock.com/Search.aspx?OrtherStyle=01010509'          #基金
                  ]

    def parse(self, response):
        item = FagaiweiItem()
        urls = response.xpath("//ul[@class='gg-list']/li/span[@class='tit']/a/@href").getall()
        titles1 = response.xpath("//ul[@class='gg-list']/li/span[@class='tit']/a/text()").getall()
        titles2 = response.xpath("//ul[@class='gg-list']/li/span[@class='code']/a/text()").getall()
        times = response.xpath("//ul[@class='gg-list']/li/span[@class='time']/text()").getall()
        dabao = zip(urls, titles1, titles2, times)
        for url, title1, title2, time in dabao:
            title = title2 + ' ' + title1
            title = ''.join(list(title)).replace('*', '').replace('/', '').replace('<', '').replace('>', '') \
                .replace('|', '').replace(':', '').replace('"', '').replace('?', '') \
                .replace('？', '')
            shijian, filename = re.findall(r'=(\d{8})(\w+)', url)[0]
            url2 = 'http://php.cnstock.com/texts/2018/' + shijian + '/' + filename + '.pdf'
            durl = url2  # PDF文件下载地址
            if durl[-4:] == '.pdf':
                # print("==================================\n{}".format(durl))
                result = session.query(NewsItemInfo).filter_by(url=url2, web_id=67).count()
                if result:
                    # print("PDF 文件地址： {} 存在".format(url2))
                    pass
                else:
                    content = pdf.main(url=url2, fileName=title)
                    if len(content) == 0:
                        item['content'] = '请点击原文链接查看'
                    else:
                        item['content'] = ''.join(list(content))
                    item['web_id'] = 67
                    item['title'] = title
                    time = time.replace('(', '').replace(')', '')
                    item['pub_time'] = time
                    item['webname'] = '中国证券网信息披露平台'
                    item['web'] = response.url
                    item['url'] = url2
                    item["keyword"] = keyword.get_keyword(item["content"])
                    yield item
