#!/usr/bin/python3
# -*- coding:utf-8 -*-
__author__ = "jake"
__email__ = "jakejie@163.com"
"""
Project:fagaiwei
FileName = PyCharm
Version:1.0
CreateDay:2018/4/17 17:01
"""
import os
import time
from scrapy import cmdline
from subprocess import Popen

if __name__ == "__main__":
    # cmdline.execute("scrapy crawl gwycrawl".split())
    # cmdline.execute("scrapy crawl gwycrawl --nolog".split())
    # Popen("scrapy crawl gjfgw".split())
    # 直接循环执行
    while True:
        start_time = time.time()
        print("START TIME :{}".format(start_time))
        os.system("scrapy crawl gwycrawl --nolog")
        # os.system("scrapy crawl gwycrawl")
        end_time = time.time()
        print("END TIME :{}".format(end_time))
        print("国务院 USE TIME {}".format(end_time-start_time))
        print("------------WAIT--------------")
        time.sleep(5)
