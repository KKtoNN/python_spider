# coding:utf-8
import scrapy
from fagaiwei.items import FagaiweiItem
from fagaiwei.jvchao_pdf import parse_jvhao_spider
from fagaiwei.jvchao_pdf.parse_jvhao_spider import allowed_domains


class xiamenSipderSpider(scrapy.Spider):
    name = 'jvchao_sipder'
    allowed_domains = allowed_domains

    # start_urls = ['http://www.cninfo.com.cn/cninfo-new/index']

    def start_requests(self):
        urls = [
            # 信息披露
            "http://www.cninfo.com.cn/cninfo-new/disclosure/szse_latest",
            # "http://www.cninfo.com.cn/cninfo-new/disclosure/szse_main_latest",
            # "http://www.cninfo.com.cn/cninfo-new/disclosure/szse_sme_latest",
            # "http://www.cninfo.com.cn/cninfo-new/disclosure/szse_gem_latest",
            # "http://www.cninfo.com.cn/cninfo-new/disclosure/sse_latest",
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
        # PUB_URL = 'http://www.cninfo.com.cn/cninfo-new/disclosure/szse/bulletin_detail/true/'
        # D_URL = 'http://www.cninfo.com.cn/cninfo-new/disclosure/szse/download/'
        # dates = response.text
        # json_str = json.loads(dates, encoding='utf-8')
        # urls = jsonpath.jsonpath(json_str, "$..announcementId")
        # title1 = jsonpath.jsonpath(json_str, "$..secCode")
        # title2 = jsonpath.jsonpath(json_str, "$..secName")
        # title3 = jsonpath.jsonpath(json_str, "$..announcementTitle")
        # timestamp = jsonpath.jsonpath(json_str, "$..announcementTime")
        # pdf = jsonpath.jsonpath(json_str, "$..adjunctUrl")
        # if title2 is None:
        #     title2 = ''
        #     titles = zip(title1, title3)
        # else:
        #     titles = zip(title1, title2, title3)
        #
        # url_contents = zip(urls, titles, timestamp, pdf)
        # for url, title, time_local, pdf in url_contents:
        #     if None in title:
        #         title = title[0] + title[2]
        #     else:
        #         title = title
        #     title = ' '.join(list(title)).replace('*', '').replace('/', '').replace('<', '').replace('>', '') \
        #         .replace('|', '').replace(':', '').replace('"', '').replace('?', '') \
        #         .replace('？', '')
        #
        #     durl = D_URL + url
        #
        #     if pdf[-4:] == '.PDF':
        #
        #         contents = pdf_to_txt.main(url=durl, fileName=title)
        #         item['content'] = '\n'.join(list(contents))
        #         times = str(time_local)[0:-3] + '.' + '000'
        #         item['pub_time'] = datetime.datetime.fromtimestamp(float(times)).strftime('%Y-%m-%d %H:%M:%S')
        #         item['webname'] = '巨潮资讯'
        #         item['web'] = response.url[0:-7]
        #         item['add_time'] = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        #         item['keyword'] = ''
        #         item['web_id'] = 56
        #         item['title'] = title
        #         item['url'] = PUB_URL + url
        #         yield item
        #     else:
        #         pass
