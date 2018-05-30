# -*- coding: utf-8 -*-
import scrapy
from fagaiwei.items import FagaiweiItem
from fagaiwei.fagaiwei_pdf import parse_fagaiwei_spider


class GjfgwSpider(scrapy.Spider):
    name = 'gjfgw10'
    allowed_domains = parse_fagaiwei_spider.allowed_domains

    def start_requests(self):
        urls = [

            'http://wzs.ndrc.gov.cn/jwtz/jwtzgk/',  # 利用外资和境外投资司-境外投资-发展情况
            'http://wzs.ndrc.gov.cn/jwtz/gbzl/',  # 利用外资和境外投资司-境外投资-国别资料
            'http://wzs.ndrc.gov.cn/wstz/wstzgk/',  # 利用外资和境外投资司-外商投资-外商投资情况
            'http://wzs.ndrc.gov.cn/wstz/kfqqk/',  # 利用外资和境外投资司-外商投资-开发区情况
            'http://wzs.ndrc.gov.cn/wzgl/',  # 利用外资和境外投资司-外债管理
            'http://wzs.ndrc.gov.cn/zcfg/',  # 利用外资和境外投资司-政策法规
            'http://zys.ndrc.gov.cn/gzdt/',  # 政策研究室-工作动态
            'http://zys.ndrc.gov.cn/xwfb/',  # 政策研究室-新闻发布
            'http://wss.ndrc.gov.cn/gzdt/',  # 国际合作司-工作动态
            'http://jys.ndrc.gov.cn/xinxi/',  # 就业和收入分配司-近期要闻
            'http://jys.ndrc.gov.cn/gzdt/',  # 就业和收入分配司-工作动态
            'http://jys.ndrc.gov.cn/dfjy2/',  # 就业和收入分配司-地方经验
            'http://jys.ndrc.gov.cn/zcfg/',  # 就业和收入分配司-政策研究
            'http://jtyss.ndrc.gov.cn/gzdt/',  # 基础产业司-工作动态
            'http://jtyss.ndrc.gov.cn/zcfg/',  # 基础产业司-政策规划
            'http://jtyss.ndrc.gov.cn/zdxm/',  # 基础产业司-重大工程
            'http://jtyss.ndrc.gov.cn/jtyj/',  # 基础产业司-问题研究
            'http://jtyss.ndrc.gov.cn/hysj/',  # 基础产业司-行业数据
            'http://jtyss.ndrc.gov.cn/dffz/',  # 基础产业司-地方发展
        ]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        datas = parse_fagaiwei_spider.url_fagaiwei(response)
        for data1 in datas:
            # print(data1)
            url = data1['url']
            date = data1['date']
            title = data1['title']
            yield scrapy.Request(url=url, callback=self.get_detail,
                                 meta={"date": date, "title": title, "laiyuan": response.url})

    def get_detail(self, response):
        item = FagaiweiItem()
        item_list = parse_fagaiwei_spider.parse_fagaiwei(response, item)
        for items in item_list:
            yield items
