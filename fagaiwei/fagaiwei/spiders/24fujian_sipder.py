# -*- coding: utf-8 -*-
import time
import scrapy
from fagaiwei.items import FagaiweiItem
from fagaiwei.keyword_others import keyword
from fagaiwei.settings import session, NewsItemInfo


class FjzfSpider(scrapy.Spider):
    name = 'fujian_sipder'
    allowed_domains = ['gov.cn']
    start_urls = ['http://www.fujian.gov.cn/zc/zxwj/szfwj/']
    SHENGFEN = '福建省'

    def start_requests(self):
        urls = [
            "http://www.fujian.gov.cn/zc/zxwj/szfwj/",
            "http://www.fujian.gov.cn/zc/zxwj/szfbgtwj/",
            # "http://www.fujian.gov.cn/zc/zxwj/sqswj/",
            "http://www.fujian.gov.cn/zc/zxwj/sqswj/fz/",
            "http://www.fujian.gov.cn/zc/zxwj/sqswj/xm/",
            "http://www.fujian.gov.cn/zc/zxwj/sqswj/zz/",
            "http://www.fujian.gov.cn/zc/zxwj/sqswj/qz/",
            "http://www.fujian.gov.cn/zc/zxwj/sqswj/sm/",
            "http://www.fujian.gov.cn/zc/zxwj/sqswj/pt/",
            "http://www.fujian.gov.cn/zc/zxwj/sqswj/np/",
            "http://www.fujian.gov.cn/zc/zxwj/sqswj/ly/",
            "http://www.fujian.gov.cn/zc/zxwj/sqswj/nd/",
            "http://www.fujian.gov.cn/zc/zxwj/bmwj/",
            "http://www.fujian.gov.cn/xw/mszx/",
            # "http://www.fujian.gov.cn/xw/zfgzdt/sxdt/",
            "http://www.fujian.gov.cn/xw/zfgzdt/sxdt/fz/",
            "http://www.fujian.gov.cn/xw/zfgzdt/sxdt/xm/",
            "http://www.fujian.gov.cn/xw/zfgzdt/sxdt/zz/",
            "http://www.fujian.gov.cn/xw/zfgzdt/sxdt/qz/",
            "http://www.fujian.gov.cn/xw/zfgzdt/sxdt/sm/",
            "http://www.fujian.gov.cn/xw/zfgzdt/sxdt/pt/",
            "http://www.fujian.gov.cn/xw/zfgzdt/sxdt/np/",
            "http://www.fujian.gov.cn/xw/zfgzdt/sxdt/ly/",
            "http://www.fujian.gov.cn/xw/zfgzdt/sxdt/nd/",
            "http://www.fujian.gov.cn/xw/zfgzdt/sxdt/ptzhsyq/",
            "http://www.fujian.gov.cn/xw/zfgzdt/szfhy/",
            "http://www.fujian.gov.cn/xw/fjyw/",

        ]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        # 获取文本也url
        url = response.url
        contens_urls = response.xpath("/html/body/div[2]/div[3]/div[2]/div[3]/div/ul/li/a/@href").getall()
        name = response.xpath("//h4/text()")[0].get()
        for contens_url in contens_urls:
            contens_url = contens_url.replace('./', '')
            contens_url = url + contens_url
            result = session.query(NewsItemInfo).filter_by(url=contens_url, web_id=24).count()
            if result:
                # print("{} 存在".format(contens_url))
                pass
            else:
                yield scrapy.Request(url=contens_url, callback=self.parse_page,
                                     meta={"name": name, "web": url, })

    def parse_page(self, response):
        # print(response.url)
        # 解析详情页的信息
        item = FagaiweiItem()
        item['webname'] = self.SHENGFEN + response.meta['name']
        item['web'] = response.meta['web']
        times = ''.join(list(response.xpath("//h5/text()")[1].get()))
        item['title'] = response.xpath("//h3/text()").get()
        item['pub_time'] = (times.split('\n')[1]).strip()
        content = ''.join(list(response.xpath("//div[@class='TRS_Editor']//text()").getall())).strip()
        laiyuan = response.xpath("//h4/text()")[0].get()
        if laiyuan == '附件下载：':
            laiyuan = response.xpath("//h5/span/text()").get()
        content = content.replace("\xa0", "")
        item['content'] = laiyuan + "\n" + content.replace("\u3000", "")
        item['url'] = response.url
        item['add_time'] = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        item["keyword"] = keyword.get_keyword(item["content"])

        item['web_id'] = 24
        return item
