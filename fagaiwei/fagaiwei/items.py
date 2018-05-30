# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class FagaiweiItem(scrapy.Item):
    web_id = scrapy.Field()
    webname = scrapy.Field()  # 网站名称
    web = scrapy.Field()  # 网站地址
    title = scrapy.Field()  # 标题
    pub_time = scrapy.Field()  # 网站发布时间
    content = scrapy.Field()  # 中文内容
    keyword = scrapy.Field()  # 关键字
    url = scrapy.Field()  # 来源地址 原来链接 详情页链接
    add_time = scrapy.Field()  # 入库时间
