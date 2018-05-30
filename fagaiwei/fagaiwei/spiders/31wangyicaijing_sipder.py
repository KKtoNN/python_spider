# coding:utf-8
import scrapy
import json
import jsonpath
from fagaiwei.items import FagaiweiItem
import time
from fagaiwei.settings import session, NewsItemInfo


class xiamenSipderSpider(scrapy.Spider):
    name = 'wangyicaijing_sipder'
    allowed_domains = ['163.com']
    start_urls = [
        'http://money.163.com/special/00251G8F/news_json.js'
    ]

    def parse(self, response):

        json_text = (response.text).split("news")[1]
        json_text = '{"news"' + json_text
        json_text = json_text.replace('{c:', '{"c":').replace(',t:', ',"t":').replace(',l:', ',"l":') \
            .replace(',p:', ',"p":').replace(';', '')
        json_str = json.loads(json_text, encoding='utf8')
        urls = jsonpath.jsonpath(json_str, '$..l')
        for url in urls:
            if url[-4:] == 'html':
                result = session.query(NewsItemInfo).filter_by(url=url, web_id=31).count()
                if result:
                    # print("PDF 文件地址： {} 存在".format(url))
                    pass
                else:

                    yield scrapy.Request(url=url, callback=self.parse_page, meta={'url': response.url})
            else:
                pass

    def parse_page(self, response):
        item = FagaiweiItem()
        item['title'] = response.xpath("//h1/text()").get()
        pub_time = response.xpath("//div[@class='post_time_source']/text()").get()
        if pub_time is not None:
            item['pub_time'] = (pub_time.replace("　来源:", '')).strip()
        else:
            item['pub_time'] = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        laiyuan = response.xpath("//div[@class='post_time_source']/a/text()").get()
        if laiyuan is None:
            item['webname'] = '网易财经'
        else:
            item['webname'] = laiyuan
        web = response.xpath("//div[@class='post_time_source']/a/@href").get()
        if web is None:
            item['web'] = 'http://money.163.com/latest/'
        else:
            item['web'] = web
        item['content'] = ''.join(
            list(response.xpath("//div[@id='endText']//p[not(script)]//text()").getall())).replace('\t', '').replace(
            '\xa0', '')
        item['url'] = response.url
        item['add_time'] = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        item['keyword'] = ''
        item['web_id'] = 31
        # print(item)
        yield item









        # for url in urls:
        #     print(url)
        #     if url not in qc_url:
        #         qc_url.append(url)
        #     else:
        #         pass
        # print(response.text)
        # with open('aaa.html','w',encoding='utf-8') as fp :
        #     fp.write(response.text)
        # print(len(qc_url))
        # for url in urls:
        #     print(url)
        # result = session.query(NewsItemInfo).filter_by(url=url, web_id=41).count()
        # if result:
        #     print("{} 存在".format(url))
        #     pass
        # else:
        #     item = FagaiweiItem()
        #     item['title'] = ''.join(list(response.xpath("//h1/text()").get())).replace('\u3000', '')
        #     pub_time = response.xpath("//div[@class = 'fl_dib']/text()").get()
        #     if pub_time is None:
        #         item['pub_time'] = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        #     else:
        #         item['pub_time'] = pub_time
        #     web = response.xpath("//div[@class = 'fl_dib']/a/@href").get()
        #     if web is None:
        #         item['web'] = 'http://news.takungpao.com/'
        #     else:
        #         item['web'] = web
        #     laiyuan = response.xpath("//div[@class = 'fl_dib']/a/text()").get()
        #     item['url'] = response.url
        #     if laiyuan is None:
        #         item['webname'] = '太公网'
        #     else:
        #         item['webname'] = laiyuan
        #     content = ''.join(list(response.xpath("//div[contains(@class,'tpk_text')]//text()").getall())) \
        #         .replace('\u3000', '').replace('\t', '').replace('\r', '')
        #     if content is None:
        #         item['content'] = '请点击原文链接查看内容'
        #     else:
        #         item['content'] = content
        #     item['add_time'] = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        #     item['keyword'] = ' '
        #     item['web_id'] = 41
        #     yield item
