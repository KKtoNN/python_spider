#!/usr/bin/python3
# -*- coding:utf-8 -*-
import re
import time
import requests
from lxml import etree
from fagaiwei.settings import session, NewsItemInfo


class FagaiweiPipeline(object):
    # 处理中国银行新闻
    start_url = 'http://www.pbc.gov.cn/goutongjiaoliu/113456/113469/index.html'
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) \
                        Chrome/64.0.3278.0 Safari/537.36'
    }

    def __init__(self):
        self.session = session

    def main(self):
        response = requests.post(url=self.start_url, headers=self.headers)
        response = response.content.decode('utf-8')
        tree = etree.HTML(response)
        urls = tree.xpath("//font[@class='newslist_style']/a/@href")
        for url_s in urls:
            url = 'http://www.pbc.gov.cn' + url_s
            result = self.session.query(NewsItemInfo).filter_by(url=url, web_id=68).count()
            if result:
                # print("存在：{}".format(url))
                pass
            else:
                titles = requests.post(url)
                c = titles.content.decode('utf-8')
                texts = etree.HTML(c)
                title = ''.join(list(texts.xpath("//h2/text()"))).strip()
                pub_time = ''.join(list(texts.xpath("//td[@class='hui12'][3]/text()")))
                content = ''.join(list(texts.xpath("//td[@class='content']//p/text()"))).strip()
                laiyuan = ''.join(list(re.findall(r'\("#laiyuan"\)\.html\("(.*?)"\)', c))).strip()

                if laiyuan != "":
                    laiyuan = laiyuan
                else:
                    laiyuan = "中国人民银行"
                pub_time = pub_time.strip()
                keyword = ' '
                web_id = 68
                info = NewsItemInfo(
                    web_id=web_id,
                    url=url,  # 原文链接
                    title=title,  # 文章标题
                    pub_time=pub_time,  # 文章发布时间
                    content=content,  # 正文内容
                    web_name_t="中国人民银行  " + laiyuan,  # 二级网站来源
                    web_url_t=self.start_url,  # 二级网站来源链接
                    keyword=keyword,  # 关键字
                    target="yes",
                    categoryid="",
                    tagid=""
                )
                try:
                    self.session.add(info)
                    self.session.commit()
                    print("新插入：{}".format(url))
                except Exception as e:
                    print("[UUU] NewsItemInfo Error :{}".format(e))
                    self.session.rollback()


if __name__ == "__main__":
    while True:
        try:
            start_time = time.time()
            print("START TIME :{}".format(start_time))
            try:
                fa = FagaiweiPipeline()
                fa.main()
            except Exception as e:
                print(e)
            end_time = time.time()
            print("END TIME :{}".format(end_time))
            print("中国人民银行 USE TIME {}".format(end_time - start_time))
            print("------------WAIT--------------")
            time.sleep(5)
        except Exception as e:
            print("中国人民银行 ERROR :{}".format(e))
