# coding:utf-8
import scrapy
import json
import jsonpath
from fagaiwei.items import FagaiweiItem
import time
from fagaiwei.settings import session, NewsItemInfo


class xiamenSipderSpider(scrapy.Spider):
    name = 'yangshiwang_sipder'
    allowed_domains = ['cctv.com']
    start_urls = [
        'http://news.cctv.com/world/data/index.json',
        'http://news.cctv.com/data/index.json',
        'http://news.cctv.com/china/data/index.json',
        'http://jingji.cctv.com/data/index.json'
    ]

    def parse(self, response):
        json_text = response.text
        json_str = json.loads(json_text, encoding='utf8')
        urls = jsonpath.jsonpath(json_str, '$..url')
        pub_times = jsonpath.jsonpath(json_str, '$..dateTime')
        titles = jsonpath.jsonpath(json_str, '$..title')
        contents = jsonpath.jsonpath(json_str, '$..description')
        dabao = zip(urls,titles,pub_times,contents)
        for url,title,pub_time,content in dabao:
            result = session.query(NewsItemInfo).filter_by(url=url, web_id=44).count()
            if result:
                # print("URL文件地址： {} 存在".format(url))
                pass
            else:
                item = FagaiweiItem()
                item['webname'] = '央视网'
                item['web'] = 'http://news.cctv.com/'
                item['url'] = url
                item['pub_time'] = pub_time
                item['content'] = content
                item['keyword'] = ''
                item['title'] = title
                item['add_time'] = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
                item['web_id'] = 44
                yield item
