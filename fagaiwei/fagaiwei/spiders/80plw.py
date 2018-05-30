# -*- coding: utf-8 -*-
from datetime import datetime
import scrapy
from fagaiwei.items import FagaiweiItem
from fagaiwei.keyword_others import keyword
from fagaiwei.jvchao_pdf import pdf_to_txt as pdf
from fagaiwei.settings import session, NewsItemInfo


class ZjzxSpider(scrapy.Spider):
    # 披漏网
    name = 'pilouwang'
    allowed_domains = ['hkexnews.hk']
    start_urls = ['http://www.hkexnews.hk/listedco/listconews/mainindex/SEHK_LISTEDCO_DATETIME_TODAY_C.HTM'
                  ]

    def parse(self, response):
        info_list = response.xpath('//body/table[2]/tr[3]/td/table/tr[contains(@class,"row")]')
        for info in info_list:
            item = FagaiweiItem()
            url = 'http://www.hkexnews.hk' + info.xpath('./td[4]/a/@href').extract_first(default='')
            # print(url)
            if url[-4:] == '.pdf':
                result = session.query(NewsItemInfo).filter_by(url=url, web_id=80).count()
                if result:
                    # print("PDF 文件地址： {} 存在".format(url))
                    pass
                else:
                    item['url'] = url
                    title = info.xpath('./td[3]/nobr/text()').extract_first() + ':' + info.xpath(
                        './td[4]/div/text()').extract_first(default='').strip()
                    title = ''.join(list(title)).replace('*', '').replace('/', '').replace('<', '').replace('>', '') \
                        .replace('|', '').replace(':', '').replace('"', '').replace('?', '') \
                        .replace('？', '')
                    item['title'] = title
                    item['web'] = response.url
                    item['webname'] = '披漏网'
                    time = ' '.join(info.xpath('./td[1]/text()').extract()).replace('/', '-')
                    item['pub_time'] = datetime.strptime(time, '%d-%m-%Y %H:%M')
                    content = pdf.main(url=url, fileName=title)
                    if len(content) == 0:
                        item['content'] = '这可能是图片或者文件，打开查看！'
                    else:
                        item['content'] = ''.join(list(content))
                    item['web_id'] = 80
                    item["keyword"] = keyword.get_keyword(item["content"])
                    yield item
