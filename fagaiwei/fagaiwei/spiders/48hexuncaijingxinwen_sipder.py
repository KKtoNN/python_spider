# coding:utf-8
import scrapy
import json
import jsonpath
from fagaiwei.items import FagaiweiItem
import time
from fagaiwei.settings import session, NewsItemInfo


class xiamenSipderSpider(scrapy.Spider):
    name = 'hexuncaijingxinwen_sipder'
    allowed_domains = ['hexun.com']
    start_urls = [
        'http://open.tool.hexun.com/MongodbNewsService/data/getOriginalNewsList.jsp?id=187804274&s=30&cp=1&priority=0&callback=hx_json',

    ]

    def parse(self, response):
        json_text = response.text[8:]
        json_text = json_text.replace(' )', '')
        json_str = json.loads(json_text, encoding='utf8')
        urls = jsonpath.jsonpath(json_str, '$..entityurl')
        laiyuan = jsonpath.jsonpath(json_str, '$..channelname')
        titles = jsonpath.jsonpath(json_str, '$..title')
        dabao = zip(urls, titles, laiyuan)
        for url, title, laiyuan in dabao:
            result = session.query(NewsItemInfo).filter_by(url=url, web_id=48).count()
            if result:
                # print("URL文件地址： {} 存在".format(url))
                pass
            else:
                yield scrapy.Request(url=url, callback=self.parse_page, meta={'title': title, 'laiyuan': laiyuan})

    def parse_page(self, response):
        item = FagaiweiItem()
        item['title'] = response.meta['title']
        item['webname'] = '和讯财经新闻网' + response.meta['laiyuan']
        item['web'] = 'http://news.hexun.com/original/'
        item['url'] = response.url
        item['pub_time'] = response.xpath("//span[@class='pr20']/text()").get()
        item['content'] = ''.join(
            list(response.xpath("//div[@class='art_contextBox']//p[not(script)]//text()").getall())).replace('\u3000',
                                                                                                             '')
        item['add_time'] = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        item['keyword'] = ''
        item['web_id'] = 48
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
