# -*- coding:utf-8 -*-
__author__ = "jake"
__email__ = "jakejie@163.com"
"""
Project:fagaiwei
FileName = PyCharm
Version:1.0
CreateDay:2018/5/10 14:23
"""
import json
import requests

url = "http://money.163.com/special/00251G8F/news_json.js?0.2185412157347837"
if __name__ == "__main__":
    response = requests.get(url).text[9:-1]
    response = response.replace('{c:', '{"c":').replace(',t:', ',"t":').replace(',l:', ',"l":').replace("n:", '"n":') \
        .replace(',p:', ',"p":').replace("category", '"category"').replace("news", '"news"')
    # print(response)
    # print(response.text)
    result = json.loads(response)
    # print(result["category"])
    news_list = result["news"]
    for news_s in news_list:
        # print(news_s)
        for news in news_s:
            title = news["t"]
            pub_time = news["p"]
            url = news["l"]
            print(title)
            print(pub_time)
            print(url)
    pass
