# -*- coding: utf-8 -*-
import datetime
import time
import scrapy
from fagaiwei.settings import session, NewsItemInfo
from fagaiwei.items import FagaiweiItem
from fagaiwei.keyword_others import keyword


class WaijiaobuSpider(scrapy.Spider):
    name = 'waijiaobu'
    allowed_domains = ['fmprc.gov.cn']
    start_urls = ['http://fmprc.gov.cn/']

    def start_requests(self):
        urls = [
            "http://www.fmprc.gov.cn/web/zyxw/",  # 外交部-重要新闻
            "http://www.fmprc.gov.cn/web/wjbz_673089/zyhd_673091/",  # 外交部-相关新闻
            "http://www.fmprc.gov.cn/web/wjbz_673089/zyjh_673099/",  # 外交部-重要讲话
            "http://www.fmprc.gov.cn/web/wjbz_673089/xghd_673097/",  # 外交部-活动
            "http://www.fmprc.gov.cn/web/wjbxw_673019/",  # 外交部-外交部新闻
            "http://www.fmprc.gov.cn/web/ziliao_674904/zyjh_674906/",  # 外交部-资料-重要讲话
        ]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        message_list = response.xpath('//div[@class="imbox_ul"]/ul/li|//div[@class="rebox_news"]/ul/li')
        # print(len(message_list))
        for message in message_list:
            title = "".join(message.xpath('a/text()').extract())
            href = "".join(message.xpath('a/@href').extract())
            date = "".join(message.xpath('text()').extract())
            date = date.replace("(", "").replace(")", "")
            try:
                date = datetime.datetime.strptime(str(date).replace('/', '-'), '%Y-%m-%d')
                # print(date)
            except Exception as e:
                # print(e)
                date = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
            url = response.url + href
            # print(title, url, date)
            result = session.query(NewsItemInfo).filter_by(url=url, web_id=10).count()
            if result:
                # print("{} 存在".format(url))
                pass
            else:
                yield scrapy.Request(url=url, callback=self.get_detail,
                                 meta={"title": title, "date": date, "laiyuan": response.url})

    def get_detail(self, response):
        item = FagaiweiItem()
        item["url"] = response.url
        item["pub_time"] = response.meta["date"]
        item["title"] = response.meta["title"]
        item["webname"] = "外交部"
        item["web"] = response.meta["laiyuan"]
        item["web_id"] = 10
        contents = "".join(response.xpath('//*[@id="News_Body_Txt_A"]/p/text()|\
                                            //*[@id="News_Body_Txt_A"]/p/strong/text()|\
                                            //*[@id="News_Body_Txt_A"]/p/strong/text()').extract())
        # print(contents)
        if contents != "":
            item["content"] = contents.replace("\u3000", "")
        else:
            item["content"] = "可能是图片 请打开详情页查看"
        item["keyword"] = keyword.get_keyword(item["content"])
        return item
