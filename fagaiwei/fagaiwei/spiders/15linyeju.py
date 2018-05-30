# -*- coding: utf-8 -*-
import datetime
import time
import scrapy
from fagaiwei.settings import session, NewsItemInfo
from fagaiwei.items import FagaiweiItem
from fagaiwei.keyword_others import keyword


class LinyejuSpider(scrapy.Spider):
    name = 'linyeju'
    allowed_domains = ['forestry.gov.cn']
    start_urls = ['http://forestry.gov.cn/']

    def start_requests(self):
        urls = [
            "http://www.forestry.gov.cn/Common/index/3563.html",  # 中国林业网 > 信息发布 > 森林防火与森林公安 > 火险预报
            "http://www.forestry.gov.cn/Common/index/5384.html",  # 中国林业网 > 信息发布 > 集体林改 > 各地动态
            "http://www.forestry.gov.cn/Common/index/5383.html",  # 中国林业网 > 信息发布 > 集体林改 > 重要信息
            "http://www.forestry.gov.cn/Common/index/146.html",  # 中国林业网 > 信息发布 > 生物多样性 > 工作动态
            "http://www.forestry.gov.cn/Common/index/135.html",  # 中国林业网 > 信息发布 > 防沙治沙 > 工作动态
            "http://www.forestry.gov.cn/Common/index/448.html",  # 中国林业网 > 信息发布 > 资源管理 > 林地林权
            "http://www.forestry.gov.cn/Common/index/449.html",  # 中国林业网 > 信息发布 > 资源管理 > 采伐利用
            "http://www.forestry.gov.cn/Common/index/447.html",  # 中国林业网 > 信息发布 > 资源管理 > 资源监测
            "http://www.forestry.gov.cn/Common/index/446.html",  # 中国林业网 > 信息发布 > 资源管理 > 综合信息
            "http://www.forestry.gov.cn/Common/index/395.html",  # 中国林业网 > 信息发布 > 造林绿化 > 绿化基金
            "http://www.forestry.gov.cn/Common/index/394.html",  # 中国林业网 > 信息发布 > 造林绿化 > 林业有害生物防治
            "http://www.forestry.gov.cn/Common/index/393.html",  # 中国林业网 > 信息发布 > 造林绿化 > 国土绿化
            "http://www.forestry.gov.cn/Common/index/392.html",  # 中国林业网 > 信息发布 > 造林绿化 > 植树造林
            "http://www.forestry.gov.cn/Common/index/4423.html",  # 中国林业网 > 信息发布 > 科学技术 > 科技动态
            "http://www.forestry.gov.cn/Common/index/3605.html",  # 中国林业网 > 信息发布 > 陆生野生动物疫源疫病监测 > 公文公告
            "http://www.forestry.gov.cn/Common/index/3293.html",  # 中国林业网 > 信息发布 > 陆生野生动物疫源疫病监测 > 应急预案
            "http://www.forestry.gov.cn/Common/index/3603.html",  # 中国林业网 > 信息发布 > 陆生野生动物疫源疫病监测 > 监测预警
            "http://www.forestry.gov.cn/Common/index/3602.html",  # 中国林业网 > 信息发布 > 陆生野生动物疫源疫病监测 > 工作动态
            "http://www.forestry.gov.cn/Common/index/3244.html",  # 中国林业网 > 信息发布 > 重大沙尘暴灾害 > 工作动态
            "http://www.forestry.gov.cn/Common/index/3243.html",  # 中国林业网 > 信息发布 > 重大沙尘暴灾害 > 监测评估
            "http://www.forestry.gov.cn/Common/index/3593.html",  # 中国林业网 > 信息发布 > 重大沙尘暴灾害 > 应急预案
            "http://www.forestry.gov.cn/Common/index/3595.html",  # 中国林业网 > 信息发布 > 重大沙尘暴灾害 > 法律法规
            "http://www.forestry.gov.cn/Common/index/3599.html",  # 中国林业网 > 信息发布 > 重大外来林业有害生物灾害 > 应急处置
            "http://www.forestry.gov.cn/Common/index/3598.html",  # 中国林业网 > 信息发布 > 重大外来林业有害生物灾害 > 应急预案
            "http://www.forestry.gov.cn/Common/index/3597.html",  # 中国林业网 > 信息发布 > 重大外来林业有害生物灾害 > 监测预警
            "http://www.forestry.gov.cn/Common/index/3596.html",  # 中国林业网 > 信息发布 > 重大外来林业有害生物灾害 > 工作动态
            "http://www.forestry.gov.cn/Common/index/3564.html",  # 中国林业网 > 信息发布 > 森林防火与森林公安 > 森林火灾
            "http://www.forestry.gov.cn/Common/index/3565.html",  # 中国林业网 > 信息发布 > 森林防火与森林公安 > 公安动态
            "http://www.forestry.gov.cn/Common/index/3562.html",  # 中国林业网 > 信息发布 > 森林防火与森林公安 > 防火信息
            "http://www.forestry.gov.cn/Common/index/3598.html",  # 中国林业网 > 信息发布 > 重大外来林业有害生物灾害 > 应急预案
        ]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        message_list = response.xpath('//div[@class="inner"]/div[2]/ul/li')
        # print(len(message_list))
        for message in message_list:
            title = "".join(message.xpath('a/text()').extract())
            href = "".join(message.xpath('a/@href').extract())
            date = "".join(message.xpath('span/text()').extract())
            try:
                date = datetime.datetime.strptime(str(date).replace('/', '-'), '%Y-%m-%d')
                # print(date)
            except Exception as e:
                # print(e)
                date = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
            url = "http://www.forestry.gov.cn" + href
            # print(title, url, date)
            result = session.query(NewsItemInfo).filter_by(url=url, web_id=15).count()
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
        from_s = "".join(response.xpath('//*[@id="forestry_datasource"]/text()').extract())
        if from_s:
            item["webname"] = from_s.replace("来源:", "")
        else:
            item["webname"] = "中国林业网"
        item["web"] = response.meta["laiyuan"]
        # item["keyword"] = ""
        item["web_id"] = 15
        contents = "".join(response.xpath('//*[@id="zoomit"]/p/text()|\
                                            //*[@id="content_main"]/h1/text()|\
                                            //*[@id="forestry_content"]/text()|\
                                            //*[@id="forestry_content"]/strong/text()|\
                                            //*[@id="zoom"]/text()|\
                                            //*[@id="zoom"]/p/text()|\
                                            //*[@id="zoomit"]/span/text()|\
                                            //*[@id="zoomit"]/span/p/text()|\
                                            //*[@id="zoomit"]/span/p/strong/text()|\
                                            //*[@id="zoomit"]/span/strong/text()|\
                                            //*[@id="zoomit"]/span/div/text()|\
                                            //*[@id="zoomit"]/span/div/div/text()|\
                                            //*[@id="zoomit"]/span/div/span/text()|\
                                            //*[@id="zoomit"]/span/div/b/span/text()|\
                                            //*[@id="zoomit"]/span/div/strong/text()|\
                                            //*[@id="zoomit"]/div/span/text()|\
                                            //*[@id="zoomit"]/div/span/strong/text()|\
                                            //*[@id="zoomit"]/p/span/text()|\
                                            //*[@id="zoomit"]/p/span/span/text()|\
                                            //*[@id="zoomit"]/p/span/span/span/text()|\
                                            //*[@id="zoomit"]/strong/text()|\
                                            //*[@id="zoomit"]/div/strong/span/text()|\
                                            //*[@id="zoomit"]/p/div/strong/span/text()|\
                                            //*[@id="zoomit"]/p/strong/div/span/text()|\
                                            //*[@id="zoomit"]/p/strong/div/a/span/text()|\
                                            //*[@id="zoomit"]/p/strong/div/span/span/text()|\
                                            //*[@id="zoomit"]/div/strong/div/span/text()|\
                                            //*[@id="zoomit"]/p/div/strong/div/span/text()|\
                                            //*[@id="zoomit"]/div/span/text()|\
                                            //*[@id="zoomit"]/div/a/span/text()|\
                                            //*[@id="zoomit"]/div/span/span/text()|\
                                            //*[@id="zoomit"]/div/span/span/a/text()|\
                                            //*[@id="zoomit"]/p/strong/text()').extract())
        # print(contents)
        if contents != "":
            item["content"] = contents.replace("\u3000", "").replace("\xa0", "")
        else:
            item["content"] = "可能是图片 请打开详情页查看"
        item["keyword"] = keyword.get_keyword(item["content"])

        return item
