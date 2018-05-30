import time
import json
import scrapy
import jsonpath
from fagaiwei.items import FagaiweiItem
from fagaiwei.keyword_others import keyword
from fagaiwei.settings import session, NewsItemInfo


class xiamenSipderSpider(scrapy.Spider):
    name = 'renmingwang_sipder'
    allowed_domains = ['people.com.cn', 'xueqiu.com']
    start_urls = [
        'http://news.people.com.cn/210801/211150/index.js',
    ]

    def parse(self, response):
        urlsy = []
        response = response.text
        json_str = json.loads(response, encoding='utf-8')
        urls = jsonpath.jsonpath(json_str, '$..url')
        nodeIds = jsonpath.jsonpath(json_str, '$..nodeId')
        titles = jsonpath.jsonpath(json_str, '$..title')
        datas = jsonpath.jsonpath(json_str, '$..date')
        dabaos = zip(urls, nodeIds, titles, datas)
        for url, node, titles, datas in dabaos:
            # print(url)
            node = int(node)
            # 把不需要的nodeID写进去就可以过滤他那一类的新闻
            not_node = [1016, 368583, 174585]
            if url not in urlsy:
                if node not in not_node:
                    urlsy.append(url)
                    result = session.query(NewsItemInfo).filter_by(url=url, web_id=33).count()
                    if result:
                        # print("{} 存在".format(url))
                        pass
                    else:
                        yield scrapy.Request(url=url, callback=self.parse_page, meta={'title': titles,
                                                                                      'data': datas})
                else:
                    pass
            else:
                pass

    def parse_page(self, response):
        item = FagaiweiItem()
        mrurl = 'http://www.people.com.cn/'
        title = response.meta['title']
        item['title'] = title.replace('&nbsp', '')
        item['pub_time'] = response.meta['data']
        laiyuan = response.xpath("//div[@class='box01']/div/a/@href|"
                                 "//div[@class='artOri']/a/@href|"
                                 "//div[@class='text_c']/p/a/@href|"
                                 "//h2/a/@href|"
                                 "//div[@class='fr']/a[1]/@href").get()

        # 判断是否有获取到的来源链接
        if laiyuan is None:
            item['web'] = mrurl
        elif laiyuan.startswith('http'):
            item['web'] = laiyuan
        else:
            item['web'] = mrurl

        item["url"] = response.url
        # 获取文章来源
        webname = response.xpath("//div[@class='box01']/div/a/text()|"
                                 "//div[@class='artOri']/a/text()|"
                                 "//div[@class='text_c']/p/a/text()|"
                                 "//h2/a/text()|"
                                 "//div[@class='fr']/a[1]/text()").get()

        if webname is None:
            item['webname'] = '人民网'
        else:
            item['webname'] = webname

        item['content'] = ''.join(list(response.xpath("//div[@class='box_con']//text()|"
                                                      "//div[@class='show_text']//text()|"
                                                      "//div[contains(@class,'box_text')]//text()|"
                                                      "//div[@class='show_text']//text()|"
                                                      "//div[@class='artDet']//text()|"
                                                      "//div[contains(@class,'content')]//text()|"
                                                      "//div[contains(@class,'text_con_left')]//text()").getall())) \
            .replace("\u3000", '').strip()

        item['add_time'] = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        item["keyword"] = keyword.get_keyword(item["content"])

        item['web_id'] = 33

        return item
