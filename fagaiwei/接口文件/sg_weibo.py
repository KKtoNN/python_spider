#!/usr/bin/python3
# -*- coding:utf-8 -*-
import datetime
import time
import re
import pymysql
from pyquery import PyQuery as pq
import requests
from lxml import etree
from urllib.parse import quote

host = '192.168.0.147'
user = 'crawl'
passwd = 'crawlpassword'
db = 'shares'


def save(item):
    db = pymysql.connect(charset='utf8', host=host, user=user, passwd=passwd, db='shares')
    cursor = db.cursor()
    keys = ','.join(item.keys())
    values = ','.join(["%s"] * len(item))
    try:
        sql = 'insert into {table}({keys}) values ({values})'.format(table='shares_newsdetail', keys=keys,
                                                                     values=values)
        cursor.execute(sql, tuple(item.values()))
        db.commit()
    except Exception as e:
        print(e)
        db.rollback()
    finally:
        db.close()


class sg_wechat():
    def __init__(self, page=1):
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.117 Safari/537.36'}

    def get_keyword(self):
        keyword = input(': ')
        if not keyword:
            self.params = {}
            self.url = 'http://weixin.sogou.com/'
        else:
            self.params = {'type': 2,
                           'ie': 'utf8',
                           's_from': 'input',
                           '_sug_': 'y',
                           '_sug_type_': '',
                           }
            self.params['query'] = keyword
            self.url = 'http://weixin.sogou.com/weixin'

    def process_main(self):
        self.get_keyword()
        while True:
            try:
                response = requests.get(self.url, params=self.params, timeout=2, headers=self.headers)
                # print(response.url)
                break
            except requests.exceptions.ConnectionError:
                print('ConnectionError -- please wait 3 seconds')
                time.sleep(3)
            except requests.exceptions.ChunkedEncodingError:
                print('ChunkedEncodingError -- please wait 3 seconds')
                time.sleep(3)
            except:
                print('Unfortunitely -- An Unknow Error Happened, Please wait 3 seconds')
                time.sleep(3)
        if not response.status_code == 200:
            print('Request Failed!')
            exit()
        response.encoding = 'utf-8'
        doc = pq(response.text)

        content_list = doc('.news-list li')
        keys = ('web_name_t', 'web_url_t', 'url', 'title', 'pub_time', 'keyword', 'content', 'add_time', 'web_id')
        for content in content_list.items():
            item = dict.fromkeys(keys, ' ')
            item['web_name_t'] = content('.account').text()
            item['web_url_t'] = response.url
            item['url'] = content('h3 a').attr('href')
            item['title'] = content('h3').text()
            timestamp = content('.s-p').attr('t')
            item['pub_time'] = datetime.datetime.fromtimestamp(int(timestamp)).strftime('%Y-%m-%d %H:%M:%S')
            item['content'] = content('.txt-info').text().replace('\u3000', '')
            item['add_time'] = datetime.datetime.now().strftime('%Y-%m-%d %H-%M-%S')
            item['web_id'] = 30
            # keyword未获取,默认‘ ’
            # save(item)
            print('item')
            np = doc('#sogou_next')  # 下一页


class weibo():
    def __init__(self):
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.117 Safari/537.36'}

    def get_keyword(self):
        keyword = input(': ')
        while not keyword:
            keyword = input('\r\nnot empty,input again: ')
        self.url = 'https://s.weibo.com/weibo/{keyword}&Refer=index'.format(keyword=quote(quote(keyword)))

    def get_resource(self):
        while 1:
            try:
                page_resource = requests.get(self.url).text
                return page_resource
            except requests.exceptions.ConnectionError:
                print('ConnectionError -- please wait 3 seconds')
                time.sleep(3)
            except requests.exceptions.ChunkedEncodingError:
                print('ChunkedEncodingError -- please wait 3 seconds')
                time.sleep(3)
            except:
                print('Unfortunitely -- An Unknow Error Happened, Please wait 3 seconds')
                time.sleep(3)

    def process_content(self, content_tmp):
        content_pattern = re.compile(r'<p class=.*?(?=comment_txt).*?>(.*?)<\\/p>')
        content = ''.join(content_pattern.findall(content_tmp, re.S))
        process_content = re.sub(
            r'\\n|\\t|<(.*?)?em(.*?)?>|<(.*?)?a(.*?)?>|<(.*?)?span(.*?)?>|<(.*?)?img(.*?)?>|\\u200b', '', content)
        result = bytes(process_content.encode('utf-8')).decode('unicode_escape')
        return result

    def process_title_link(self, url_link_tmp):
        name_link_pattern = re.compile(r'nick-name=.*?"(.*?)\\".*?href=.*?"(.*?)\\+"(?= target)')
        name_link = name_link_pattern.findall(url_link_tmp, re.S)
        if not len(name_link):
            title, url = ' ', ' '
        else:
            title, url = name_link[0]
        title = bytes(title.encode('utf-8')).decode('unicode_escape')
        url = 'http:' + url.replace('\\', '')
        return title, url

    def process_date(self, date_tmp):
        date_pattern = re.compile(r'date=.*?"(.*?)\\"')
        timestamp = ''.join(date_pattern.findall(date_tmp))[:11]
        result = datetime.datetime.fromtimestamp(int(timestamp)).strftime('%Y-%m-%d %H:%M:%S')
        return result

    def process_main(self):
        self.get_keyword()
        data = self.get_resource()
        detail_pattern = re.compile(r'<!--feed_detail-->(.*?)<!--\\/feed_detail-->')  # 匹配每篇细节
        # name_link_pattern = re.compile(r'nick-name=.*?"(.*?)\\".*?href=.*?"(.*?)\\+"(?= target)')    #匹配ID和url
        # content_pattern = re.compile(r'<p class=.*?(?=comment_txt).*?>(.*?)<\\/p>')                  #匹配摘要
        # date_pattern = re.compile(r'date=.*?"(.*?)\\"')                                              #匹配时间
        # process_content = re.compile(r'\\n|\\t|<(.*?)?em(.*?)?>|<(.*?)?a(.*?)?>|<(.*?)?span(.*?)?>|<(.*?)?img(.*?)?>')  #处理摘要
        item_list = re.findall(detail_pattern, data)
        keys = ('web_name_t', 'web_url_t', 'url', 'title', 'pub_time', 'keyword', 'content', 'add_time', 'web_id')
        for tmp in item_list:
            item = dict.fromkeys(keys, ' ')
            item['web_name_t'] = '微博搜索'
            item['web_url_t'] = 'https://s.weibo.com'
            item['title'], item['url'] = self.process_title_link(tmp)
            item['pub_time'] = self.process_date(tmp)
            item['content'] = self.process_content(tmp)
            item['add_time'] = datetime.datetime.now().strftime('%Y-%m-%d %H-%M-%S')
            item['web_id'] = 29
            # content = ''.join(re.findall(r'<p class=.*?(?=comment_txt).*?>(.*?)<\\/p>',tmp, re.S))
            # process_content =re.sub(r'\\n|\\t|<(.*?)?em(.*?)?>|<(.*?)?a(.*?)?>|<(.*?)?span(.*?)?>|<(.*?)?img(.*?)?>','',content)
            # print(bytes(process_content.encode('utf-8')).decode('unicode_escape'))
            print(item)


def main(keyword):
    print("==========={}".format(keyword))


if __name__ == '__main__':
    main(keyword="keyword")
    # sgwe = sg_wechat()
    # sgwe.process_main()
    #
    # weibo = weibo()
    # weibo.process_main()
