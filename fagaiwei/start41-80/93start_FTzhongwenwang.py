from scrapy import cmdline
# cmdline.execute("scrapy crawl shanghaizhengsuo_sipder".split())


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
        # cmdline.execute("scrapy crawl FTzhognwenwang_sipder".split())
    # cmdline.execute("scrapy crawl FTzhognwenwang_sipder --nolog".split())
# Popen("scrapy crawl dizhen".split())
    # 直接循环执行
    while True:
        start_time = time.time()
        print("START TIME :{}".format(start_time))
        os.system("scrapy crawl FTzhognwenwang_sipder --nolog")
        # os.system("scrapy crawl FTzhognwenwang_sipder ")
        # os.system("scrapy crawl dizhen")
        end_time = time.time()
        print("END TIME :{}".format(end_time))
        print("FT中文网 USE TIME {}".format(end_time - start_time))
        print("------------WAIT--------------")
        time.sleep(5)
