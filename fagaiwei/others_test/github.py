# -*- coding:utf-8 -*-
__author__ = "jake"
__email__ = "jakejie@163.com"
"""
Project:fagaiwei
FileName = PyCharm
Version:1.0
CreateDay:2018/5/5 17:25
"""
import requests
from lxml import etree

headers = {
    "Server": "GitHub.com",
    "User-Agent": "Mozilla/5.0 (X11; CrOS i686 0.12.433) AppleWebKit/534.30 (KHTML, like Gecko) Chrome/12.0.742.77 Safari/534.30",
}
url = "https://github.com/"
login_url = "https://github.com/login"
post_url = "https://github.com/sessio"
session = requests.session()

response = session.get(login_url, headers=headers)

tree = etree.HTML(response.text)
token = "".join(tree.xpath('//*[@id="login"]/form/input[2]/@value'))
print(token)
post_data = {
    "commit": "Sign in",
    "utf8": "✓",
    "authenticity_token": token,
    "login": "jakejie@163.com",
    "password": "zhujie165102",
}
response = session.post(post_url, data=post_data)
print(response)
response = session.get(url)
print(response)
print(response.text)

if __name__ == "__main__":
    pass
