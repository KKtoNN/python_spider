# -*- coding: utf-8 -*-
import scrapy
from fagaiwei.items import FagaiweiItem
from fagaiwei.settings import session, NewsItemInfo
from fagaiwei.jvchao_pdf import pdf_to_txt as pdf
from fagaiwei.keyword_others import keyword

class xiamenSipderSpider(scrapy.Spider):
    name = 'shanghaizhengsuo_spider'
    allowed_domains = ['sse.com.cn']

    start_urls = [
        'http://www.sse.com.cn/disclosure/listedinfo/announcement/s_docdatesort_desc_2016openpdf.htm',
    ]

    def parse(self, response):

        titles = response.xpath("//dd/em/a/text()").getall()
        urls = response.xpath("//dd/a/@href").getall()
        dates = response.xpath("//dd/span/text()").getall()

        # print(titles,urls,dates)
        dabao = zip(urls, titles, dates)
        for url, title, time in dabao:
            if url[-4:] == '.pdf':
                result = session.query(NewsItemInfo).filter_by(url=url, web_id=55).count()
                if result:
                    # print("PDF 文件地址： {} 存在".format(url))
                    pass
                else:
                    item = FagaiweiItem()
                    item['webname'] = '上海证券交易所'
                    item['web'] = response.url
                    title = ''.join(list(title)).replace('*', '').replace('/', '').replace('<', '').replace('>', '') \
                        .replace('|', '').replace(':', '').replace('"', '').replace('?', '') \
                        .replace('？', '').replace('\t', '')
                    time = time.replace('\r\n\r\n\r\n', '').strip()
                    item['pub_time'] = time  # datetime.strptime(time, '%Y-%m-%d')
                    item['url'] = url
                    item['title'] = title
                    content = pdf.main(url=url, fileName=title)
                    # if len(content) == 0:
                    #     item['content'] = '请打开原文链接查看'
                    # else ：
                    # item['content'] = content
                    if len(content) == 0:
                        item['content'] = '请点击原文链接查看' + response.url
                    else:
                        item['content'] = ''.join(list(content))
                    # item['add_time'] = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
                    item["keyword"] = keyword.get_keyword(item["content"])
                    item['web_id'] = 55
                    # print(item)
                    yield item
            else:

                pass
