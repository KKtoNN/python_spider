# -*- coding:utf-8 -*-
__author__ = "jake"
__email__ = "jakejie@163.com"
"""
Project:fagaiwei
FileName = PyCharm
Version:1.0
CreateDay:2018/5/8 12:40
"""
import datetime
import time
import json
import jsonpath
from fagaiwei.settings import session, NewsItemInfo
from fagaiwei.keyword_others import keyword
from fagaiwei.jvchao_pdf import pdf_to_txt

allowed_domains = ['cninfo.com.cn']


def parse_juchao(response, item):
    PUB_URL = 'http://www.cninfo.com.cn/cninfo-new/disclosure/szse/bulletin_detail/true/'
    D_URL = 'http://www.cninfo.com.cn/cninfo-new/disclosure/szse/download/'
    dates = response.text
    json_str = json.loads(dates, encoding='utf-8')
    urls = jsonpath.jsonpath(json_str, "$..announcementId")
    title1 = jsonpath.jsonpath(json_str, "$..secCode")
    title2 = jsonpath.jsonpath(json_str, "$..secName")
    title3 = jsonpath.jsonpath(json_str, "$..announcementTitle")
    timestamp = jsonpath.jsonpath(json_str, "$..announcementTime")
    pdf = jsonpath.jsonpath(json_str, "$..adjunctUrl")
    if title2 is None:
        title2 = ''
        titles = zip(title1, title3)
    else:
        titles = zip(title1, title2, title3)

    url_contents = zip(urls, titles, timestamp, pdf)
    for url, title, time_local, pdf in url_contents:
        # item = {}
        if None in title:
            title = title[0] + title[2]
        else:
            title = title
        title = ' '.join(list(title)).replace('*', '').replace('/', '').replace('<', '').replace('>', '') \
            .replace('|', '').replace(':', '').replace('"', '').replace('?', '') \
            .replace('？', '')

        durl = D_URL + url  # PDF文件下载地址
        if pdf[-4:] == '.PDF':
            # print("==================================\n{}".format(durl))
            result = session.query(NewsItemInfo).filter_by(url=PUB_URL + url, web_id=56).count()
            if result:
                # print("PDF 文件地址： {} 存在".format(PUB_URL + url))
                pass
            else:
                contents = pdf_to_txt.main(url=durl, fileName=title)
                if len(contents) == 0:
                    item['content'] = '请点击原文链接查看'
                else:
                    item['content'] = '\n'.join(list(contents))

                times = str(time_local)[0:-3] + '.' + '000'
                item['pub_time'] = datetime.datetime.fromtimestamp(float(times)).strftime('%Y-%m-%d %H:%M:%S')
                item['webname'] = '巨潮资讯'
                item['web'] = response.url[0:-7]
                item['add_time'] = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
                item["keyword"] = keyword.get_keyword(item["content"])
                item['web_id'] = 56
                item['title'] = title
                item['url'] = PUB_URL + url
                yield item
                #         item_list.append(item)
                # return item_list
