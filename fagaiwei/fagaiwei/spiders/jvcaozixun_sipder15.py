# coding:utf-8
import scrapy
from fagaiwei.items import FagaiweiItem
from fagaiwei.jvchao_pdf import parse_jvhao_spider
from fagaiwei.jvchao_pdf.parse_jvhao_spider import allowed_domains


class xiamenSipderSpider(scrapy.Spider):
    name = 'jvchao_sipder15'
    allowed_domains = allowed_domains

    # start_urls = ['http://www.cninfo.com.cn/cninfo-new/index']

    def start_requests(self):
        urls = [
            # 信息披露
            "http://www.cninfo.com.cn/cninfo-new/disclosure/fund_other_latest",

        ]
        for url in urls:
            yield scrapy.FormRequest(url=url,
                                     formdata={"email": "xxx", "password": "xxxxx"},
                                     callback=self.parse,
                                     )

    def parse(self, response):
        item = FagaiweiItem()
        item_list = parse_jvhao_spider.parse_juchao(response, item)
        for items in item_list:
            yield items