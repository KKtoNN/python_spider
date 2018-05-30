#!/usr/bin/python3
# -*- coding:utf-8 -*-
__author__ = "jake"
__email__ = "jakejie@163.com"
"""
Project:fagaiwei
FileName = PyCharm
Version:1.0
CreateDay:2018/4/19 18:46
"""

import os
import time
from scrapy import cmdline
from subprocess import Popen
from scrapy.utils.project import get_project_settings
from scrapy.crawler import CrawlerProcess


# 同时运行多个spider文件
def main():
    setting = get_project_settings()
    process = CrawlerProcess(setting)
    didntWorkSpider = ['sample']

    for spider_name in process.spiders.list():
        if spider_name in didntWorkSpider:
            continue
        print("Running spider %s --nolog" % (spider_name))
        process.crawl(spider_name)
    process.start()


if __name__ == "__main__":
    # main()
    # cmdline.execute("scrapy crawl dizhen".split())
    # cmdline.execute("scrapy crawl dizhen --nolog".split())
    # Popen("scrapy crawl dizhen".split())
    # 直接循环执行
    while True:
        start_time = time.time()
        print("START TIME :{}".format(start_time))
        os.system("scrapy crawl dizhen --nolog")
        # os.system("scrapy crawl dizhen")
        end_time = time.time()
        print("END TIME :{}".format(end_time))
        print("地震局 USE TIME {}".format(end_time - start_time))
        print("------------WAIT--------------")
        time.sleep(5)

