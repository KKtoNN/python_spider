import scrapy
import re
from fagaiwei.items import FagaiweiItem
from fagaiwei.keyword_others import keyword
import time
import datetime
from fagaiwei.settings import session, NewsItemInfo


class xiamenSipderSpider(scrapy.Spider):
    name = 'xiamen_sipder'
    allowed_domains = ['xm.gov.cn']

    def start_requests(self):
        urls = [
            "http://www.xm.gov.cn/zwgk/flfg/zfgz/",
            "http://www.xm.gov.cn/zwgk/flfg/sfwj/",
            "http://www.xm.gov.cn/zwgk/flfg/sfbwj/",
            "http://www.xm.gov.cn/zwgk/flfg/gqwj/",
            "http://www.xm.gov.cn/zwgk/flfg/bmwj/",
            "http://www.xm.gov.cn/zwgk/flfg/qtwj/",
            "http://www.xm.gov.cn/zwgk/ldhd/hy/",
            "http://www.xm.gov.cn/zwgk/ldhd/dy/",
            "http://www.xm.gov.cn/zwgk/ldhd/hd/",
        ]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        # 获取页面详情页的url
        url = response.url
        orurl = 'http://www.xm.gov.cn/'
        contens_urls = response.xpath("//div[@class='gl_list1']//li/a/@href").getall()
        name = response.xpath("//li[@class='on']/a/text()")[-1].get()

        for contens_url in contens_urls:
            if contens_url.startswith('./'):
                contens_url = contens_url.replace('./', '')
                contens_url = url + contens_url
            elif contens_url.startswith('../'):
                contens_url = contens_url.replace('../', '')
                contens_url = orurl + contens_url

            result = session.query(NewsItemInfo).filter_by(url=contens_url, web_id=25).count()
            if result:
                # print("{} 存在".format(contens_url))
                pass
            else:
                yield scrapy.Request(url=contens_url, callback=self.parse_page,
                                     meta={"url": url, "name": name})

    def parse_page(self, response):
        item = FagaiweiItem()
        item['webname'] = "厦门" + response.meta['name']
        item['web'] = response.meta['url']
        item['title'] = response.xpath("//div[@class='zfxx_xl_tit1']/text()|"
                                       "//div[@class='xl_tit1']/text()|"
                                       "//div[@class='zfxx_xl_tit2']/text()").get()
        times = ''.join(list(response.xpath("//div[@class='zfxx_xl_tit2']/text()|"
                                            "//div[@class='xl_tit2']/text()|"
                                            "/html/body/div[2]/div[3]/div[3]/text()[1]"
                                            ).getall())).strip()
        time_s = "".join(re.findall(re.compile(r'([0-9]{4}-[0-9]{2}-[0-9]{2} [0-9]{2}:[0-9]{2})'), times))
        # print(time_s)
        try:
            time_s = datetime.datetime.strptime(str(time_s).replace('/', '-'), '%Y-%m-%d %H:%M')
            # print(date)
        except Exception as e:
            # print(e)
            time_s = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
        # print(time_s)
        item['pub_time'] = time_s
        laiyuan = response.xpath("//h4/text()").get()
        bbb = ''.join(list(response.xpath("//div[@class='zfxx_xl_con']/div[4]/p/text()|\
                                          //div[@class='Custom_UnionStyle']/p/text()|\
                                          //div[@class='TRS_Editor']/div/span/text()|\
                                          //div[@class='TRS_Editor']/div/p/text()|\
                                          //div[@class='Custom_UnionStyle']/p/text()"
                                          ).getall())).replace('\u3000', '') \
            .replace('\ue005', '').replace('\n', '').replace('', '').replace('\ue003', ''). \
            replace('\ue004', '').replace('\xa0', '')
        if laiyuan == None:
            item['content'] = bbb
        else:
            item['content'] = laiyuan + bbb
        item['url'] = response.url
        item['add_time'] = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        item["keyword"] = keyword.get_keyword(item["content"])

        item['web_id'] = 25
        return item
