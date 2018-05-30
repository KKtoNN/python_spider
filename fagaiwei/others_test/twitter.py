# -*- coding:utf-8 -*-
__author__ = "jake"
__email__ = "jakejie@163.com"
"""
Project:fagaiwei
FileName = PyCharm
Version:1.0
CreateDay:2018/5/7 14:28
"""
import re
import requests
from lxml import etree

headers = {
    "origin": "https://twitter.com",
    # "path": "/1.1/users/phone_number_available.json?raw_phone_number=%2B8615912345677",
    # "referer": "https://twitter.com/i/flow/signup",
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36,"
}
# options_url = "https://api.twitter.com/1.1/users/phone_number_available.json?raw_phone_number=+8615912345677"
# get_url = "https://api.twitter.com/1.1/users/phone_number_available.json?raw_phone_number=+8615912345677"

session = requests.session()
# 使用找回密码功能验证
post_url = "https://twitter.com/account/begin_password_reset?lang=zh-cn"
begin_url = "https://twitter.com/account/begin_password_reset?lang=zh-cn"
sent_url = "https://twitter.com/account/send_password_reset?lang=zh-cn"
response = session.get(begin_url, headers=headers)
# print(response)
# print(response.text)

com = re.compile(r'name="authenticity_token" value="(.*?)"')
token = "".join(re.findall(com, response.text))

# tree = etree.HTML(response.text)
# token = "".join(tree.xpath('//div[@class="Section"]/form/imput[1]/@value'))
print(token)
form_data = {
    "authenticity_token": token,
    "account_identifier": "guangdota@gmail.com",
}

response = session.post(post_url, data=form_data,headers=headers)
print(response)

response = requests.get(sent_url)
print(response)
print(response.text)
# 使用注册的时候进行验证
# response = session.options(options_url, headers=headers)
# print(response)
# print(response.text)
#
# response = session.get(get_url, headers=headers)
# print(response)
# print(response.text)

if __name__ == "__main__":
    pass
