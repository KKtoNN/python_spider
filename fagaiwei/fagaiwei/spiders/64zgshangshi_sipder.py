import scrapy
from fagaiwei.items import FagaiweiItem
import time
from fagaiwei.settings import session, NewsItemInfo
from fagaiwei.keyword_others import keyword


class xiamenSipderSpider(scrapy.Spider):
    name = 'zgshangshi_spider'
    allowed_domains = ['cnlist.com']

    # start_urls = [
    #     'http://news.cnstock.com/news/sns_yw/index.html',
    # ]

    def start_requests(self):
        urls = [
            "http://www.cnlist.com/information/newsSplitList.jsp?url=/getMultilevelCapitalMarketList.do&pageName=marketSplitList&typeCode=zbsc",
            "http://www.cnlist.com/information/newsSplitList.jsp?url=/getNewsDisclosureList.do&typeCode=xxpl&columnCode=shzb",
            "http://www.cnlist.com/information/newsSplitList.jsp?url=/getCompanyNewsList.do&typeCode=gsxw&columnCode=shzb",
            "http://www.cnlist.com/information/newsSplitList.jsp?url=/getFinancialNewsList.do&typeCode=cjxw&columnCode=gjcj",
            "http://www.cnlist.com/information/newsSplitList.jsp?url=/getFinancialNewsList.do&typeCode=cjxw&columnCode=zqyw",
            "http://www.cnlist.com/information/newsSplitList.jsp?url=/getFinancialNewsList.do&typeCode=cjxw&columnCode=gncj",
            "http://www.cnlist.com/information/newsSplitList.jsp?url=/getFinancialNewsList.do&typeCode=cjxw&columnCode=gjcj",
        ]

        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        pub_title = '中国上市公司'
        title2 = response.xpath("//span[@class='title']/text()").get()
        webname = pub_title + title2
        urls = response.xpath("//div[@class='list_data']//li/a/@onclick").getall()
        urla = response.url
        data = response.xpath("//span[@class='date']/text()").get()
        if data.startswith('2018'):
            data = data
        else:
            data = '2018-' + data
        for url in urls:
            url = 'http://www.cnlist.com' + url.replace("OpenDetail('", '') \
                .replace(',', '?id=').replace("');", '').replace(' ', '').replace("'", "")

            result = session.query(NewsItemInfo).filter_by(url=url, web_id=64).count()
            if result:
                # print("PDF 文件地址： {} 存在".format(url))
                pass
            else:
                yield scrapy.Request(url=url, callback=self.parse_page,
                                     meta={'url': urla, 'webname': webname, 'data': data})

    def parse_page(self, response):
        item = FagaiweiItem()
        item['url'] = response.url
        item['pub_time'] = response.meta['data']
        item['webname'] = response.meta['webname']
        item['web'] = response.meta['url']
        item['title'] = ''.join(list(response.xpath("//div[@class='list_content_title']/span/text()").get())) \
            .replace('&nbsp', '').replace('\xa0', '')

        content = ''.join(list(response.xpath("//div[@class='list_content_details']//text()"
                                              # "//div[@class='logtext']//p//text()|"
                                              # "//div[@class='logtext']//text()|"
                                              # "//td[@class='logtext']//text()|"
                                              # "//p[@class='des']/text()"
                                              ).getall())).replace('\u3000', '').replace('\xa0', '').replace('&nbsp;',
                                                                                                             '').replace(
            '\t', '').replace('\r\n', '')
        if content == '':
            item['content'] = '请点击原文链接查看' + response.url
        else:
            item['content'] = content

        item['add_time'] = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        item["keyword"] = keyword.get_keyword(item["content"])
        item['web_id'] = 64
        # print(item)
        return item
