#!/usr/bin/python3
# -*- coding:utf-8 -*-
__author__ = "jake"
__email__ = "jakejie@163.com"
"""
Project:fagaiwei
FileName = PyCharm
Version:1.0
CreateDay:2018/4/28 9:25
"""

import os
import time
import requests
from scrapy import cmdline
from lxml import etree
from subprocess import Popen
from scrapy.utils.project import get_project_settings
from scrapy.crawler import CrawlerProcess
from fagaiwei.settings import DEFAULT_REQUEST_HEADERS


class HuaerjieJianwen(object):
    def __init__(self):
        pass

    def get_response(self, url):
        response = requests.get(url, headers=DEFAULT_REQUEST_HEADERS)
        return response

    def get_message_list(self, response):
        tree = etree.HTML(response.text)
        message_list = tree.xpath('//div[@class="wscn-tabs__content"]/div/div')
        info = []
        for message in message_list:
            # date = "".join(message.xpath('span/a/text()|span/text()').extract())
            # date = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
            title = "".join(message.xpath('div/div/a[1]/text()')).replace(" ", "").replace("\n", "")
            href = "".join(message.xpath('div/div/a[1]/@href'))
            info.append([title, href])
        return info

    def get_detail(self, response, title, laiyuan):
        # print(response.text)
        item = {}
        item["url"] = response.url
        response = etree.HTML(response.text)
        item["pub_time"] = "".join(response.xpath('//div[@class="article__heading"]/div/div/span/text()'))
        item["title"] = title
        item["webname"] = "华尔街见闻"
        item["web"] = laiyuan
        item["keyword"] = ""
        item["web_id"] = 28
        contents = "".join(response.xpath('//div[@class="article__content"]/div/div/text()|\
                                           //div[@class="article__content"]/div/div/p/text()|\
                                           //div[@class="article__content"]/div/div/p/strong/text()|\
                                           //div[@class="article__content"]/div/div/h2/text()|\
                                           //div[@class="article__content"]/div/div/h2/strong/text()|\
                                           //div[@class="article__content"]/div/div/h2/p/text()'))
        # print(contents)
        if contents != "":
            item["content"] = contents.replace("\u3000", "").replace("\xa0", "")
        else:
            item["content"] = "可能是图片 请打开详情页查看"
        print(item)


def main():
    huaerjie = HuaerjieJianwen()
    urls = [
        "https://wallstreetcn.com/news/global",  # 华尔街见闻 最新
        # "https://wallstreetcn.com/news/shares",  # 华尔街见闻 股市
        # "https://wallstreetcn.com/news/bonds",  # 华尔街见闻 债市
        # "https://wallstreetcn.com/news/commodities",  # 华尔街见闻 商品
        # "https://wallstreetcn.com/news/forex",  # 华尔街见闻 外汇
        # "https://wallstreetcn.com/news/enterprise",  # 华尔街见闻 公司
        # "https://wallstreetcn.com/news/economy",  # 华尔街见闻 经济
        # "https://wallstreetcn.com/news/charts",  # 华尔街见闻 数据
        # "https://wallstreetcn.com/news/china",  # 华尔街见闻 中国
        # "https://wallstreetcn.com/news/us",  # 华尔街见闻 美国
        # "https://wallstreetcn.com/news/europe",  # 华尔街见闻 欧洲
        # "https://wallstreetcn.com/news/japan",  # 华尔街见闻 日本
    ]
    for url in urls:
        response = huaerjie.get_response(url)
        messages = huaerjie.get_message_list(response)
        print(len(messages))
        # print(messages)
        for message in messages:
            title, href = message[0], message[1]
            if title and href:
                res = huaerjie.get_response(url="https://wallstreetcn.com" + href)
                huaerjie.get_detail(res, title, url)


if __name__ == "__main__":
    # main()
    # cmdline.execute("scrapy crawl huaerjiejianwen".split())
    # cmdline.execute("scrapy crawl huaerjiejianwen --nolog".split())
    # Popen("scrapy crawl huaerjiejianwen".split())
    # 直接循环执行
    while True:
        start_time = time.time()
        print("START TIME :{}".format(start_time))
        os.system("scrapy crawl huaerjiejianwen --nolog")
        # os.system("scrapy crawl huaerjiejianwen")
        end_time = time.time()
        print("END TIME :{}".format(end_time))
        print("华尔街见闻 USE TIME {}".format(end_time - start_time))
        print("------------WAIT--------------")
        time.sleep(5)
