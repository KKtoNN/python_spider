# -*- coding:utf-8 -*-
__author__ = "jake"
__email__ = "jakejie@163.com"
"""
Project:fagaiwei
FileName = PyCharm
Version:1.0
CreateDay:2018/5/11 9:28
"""
import requests

host_url = "https://www.toutiao.com/ch/news_finance/"
headers = {
    # "referer": "https://www.toutiao.com/ch/news_finance/",
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36",
    # "x-requested-with": "XMLHttpRequest",
    'cookie': 'tt_webid=6535223378431985156; uuid="w:630ba667869849d1a1157218171d02bf"; UM_distinctid=162467198f4bd2-0bfb6aa5147744-4323461-1fa400-162467198f5753; tt_webid=6535223378431985156; WEATHER_CITY=%E5%8C%97%E4%BA%AC; CNZZDATA1259612802=1890294813-1521598838-%7C1525999183; __tasessionId=5w05qj3211526001907102',
    # 'upgrade-insecure-requests': '1',
}


def main():
    session = requests.session()
    res1 = session.get(host_url)
    res2 = session.get("https://www.toutiao.com/stream/widget/local_weather/data/?city=%E5%8C%97%E4%BA%AC")
    res3 = session.get("https://www.toutiao.com/stream/widget/local_weather/city/")
    res4 = session.get("https://www.toutiao.com/hot_words/")
    res5 = session.get("https://www.toutiao.com/api/pc/hot_video/?widen=1")
    print(res1, res2, res3, res4, res5)
    # print(res.text)
    url = "http://www.toutiao.com/api/pc/feed/?category=news_finance&utm_source=toutiao&widen=1&max_behot_time=0&max_behot_time_tmp=0&tadrequire=true&as=A1558A0F046F108&cp=5AF48F7100E85E1&_signature=H16nxwAARa7RNSEV6Dqddx9ep9"
    response = session.get(url)
    print(response)
    print(response.text)


if __name__ == "__main__":
    main()
    pass
