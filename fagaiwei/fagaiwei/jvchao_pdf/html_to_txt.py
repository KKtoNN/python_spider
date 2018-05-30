# -*- coding:utf-8 -*-
import requests


def get_url(url):
    response = requests.get(url)
    content = response.text
    return content


def main(url):
    content = get_url(url)
    return content


if __name__ == '__main__':
    url = "http://php.cnstock.com/news_new/index.php/api/fileview?ID=1204920051&db=txt"
    # get_url(url)
    content = main(url)
    print(content)
    # main()
