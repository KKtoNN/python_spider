# -*- coding: utf-8 -*-
import time
import scrapy
from lxml import etree
from fagaiwei.items import FagaiweiItem
from fagaiwei.settings import session, NewsItemInfo
from fagaiwei.keyword_others import keyword


class ClsSipderSpider(scrapy.Spider):
    name = 'cls_sipder'
    allowed_domains = ['cailianpress.com']
    start_urls = ['http://cailianpress.com/']

    def parse(self, response):
        item = FagaiweiItem()
        html = etree.HTML(response.text)
        divs = html.xpath("//div[@data-jsx='99852006']/div")[1:-3]
        dates = ''.join(list(html.xpath(".//div[@class='time']/text()"))).strip()
        for div in divs:
            item['webname'] = '财联社'
            item['web'] = 'http://cailianpress.com'
            try:
                da = ''.join(list(div.xpath(".//div/div[@class='cTime']/text()"))).strip()
                if str(dates) in da:
                    times = da
                else:
                    times = dates + ' ' + da
            except Exception as e:
                times = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
            content = ''.join(list(div.xpath(".//div[@class='newsRight']/p/text()"))).strip()
            if "【" in content:
                item['title'] = ''.join(list(content.split('】')[0] + "】"))
                if len(item["title"]) < 10:
                    item['title'] = ''.join(list(content[0:30]))
            else:
                item['title'] = ''.join(list(content[0:30]))
            item['pub_time'] = times
            item['content'] = content
            item['url'] = 'http://cailianpress.com?' + str(times).replace(" ", "").replace(":", "")
            item["keyword"] = keyword.get_keyword(item["content"])
            item['web_id'] = 73
            # print(item)
            result = session.query(NewsItemInfo).filter_by(url=item['url'], web_id=73).count()
            if result:
                # print("{} 存在".format(item['url']))
                pass
            else:
                yield item
