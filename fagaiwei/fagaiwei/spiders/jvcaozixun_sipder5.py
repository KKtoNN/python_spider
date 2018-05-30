# coding:utf-8
import scrapy
from fagaiwei.items import FagaiweiItem
from fagaiwei.jvchao_pdf import parse_jvhao_spider
from fagaiwei.jvchao_pdf.parse_jvhao_spider import allowed_domains


class xiamenSipderSpider(scrapy.Spider):
    name = 'jvchao_sipder5'
    allowed_domains = allowed_domains

    # start_urls = ['http://www.cninfo.com.cn/cninfo-new/index']

    def start_requests(self):
        urls = [
            # 信息披露
            "http://www.cninfo.com.cn/cninfo-new/disclosure/sse_latest",
            # "http://www.cninfo.com.cn/cninfo-new/disclosure/pre_disclosure_latest",
            # "http://www.cninfo.com.cn/cninfo-new/disclosure/staq_net_delisted_latest",
            # "http://www.cninfo.com.cn/cninfo-new/disclosure/neeq_company_latest",
            # "http://www.cninfo.com.cn/cninfo-new/disclosure/hke_latest",
            # "http://www.cninfo.com.cn/cninfo-new/disclosure/hke_main_latest",
            # "http://www.cninfo.com.cn/cninfo-new/disclosure/hke_gem_latest",
            # "http://www.cninfo.com.cn/cninfo-new/disclosure/fund_latest",
            # "http://www.cninfo.com.cn/cninfo-new/disclosure/fund_listed_latest",
            # "http://www.cninfo.com.cn/cninfo-new/disclosure/fund_sse_latest",
            # "http://www.cninfo.com.cn/cninfo-new/disclosure/fund_other_latest",
            # "http://www.cninfo.com.cn/cninfo-new/disclosure/bond_latest",
            # "http://www.cninfo.com.cn/cninfo-new/disclosure/bond_szse_latest",
            # "http://www.cninfo.com.cn/cninfo-new/disclosure/bond_sse_latest",
            # "http://www.cninfo.com.cn/cninfo-new/disclosure/regulator_szse_latest",
            # "http://www.cninfo.com.cn/cninfo-new/disclosure/regulator_szse_latest",
            # "http://www.cninfo.com.cn/cninfo-new/disclosure/regulator_sse_latest",
            # "http://www.cninfo.com.cn/cninfo-new/disclosure/continue_supervise_latest",

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
